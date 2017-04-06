import random
import string

import dotenv
from app.models import LongUrl, ShortUrl, User, Visitor
from flask import abort, g, jsonify, request, url_for
from sqlalchemy import desc, func

from . import api
from .. import db
from .authentication import auth
from .errors import forbidden, not_found, unauthorized
from .validators import ValidateLongUrl, ValidateShortUrl

dotenv.load()


@api.route('/shorten', methods=['POST'])
def shorten():
    long_url_input = ValidateLongUrl(request)
    if not long_url_input.validate():
        return forbidden(long_url_input.errors)
    long_url = request.json.get('long_url')
    search_long_url = LongUrl.query.filter_by(long_url=long_url).first()
    if search_long_url:
        short_url = search_long_url.short_urls.filter_by(
            user=g.current_user).first()
        if short_url and request.json.get('vanity'):
            return jsonify({'success': True,
                            'message': short_url.short_url,
                            'info': 'Url shortened by you before'})
        if short_url:
            return jsonify({'success': True, 'message': short_url.short_url,
                            'short_url_url': url_for('api.shorturls',
                                                     _external=True)
                            + str(short_url.short_url_id)})
        new_short_url = get_short_url()
        return update_new_short_url(new_short_url, search_long_url)
    new_short_url = get_short_url()
    return add_new_short_url(new_short_url, long_url)


def update_new_short_url(new_short_url, long_url):
    long_url.short_urls.append(new_short_url)
    g.current_user.short_urls.append(new_short_url)
    new_short_url.save()
    return jsonify({'success': True, 'message': new_short_url.short_url,
                    'short_url_url': url_for('api.shorturls',
                                             _external=True)
                    + str(new_short_url.short_url_id)})


def add_new_short_url(new_short_url, long_url):
    new_short_url.save()
    new_long_url = LongUrl(long_url=long_url)
    new_long_url.short_urls.append(new_short_url)
    g.current_user.short_urls.append(new_short_url)
    new_long_url.save()
    return jsonify({'success': True, 'message': new_short_url.short_url,
                    'short_url_url': url_for('api.shorturls',
                                             _external=True)
                    + str(new_short_url.short_url_id)})


def generate_short_url(len_range=5):
    url_prefix = dotenv.get('URL_PREFIX')
    new_short_url = url_prefix + ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase
                      + string.digits) for _ in range(len_range))
    if ShortUrl.query.filter_by(short_url=new_short_url).first():
        generate_short_url(len_range + 1)
    return ShortUrl(short_url=new_short_url)


def get_short_url():
    new_short_url = None
    if request.json.get('vanity') and not g.current_user.is_anonymous:
        new_short_url = get_vanity_url(request.json.get('vanity'))
        return new_short_url
    if request.json.get('vanity') and g.current_user.is_anonymous:
        abort(unauthorized('Invalid credentials'))
    new_short_url = generate_short_url()
    return new_short_url


def get_vanity_url(vanity):
    url_prefix = dotenv.get('URL_PREFIX')
    full_vanity_url = url_prefix + vanity
    if ShortUrl.query.filter_by(short_url=full_vanity_url).first():
        vanity_error = "Vanity string '{}' has been taken".format(vanity)
        abort(forbidden(vanity_error))
    return ShortUrl(short_url=full_vanity_url)


@api.route('/shorturl/recent', methods=['GET'])
def most_recent():
    recent_urls = ShortUrl.query.order_by(
        desc(ShortUrl.date_time)).limit(5).all()
    if recent_urls:
        urls = []
        for i in range(len(recent_urls)):
            urls.append({'short_url': recent_urls[i].short_url,
                         'short_url_url': recent_urls[i].short_url_id
                         })
        return jsonify({'success': True, 'message': urls})
    return not_found('No url found')


@api.route('/shorturl/<int:id>/activate/', methods=['PUT'])
def activate_url(id):
    return toggle_url_activation(id, 'activate')


@api.route('/shorturl/<int:id>/deactivate/', methods=['PUT'])
def deactivate_url(id):
    return toggle_url_activation(id, 'deactivate')


def toggle_url_activation(id, activate_or_deactivate):
    endpoint_map = {'activate': 1, 'deactivate': 0}
    short_url = ShortUrl.query.filter_by(short_url_id=id).first()
    if not short_url or short_url.deleted:
        return not_found('No url with the id {}'.format(id))
    if short_url.user == g.current_user:
        short_url.active = endpoint_map[activate_or_deactivate]
        db.session.commit()
        return jsonify({'success': True, 'message': url_for(
            'api.shorturls', _external=True) + str(short_url.short_url_id)})
    return unauthorized('Invalid credentials')


@api.route('/shorturl/', methods=['GET'])
def shorturls():
    user_urls = ShortUrl.query.filter_by(user=g.current_user).all()
    if user_urls:
        urls = []
        for i in range(len(user_urls)):
            urls.append({'short_url': user_urls[i].short_url,
                         'short_url_url': user_urls[i].short_url_id,
                         'long_url': user_urls[i].long_url.long_url
                         })
        return jsonify({'success': True, 'message': urls})
    return not_found('No shortened url found')


@api.route('/shorturl/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def shorturl(id):
    request_mapping = {'GET': get_short_url_details,
                       'DELETE': delete_short_url,
                       'PUT': change_short_url_target}
    url = ShortUrl.query.filter_by(user=g.current_user).filter_by(
        short_url_id=id).filter_by(deleted=0).first()
    if not url:
        return not_found(
            "No shortened url with id '{}' found for you".format(id))
    return request_mapping[request.method](id, url)

# Add visitors details(urls maybe)


def get_short_url_details(id, url):
    url_details = {'url': url.short_url,
                   'url_url': url_for('api.shorturls', _external=True)
                   + str(url.short_url_id),
                   'long_url': url.long_url.long_url, 'active': url.active}
    return jsonify({'success': True, 'message': url_details})


def delete_short_url(id, url):
    count = len(ShortUrl.query.filter_by(long_url=url.long_url).all())
    if count <= 1:
        LongUrl.query.filter_by(long_url=url.long_url.long_url).delete()
    url.deleted = 1
    db.session.commit()
    return jsonify({'success': True, 'message': 'deleted'})


def change_short_url_target(id, url):
    long_url_input = ValidateLongUrl(request)
    if not long_url_input.validate():
        return forbidden(long_url_input.errors)
    new_long_url = request.json.get('long_url')
    has_short_url = ShortUrl.query.filter_by(
        user=g.current_user).filter(ShortUrl.long_url.has(long_url=new_long_url)).first()
    if has_short_url:
        return forbidden("The url already has a shortened url '{}'".format(
            has_short_url.short_url))
    count = len(ShortUrl.query.filter_by(long_url=url.long_url).all())
    if count <= 1:
        LongUrl.query.filter_by(long_url=url.long_url.long_url).delete()
    new_long_url_check = LongUrl.query.filter_by(long_url=new_long_url).first()
    if not new_long_url_check:
        new_long_url_check = LongUrl(long_url=new_long_url)
        new_long_url_check.save()
    url.long_url = new_long_url_check
    db.session.commit()
    return jsonify({'success': True, 'message': 'updated'})


@api.route('/shorturl/popular/', methods=['GET'])
def popular():
    urls = ShortUrl.query(func.count(ShortUrl.visitors.visitor_id).label(
        'total')). order_by('total desc').all()  # Might consider limits later
    if not urls:
        popular_urls = []
        for url in urls:
            visitors = Visitor.query(Visitor.visitor_id).filter(
                ShortUrl.visitors.any(short_url_id=url.short_url_id)).all()
            popular_urls.append({
                'short_url_url': url_for(
                    'api.shorturl', _external=True) + str(url.short_url_id),
                'short_url': url.short_url,
                'number_of_visits': url.total,
                'visitors': [
                    url_for('api.visitor', vid=visitor.visitor_id,
                            id=url.short_url_id,
                            _external=True) for visitor in visitors]
            })
        return jsonify({'success': True, 'popular_urls': popular_urls})
    return not_found('No url was found')


@api.route('/shorturl/<int:id>/visitors/', methods=['GET'])
def visitors(id):
    if ShortUrl.query.filter_by(
            short_url_id=id).filter_by(user=g.current_user).first():
        visitors = Visitor.query(Visitor.visitor_id).filter(
            ShortUrl.visitors.any(short_url_id=id)).all()
        if not visitors:
            visitors_details = []
            for visitor in visitors:
                visitor_details = visitor.get_details()
                visitor_details['visitor_url'] = url_for(
                    'api.visitor', vid=visitor.visitor_id,
                    id=id, _external=True)
                visitors_details.append(visitor_details)
            return jsonify({'success': True, 'visitors': visitors_details})
        return not_found('No visitor found for this URL')
    return not_found("No URL found with id '{}'".format(id))


# Abstract visitors detail (keep it DRY)
@api.route('/shorturl/<int:id>/visitors/<int:vid>', methods=['GET'])
def visitor(id, vid):
    if ShortUrl.query.filter_by(
            short_url_id=id).filter_by(user=g.current_user).first():
        visitor = Visitor.query.filter_by(visitor_id=vid).first()
        if visitor:
            visitor_details = visitor.get_details()
            visitor_details['visitor_url'] = url_for(
                'api.visitor', vid=vid, id=id, _external=True)
            return jsonify({'success': True, 'visitor': visitor_details})
        return not_found("No visitor to this URL with id '{}'".format(vid))
    return not_found("No URL found with id '{}'".format(id))


# check for deleted and deactivated urls in all other route implementation
@api.route('/visit/', methods=['POST'])
def visit():
    short_url_input = ValidateShortUrl(request)
    if not short_url_input.validate():
        return forbidden(short_url_input.errors)
    short_url = request.json.get('short_url')
    short_url_details = ShortUrl.query.filter_by(
        short_url=short_url).filter_by(deleted=0).first()
    if not short_url_details:
        return not_found('No matching URL found')
    elif not short_url_details.active:
        return forbidden('URL has been deactivated')
    else:
        add_visit(short_url_details)
        return jsonify(
            {'success': True, 'long_url': short_url_details.long_url.long_url})


def add_visit(url):
    agent = request.user_agent
    visitor = Visitor(ip_address=request.remote_addr,
                      browser=agent.browser, platform=agent.platform)
    visitor.short_urls.append(url)
    visitor.save()

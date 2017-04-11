import random
import string

import dotenv
from app.models import LongUrl, ShortUrl, Visitor, visits
from flask import abort, g, jsonify, request, url_for
from sqlalchemy import desc, func

from . import api
from .. import db
from .errors import (bad_request, forbidden, not_found, unauthorized,
                     unavailable)
from .validators import ValidateLongUrl, ValidateShortUrl

dotenv.load()


@api.route('/shorten', methods=['POST'])
def shorten():
    """
    This function accepts a json object from the request body which contains
    a URL. The URL is shortened and saved in the database returning the
    details of the shortened URL.
    """
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
                            'url': short_url.get_details(),
                            'info': 'Url shortened by you before'})
        if short_url:
            return jsonify({'success': True,
                            'url': short_url.get_details(),
                            })
        new_short_url = get_short_url()
        return update_new_short_url(new_short_url, search_long_url)
    new_short_url = get_short_url()
    return add_new_short_url(new_short_url, long_url)


def update_new_short_url(new_short_url, long_url):
    """
    Return a shortened URL details after linking it to a long URL.

    Keyword arguments:
    new_short_url -- the newly generated shortened URL
    long_url -- the existing long URL
    """
    long_url.short_urls.append(new_short_url)
    g.current_user.short_urls.append(new_short_url)
    new_short_url.save()
    return jsonify({'success': True,
                    'url': new_short_url.get_details()
                    })


def add_new_short_url(new_short_url, long_url):
    """
    Return a shortened URL details after saving it along its long URL.

    Keyword arguments:
    new_short_url -- the newly generated shortened URL
    long_url -- the new long URL to be linked and saved with the shortened URL
    """
    new_short_url.save()
    new_long_url = LongUrl(long_url=long_url)
    new_long_url.short_urls.append(new_short_url)
    g.current_user.short_urls.append(new_short_url)
    new_long_url.save()
    return jsonify({'success': True,
                    'url': new_short_url.get_details()
                    })


def generate_short_url(len_range=5):
    """
    This is a recursive function that generates a random string of length
    len_range.

    Keyword arguments:
    len_range -- the integer value used to determine the length of the string
                 it is given a default value of 5
    """
    url_prefix = dotenv.get('URL_PREFIX')
    new_short_url = url_prefix + ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase
                      + string.digits) for _ in range(len_range))
    if ShortUrl.query.filter_by(short_url=new_short_url).first():
        generate_short_url(len_range + 1)
    return ShortUrl(short_url=new_short_url)


def get_short_url():
    """
    This function returns a short_url object according to the user and/or the
    the inputs supplied through the request.

    Keyword arguments:
    vanity -- a string value that is sent through the request body
    """
    new_short_url = None
    if request.json.get('vanity') and not g.current_user.is_anonymous:
        new_short_url = get_vanity_url(request.json.get('vanity'))
        return new_short_url
    if request.json.get('vanity') and g.current_user.is_anonymous:
        abort(unauthorized('Invalid credentials'))
    new_short_url = generate_short_url()
    return new_short_url


def get_vanity_url(vanity):
    """
    This function returns a shortened URL generated using vanity string

    Keyword arguments:
    vanity -- a string value that is sent through the request body
    """
    url_prefix = dotenv.get('URL_PREFIX')
    full_vanity_url = url_prefix + vanity
    if ShortUrl.query.filter_by(
            short_url=full_vanity_url).filter_by(deleted=0).first():
        vanity_error = "Vanity string '{}' has been taken".format(vanity)
        abort(forbidden(vanity_error))
    return ShortUrl(short_url=full_vanity_url)


@api.route('/shorturl/recent', methods=['GET'])
def most_recent():
    """
    This function returns the list of most recently added shortened URLs.
    """
    recent_urls = ShortUrl.query.order_by(
        desc(ShortUrl.date_time)).filter_by(deleted=0).limit(10).all()
    if recent_urls:
        urls = []
        for i in range(len(recent_urls)):
            urls.append(recent_urls[i].get_details())
        return jsonify({'success': True, 'recents': urls})
    return not_found('No url found')


@api.route('/shorturl/<int:id>/activate', methods=['PUT'])
def activate_url(id):
    """
    This function activates a shortened URL whose id is passed by calling the
    toggle_url_activation function.

    Keyword arguments:
    id -- the integer value representing the short_url unique identifier
    """
    return toggle_url_activation(id, 'activate')


@api.route('/shorturl/<int:id>/deactivate', methods=['PUT'])
def deactivate_url(id):
    """
    This function deactivates a shortened URL whose id is passed by calling the
    toggle_url_activation function.

    Keyword arguments:
    id -- the integer value representing the short_url unique identifier
    """
    return toggle_url_activation(id, 'deactivate')


def toggle_url_activation(id, activate_or_deactivate):
    """
    This function toggles the active value of shortened URL with id supplied

    Keyword arguments:
    id -- the integer value for the unique identification of the URL
    activate_or_deactivate -- a string value that indicate if to activate or
                              deactivate
    """
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
    """
    This function returns a collection of shortened URLs by the current user
    """
    user_urls = ShortUrl.query.filter_by(
        user=g.current_user).filter_by(deleted=0).all()
    if user_urls:
        urls = []
        for i in range(len(user_urls)):
            urls.append(user_urls[i].get_details())
        return jsonify({'success': True, 'urls': urls})
    return not_found('No shortened url found')


@api.route('/shorturl/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def shorturl(id):
    """
    This function handles deleting, updating and getting the details of a
    short URL by mapping request method to the appropraite function.

    Keyword arguments:
    id -- the integer value for the unique identification of the URL
    """
    request_mapping = {'GET': get_short_url_details,
                       'DELETE': delete_short_url,
                       'PUT': change_short_url_target}
    url = ShortUrl.query.filter_by(user=g.current_user).filter_by(
        short_url_id=id).filter_by(deleted=0).first()
    if not url:
        return not_found(
            "No shortened url with id '{}' found for you".format(id))
    return request_mapping[request.method](url)


def get_short_url_details(url):
    """
    This function returns the details of a shorl URL

    Keyword arguments:
    url -- the short url object for which details will be returned
    """
    return jsonify({'success': True, 'url': url.get_details()})


def delete_short_url(url):
    """
    This function deletes a shorl URL by setting its deleted propert to 1.

    Keyword arguments:
    url -- the short url object to be deleted
    """
    count = len(ShortUrl.query.filter_by(long_url=url.long_url).all())
    if count <= 1:
        LongUrl.query.filter_by(long_url=url.long_url.long_url).delete()
    url.deleted = 1
    db.session.commit()
    return jsonify({'success': True, 'message': 'deleted'})


def change_short_url_target(url):
    """
    This function updates the long URL of a short URL with the long URL
    supplied in the body of the request.

    Keyword arguments:
    url -- the short url object to be updated
    long_url -- the string value to be updated in the short URL
    """
    long_url_input = ValidateLongUrl(request)
    if not long_url_input.validate():
        return bad_request(long_url_input.errors)
    new_long_url = request.json.get('long_url')
    has_short_url = ShortUrl.query.filter_by(
        user=g.current_user).filter(ShortUrl.long_url.has(
            long_url=new_long_url)).filter_by(deleted=0).first()
    if has_short_url:
        return forbidden("The url already has a shortened url '{}'".format(
            has_short_url.short_url))
    count = len(ShortUrl.query.filter_by(
        long_url=url.long_url).filter_by(deleted=0).all())
    if count <= 1:
        LongUrl.query.filter_by(long_url=url.long_url.long_url).delete()
    new_long_url_check = LongUrl.query.filter_by(long_url=new_long_url).first()
    if not new_long_url_check:
        new_long_url_check = LongUrl(long_url=new_long_url)
        new_long_url_check.save()
    url.long_url = new_long_url_check
    db.session.commit()
    return jsonify({'success': True, 'message': 'updated'})


@api.route('/shorturl/popular', methods=['GET'])
def popular():
    """
    This function return a collection of popular short URLs based on the
    number of visits they have.
    """
    urls = db.session.query(ShortUrl, func.count(visits.c.short_url_id).label(
        'total')).outerjoin(visits).group_by(
        ShortUrl.short_url_id).order_by(
        desc('total')).filter(ShortUrl.deleted == 0).limit(10).all()
    if urls:
        popular_urls = []
        for url in urls:
            url_details = url[0].get_details()
            popular_urls.append(url_details)
        return jsonify({'success': True, 'popular_urls': popular_urls})
    return not_found('No URL found')


@api.route('/shorturl/<int:id>/visitors/', methods=['GET'])
def visitors(id):
    """
    This function returns a list of visitors to the URL with the id supplied.

    Keyword arguments:
    id -- the integer value identifying the URL
    """
    if ShortUrl.query.filter_by(short_url_id=id).filter_by(
            user=g.current_user).filter_by(deleted=0).first():
        visitors = Visitor.query.filter(
            Visitor.short_urls.any(short_url_id=id)).all()
        if visitors:
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


@api.route('/shorturl/<int:id>/visitors/<int:vid>', methods=['GET'])
def visitor(id, vid):
    """
    This function returns the details of a visitor with the id supplied.

    Keyword arguments:
    id -- the integer value identifying the URL visited by the visitor
    vid -- the integer value identifying the visitor
    """
    if ShortUrl.query.filter_by(short_url_id=id).filter_by(
            user=g.current_user).filter_by(deleted=0).first():
        visitor = Visitor.query.filter_by(visitor_id=vid).first()
        if visitor:
            visitor_details = visitor.get_details()
            visitor_details['visitor_url'] = url_for(
                'api.visitor', vid=vid, id=id, _external=True)
            return jsonify({'success': True, 'visitor': visitor_details})
        return not_found("No visitor to this URL with id '{}'".format(vid))
    return not_found("No URL found with id '{}'".format(id))


@api.route('/visit/', methods=['POST'])
def visit():
    """
    This function returns the long URL equivalent of the shortened URL
    supplied.

    Keyword arguments:
    short_url -- the shortened url format string
    """
    short_url_input = ValidateShortUrl(request)
    if not short_url_input.validate():
        return bad_request(short_url_input.errors)
    short_url = request.json.get('short_url')
    short_url_details = ShortUrl.query.filter_by(
        short_url=short_url).first()
    if not short_url_details:
        return not_found('No matching URL found')
    elif short_url_details.deleted:
        return not_found('URL has been deleted')
    elif not short_url_details.active:
        return unavailable('URL has been deactivated')
    else:
        add_visit(short_url_details)
        return jsonify(
            {'success': True, 'long_url': short_url_details.long_url.long_url})


def add_visit(url):
    """
    This function adds the visit details of the URL supplied.

    Keyword arguments:
    url -- the shortened URL visited by the visitor.
    """
    agent = request.user_agent
    visitor = Visitor(ip_address=request.remote_addr,
                      browser=agent.browser, platform=agent.platform)
    visitor.short_urls.append(url)
    visitor.save()

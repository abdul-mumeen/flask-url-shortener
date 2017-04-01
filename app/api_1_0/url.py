import random
import string

import dotenv
from app.models import LongUrl, ShortUrl, User, Visitor
from flask import abort, g, jsonify, request, url_for
from sqlalchemy import desc

from . import api
from .authentication import auth
from .errors import forbidden, not_found, unauthorized
from .validators import ValidateLongUrl

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
                            'message2': 'Url shortened before'})
        if short_url:
            return jsonify({'success': True, 'message': short_url.short_url,
                            'short_url_url': url_for('api.shorturl',
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
                    'short_url_url': url_for('api.shorturl',
                                             _external=True)
                    + str(new_short_url.short_url_id)})


def add_new_short_url(new_short_url, long_url):
    new_short_url.save()
    new_long_url = LongUrl(long_url=long_url)
    new_long_url.short_urls.append(new_short_url)
    g.current_user.short_urls.append(new_short_url)
    new_long_url.save()
    return jsonify({'success': True, 'message': new_short_url.short_url,
                    'short_url_url': url_for('api.shorturl',
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
        short_url.activate = endpoint_map[activate_or_deactivate]
        return jsonify({'success': True, 'message': url_for('api.shorturl',
                                                            _external=True) + str(short_url.short_url_id)})
    return unauthorized('Invalid credentials')


@api.route('/shorturl/')
def shorturl():
    pass

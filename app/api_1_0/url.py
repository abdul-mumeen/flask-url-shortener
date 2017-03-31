from app.models import User, ShortUrl, LongUrl, Visitor
from . import api
from flask import g, jsonify, request, abort
from .authentication import auth
from .errors import not_found, forbidden, unauthorized
from .validators import ValidateLongUrl

import random
import string
import dotenv
dotenv.load()


@api.route('/shorten', methods=['POST'])
def shorten():
    long_url_input = ValidateLongUrl(request)
    if not long_url_input.validate():
        return forbidden(long_url_input.errors)
    long_url = request.json.get('long_url')
    search_long_url = LongUrl.query.filter_by(long_url=long_url).first()
    if search_long_url:
        short_url = search_long_url.short_urls.filter_by(user=g.current_user).first()
        if short_url and request.json.get('vanity'):
            return jsonify({'success': True,
                            'message': short_url.short_url,
                            'message2': 'Url shortened before'})
        if short_url:
            return jsonify({'success': True, 'message': short_url.short_url})
        new_short_url = get_short_url()
        return update_new_short_url(new_short_url, search_long_url)
    new_short_url = get_short_url()
    return add_new_short_url(new_short_url, long_url)


def update_new_short_url(new_short_url, long_url):
    long_url.short_urls.append(new_short_url)
    g.current_user.short_urls.append(new_short_url)
    new_short_url.save()
    return jsonify({'success': True, 'message': new_short_url.short_url})


def add_new_short_url(new_short_url, long_url):
    new_short_url.save()
    new_long_url = LongUrl(long_url=long_url)
    new_long_url.short_urls.append(new_short_url)
    g.current_user.short_urls.append(new_short_url)
    new_long_url.save()
    return jsonify({'success': True, 'message': new_short_url.short_url})


def genarate_short_url(len_range=5):
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
        return abort(unauthorized('Invalid credentials'))
    new_short_url = genarate_short_url()
    return new_short_url


def get_vanity_url(vanity):
    url_prefix = dotenv.get('URL_PREFIX')
    full_vanity_url = url_prefix + vanity
    if ShortUrl.query.filter_by(short_url=full_vanity_url).first():
        vanity_error = "Vanity string '{}' has been taken".format(vanity)
        abort({'message': vanity_error})
    return ShortUrl(short_url=full_vanity_url)


@api.route('/shorturl/recent', methods=['GET'])
def most_recent():
    recent_urls = ShortUrl.query.order_by('date_time desc').limit(5).all()
    if recent_urls:
        urls = []
        for i in range(len(recent_urls)):
            urls.append({'short_url': recent_urls[i].short_url,
                         'short_url_url': recent_urls[i].short_url_id
                         })
        return jsonify({'success': True, 'message': urls})
    return not_found('No url found')

#
# @api.route('/users/<int:id>', methods=['GET'])
# @api.route('/users/influential/', methods=['GET'])
# @api.route('/shorturl/popular/', methods=['GET])
# @api.route('/shorturl/<int:id>', methods=['DELETE'])
# @api.route('/shorturl/<int:id>', methods=['PUT'])
# @api.route('/shorturl/<int:id>', methods=['GET'])
# @api.route('/shorturl/', methods=['GET'])
# @api.route('/shorturl/<int:id>/target/', methods=['PUT'])


@api.route('/shorturl/<int:id>/activate/', methods=['PUT'])
@api.route('/shorturl/<int:id>/deactivate/', methods=['PUT'])
def toggle_url_activation(id):
    endpoint_map = {'activate': 1, 'deactivate': 0}
    short_url = ShortUrl.query.filter_by(short_url_id=id)
    if not short_url or short_url.deleted:
        return not_found('No url with the id {}'.format(id))
    if short_url.user == g.current_user:
        value = request.endpoint.split('/')[-2]
        short_url.activate = endpoint_map[value]
        return jsonify({'success': True, 'message': short_url.short_url})
    return unauthorized('Invalid user access')

from flask import g, jsonify

from app.models import ShortUrl, User, visits
from app.api_1_0 import api
from app import db
from app.api_1_0.errors import not_found


@api.route('/user', methods=['GET'])
def user():
    """
    Return the details of the currently logged in user.
    """
    return jsonify({'success': True, 'user': g.current_user.get_details()})


@api.route('/users/influential', methods=['GET'])
def influential():
    """
    Return a list of influential users which is base on the total number of
    visits users have on all their shortened URLs.
    """
    users_and_visits = (db.session.query(
        User, db.func.count(visits.c.visitor_id)
        .label('total'))
        .join(ShortUrl)
        .outerjoin(visits)
        .filter(User.email != 'anonymous@anonymous.com')
        .filter(ShortUrl.deleted == 0)
        .group_by(User.user_id)
        .order_by(db.desc('total')).all())
    if users_and_visits:
        users = []
        for user_and_visits in users_and_visits:
            user_details = user_and_visits[0].get_details()
            user_details['number_of_visits'] = user_and_visits[1]
            users.append(user_details)
        return jsonify({'success': True, 'users': users})
    return not_found('No user found')

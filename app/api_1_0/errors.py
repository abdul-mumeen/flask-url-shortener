from flask import jsonify


def unavailable(message):
    """
    This function returns a custom unavailable error message.

    keyword arguments:
    message -- the string variable containing the message to be displayed
    """
    response = jsonify({'error': 'unavailable', 'message': message})
    response.status_code = 451
    return response


def bad_request(message):
    """
    This function returns a custom bad request error message.

    keyword arguments:
    message -- the string variable containing the message to be displayed
    """
    response = jsonify({'error': 'bad_request', 'message': message})
    response.status_code = 400
    return response


def forbidden(message):
    """
    This function returns a custom forbidden error message.

    keyword arguments:
    message -- the string variable containing the message to be displayed
    """
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def unauthorized(message):
    """
    This function returns a custom unauthorized error message.

    keyword arguments:
    message -- the string variable containing the message to be displayed
    """
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def not_found(message):
    """
    This function returns a custom not found error message.

    keyword arguments:
    message -- the string variable containing the message to be displayed
    """
    response = jsonify({'error': 'not found', 'message': message})
    response.status_code = 404
    return response

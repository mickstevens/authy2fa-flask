from flask import request, session, jsonify
from functools import wraps

from .models import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id', None)
        api_token = request.headers['X-API-TOKEN']
        if user_id:
            user = User.query.get(user_id)
            if user and user.id == user.verify_api_token(api_token).id:
                return f(*args, **kwargs)
        resp = jsonify({'message': 'Invalid token. Please authenticate.'})
        resp.status_code = 403
        return resp
    return decorated_function



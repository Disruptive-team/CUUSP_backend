from functools import wraps
from flask import request
from app.utils.ret_util import response, RespStatus


def json_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.is_json:
            return f(*args, **kwargs)
        else:
            return response(*RespStatus.ReqDataNotJSON.describe())

    return decorated_function


def auth_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        jwt = request.headers.get("Authorization")
        if jwt is not None:
            return f(*args, **kwargs)
        else:
            return response(*RespStatus.LackAuthorizationHeader.describe())

    return decorated_function

from functools import wraps

from flask import g
from flask import request

from app import jwt_util
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
            # 检查auth_token的有效性
            data = jwt_util.decode_auth_token(jwt)
            if isinstance(data, RespStatus):
                return response(*data.describe())
            else:
                # 存在g里面
                g.auth_token = data
                return f(*args, **kwargs)
        else:
            return response(*RespStatus.LackAuthorizationHeader.describe())

    return decorated_function

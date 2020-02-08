"""
认证模块，提供微信登录,QQ登录,手机登录认证

"""

from flask import request

from app import jwt_util
from . import api
from .decorators import json_required
from .service.auth_service import bind_wx, change_user_info_wx, get_role_wx, get_open_id_wx
from ..utils.login_util import get_wx_login_data
from ..utils.req_util import check_args, get_data_by_jwt
from ..utils.ret_util import response, RespStatus


@api.route('/user/wx/login', methods=["POST"])
@json_required
def login():
    """
    提供各个方式的登录
    :return:
    """
    type, code = request.get_json().get("type"), request.get_json().get("code")
    lack, lack_msg = check_args(type=type, code=code)
    if not lack:
        return response(msg=lack_msg)

    wx_data = get_wx_login_data(code)
    if wx_data.get('session_key') and wx_data.get('openid'):
        # 返回微信用户id号
        we_id = bind_wx(wx_data.get('openid'), wx_data.get('session_key'))
        # 判断用户角色
        role_id = get_role_wx(we_id)
        jwt_data = {
            "role": role_id,
            "uid": we_id
        }
        auth_token = jwt_util.encode_auth_token(jwt_data).decode()
        return response(data={"auth_token": auth_token})
    else:
        return response(code=RespStatus.Auth_WX_Error.value, msg=wx_data.get('errmsg'))


@api.route('/user/wx/updateUserInfo', methods=["POST"])
@json_required
def update_user_info():
    """
    更新微信登录的用户信息
    :return:
    """
    # 从jwt中获取open_id
    jwt_data = get_data_by_jwt(request)
    if isinstance(jwt_data, RespStatus):
        return response(*jwt_data.describe())
    open_id = get_open_id_wx(*[x for x in jwt_data.get("data").values()])
    data = request.get_json()
    user_info = {
        "nick_name": data.get('nick_name'),
        "gender": data.get('gender'),
        "avatar_url": data.get('avatar_url'),
        "country": data.get('country'),
        "city": data.get('city'),
    }
    change_user_info_wx(open_id=open_id, **user_info)

    return response(msg="更新资料成功")



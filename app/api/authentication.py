"""
认证模块，提供微信登录,QQ登录,手机登录认证

"""

from flask import request

from app import jwt_util, logger
from . import api
from .decorators import json_required, auth_token_required
from .service.auth_service import bind_wx, change_user_info_wx, get_role_wx, get_open_id_wx, wxAddNewUser, \
    updateUserPermission, queryUserRole
from ..utils.login_util import get_wx_login_data
from ..utils.req_util import check_args, get_data_by_jwt
from ..utils.ret_util import response, RespStatus, RoleStatus


@api.route('/user/wx/login', methods=["POST"])
@json_required
def login_wx():
    """
    提供各个方式的登录
    :return:
    """
    type = request.get_json().get("type")
    code = request.get_json().get("code")
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
@auth_token_required
def update_user_info():
    """
    更新微信登录的用户信息
    :return:
    """
    # 从jwt中获取open_id
    jwt_data = get_data_by_jwt(request)
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

    return response(msg="更新用户资料成功")


@api.route('/user/wx/bind', methods=["POST"])
@json_required
@auth_token_required
def bind_wx_():
    jwt_data = get_data_by_jwt(request)
    data = request.get_json()
    # 获取学号密码
    stn = data.get('student_number')
    pwd = data.get('password')
    logger.debug(f"获取到用户名{stn} 密码{pwd}")
    lack, lack_msg = check_args(student_number=stn, password=pwd)
    if not lack:
        return response(code=RespStatus.LackArgs.value, msg=lack_msg)

    # 获取微信id
    we_id = jwt_data['data'].get("uid")
    logger.debug(f"从auth_token中获取到信息是{jwt_data}")
    # 插入新用户
    wxAddNewUser(stn, pwd, we_id)
    # 修改微信id的权限,并且下发新的auth_token
    role = RoleStatus.WX_Auth.value
    updateUserPermission(we_id, role)

    role_id = get_role_wx(we_id)
    jwt_data = {
        "role": role_id,
        "uid": we_id
    }
    auth_token = jwt_util.encode_auth_token(jwt_data).decode()
    return response(msg="绑定学号成功", data={"auth_token": auth_token})


@api.route('/user/wx/checkBind', methods=["GET"])
@auth_token_required
def check_bind_wx():
    jwt_data = get_data_by_jwt(request)
    we_id = jwt_data['data'].get("uid")
    role = queryUserRole(we_id)
    if role:
        if role==RoleStatus.WX_Auth.value:
            return response(msg="查询用户权限成功", data={"bind": 1})
        else:
            return response(msg="查询用户权限成功", data={"bind": 0})
    else:
        return response(code=RespStatus.QueryError.value, msg="查询用户权限失败")

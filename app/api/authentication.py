"""
认证模块，提供微信登录,QQ登录,手机登录认证

"""

from flask import request, g

from app import jwt_util, logger
from . import api
from .decorators import json_required, auth_token_required
from .service.auth_service import bind_wx, change_user_info_wx, get_role_wx, add_new_user_wx, \
    update_user_permission_wx, queryUserRole
from ..utils.login_util import get_wx_login_data
from ..utils.req_util import check_args
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
        # 微信用户增加or更新
        open_id = wx_data.get("openid")
        bind_wx(wx_data.get('openid'), wx_data.get('session_key'))
        # 查询用户角色
        role_id = get_role_wx(open_id)
        jwt_data = {
            "role": role_id,
            "uid": open_id
        }
        auth_token = jwt_util.encode_auth_token(jwt_data).decode()
        logger.debug(f"用户id[{open_id}] 角色[{role_id}]正在访问login")
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
    # 从auth_token中获取open_id
    auth_token = g.get("auth_token")
    open_id = auth_token['data'].get("uid")
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
    # jwt_data = get_data_by_jwt(request)
    auth_token = g.get("auth_token")
    # logger.debug(f"通过g获取了auth_token:{jwt_data}")

    data = request.get_json()
    # 获取学号密码
    stn = data.get('student_number')
    pwd = data.get('password')
    logger.debug(f"获取到用户名{stn} 密码{pwd}")
    lack, lack_msg = check_args(student_number=stn, password=pwd)
    if not lack:
        return response(code=RespStatus.LackArgs.value, msg=lack_msg)

    # 获取微信open_id
    open_id = auth_token['data'].get("uid")
    logger.debug(f"从auth_token中获取到信息是{auth_token}")
    # 插入新用户
    add_new_user_wx(stn, pwd, open_id)
    # 修改微信id的权限,并且下发新的auth_token
    role = RoleStatus.WX_Auth.value
    update_user_permission_wx(open_id, role)

    role_id = get_role_wx(open_id)
    auth_token = {
        "role": role_id,
        "uid": open_id
    }
    logger.warning(f"更改用户权限之后的jwt_data为{auth_token}")
    auth_token = jwt_util.encode_auth_token(auth_token).decode()
    return response(msg="绑定学号成功", data={"auth_token": auth_token})


@api.route('/user/wx/checkBind', methods=["GET"])
@auth_token_required
def check_bind_wx():
    # jwt_data = get_data_by_jwt(request)
    auth_token = g.get("auth_token")
    # logger.debug(f"通过g获取了auth_token:{jwt_data}")
    open_id = auth_token['data'].get("uid")
    logger.debug(f"查询微信id为：{open_id}")
    role = queryUserRole(open_id)
    logger.error(f"role {role}")
    if role:
        logger.debug(f"用户权限为{role}")
        if role == RoleStatus.WX_Auth.value:
            return response(msg="查询用户权限成功", data={"bind": 1})
        else:
            return response(msg="查询用户权限成功", data={"bind": 0})
    else:
        return response(code=RespStatus.QueryError.value, msg="查询用户权限失败,可能是没有此用户!")





# @api.route('/user/wx/unBind')
# @auth_token_required
# def check_auth_token():
#     auth_token = g.get("auth_token")
#     # 查询
#     uid = auth_token["data"].get("uid")
#     role = auth_token["data"].get("role")
#
#     unBind(uid,role)

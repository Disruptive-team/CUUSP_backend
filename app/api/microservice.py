"""
微服务模块，提供微服务认证,微服务使用
"""
from flask import request

from app import logger
from app.utils.ret_util import response, RespStatus
from . import api, json_required, auth_token_required
from .service.ms_service import get_all_ms, reg_ms, get_u_number_pwd, get_key_iv_by_appid
from ..utils.crypto_util import AES256CBC
from ..utils.req_util import check_args, get_data_by_jwt


@api.route('/ms/getAll', methods=['GET'])
def get_all():
    """
    获取所有的微服务
    """
    data = get_all_ms()
    logger.debug("获取微服务列表成功...")
    return response(data=data)


@api.route('/ms/reg', methods=['POST'])
@json_required
def ms_reg():
    # 需要 url,name,link,返回key,iv,app_id
    # 还有注册类型 newMs addSubMs
    regType = request.args.get("regType")
    lack, lack_msg = check_args(regType=regType)
    if not lack:
        return response(code=RespStatus.LackArgs.value, msg=lack_msg)

    if regType == 'newMs':
        # 注册新的微服务
        data = request.get_json()
        link = data.get("link")
        name = data.get("name")
        img_url = data.get("img_url")
        lack, lack_msg = check_args(link=link, name=name, img_url=img_url)
        if not lack:
            return response(code=RespStatus.LackArgs.value, msg=lack_msg)
        data = reg_ms(link, name, img_url)

        logger.debug(f"注册成功,data为{data}")
        return response(msg='注册成功', data=data)
    elif regType == 'addSubMs':
        # 检测appid
        appid = request.args.get("appid")
        lack, lack_msg = check_args(appid=appid)
        if not lack:
            return response(msg=lack_msg)
        # TODO 增加子模块
    else:
        return response(code=400, msg='regType error！')


@api.route('/ms/getUserSecret', methods=["GET", "POST"])
@json_required
@auth_token_required
def getUserSecret():
    # 知道微服务ID E(appid)+appid

    # 获取加密认证
    data = request.get_json()
    verify = data.get('verify')
    appid = data.get('appid')
    lack, lack_msg = check_args(verify=verify, appid=appid)
    if not lack:
        return response(code=RespStatus.LackArgs.value, msg=lack_msg)
    logger.debug(f"微服务Post data:{data}")

    # 检查是否一样
    key_iv = get_key_iv_by_appid(appid)
    key = key_iv['key'].encode()
    iv = key_iv['iv'].encode()
    f = AES256CBC(key, iv)
    de_appid = f.decrypt(verify.encode())
    logger.debug(f"appid: {appid} de_appid:{de_appid}")
    if de_appid != appid:
        return response(code=RespStatus.Forbidden.value, msg='verify error!')

    jwt_data = get_data_by_jwt(request)

    user_info = get_u_number_pwd(*[x for x in jwt_data.get("data").values()])
    if user_info is None:
        return response(code=RespStatus.QueryError.value, msg="获取用户信息失败")
    logger.debug(f"查询到用户名和密码{user_info}")
    # 加密用户名和密码
    c = AES256CBC(key, iv)
    user_info['student_number'] = c.encrypt(user_info['student_number']).decode()
    user_info['password'] = c.encrypt(user_info['password']).decode()
    return response(msg="获取用户信息成功", data=user_info)

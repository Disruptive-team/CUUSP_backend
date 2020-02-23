"""
对数据库操作的简单封装
"""
from app.models import WechatBind, Student
from app import db_wrapper, logger
from app.utils.ret_util import RoleStatus

import datetime


def bind_wx(open_id, secret_key):
    # 第一次登录数据库新加数据，如果是session_key失效就更新
    with db_wrapper.database.atomic():
        data = WechatBind.get_or_none(open_id=open_id)
        if data is None:
            WechatBind.insert(open_id=open_id, secret_key=secret_key,
                              create_time=datetime.datetime.now()).execute()
        else:
            WechatBind.update(secret_key=secret_key).where(WechatBind.open_id == open_id).execute()
            # return WechatBind.select().where(WechatBind.open_id == open_id).get().we_id


def change_user_info_wx(open_id, **kwargs):
    # 修改微信用户资料

    with db_wrapper.database.atomic():
        wx_user = WechatBind.select().where(WechatBind.open_id == open_id).get()
        wx_user.avatar_url = kwargs.get("avatar_url")
        wx_user.nick_name = kwargs.get("nick_name")
        wx_user.city = kwargs.get("city")
        wx_user.country = kwargs.get("country")
        wx_user.gender = kwargs.get("gender")
        affect_row = wx_user.save()
        if affect_row != 1:
            return None
        else:
            return affect_row


def get_role_wx(open_id):
    # 获取微信用户的权限

    with db_wrapper.database.atomic():
        wx_user = WechatBind.get_or_none(WechatBind.open_id == open_id)
        if wx_user:
            return wx_user.permission
        else:
            return None


def get_open_id_wx(role_id, we_id):
    # 获取微信openid
    with db_wrapper.database.atomic():
        if role_id in [RoleStatus.WX_Visitor.value, RoleStatus.WX_Auth.value]:
            with db_wrapper.database.atomic():
                data = WechatBind.get_or_none(WechatBind.we_id == we_id)
                if data is not None:
                    return data.open_id
                else:
                    return None


def add_new_user_wx(student_number, password, open_id):
    # 增加微信绑定
    with db_wrapper.database.atomic():
        stu = Student()
        stu.student_number = student_number
        stu.password = password
        stu.save()
        affect_row = WechatBind.update(student=stu.s_id).where(WechatBind.open_id == open_id).execute()
        if affect_row != 1:
            return None
        else:
            return affect_row


def update_user_permission_wx(open_id, role):
    # 更新微信用户的权限

    with db_wrapper.database.atomic():
        wx_user = WechatBind.get_or_none(WechatBind.open_id == open_id)
        if wx_user:
            wx_user.permission = role
            affect_row = wx_user.save()
            logger.debug(f"更新微信用户的权限影响的行数为{affect_row}")
            if affect_row != 1:
                return 0
            else:
                return affect_row
        else:
            return None


def queryUserRole(open_id):
    # 查询微信用户的权限
    with db_wrapper.database.atomic():
        wx_user = WechatBind.get_or_none(WechatBind.open_id == open_id)
        if wx_user:
            return wx_user.permission
        else:
            return None

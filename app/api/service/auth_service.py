"""
对数据库操作的简单封装
"""
from app.models import WechatBind, Student
from app import db_wrapper
from app.utils.ret_util import RoleStatus


def bind_wx(open_id, secret_key):
    """
    返回主键的值
    :param open_id: str
    :param secret_key: str
    :return: int
    """
    # 第一次登录数据库新加数据，如果是session_key失效就更新
    with db_wrapper.database.atomic():
        data = WechatBind.get_or_none(open_id=open_id)
        if data is None:
            return WechatBind.insert(open_id=open_id, secret_key=secret_key).execute()
        else:
            WechatBind.update(secret_key=secret_key).where(WechatBind.open_id == open_id).execute()
            return WechatBind.select().where(WechatBind.open_id == open_id).get().we_id


def change_user_info_wx(open_id, **kwargs):
    """
    修改微信用户资料
    :param open_id: str
    :param kwargs: dict
    :return:
    """
    with db_wrapper.database.atomic():
        wx_user = WechatBind.select().where(WechatBind.open_id == open_id).get()
        wx_user.avatar_url = kwargs.get("avatar_url")
        wx_user.nick_name = kwargs.get("nick_name")
        wx_user.city = kwargs.get("city")
        wx_user.country = kwargs.get("country")
        wx_user.gender = kwargs.get("gender")
        return wx_user.save()


def get_role_wx(wx_id):
    """
    获取微信用户的权限
    :param wx_id: int
    :return:
    """
    with db_wrapper.database.atomic():
        user = Student.get_or_none(Student.we == wx_id)
        if user is None:
            return RoleStatus.WX_Visitor.value
        else:
            return RoleStatus.WX_Auth.value

def get_open_id_wx(role_id,we_id):
    if role_id in [RoleStatus.WX_Visitor.value,RoleStatus.WX_Auth.value]:
        with db_wrapper.database.atomic():
            data = WechatBind.get_or_none(WechatBind.we_id==we_id)
            if data is not None:
                return data.open_id


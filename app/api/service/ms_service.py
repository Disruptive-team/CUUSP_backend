"""
对数据库操作的简单封装,用于微服务
"""
from app.models import WechatBind, Student, MicroService
from app import db_wrapper
from app.utils.ret_util import RoleStatus


def get_all_ms():
    """
    返回所有的微服务信息
    """
    all_data = MicroService.select()
    ms_list = []
    for data in all_data:
        temp = {
            "ms_id": data.ms_id,
            "ms_name": data.ms_name,
            "ms_url": data.ms_url,
            "img_url": data.img_url,
        }
        ms_list.append(temp)
    return ms_list

"""
对数据库操作的简单封装,用于微服务
"""
from app.models import WechatBind, Student, MicroService
from app import db_wrapper
from app.utils import gen_ms_appid
from app.utils.ret_util import RoleStatus
from app.utils.crypto_util import AES256CBC


def get_all_ms():
    # 返回所有的微服务信息
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


def reg_ms(link, name, img_url):
    # 注册微服务
    with db_wrapper.database.atomic():
        info = MicroService()
        info.ms_url = link
        info.ms_name = name
        info.img_url = img_url

        key = AES256CBC.generate_key()
        iv = AES256CBC.generate_iv()
        appid = gen_ms_appid()
        info.ms_key = key.decode()
        info.ms_iv = iv.decode()
        info.ms_appid = appid
        affect_row = info.save()
        if affect_row != 1:
            return None
        else:
            ms_id = info.ms_id
            return {'id': ms_id, "key": key.decode(), "iv": iv.decode(), "appid": appid}


def get_u_number_pwd(role_id, we_id):
    # 获取学号密码，通过role_id和we_id
    if role_id in [RoleStatus.WX_Auth.value]:
        with db_wrapper.database.atomic():
            query = WechatBind.select(Student.student_number, Student.password).join(Student).where(
                (WechatBind.student == Student.s_id) & (WechatBind.we_id == we_id)).dicts()
            if query.count() != 0:
                return query.get()
            else:
                return None


def get_key_iv_by_appid(appid):
    # 通过appid获取key和iv
    exist = MicroService.get_or_none(MicroService.ms_appid == appid)
    if exist:
        return {'key': exist.ms_key, 'iv': exist.ms_iv}
    else:
        return None

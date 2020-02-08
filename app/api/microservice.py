"""
微服务模块，提供微服务认证,微服务使用
"""
from . import api
from .service.ms_service import get_all_ms
from app.utils.ret_util import response

from app import logger
@api.route('/ms/getAll', methods=['GET'])
def get_all():
    """
    获取所有的微服务
    """
    data = get_all_ms()
    logger.info("data....")
    return response(data=data)

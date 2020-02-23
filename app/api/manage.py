from flask import g

from . import api, auth_token_required
from .service.manage_service import getActiveSwiper
from .. import logger
from ..utils.ret_util import response


@api.route('/getActiveSwiper', methods=["GET"])
def get_swiper():
    data = getActiveSwiper()
    print(111)
    logger.info("获取轮播图成功")
    return response(msg="获取轮播图成功!", data=data)


@api.route("/testg")
@auth_token_required
def testg():
    print(dir(g))
    print(g.get("auth_token"))
    return "aaaa"


@api.route("/testg1")
def testg1():
    print(dir(g))
    # print(g.auth_token)
    return "sss"

from app.models import Swiper
from app import db_wrapper, logger


def getActiveSwiper():
    data = Swiper.select(
        Swiper.img_url,
        Swiper.jump_url,
        Swiper.priority
    ).where(Swiper.enable == 1).order_by(Swiper.priority.desc()).dicts()
    if data.count() == 0:
        return None
    else:
        return [x for x in data]

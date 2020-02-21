from app.api.service.ms_service import get_all_ms, reg_ms, get_u_number_pwd, get_key_iv_by_appid
from tests.test_base import BaseTestCase


class MSTestCase(BaseTestCase):

    def test_get_all_ms(self):
        ms_list = get_all_ms()
        self.assertNotEqual(ms_list,None)

    def test_reg_ms(self):
        info = {
            'link':'baidu.com',
            "name":"百度",
            "img_url":"xxx.com/1.jpg"
        }
        ms_data = reg_ms(**info)
        self.assertNotEqual(ms_data,None)

    def test_get_u_number_pwd(self):
        data = get_u_number_pwd(10001,3)
        self.assertEqual(data,None)

    def test_get_key_iv_by_appid(self):
        data = get_key_iv_by_appid("MS_54e643e33e1ba13d96c9a")
        self.assertNotEqual(data,None)
        data = get_key_iv_by_appid("xxx")
        self.assertEqual(data,None)


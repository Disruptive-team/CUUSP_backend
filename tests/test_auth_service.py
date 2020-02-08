from app.api.service.auth_service import change_user_info_wx, get_role_wx, get_open_id_wx
from app.utils.ret_util import RoleStatus
from tests.test_base import BaseTestCase


class ServiceTestCase(BaseTestCase):

    def test_change_wx_user_info(self):
        user_info = {
            "nick_name": "Li",
            'gender': 2,
            'avatar_url': "baidu.com",
            'country': "中国",
            'city': '绵阳'
        }
        affect_row = change_user_info_wx("open_id_1", **user_info)
        self.assertEqual(affect_row, 1)

    def test_get_wx_role(self):
        role_id = get_role_wx(1)
        self.assertEqual(role_id, RoleStatus.WX_Auth.value)
        role_id_2 = get_role_wx(5)
        self.assertEqual(role_id_2, RoleStatus.WX_Visitor.value)

    def test_get_open_id_wx(self):
        open_id = get_open_id_wx(RoleStatus.WX_Auth.value, 1)
        self.assertEqual(open_id,"open_id_1")
        open_id_2 = get_open_id_wx(RoleStatus.WX_Visitor.value, 5)
        self.assertEqual(open_id_2,"open_id_5")

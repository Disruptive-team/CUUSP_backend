from app.api.service.ms_service import get_all_ms
from tests.test_base import BaseTestCase


class MSTestCase(BaseTestCase):

    def test_get_all_ms(self):
        ms_list = get_all_ms()
        self.assertEqual(len(ms_list),5)

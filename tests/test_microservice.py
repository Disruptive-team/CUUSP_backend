from tests.test_base import BaseTestCase


class MSAPITestCase(BaseTestCase):
    def test_get_all(self):
        response = self.client.get(
            '/api/ms/getAll'
        )
        self.assertEqual(response.get_json().get("code"), 200)
        print(response.get_json())

    def test_ms_reg(self):
        response = self.client.post(
            '/api/ms/reg',
            json={
                "link": "baidu.com",
                "name": "234",
                "img_url": "xxx.com1.jpg"}

        )
        self.assertEqual(response.get_json().get("code"), 200)
        print(response.get_json())

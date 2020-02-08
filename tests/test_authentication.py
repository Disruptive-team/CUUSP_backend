from tests.test_base import BaseTestCase


class AuthTestCase(BaseTestCase):

    def get_api_headers(self, auth_token=None):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': auth_token
        }

    def test_wx_bind(self):
        response = self.client.post(
            '/api/user/wx/login',
            headers=self.get_api_headers(),
            json={
                "code":"0232MdKA0jVWvj2GHjHA0vKYJA02MdKH",
                "type":"wx"
            }
        )
        self.assertEqual(response.get_json().get("code"),200)
        print(response.get_json())

    def test_update_user_info(self):
        auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJoZWFkZXJzIjp7InR5cCI6IkpXVCIsImFsZyI6IkhTMjU2In0sImlzcyI6IksuRGVuZyIsImV4cCI6MTU4OTQ2MDIyMCwiaWF0IjoxNTgwOTA2NjIwLCJkYXRhIjp7InJvbGUiOjEwMDAwLCJ1aWQiOjI1Nn19.d4rYrc2Cc0LIo1wO2e2I-oIajylgT-8vL4eNaG7mReQ"
        user_info = {
            "nick_name": "Li",
            'gender': 2,
            'avatar_url': "http://baidu.com",
            'country': "四川省",
            'city': '绵阳市'
        }
        response = self.client.post(
            '/api/user/wx/updateUserInfo',
            headers=self.get_api_headers(auth_token),
            json=user_info
        )
        self.assertEqual(response.get_json().get('code'),200)
        print(response.get_json())

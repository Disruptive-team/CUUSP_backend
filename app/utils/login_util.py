from .requests_util import get
import os


def get_wx_login_data(code: str):
    params = {
        "appid": os.environ.get('appid'),
        "secret": os.environ.get('appsecret'),
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    code2Session_url = "https://api.weixin.qq.com/sns/jscode2session"
    return get(code2Session_url, params=params).json()


if __name__ == '__main__':
    print(get_wx_login_data("033A7dmf0LEz5x1oKIof0Y4qmf0A7dmi"))
    # session_key  openid
    # errcode errormsg
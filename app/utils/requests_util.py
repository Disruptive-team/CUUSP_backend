import requests
from functools import partial

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',

}
get = partial(requests.get, headers=headers,timeout=15)
post = partial(requests.post, headers=headers,timeout=15)

if __name__ == '__main__':
    payload = {
        "wd": 123
    }
    print(get("http://baidu.com/s", params=payload).url)

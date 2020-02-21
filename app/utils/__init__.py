"""
公共工具类
"""
import hashlib
import time
import os


def gen_ms_appid():
    # 生成24位唯一的appid
    encode_str = str(int(time.time())) + str(os.urandom(64))
    m = hashlib.sha1()
    m.update(str.encode(encode_str))
    return 'MS_' + m.hexdigest()[:21]

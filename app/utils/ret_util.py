from enum import Enum, unique

from flask import jsonify


@unique
class RespStatus(Enum):
    """
    返回的状态码及说明
    """

    def describe(self, ret=True):
        if not ret:
            return self.name, self.value
        else:
            return self.value, self.name

    # 通用状态码
    OK = 200
    BadRequest = 400
    Forbidden = 403
    NotFound = 404
    MethodNotAllowed = 405
    ServerError = 500
    GateWayError = 502

    # 业务状态码，原则上与通用状态码一致
    # 设计原则为 AABBCC
    # AA状态号 BB业务号 CC业务码

    # JWT相关 01
    ExpiredSignature = 400101
    InvalidToken = 400102
    LackAuthorizationHeader = 400103

    # 认证相关 02
    Auth_WX_Error = 400201

    # 数据库相关 03
    InsertError = 400301
    UpdateError = 400302
    QueryError = 400303
    DeleteError = 400304
    DataBaseError = 400305

    # 其它 99
    ReqDataNotJSON = 409901
    LackArgs = 409902


@unique
class RoleStatus(Enum):
    # 角色说明
    WX_Visitor = 10000
    QQ_Visitor = 20000
    Phone_Visitor = 30000

    WX_Auth = 10001
    QQ_Auth = 20001
    Phone_Auth = 30001
    Admin = 40001


def resp_wrapper(code=200, msg="ok", data=None):
    obj = {
        'code': code,
        'msg': msg,
        'data': data
    }
    return jsonify(obj)


response = resp_wrapper
if __name__ == '__main__':
    print(resp_wrapper(msg=RespStatus.ExpiredSignature.name))

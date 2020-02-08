from app import jwt_util
from .resp_code_util import RespStatus

def check_args(**kwargs) -> tuple:
    args_list = []
    for k, v in kwargs.items():
        if v is None:
            msg = "Missing arg `{}`".format(k)
            args_list.append(msg)
    if args_list:
        return False, args_list
    return True, None


def get_data_by_jwt(request):
    jwt = request.headers.get("Authorization")
    if jwt is None:
        return RespStatus.LackAuthorizationHeader
    return jwt_util.decode_auth_token(jwt)
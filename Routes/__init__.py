from vibora.responses import JsonResponse
from vibora.blueprints import Blueprint
from vibora import Request
from time import time
import basicauth
import Controllers
from Utils.Exceptions import *
from mongoengine import DoesNotExist


bp = Blueprint()


def err_resp(code: int, msg: str):
    """
    generate error response
    :param code: error code
    :param msg: error msg
    :return: JsonResponse
    """

    return JsonResponse({
        "ok": False,
        "code": code,
        "msg": msg,
        "timestamp": time()
    }, status_code=code)


def suc_resp(content):
    """
    generate success response
    :param content: resp content
    :return: JsonResponse
    """
    content['ok'] = True
    content['timestamp'] = time()
    return JsonResponse(content)


def extract_bearer(authorization):
    """
    extract bearer token from authorization header
    :param authorization: Authorization header value
    :return: token on success
    :raises TokenDoesNotExist:
    :raises InvalidMethod:
    :raises InvalidValue:
    """

    if not authorization:
        raise TokenDoesNotExist()

    split = authorization.split(" ")
    if len(split) != 2:
        raise InvalidValue()

    if split[0] != "Bearer":
        raise InvalidMethod()

    return split[0]


@bp.route('/register', methods=['POST'])
async def register(request: Request):
    """
    register a new user
    provide user gid and password to register
    Authorization: Basic gid:password
    """
    gid, pswd = basicauth.decode(request.headers.get('Authorization'))
    try:
        user = Controllers.register(gid, pswd)
    except UserAlreadyExist:
        return err_resp(400, "user already exist")

    return suc_resp({
        "gid": user.gid,
        "reg_date": user.reg_date
    })


@bp.route('/login', methods=['GET'])
async def login(request: Request):
    """
    login a user
    provide user gid and password as basic auth
    """
    gid, pswd = basicauth.decode(request.headers.get('Authorization'))
    try:
        session = Controllers.login(gid, pswd)
    except DoesNotExist:
        return err_resp(404, "user does not exist")

    jwt_token, payload = session.generate_jwt()
    return suc_resp({
        "jwt": {
            "token": jwt_token,
            "refresh_token": session.refresh_token,
            "payload": payload
        },
        "gid": gid
    })


@bp.route('/token/logout', methods=['POST'])
async def logout(request: Request):
    """
    provide refresh token as Bearer token
    """

    try:
        token = extract_bearer(request.headers.get("Authorization"))
    except InvalidMethod:
        err_resp(400, "bad authorization method")
    except InvalidValue:
        err_resp(400, "bad authorization token")
    except TokenDoesNotExist:
        return err_resp(400, "missing authorization token")

    try:
        session = Controllers.logout(token)
    except DoesNotExist:
        return err_resp(404, "session was not found")

    return suc_resp({
        "logged_out": True,
        "token": token,
        "gid": session.user.gid
    })


@bp.route('/token/refresh', methods=['GET'])
async def refresh_token(request: Request):
    """
    refresh jwt token using refresh token
    Authorization: Bearer [Refresh Token]
    """

    try:
        token = extract_bearer(request.headers.get("Authorization"))
    except InvalidMethod:
        err_resp(400, "bad authorization method")
    except InvalidValue:
        err_resp(400, "bad authorization token")
    except TokenDoesNotExist:
        return err_resp(400, "missing authorization token")

    try:
        session = Controllers.refresh_token(token)
    except DoesNotExist:
        return err_resp(404, "session was not found")

    jwt_token, payload = session.generate_jwt()
    return suc_resp({
        "jwt": {
            "token": jwt_token,
            "refresh_token": session.refresh_token,
            "payload": payload
        },
        "gid": session.user.gid
    })


@bp.route('/password/reset', methods=['POST'])
async def reset_password(request: Request):
    # provide old password and new
    pass


@bp.route('/password/forgot', methods=['POST'])
async def forgot_password(request: Request):
    # issue temp token for password reset
    pass


@bp.route('/verify', methods=['POST'])
async def verify(request: Request):
    # provide token and jwt code
    pass

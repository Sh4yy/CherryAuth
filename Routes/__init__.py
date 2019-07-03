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


def extract_basic(authorization):
    """
    extract basic authorization from header
    :param authorization: Authorization header value
    :return: gid, password on success
    :raises TokenDoesNotExist:
    """
    if not authorization:
        raise TokenDoesNotExist()

    return basicauth.decode(authorization)


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
    try:

        gid, pswd = extract_basic(request.headers.get('Authorization'))
        user = Controllers.register(gid, pswd)
        return suc_resp({
            "gid": user.gid,
            "reg_date": user.reg_date
        })

    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except UserAlreadyExist:
        return err_resp(400, "user already exist")


@bp.route('/login', methods=['GET'])
async def login(request: Request):
    """
    login a user
    provide user gid and password as basic auth
    """
    try:

        gid, pswd = extract_basic(request.headers.get('Authorization'))
        session = Controllers.login(gid, pswd)
        jwt_token, payload = session.generate_jwt()
        return suc_resp({
            "jwt": {
                "token": jwt_token,
                "refresh_token": session.refresh_token,
                "payload": payload
            },
            "gid": gid
        })

    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except DoesNotExist:
        return err_resp(404, "user does not exist")


@bp.route('/token/logout', methods=['POST'])
async def logout(request: Request):
    """
    provide refresh token as Bearer token
    """
    try:

        token = extract_bearer(request.headers.get("Authorization"))
        session = Controllers.logout(token)
        return suc_resp({
            "logged_out": True,
            "token": token,
            "gid": session.user.gid
        })

    except InvalidMethod:
        err_resp(400, "bad authorization method")
    except InvalidValue:
        err_resp(400, "bad authorization token")
    except TokenDoesNotExist:
        return err_resp(400, "missing authorization token")
    except DoesNotExist:
        return err_resp(404, "session was not found")


@bp.route('/token/refresh', methods=['GET'])
async def refresh_token(request: Request):
    """
    refresh jwt token using refresh token
    Authorization: Bearer [Refresh Token]
    """
    try:

        token = extract_bearer(request.headers.get("Authorization"))
        session = Controllers.refresh_token(token)
        jwt_token, payload = session.generate_jwt()
        return suc_resp({
            "jwt": {
                "token": jwt_token,
                "refresh_token": session.refresh_token,
                "payload": payload
            },
            "gid": session.user.gid
        })

    except InvalidMethod:
        return err_resp(400, "bad authorization method")
    except InvalidValue:
        return err_resp(400, "bad authorization token")
    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except DoesNotExist:
        return err_resp(404, "session was not found")


@bp.route('/password/change', methods=['POST'])
async def change_password(request: Request):
    """
    change user's password
    requires old password as basic authorization
    and new_password field in body as well as an
    optional kill_sessions boolean field to kill
    all the currently active sessions.
    """
    try:
        gid, old_pswd = extract_basic(request.headers.get('Authorization'))
        json_data = await request.json()

        if 'new_password' not in json_data:
            return err_resp(400, 'missing new_password field')
        new_password = json_data.get('new_password')
        kill_sessions = json_data.get('kill_sessions', False)
        Controllers.change_password(gid, old_pswd, new_password, kill_sessions)
        return suc_resp({
            "changed_password": True,
            "killed_sessions": kill_sessions,
        })

    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except DoesNotExist:
        return err_resp(404, "user was not found")
    except WrongPassword:
        return err_resp(401, "wrong password")


@bp.route('/password/reset/request', methods=['POST'])
async def reset_password_request(request: Request):
    # issue temp token for password reset
    pass


@bp.route('/password/reset', methods=['POST'])
async def reset_password(request: Request):
    # provide password token for reset
    pass


@bp.route('/verify', methods=['POST'])
async def verify(request: Request):
    # provide token and jwt code
    pass

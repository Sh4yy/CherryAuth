from sanic.response import json
from time import time
import basicauth
import controllers
from Utils.Exceptions import *
from mongoengine import DoesNotExist
from Utils import JWT
from sanic import Blueprint
# from Utils.Caching import VerifyCache


bp = Blueprint('routes')


def err_resp(code: int, msg: str, err_subcode=None):
    """
    generate error response
    :param code: error code
    :param msg: error msg
    :param err_subcode: specific error details
    :return: JsonResponse
    """
    return json({
        "ok": False,
        "code": code,
        "msg": msg,
        "timestamp": time(),
        "error_subcode": err_subcode
    }, status=code)


def suc_resp(content):
    """
    generate success response
    :param content: resp content
    :return: JsonResponse
    """
    content['ok'] = True
    content['timestamp'] = time()
    return json(content)


def extract_basic(authorization):
    """
    extract basic authorization from header
    :param authorization: Authorization header value
    :return: uid, password on success
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

    return split[1]


# @bp.route('/verify', methods=['POST'], cache=VerifyCache())
@bp.post('/verify')
def verify(request):
    """
    verify a user's jwt token
    """
    try:

        jwt_token = extract_bearer(request.headers.get('Authorization'))
        return suc_resp({
            "valid": True,
            "payload": JWT.verify_jwt(jwt_token)
        })

    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except InvalidMethod:
        return err_resp(400, "invalid authorization method")
    except InvalidValue:
        return err_resp(400, "invalid authorization token")
    except JWT.ExpiredSignatureError:
        return err_resp(401, "expired signature")
    except JWT.InvalidSignatureError:
        return err_resp(401, "invalid signature")
    except JWT.InvalidTokenError:
        return err_resp(401, "invalid token")


# @bp.route('/register', methods=['POST'])
@bp.route('/register')
def register(request):
    """
    register a new user
    provide user uid and password to register
    Authorization: Basic uid:password
    """
    try:

        uid, pswd = extract_basic(request.headers.get('Authorization'))
        user = controllers.register(uid, pswd)
        return suc_resp({
            "uid": user.uid,
            "reg_date": user.reg_date
        })

    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except UserAlreadyExist:
        return err_resp(400, "user already exist")


# @bp.route('/login', methods=['GET'])
@bp.get('/login')
def login(request):
    """
    login a user
    provide user uid and password as basic auth
    """
    try:

        uid, pswd = extract_basic(request.headers.get('Authorization'))
        session = controllers.login(uid, pswd)
        jwt_token, payload = session.generate_jwt()
        return suc_resp({
            "jwt": {
                "token": jwt_token,
                "refresh_token": session.refresh_token,
                "payload": payload
            },
            "uid": uid
        })

    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except DoesNotExist:
        return err_resp(404, "user does not exist")
    except IncorrectCredentials:
        return err_resp(401, "incorrect credentials")


# @bp.route('/logout', methods=['POST'])
@bp.post('/logout')
def logout(request):
    """
    provide refresh token as Bearer token
    """
    try:

        token = extract_bearer(request.headers.get("Authorization"))
        session = controllers.logout(token)
        return suc_resp({
            "logged_out": True,
            "token": token,
            "uid": session.user.uid
        })

    except InvalidMethod:
        err_resp(400, "invalid authorization method")
    except InvalidValue:
        err_resp(400, "invalid authorization token")
    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except DoesNotExist:
        return err_resp(404, "session does not exist")


# @bp.route('/token/refresh', methods=['GET'])
@bp.get('/token/refresh')
def refresh_token(request):
    """
    refresh jwt token using refresh token
    Authorization: Bearer [Refresh Token]
    """
    try:

        token = extract_bearer(request.headers.get("Authorization"))
        session = controllers.refresh_token(token)
        jwt_token, payload = session.generate_jwt()
        return suc_resp({
            "jwt": {
                "token": jwt_token,
                "refresh_token": session.refresh_token,
                "payload": payload
            },
            "uid": session.user.uid
        })

    except InvalidMethod:
        return err_resp(400, "invalid authorization method")
    except InvalidValue:
        return err_resp(400, "invalid authorization token")
    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except DoesNotExist:
        return err_resp(404, "session does not exist")


# @bp.route('/password/change', methods=['POST'])
@bp.post('/password/change')
def change_password(request):
    """
    change user's password
    requires old password as basic authorization
    and new_password field in body as well as an
    optional kill_sessions boolean field to kill
    all the currently active sessions.
    """
    try:

        uid, old_pswd = extract_basic(request.headers.get('Authorization'))
        json_data = request.json()

        if 'new_password' not in json_data:
            return err_resp(400, 'missing new_password field')
        new_password = json_data.get('new_password')
        kill_sessions = json_data.get('kill_sessions', False)
        controllers.change_password(uid, old_pswd, new_password, kill_sessions)
        return suc_resp({
            "changed_password": True,
            "killed_sessions": kill_sessions,
        })

    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except UserWasNotFound:
        return err_resp(404, "user was not found")
    except WrongPassword:
        return err_resp(401, "incorrect credentials")


# @bp.route('/password/reset/request', methods=['POST'])
@bp.post('/password/reset/request')
def reset_password_request(request):
    # issue temp token for password reset
    pass


# @bp.route('/password/reset', methods=['POST'])
@bp.post('/password/reset')
def reset_password(request):
    # provide password token for reset
    pass




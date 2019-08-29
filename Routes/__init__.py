import controllers
from mongoengine import DoesNotExist
from Utils import JWT
from sanic import Blueprint
from Utils.RouteUtils import *


bp = Blueprint('auth_routes')


@bp.post('/verify', version=1)
async def verify(request):
    """
    verify a user's jwt token
    """
    try:

        jwt_token = extract_bearer(request.headers.get('Authorization'))
        payload = controllers.verify_jwt_token(jwt_token)

        return suc_resp({
            "valid": True,
            "payload": payload
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


@bp.post('/register', version=1)
async def register(request):
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
            "reg_date": user.date_created
        })

    except TokenDoesNotExist:
        return err_resp(400, "missing authorization header")
    except UserAlreadyExist:
        return err_resp(400, "user already exist")


@bp.get('/login', version=1)
async def login(request):
    """
    login a user
    provide user uid and password as basic auth
    """
    try:

        uid, pswd = extract_basic(request.headers.get('Authorization'))
        session = controllers.login(uid, pswd)
        jwt_token, payload = session.gen_jwt(ttl=timedelta(days=7).total_seconds())

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


@bp.post('/logout', version=1)
async def logout(request):
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
@bp.get('/token/refresh', version=1)
async def refresh_token(request):
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


@bp.post('/password/change', version=1)
async def change_password(request):
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


@bp.post('/password/reset/request', version=1)
async def reset_password_request(request):
    # issue temp token for password reset
    pass


@bp.post('/password/reset', version=1)
async def reset_password(request):
    # provide password token for reset
    pass




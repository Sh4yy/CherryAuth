from models import User, Credentials, Session
from Utils.Exceptions import *
from Utils.CacheEngine import Cache
from Utils import JWT


def register(uid, password):
    """
    register a new user
    :param uid: user's global id
    :param password: user's password
    :return: user instance
    :raises UserAlreadyExist:
    """

    if User.find_with_uid(uid) is not None:
        raise UserAlreadyExist()

    user = User.register(uid)
    Credentials.init(user, password)

    return user


def login(uid, password):
    """
    login a user
    :param uid: user's global id
    :param password: user's password
    :return: Session instance
    :raises IncorrectCredentials:
    :raises UserWasNotFound:
    """

    user = User.find_with_uid(uid)
    if not user:
        raise UserWasNotFound()

    credentials = user.credentials.get()
    if not credentials.does_match(password):
        raise IncorrectCredentials()

    session = Session.init(user)
    return session


def logout(ref_token):
    """
    logout a user from a session
    :param ref_token: user's refresh token
    :return: Session instance
    :raises RefreshTokenIsNotValid
    """

    session = Session.find_with_refresh_token(ref_token)
    if not session:
        raise RefreshTokenIsNotValid()

    session.delete_instance()
    return session


def refresh_token(ref_token):
    """
    create a new jwt token
    :param ref_token: user's refresh token
    :return: Session instance
    """

    return Session.find_with_refresh_token(ref_token)


def terminate_sessions(uid):
    """
    terminate all sessions for a user
    :param uid: user's uid
    :return: True on success
    :raises DoesNotExist: if user was not found
    """

    user = User.find_with_uid(uid)
    sessions = Session.find_with_user(user)
    if not sessions:
        return True

    for session in sessions:
        session.delete_instance()

    return True


def verify_jwt_token(jwt_token):
    """
    verify if a token is valid
    :param jwt_token: target jwt token
    :return: payload
    :raises ExpiredSignatureError: if signature is expired
    :raises InvalidSignatureError: if signature is not valid
    :raises InvalidTokenError: for the rest of the token errors
    """

    payload = Cache.lookup_jwt(jwt_token)

    if payload is None:
        payload = JWT.verify_jwt(jwt_token)
        Cache.set_jwt(jwt_token, payload, ttl=30)

    return payload


def change_password(uid, old_password, new_password, kill_sessions=False):
    """
    change user's password
    :param uid: user's uid
    :param old_password: user's old password
    :param new_password: user's new password
    :param kill_sessions: terminate all active sessions
    :return: True on success
    :raises UserWasNotFound: if user was not found
    :raises WrongPassword: if old password is not valid
    """

    user = User.find_with_uid(uid)
    if not user:
        raise UserWasNotFound()

    credentials = user.credentials.get()
    if not credentials.does_match(old_password):
        raise WrongPassword()

    credentials.change(new_password).save()

    if kill_sessions:
        terminate_sessions(uid)

    return True

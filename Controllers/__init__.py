from Models import User, Credentials, Session
from Utils.Exceptions import UserAlreadyExist, IncorrectCredentials
from mongoengine import DoesNotExist


def register(gid, pswd):
    """
    register a new user
    :param gid: user's global id
    :param pswd: user's password
    :return: user instance
    :raises UserAlreadyExist:
    """

    try:
        User.find_with_gid(gid)
        raise UserAlreadyExist()
    except DoesNotExist:
        pass

    credentials = Credentials.init_and_salt(pswd)
    user = User.register(gid, credentials=credentials)
    return user


def login(gid, pswd):
    """
    login a user
    :param gid: user's global id
    :param pswd: user's password
    :return: Session instance
    :raises DoesNotExist:
    """

    user = User.find_with_gid(gid)
    if not user.credentials.does_math(pswd):
        raise IncorrectCredentials()

    session = Session.init(user)
    return session


def logout(ref_token):
    """
    logout a user from a session
    :param ref_token: user's refresh token
    :return: Session instance
    """

    session = Session.find_with_refresh_token(ref_token)
    session.delete()
    return session


def refresh_token(ref_token):
    """
    create a new jwt token
    :param ref_token: user's refresh token
    :return: Session instance
    """

    return Session.find_with_refresh_token(ref_token)

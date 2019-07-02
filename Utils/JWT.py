import jwt
from datetime import datetime, timedelta
from Utils import config
import secrets


def gen_secret():
    """
    generate a new jwt secret
    :return: True secret on success
    :raises: Exception if secret already exist
    """
    if 'jwt' not in config:
        config['jwt'] = {}
    if 'secret' not in config['jwt']:
        config['jwt']['secret'] = secrets.token_hex(256)
        config.dump()
    else:
        raise Exception('jwt secret already exists')
    return get_secret()


def get_secret():
    """
    get jwt secret
    :return: jwt secret as string
    :raises: Exception if secret does not exist
    """
    if 'jwt' not in config or 'secret' not in config['jwt']:
        raise Exception('jwt secret does not exist')
    return config['jwt']['secret']


def gen_jwt(uid: str, ttl: int, algorithm='HS256'):
    """
    generate a new jwt token
    :param uid: user_id as string
    :param ttl: time to live in seconds
    :param algorithm: jwt algorithm used (defaults to HS256)
    :return: jwt token (str)
    """
    iat = datetime.utcnow()
    exp = datetime.utcnow() + timedelta(seconds=ttl)
    return jwt.encode({
        "iat": iat,
        "exp": exp,
        "uid": uid
    }, key=get_secret(),
       algorithm=algorithm)


def verify_jwt(token: str, algorithm='HS256'):
    """
    verify a jwt token
    :param token: jwt token (str)
    :return: payload if jwt is valid
    :raises ExpiredSignatureError: if signature is expired
    :raises InvalidSignatureError: if signature is not valid
    :raises InvalidTokenError: for the rest of the token errors
    """

    return jwt.decode(token, get_secret(), verify=True, algorithm=algorithm)

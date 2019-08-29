from sanic.response import json
from time import time
import basicauth
from .Exceptions import *
from datetime import timedelta
from functools import wraps


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

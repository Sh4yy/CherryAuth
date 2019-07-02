from uuid import uuid4


def gen_access_token():
    """
    generates access token
    in order to change access token's format
    change the implementation of this method
    :return: access token as string
    """

    return uuid4().hex


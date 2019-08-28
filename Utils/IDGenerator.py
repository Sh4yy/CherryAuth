from secrets import token_hex


def gen_token(length=32):
    """
    generates access token
    in order to change access token's format
    change the implementation of this method
    :param length: token length in bytes
    :return: access token as string
    """

    return token_hex(length)


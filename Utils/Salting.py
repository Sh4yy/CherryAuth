import secrets
import scrypt


# references:
# http://split.to/eb1JzlI
# http://split.to/uVdUTUw
# http://split.to/09tF8SB


def gen_salt(length=32) -> bytes:
    """
    generate a new random salt
    :param length: length of the salt bytes
    :return: salt bytes
    """
    return secrets.token_bytes(length)


def hash_pswd(password: str, salt: bytes) -> bytes:
    """
    salt and hash a new password
    :param password: password to be salted (str)
    :param salt: salt (bytes)
    :return: hashed and salted password bytes
    """

    return scrypt.hash(password, salt, N=16384, r=8, p=1, buflen=32)


def validate_pswd(hashed_password: bytes, salt: bytes, password: str):
    """
    check whether a given password is valid

    :param hashed_password: previously salted and hashed password
    :param salt: previously used hash (for the salted password)
    :param password: new given password
    :return: True on success
    """

    return hash_pswd(password, salt) == hashed_password








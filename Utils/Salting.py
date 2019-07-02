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


def hash_pswd(pswd: str, salt: bytes) -> bytes:
    """
    salt and hash a new password
    :param pswd: password to be salted (str)
    :param salt: salt (bytes)
    :return: hashed and salted password bytes
    """

    return scrypt.hash(pswd, salt, N=16384, r=8, p=1, buflen=32)


def validate_pswd(hashed_pswd: bytes, salt: bytes, pswd: str):
    """
    check whether a given password is valid

    :param hashed_pswd: previously salted and hashed password
    :param salt: previously used hash (for the salted password)
    :param pswd: new given password
    :return: True on success
    """

    return hash_pswd(pswd, salt) == hashed_pswd








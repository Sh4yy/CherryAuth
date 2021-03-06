
class AuthExceptions(Exception):
    pass


class UserAlreadyExist(AuthExceptions):
    pass


class IncorrectCredentials(AuthExceptions):
    pass


class TokenDoesNotExist(AuthExceptions):
    pass


class InvalidMethod(AuthExceptions):
    pass


class InvalidValue(AuthExceptions):
    pass


class WrongPassword(AuthExceptions):
    pass


class UserWasNotFound(AuthExceptions):
    pass


class RefreshTokenIsNotValid(AuthExceptions):
    pass

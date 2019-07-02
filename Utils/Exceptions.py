
class AuthExceptions(Exception):
    pass


class UserAlreadyExist(AuthExceptions):
    pass


class IncorrectCredentials(AuthExceptions):
    pass

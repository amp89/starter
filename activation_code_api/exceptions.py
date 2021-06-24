class InvalidCodeException(Exception):
    pass

class ExpiredCodeException(Exception):
    pass

class PasswordDoesNotMatchException(Exception):
    pass

class UserExistsException(Exception):
    pass
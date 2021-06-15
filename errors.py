from enum import Enum
class AccessErrorType(Enum):
     LOGIN_NOT_EXIST = 1
     PASSWORD_FASLE = 2


class RegisterError(Exception):
    def __init__(self, text):
        self.txt = text

class AccessError(Exception):
    def __init__(self, text, type):
        self.type = type
        self.txt = text

    def __str__(self):
        return self.txt

class OrdinaryError(Exception):
    def __init__(self, text):
        self.txt = text




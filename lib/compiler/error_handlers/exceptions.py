class SilverException(Exception):
    pass


class MissingTerm(SilverException):
    pass


class InvalidTerm(SilverException):
    pass


class UnexpectedTerm(SilverException):
    pass

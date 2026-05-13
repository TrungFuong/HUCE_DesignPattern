class DomainException(Exception):
    pass


class NotFoundException(DomainException):
    pass


class UnauthorizedException(DomainException):
    pass

class BadRequestException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UnauthorizedException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ForbiddenException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ConflictException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
class HttpError(Exception):
    def __init__(self, message, code):
        self.code = code
        self.msg = message
        super().__init__(self, message)


class BadRequestError(HttpError):
    def __init__(self, message):
        super().__init__(message, code=400)


class UnauthorizedError(HttpError):
    def __init__(self):
        super().__init__(message="You are not authorized", code=401)


class NotFoundError(HttpError):
    def __init__(self, message):
        super().__init__(message, code=404)


class InternalServerError(HttpError):
    def __init__(self, message):
        super().__init__(message, code=500)

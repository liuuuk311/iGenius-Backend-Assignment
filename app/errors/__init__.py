class UnauthorizedError(Exception):
    status_code = 401


class BadRequestError(Exception):
    status_code = 400


class NotFoundError(Exception):
    status_code = 404


class ForbiddenError(Exception):
    status_code = 403


class InternalError(Exception):
    status_code = 500

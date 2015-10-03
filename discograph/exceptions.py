# -*- encoding: utf-8 -*-
from werkzeug.exceptions import HTTPException


class APIError(Exception):

    def __init__(
        self,
        message='Bad Request',
        status_code=400,
        ):
        Exception.__init__(self)
        self.status_code = status_code
        self.message = message


class RateLimitError(APIError):

    def __init__(
        self,
        status_code=429,
        message='Too Many Requests',
        ):
        APIError.__init__(
            self,
            status_code=status_code,
            message=message,
            )
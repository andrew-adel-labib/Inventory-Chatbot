class APIError(Exception):
    status_code = 400
    message = "Bad request"

    def to_response(self):
        return {
            "status": "error",
            "message": self.message,
        }


class UnauthorizedError(APIError):
    status_code = 403
    message = "Unauthorized"


class UnsupportedIntentError(APIError):
    status_code = 400
    message = "Unsupported intent"
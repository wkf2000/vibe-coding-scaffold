class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ExternalServiceError(AppError):
    def __init__(self, message: str = "Upstream service error") -> None:
        super().__init__(code="upstream_error", message=message, status_code=502)


class ValidationFailure(AppError):
    def __init__(self, message: str = "Validation failed") -> None:
        super().__init__(code="validation_failed", message=message, status_code=422)

"""Common application error classes and error codes."""

from typing import Any


class AppError(Exception):
    """Base application exception."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class AuthenticationError(AppError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid email or password", details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="AUTH_INVALID_CREDENTIALS", details=details)


class UnauthorizedError(AppError):
    """Raised when user lacks permissions or authorization."""

    def __init__(self, message: str = "Unauthorized", details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="UNAUTHORIZED", details=details)


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found", details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="NOT_FOUND", details=details)


class ConflictError(AppError):
    """Raised when a resource already exists or conflict occurs."""

    def __init__(self, message: str = "Resource conflict", details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="CONFLICT", details=details)


class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(self, message: str = "Validation failed", details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, code="VALIDATION_ERROR", details=details)

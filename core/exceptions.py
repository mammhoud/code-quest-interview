from ninja_schema import Schema


# =====================
# Custom Exception Classes
# =====================
class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


class InactiveError(Exception):
    """Raised when a resource is inactive (e.g., 403 Forbidden)"""

    pass


class ExistsError(Exception):
    """Raised when a resource already exists (e.g., 409 Conflict)"""

    pass


class DeleteError(Exception):
    """Raised when a deletion operation fails (e.g., 400 Bad Request)"""

    pass


class SchemaError(Exception):
    """Raised for schema validation errors (e.g., 422 Unprocessable Entity)"""

    pass


# HTTP-related errors
class NotFoundError(Exception):
    """404 Not Found"""

    pass


class UnauthorizedError(Exception):
    """401 Unauthorized"""

    pass


class ForbiddenError(Exception):
    """403 Forbidden"""

    pass


class BadRequestError(Exception):
    """400 Bad Request"""

    pass


class ConflictError(Exception):
    """409 Conflict"""

    pass


# =====================
# Response Schemas
# =====================
class Error(Schema):
    message: str
    # Optional: Add error code for better debugging
    # code: Optional[int]


class Success(Schema):
    message: str
    # Optional: Add a code or detail field
    # code: Optional[int]
    # detail: Optional[str]

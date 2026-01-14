class QAFrameworkException(Exception):
    """Base exception for the QA Framework."""
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(message)
        self.original_exception = original_exception

class ConfigurationResultError(QAFrameworkException):
    """Raised when configuration loading fails."""
    pass

class DriverInitializationError(QAFrameworkException):
    """Raised when a driver fails to initialize."""
    pass

class ElementInteractionError(QAFrameworkException):
    """Raised when an interaction with a UI element fails."""
    pass

class APIGatewayError(QAFrameworkException):
    """Raised when an API request fails."""
    pass

class DataLoadingError(QAFrameworkException):
    """Raised when loading test data fails."""
    pass

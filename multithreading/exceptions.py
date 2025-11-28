class BaseAppException(Exception):
    """Базовое исключение приложения"""
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

class ValidationError(BaseAppException):
    """Ошибка валидации данных"""
    pass

class InputError(BaseAppException):
    """Ошибка ввода данных"""
    pass

class CryptoError(BaseAppException):
    """Ошибка шифрования"""
    pass

class ServerError(BaseAppException):
    """Ошибка сервера"""
    pass

class QueueError(BaseAppException):
    """Ошибка работы с очередью"""
    pass

class TimeoutError(BaseAppException):
    """Ошибка таймаута"""
    pass
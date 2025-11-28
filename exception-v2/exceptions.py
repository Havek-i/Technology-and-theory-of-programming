class BaseAppException(Exception):
    """Базовое исключение приложения"""
    pass

class ValidationError(BaseAppException):
    """Ошибка валидации данных"""
    pass

class InputError(BaseAppException):
    """Ошибка ввода данных"""
    pass

class CryptoError(BaseAppException):
    """Ошибка шифрования"""
    pass
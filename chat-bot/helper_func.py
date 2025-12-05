# helper_func.py (без изменений, можно оставить как есть)
from log import server_logger

def normalize_input_data(string: str, shift: str) -> tuple[str, int]:
    '''Функция, которая обрабатывает входные данные'''
    server_logger.info("Нормализация входных данных")

    string = string.lower()
    shift = int(shift)
    
    server_logger.info(f"Данные успешно нормализованы: {string}, {shift}")

    return (string, shift)

def submenu() -> str:
    '''Функция, которая показывает подменю (для бота не используется напрямую)'''
    server_logger.info("Вызов подменю")
    return "Выберите метод ввода"
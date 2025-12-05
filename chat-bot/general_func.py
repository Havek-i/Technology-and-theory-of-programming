# general_func.py (адаптированный для бота)
import random
import string
import helper_func as hf
from log import server_logger

def crypto(string: str, shift: int) -> str:
    '''Функция, которая реализует алгоритм шифра Виженера'''
    server_logger.info(f"Запуск алгоритма шифрования с параметрами: {string}, {shift}")

    result = []
    for char in string:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            # Вычисляем новую позицию символа с учетом сдвига
            new_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(new_char)
        else:
            result.append(char)
    
    result_str = ''.join(result)
    server_logger.info(f"Алгоритм успешно завершил работу с результатом: {result_str}")

    return result_str

def input_params(user_input: str) -> tuple[str, int]:
    '''Функция, которая принимает исходные данные от пользователя'''
    try:      
        server_logger.info('Ручной ввод параметров')

        string, shift = user_input.strip().split(' ')
        string, shift = hf.normalize_input_data(string, shift)

        server_logger.info('Данные успешно введены')
        return (string, shift)
    except Exception as e:
        raise Exception(f"Ошибка при введении данных: {str(e)}")

def generating_params() -> tuple[str, int]:
    '''Функция, которая генерирует значения случайным образом'''
    server_logger.info('Вызов случайной генерации данных')

    length = random.randrange(5, 15)
    shift = random.randrange(1, 26)

    random_string = ''.join(random.choices(string.ascii_letters, k=length))

    server_logger.info(f'Данные успешно сгенерированы: {random_string}, {shift}')

    return (random_string.lower(), shift)

def result(encrypted_string: str) -> str:
    '''Функция, которая возвращает результат'''
    if not encrypted_string:
        return "Результат отсутствует. Сначала выполните шифрование."
    
    result_text = f"🔐 Результат шифрования:\n{encrypted_string}"
    server_logger.info(f'Вывод результата: {encrypted_string}')
    
    return result_text

# В general_func.py добавьте эту функцию:
def format_result_display(string: str, shift: int, encrypted: str) -> str:
    '''Форматирование результата для отображения в Telegram'''
    return f"""
📊 Результат шифрования:

📝 Исходный текст: {string}
🔢 Сдвиг: {shift}
🔐 Зашифрованный текст: {encrypted}
    """
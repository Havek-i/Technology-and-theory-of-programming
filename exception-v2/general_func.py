import random
import string
import helper_func as hf
from logg import server_logger
from exceptions import CryptoError, InputError
from messages import Messages

def start_menu() -> None:
    '''Функция, которая отображет меню'''

    server_logger.info("Вызов меню")
    print(Messages.MENU)


def crypto(string: str, shift: int) -> str:
    '''Функция, которая реализует аглоритм шифра Виженера
    
    Arguments
    ---------
        string : str
            Исходная строка
        shift : int 
            Величина сдвига
    
    Returns
    -------
        result : str
            Зашифрованная строка
            
    '''    
    try:
        server_logger.info(f"Запуск алгоритма шифрования с параметрами: {string}, {shift}")
        print(Messages.INFO["algorithm_started"])
        
        result = []
        for char in string:
            if char.isalpha():
                base = ord('a') if char.islower() else ord('A')
                new_char = chr((ord(char) - base + shift) % 26 + base)
                result.append(new_char)
            else:
                result.append(char)
                
        print(Messages.INFO["algorithm_completed"])
        encrypted_text = ''.join(result)
        
        server_logger.info(f"Алгоритм успешно завершил работу с результатом: {encrypted_text}")
        return encrypted_text
        
    except Exception as e:
        server_logger.exception(Messages.ERROR["crypto_failed"])
        raise CryptoError(Messages.ERROR["crypto_failed"]) from e


def input_params() -> tuple[str, int]:
    '''Функция, которая принимает исходные данные
    
    Returns
    -------
        tuple : [str, int]
            Кортеж, состоящий из введённых данных Пользователем: строка и величина сдвига
    '''
    try:
        server_logger.info('Ручной ввод параметров')

        user_input = input(Messages.INFO["enter_data"]).strip()
        string, shift = user_input.split(' ')
        string, shift = hf.normalize_input_data(string, shift)

        server_logger.info('Данные успешно введены')
        print(Messages.INFO["data_entered"])
        return (string, shift)
        
    except Exception as e:
        server_logger.exception(Messages.ERROR["input_failed"])
        raise InputError(Messages.ERROR["input_failed"]) from e


def generating_params() -> tuple[str, int]:
    '''Функция, которая генерирует значения случайным образом
    
    Returns
    -------
        tuple : [str, int]
            Кортеж, состоящий из сгенерированных данных: строки и величины сдвига
    '''
    try:
        server_logger.info('Вызов случайной генерации данных')

        length = random.randint(5, 15)
        shift = random.randint(1, 25)
        random_string = ''.join(random.choices(string.ascii_letters, k=length))

        server_logger.info(f'Данные успешно сгенерированы: {random_string}, {shift}')
        print(f"Сгенерированные данные: ({random_string}, {shift})")
        return (random_string, shift)
        
    except Exception as e:
        server_logger.exception(Messages.ERROR["generation_failed"])
        raise InputError(Messages.ERROR["generation_failed"]) from e
    

def result(string: str) -> None:
    '''Функция, которая вывод результат
    
    Arguments
    ---------
        string : str
            Зашифрованная строка
    '''
    try:
        print(f"Результат: {string}")
        server_logger.info(f'Вывод результата: {string}')
    except Exception as e:
        server_logger.exception(Messages.ERROR["output_failed"])
        raise CryptoError(Messages.ERROR["output_failed"]) from e
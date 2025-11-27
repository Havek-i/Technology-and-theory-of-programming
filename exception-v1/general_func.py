import random
import string
import helper_func as hf
from logg import server_logger

def start_menu() -> None:
    '''Функция, которая отображет меню'''

    menu = '''
    =============================
    1. Ввести данные.
    2. Выполнить алгоритм.
    3. Вывести результат.
    0. Завершение работы прграммы.
    =============================
    '''
    server_logger.info("Вызов меню")
    
    print(menu)


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

        print("Начало алгоритма...")
        result = []
        for char in string:
            base = ord('a')
            # Вычисляем новую позицию символа с учетом сдвига и закольцованности алфавита
            new_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(new_char)
        print("Алгоритм завершил работу")
        
        server_logger.info(f"Алгоритм успешно завершил работу с результатом: {''.join(result)}")

        return ''.join(result)
    except (TypeError, ValueError, BaseException) as e:
        server_logger.exception(f"Ошибка при выполнении шифрования: {e}")
        return e


def input_params() -> tuple[str, int]:
    '''Функция, которая принимает исходные данные
    
    Returns
    -------
        tuple : [str, int]
            Кортеж, состоящий из введённых данных Пользователем: строка и величина сдвига
    '''
    try:
        server_logger.info('Ручной ввод параметров')

        string, shift = input("Введите данные: ").strip().split(' ')
        string, shift = hf.normalize_input_data(string, shift) #Использование вспомогательной функции

        server_logger.info('Данные успешно введены')

        print("Данные были введены!")
        return (string, shift)
    except (TypeError, ValueError) as e:
        server_logger.exception(f"Ошибка при введении данных: {e}")
        return e


def generating_params() -> tuple[str, int]:
    '''Функция, которая генерирует значения случайным образом
    
    Returns
    -------
        tuple : [str, int]
            Кортеж, состоящий из сгенерированных данных: строки и величины сдвига
    '''
    try:
        server_logger.info('Вызов случайной генерации данных')

        length = random.randrange(1, 20)
        shift = random.randrange(1, 20)

        random_string = ''.join(random.choices(string.ascii_uppercase, k=length))

        server_logger.info(f'Данные успешно сгенерированы: {random_string}, {shift}')

        print((random_string, shift))
        return (random_string, shift)
    except BaseException as e:
        server_logger.exception(f"Ошибка при генерации данных: {e}")
        return e
    

def result(string: str) -> None:
    '''Функция, которая вывод результат
    
    Arguments
    ---------
        string : str
            Зашифрованная строка
    '''
    try:
        string = string.capitalize()
        print(string)

        server_logger.info(f'Вывод результата: {string}')
    except (TypeError, ValueError, BaseException) as e:
        server_logger.exception(f"Ошибка вывода результата: {e}")
        return e
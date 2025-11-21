import random
import string
import helper_func as hf

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
    print(menu)


def crypto(string: str, shift: int) -> str:
    '''Функция, которая реализует аглоритм шифра Виженера'''    
    
    print("Начало алгоритма...")
    result = []
    for char in string:
        base = ord('a')
        # Вычисляем новую позицию символа с учетом сдвига и закольцованности алфавита
        new_char = chr((ord(char) - base + shift) % 26 + base)
        result.append(new_char)
    print("Алгоритм завершил работу")
    
    return ''.join(result)

def input_params() -> tuple[str, int]:
    '''Функция, которая принимает исходные данные'''
    
    string, shift = input("Введите данные: ").strip().split(' ')
    string, shift = hf.normalize_input_data(string, shift)
    print("Данные были введены!")
    return (string, shift)
    
def generating_params() -> tuple[str, int]:
    '''Функция, которая генерирует значения случайным образом'''

    length = random.randrange(1, 20)
    shift = random.randrange(1, 20)

    random_string = ''.join(random.choices(string.ascii_uppercase, k=length))

    print((random_string, shift))
    return (random_string, shift)
    

def result(string: str) -> None:
    '''Функция, которая вывод результат'''
    
    string = string.capitalize()
    print(string)
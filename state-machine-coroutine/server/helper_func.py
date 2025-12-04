# helper_func.py
from log import server_logger

def normalize_input_data(string: str, shift: str) -> tuple[str, int]:
    '''Функция, которая обрабатывает входные данные
    
    Arguments
    ---------
        string : str
            Исходная строка
        shift : str 
            Величина сдвига
    
    Returns
    -------
        tuple : [str, int]
            Кортеж, состоящий из преобразованных строки и величины сдвига
    '''
    
    server_logger.info("Нормализация входных данных")

    string = string.lower()
    shift = int(shift)
    
    server_logger.info(f"Данные успешно нормализованы: {string}, {shift}")

    return (string, shift)

def submenu() -> str:
    '''Функция, которая показывает подменю и обрабатывает выбранный пункт
    
    Returns
    -------
        choice : str
            Выбранный пункт меню
    '''
    
    server_logger.info("Вызов подменю")

    submenu_text = '''
        \t============================
        \t1. Самостояльный ввод данных
        \t2. Случайная генерация
        \t============================
        '''

    print(submenu_text)
    return input("\t\tВыберите пункт: ")
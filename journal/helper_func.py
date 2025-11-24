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
    
    string = string.lower()
    shift = int(shift)
    
    return (string, shift)

def submenu(submenu: str = None) -> int:
    '''Функция, которая показывает подменю и обрабатывает выбранный пункт
    
    Arguments
    ---------
        Submenu : str | None
            Исходная строка
    
    Returns
    -------
        func : function
            Функция, запрашивающая у Пользователя пункт submenu
    '''
    
    if submenu is None:
        submenu = '''
        \t============================
        \t1. Самостояльный ввод данных
        \t2. Случайная генерация
        \t============================
        '''

    print(submenu)
    return int(input("\t\tВыберите пункт: "))
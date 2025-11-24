def normalize_input_data(string: str, shift: str) -> tuple[str, int]:
    '''Функция, которая обрабатывает входные данные'''
    
    string = string.lower()
    shift = int(shift)
    
    return (string, shift)

def submenu(submenu: str = None) -> int:
    '''Функция, которая показывает подменю и обрабатывает выбранный пункт'''
    
    if submenu is None:
        submenu = '''
        \t============================
        \t1. Самостояльный ввод данных
        \t2. Случайная генерация
        \t============================
        '''

    print(submenu)
    return int(input("\t\tВыберите пункт: "))
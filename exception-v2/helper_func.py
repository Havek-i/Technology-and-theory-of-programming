from logg import server_logger
from exceptions import ValidationError
from messages import Messages

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
    
    try:
        server_logger.info("Нормализация входных данных")

        string = string.lower()
        shift = int(shift)

        server_logger.info(f"Данные успешно нормализованы: {string}, {shift}")
        return (string, shift)
    except (TypeError, ValueError) as e:
        server_logger.exception(Messages.ERROR["normalization_failed"])
        raise ValidationError(Messages.ERROR["invalid_value"]) from e
    except BaseException as e:
        server_logger.exception(Messages.ERROR["normalization_failed"])
        raise ValidationError(Messages.ERROR["normalization_failed"]) from e

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
    
    server_logger.info("Вызов подменю")

    if submenu is None:
        submenu = Messages.SUBMENU

    print(submenu)
    return int(input("\t\tВыберите пункт: "))
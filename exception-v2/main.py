import general_func as gf
import helper_func as hf
from logg import client_logger
from exceptions import BaseAppException
from messages import Messages


def main():
    """Главная функция"""
    
    global data
    global result
    data, result = None, None

    while True:
        try:
            gf.start_menu()

            client_logger.info("Выбор пункта меню")
            item = int(input(Messages.INFO["select_menu_item"]).strip())
            client_logger.info(f"Клиент выбрал пункт: {item}")

            match item:
                case 0:
                    break

                case 1:
                    client_logger.info("Вызов подменю пункта 1")
                    sub_item = hf.submenu()
                    client_logger.info(f"Клиент выбрал подпункт: {sub_item}")

                    if sub_item == 1:
                        data = gf.input_params()
                    elif sub_item == 2:
                        data = gf.generating_params()
                    else:
                        print(Messages.ERROR["invalid_submenu_item"])
                        continue
                    
                    result = None

                case 2:
                    if data:
                        result = gf.crypto(string=data[0], shift=data[1])
                    else:
                        print(Messages.ERROR["no_data"])

                case 3:
                    if result:
                        gf.result(result)
                    else:
                        print(Messages.ERROR["no_result"])
                
                case _:
                    print(Messages.ERROR["invalid_menu_item"])
                    continue
        
        except (ValueError, TypeError) as e:
            client_logger.exception("Ошибка ввода данных")
            print(Messages.ERROR["general_error"])
            continue
        except BaseAppException as e:
            client_logger.exception(f"Ошибка приложения: {e}")
            print(Messages.ERROR["general_error"])
            continue
        except Exception as e:
            client_logger.exception(f"Непредвиденная ошибка: {e}")
            print(Messages.ERROR["general_error"])
            continue

if __name__ == '__main__':
    main()

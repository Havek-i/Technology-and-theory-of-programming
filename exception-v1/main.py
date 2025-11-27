import general_func as gf
import helper_func as hf
from logg import client_logger


def main():
    """Главная функция"""
    
    global data
    global result
    data, result = None, None

    while True:
        try:
            gf.start_menu()

            client_logger.info("Выбор пункта меню")
            item = int(input('Введите пункт меню: ').strip())
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
                        print("Вы ввели некорректный подпункт, попробуйте ещё раз.")
                        continue
                    
                    if isinstance(data, BaseException):
                            raise Warning

                    result = None

                case 2:
                    if data:
                        result = gf.crypto(string=data[0], shift=data[1])
                        if isinstance(result, BaseException):
                            raise Warning
                    else:
                        print("Вы не ввели данные. Попробуйте для начала выполнить пункт 1.")

                case 3:
                    if result:
                        gf.result(result)
                        if isinstance(result, BaseException):
                            raise Warning
                    else:
                        print("Вы не выполнили алгоритм. Попробуйте выполнить для начала пункт 2")
                
                case _:
                    print("Такой команды нет в списке. Попробуйте ещё раз!")
                    continue
        
        except (TypeError, ValueError, Warning) as e:
            client_logger.exception(f"Ошибка при обработке данных | вызове функции | возврате функции")
            print("При выполнении программы произошла ошибка. Пожалуйста, попроуйте ещё раз.")
            continue

if __name__ == '__main__':
    main()

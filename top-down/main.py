import general_func as gf
import helper_func as hf

def main():
    global data
    global result
    data, result = None, None

    while True:
        gf.start_menu()
        item = int(input('Введите пункт меню: ').strip())
        
        match item:
            case 0:
                break

            case 1:
                sub_item = hf.submenu()
                if sub_item == 1:
                    data = gf.input_params()
                elif sub_item == 2:
                    data = gf.generating_params()
                else:
                    print("Вы ввели некорректный подпункт, попробуйте ещё раз.")
                    continue
                
                result = None

            case 2:
                if data:
                    result = gf.crypto(string=data[0], shift=data[1])
                else:
                    print("Вы не ввели данные. Попробуйте для начала выполнить пункт 1.")

            case 3:
                if result:
                    gf.result(result)
                else:
                    print("Вы не выполнили алгоритм. Попробуйте выполнить для начала пункт 2")
            
            case _:
                print("Такой команды нет в списке. Попробуйте ещё раз!")
                continue


if __name__ == '__main__':
    main()

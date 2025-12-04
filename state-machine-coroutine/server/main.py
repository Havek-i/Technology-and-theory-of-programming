# main.py
from state_machine import StateMachine

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

if __name__ == '__main__':
    SM = StateMachine()
    items = {
        '1': 'input',
        '2': 'computing',
        '3': 'result',
        '0': 'destructor'
    }

    while True:
        try:
            start_menu()
            itm = input("Ввыедите пункт: ")
            state = items.get(itm)
            if state == None:
                raise Exception("Неверная команда")

            if itm == '0':
                SM.manager(state)
                break
            else:
                SM.manager(state)

        except Exception as e:
            print(f"Введена неверная команда. Error: {e}")
            continue
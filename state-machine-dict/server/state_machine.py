from app import AppState, Transition
from log import server_logger
from typing import Optional
import general_func as gf
import helper_func as hf

class StateMachine:
    def __init__(self):
        self.state = AppState.INIT
        self.transition = Transition()
        self.actions = {
            # Переходы из стартового состояния
            (AppState.INIT, 'input'): self._sub_menu,
            (AppState.INIT, 'error'): self._except,
            (AppState.INIT, 'destructor'): self._exit,

            # Переходы из состояния ввода данныйх
            (AppState.INPUT, 'input'): self._sub_menu,
            (AppState.INPUT, 'computing'): self._computing,
            (AppState.INPUT, 'error'): self._except,
            (AppState.INPUT, 'destructor'): self._exit,

            # Переходы из состояния вычисления
            (AppState.COMPUTING, 'input'): self._sub_menu,
            (AppState.COMPUTING, 'computing'): self._computing,
            (AppState.COMPUTING, 'result'): self._res,
            (AppState.COMPUTING, 'error'): self._except,
            (AppState.COMPUTING, 'destructor'): self._exit,
            
            # Переходы из состояния результата
            (AppState.RESULT, 'input'): self._sub_menu,
            (AppState.RESULT, 'computing'): self._computing,
            (AppState.RESULT, 'result'): self._res,
            (AppState.RESULT, 'error'): self._except,
            (AppState.RESULT, 'destructor'): self._exit,
            
            # Переходы из состояния ошибки
            (AppState.ERROR, AppState.INIT): self._restart
        }
        self._data: Optional[tuple[str, int]] = None
        self._result: Optional[str] = None


    def _sub_menu(self):
        self._data, self._result = None, None
        choice = {
            '1': gf.input_params,
            '2': gf.generating_params
        }

        try:
            sub_item = hf.submenu()
            self._data = choice.get(sub_item)()
        except Exception as e:
            server_logger.exception(f"Ошибка при состоянии {self.state.value}. Ошибка: {e}")
            self._except(state=self.state.value, exception=e)


    def _exit(self, status: str = 'normal'):
        print('Завершение работы программы.')
        if status == 'normal':
            server_logger.debug(f"Программа завершила работу успешно со статусом {status}.")
            exit(0)
        else:
            server_logger.critical(f"Программа завершила работу в аварийном состоянии. Статус: {status}")
            exit(1)


    def _res(self):
        try:
            if self._data == None: raise Exception("Не выполнена стадия шифрования.")
            gf.result(self._result)
        except Exception as e:
            self._except(state=self.state.value, exception=e)


    def _computing(self):
        try:
            if self._data == None: raise Exception("Нет исходных данный.")

            self._result = gf.crypto(string=self._data(0), shift=self._data(1))
        except Exception as e:
            self._except(state=self.state.value, exception=e)


    def _except(self, state: AppState, exception: Exception):
        if state == AppState.INIT:
            print("Непредвиденная ситуация, программа вынуждена завершить работу.")
            self._exit(status='critical')
        else:
            server_logger.exception(f"Ошибка при состоянии {self.state.value}. Ошибка: {exception}")
            print(exception)
            self._restart()
    

    def _restart(self):
        self._data, self._result = None, None
        self.state = AppState.INIT
        server_logger.warning("Перезагрузка программы")


    def manager(self, event: str):
        current_state = self.state
        next_state = self.transition.get_next_state(self.state, event)
        
        if next_state is None:
            if self.transition.get_next_state(self.state, event) is None:
                print(f"Невозможно выполнить '{event}' в состоянии '{self.state.value}'")
            return
        
        # Выполняем действие, если оно определено
        action = self.actions.get((self.state, event))
        
        try:
            if action:
                action()
        
        # Переходим в новое состояние
            self.state = next_state
            server_logger.info(f"Переход в состояние: {self.state.value}")
        except Exception as e:
            server_logger.warning(f"Переход между состояниями не удался. Ошибка: {e}")
            print(f"Ошибка при переходе между состояниями.")
            self._except(state=self.state.value, exception=e)



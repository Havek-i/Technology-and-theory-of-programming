# state_machine.py
from app import AppState, Transition
from log import server_logger
from typing import Optional, Generator, Callable
import general_func as gf
import helper_func as hf

class StateMachine:
    def __init__(self):
        self.state = AppState.INIT
        self.transition = Transition()
        self._actions_coroutine = self._actions_generator()
        next(self._actions_coroutine)  # Инициализация корутины
        self._action_map = {}  # Кэш для быстрого доступа к действиям
        self._data: Optional[tuple[str, int]] = None
        self._result: Optional[str] = None

    def _actions_generator(self) -> Generator[Optional[Callable], tuple[AppState, str], None]:
        """Корутина для управления действиями автомата"""
        action = None
        
        while True:
            # Получаем состояние и событие
            state_event = yield action
            if not state_event:
                continue
                
            state, event = state_event
            
            # Определяем действие на основе состояния и события
            if state == AppState.INIT:
                if event == 'input':
                    action = self._sub_menu
                elif event == 'error':
                    action = self._except
                elif event == 'destructor':
                    action = self._exit
                else:
                    action = None
                    
            elif state == AppState.INPUT:
                if event == 'input':
                    action = self._sub_menu
                elif event == 'computing':
                    action = self._computing
                elif event == 'error':
                    action = self._except
                elif event == 'destructor':
                    action = self._exit
                else:
                    action = None
                    
            elif state == AppState.COMPUTING:
                if event == 'input':
                    action = self._sub_menu
                elif event == 'computing':
                    action = self._computing
                elif event == 'result':
                    action = self._res
                elif event == 'error':
                    action = self._except
                elif event == 'destructor':
                    action = self._exit
                else:
                    action = None
                    
            elif state == AppState.RESULT:
                if event == 'input':
                    action = self._sub_menu
                elif event == 'computing':
                    action = self._computing
                elif event == 'result':
                    action = self._res
                elif event == 'error':
                    action = self._except
                elif event == 'destructor':
                    action = self._exit
                else:
                    action = None
                    
            elif state == AppState.ERROR:
                if event == 'initialization':
                    action = self._restart
                else:
                    action = None
            else:
                action = None

    def _get_action(self, state: AppState, event: str) -> Optional[Callable]:
        """Получение действия через корутину"""
        # Используем кэш для быстрого доступа
        key = (state, event)
        if key in self._action_map:
            return self._action_map[key]
        
        try:
            # Отправляем состояние и событие в корутину и получаем действие
            action = self._actions_coroutine.send((state, event))
            self._action_map[key] = action
            return action
        except StopIteration:
            # Пересоздаем корутину, если она завершилась
            self._actions_coroutine = self._actions_generator()
            # Инициализируем корутину
            next(self._actions_coroutine)
            # Пробуем снова
            return self._get_action(state, event)

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
            self._except(state=self.state, exception=e)

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
            if self._result is None: 
                raise Exception("Не выполнена стадия шифрования.")
            gf.result(self._result)
        except Exception as e:
            self._except(state=self.state, exception=e)

    def _computing(self):
        try:
            if self._data is None: 
                raise Exception("Нет исходных данных.")
            self._result = gf.crypto(string=self._data[0], shift=self._data[1])
        except Exception as e:
            self._except(state=self.state, exception=e)

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
        # Очищаем кэш действий при перезагрузке
        self._action_map.clear()

    def manager(self, event: str):
        current_state = self.state
        next_state = self.transition.get_next_state(self.state, event)
        
        if next_state is None:
            print(f"Невозможно выполнить '{event}' в состоянии '{self.state.value}'")
            return
        
        # Получаем действие через корутину
        action = self._get_action(self.state, event)
        
        try:
            if action:
                action()
            
            # Переходим в новое состояние
            self.state = next_state
            server_logger.info(f"Переход в состояние: {self.state.value}")
        except Exception as e:
            server_logger.warning(f"Переход между состояниями не удался. Ошибка: {e}")
            print(f"Ошибка при переходе между состояниями.")
            self._except(state=self.state, exception=e)
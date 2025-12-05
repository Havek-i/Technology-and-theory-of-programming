from app import AppState, Transition
from log import server_logger
from typing import Optional
import general_func as gf

class StateMachine:
    def __init__(self):
        self.state = AppState.INIT
        self.transition = Transition()
        self.actions = {
            # Переходы из стартового состояния
            (AppState.INIT, 'input'): self._sub_menu,
            (AppState.INIT, 'error'): self._except,
            (AppState.INIT, 'destructor'): self._exit,

            # Переходы из состояния ввода данных
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

    def _sub_menu(self, **kwargs):
        """Обработка подменю ввода"""
        user_id = kwargs.get('user_id')
        server_logger.info(f"Переход в состояние выбора метода ввода для пользователя {user_id}")
        self._data, self._result = None, None

    def _exit(self, **kwargs):
        """Завершение работы"""
        status = kwargs.get('status', 'normal')
        user_id = kwargs.get('user_id')
        
        if status == 'normal':
            server_logger.debug(f"Программа завершила работу успешно для пользователя {user_id}")
        else:
            server_logger.critical(f"Программа завершила работу в аварийном состоянии для пользователя {user_id}")

    def _res(self, **kwargs):
        """Вывод результата"""
        user_id = kwargs.get('user_id')
        try:
            if self._result is None:
                raise Exception("Не выполнена стадия шифрования.")
            
            server_logger.info(f"Вывод результата для пользователя {user_id}: {self._result}")
                
        except Exception as e:
            self._except(state=self.state, exception=e, user_id=user_id)

    def _computing(self, **kwargs):
        """Выполнение вычислений"""
        user_id = kwargs.get('user_id')
        try:
            if self._data is None:
                raise Exception("Нет исходных данных.")

            # Выполняем шифрование
            self._result = gf.crypto(string=self._data[0], shift=self._data[1])
            
            server_logger.info(f"Вычисления для пользователя {user_id} завершены. Результат: {self._result}")
                
        except Exception as e:
            self._except(state=self.state, exception=e, user_id=user_id)

    def _except(self, **kwargs):
        """Обработка исключений"""
        state = kwargs.get('state')
        exception = kwargs.get('exception')
        user_id = kwargs.get('user_id')
        
        error_msg = str(exception)
        
        if state == AppState.INIT:
            server_logger.critical(f"Критическая ошибка при инициализации для пользователя {user_id}: {error_msg}")
        else:
            server_logger.exception(f"Ошибка при состоянии {self.state.value} для пользователя {user_id}. Ошибка: {error_msg}")
            self._restart(user_id=user_id)

    def _restart(self, **kwargs):
        """Перезагрузка состояния"""
        user_id = kwargs.get('user_id')
        self._data, self._result = None, None
        self.state = AppState.INIT
            
        server_logger.warning(f"Перезагрузка программы для пользователя {user_id}")

    def set_user_data(self, user_id: int, data: tuple[str, int]):
        """Установка данных для пользователя"""
        self._data = data
        server_logger.info(f"Установлены данные для пользователя {user_id}: {data}")

    def manager(self, event: str, **kwargs):
        """Управление автоматом состояний"""
        user_id = kwargs.get('user_id')
        current_state = self.state
        next_state = self.transition.get_next_state(self.state, event)
        
        if next_state is None:
            server_logger.warning(f"Невозможно выполнить '{event}' в состоянии '{self.state.value}' для пользователя {user_id}")
            return False
        
        
        # Выполняем действие, если оно определено
        action_key = (self.state, event)
        action = self.actions.get(action_key)
        
        try:
            if action:
                # Передаем все kwargs в действие
                action(**kwargs)
        
            # Переходим в новое состояние
            self.state = next_state
            server_logger.info(f"Переход пользователя {user_id} в состояние: {self.state.value}")
            return True
            
        except Exception as e:
            server_logger.warning(f"Переход между состояниями не удался для пользователя {user_id}. Ошибка: {e}")
            self._except(state=self.state, exception=e, **kwargs)
            return False
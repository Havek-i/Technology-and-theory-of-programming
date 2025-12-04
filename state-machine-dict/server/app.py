from enum import Enum
from typing import Dict, Optional

class AppState(Enum):
    '''Состояния системы'''
    INIT = 'initialization'
    INPUT = 'input'
    COMPUTING = 'computing'
    RESULT = 'result'
    ERROR = 'error'
    destructor = 'destructor'

class Transition:
    '''Переходы между состояниями системы'''
    def __init__(self):
        # Таблица переходов: {текущее_состояние: {событие: следующее_состояние}}
        self.transitions: Dict[AppState, Dict[str, Optional[AppState]]] = {
            AppState.INIT: {
                'initialization': None,
                'input': AppState.INPUT,
                'computing': None,
                'result': None,
                'error': None,
                'destructor': AppState.destructor
            },
            AppState.INPUT: {
                'initialization': None,
                'input': AppState.INPUT,
                'computing': AppState.COMPUTING,
                'result': None,
                'error': AppState.ERROR,
                'destructor': AppState.destructor
            },
            AppState.COMPUTING: {
                'initialization': None,
                'input': AppState.INPUT,
                'computing': AppState.COMPUTING,
                'result': AppState.RESULT,
                'error': AppState.ERROR,
                'destructor': AppState.destructor
            },
            AppState.RESULT: {
                'initialization': None,
                'input': AppState.INPUT,
                'computing': AppState.COMPUTING,
                'result': AppState.RESULT,
                'error': AppState.ERROR,
                'destructor': AppState.destructor
            },
            AppState.ERROR: {
                'initialization': AppState.INIT,
                'input': None,
                'computing': None,
                'result': None,
                'error': None,
                'destructor': None
            },
            AppState.destructor: {
                'initialization': None,
                'input': None,
                'computing': None,
                'result': None,
                'error': None,
                'destructor': None
            }
        }

    def get_next_state(self, current_state: AppState, event: str) -> Optional[AppState]:
        """Возвращает следующее состояние или None, если переход невозможен"""
        return self.transitions.get(current_state, {}).get(event)
from enum import Enum
from typing import Dict, Optional

class AppState(Enum):
    '''Состояния системы'''
    INIT = 'initialization'
    INPUT = 'input'
    COMPUTING = 'computing'
    RESULT = 'result'
    ERROR = 'error'
    DISTRUCT = 'disctruct'

class Transition:
    '''Переходы между состояниями системы'''
    def __init__(self):
        # Таблица переходов: {текущее_состояние: {событие: следующее_состояние}}
        self.transitions: Dict[AppState, Dict[str, Optional[AppState]]] = {
            AppState.INIT: {
                'initialization': None,
                'input': AppState.INPUT,
                'computing': AppState.ERROR,
                'result': AppState.ERROR,
                'error': AppState.DISTRUCT,
                'disctruct': AppState.DISTRUCT
            },
            AppState.INPUT: {
                'initialization': None,
                'input': None,
                'computing': AppState.COMPUTING,
                'result': AppState.ERROR,
                'error': AppState.ERROR,
                'disctruct': AppState.DISTRUCT
            },
            AppState.COMPUTING: {
                'initialization': None,
                'input': AppState.INPUT,
                'computing': None,
                'result': AppState.RESULT,
                'error': AppState.ERROR,
                'disctruct': AppState.DISTRUCT
            },
            AppState.RESULT: {
                'initialization': None,
                'input': AppState.INPUT,
                'computing': AppState.COMPUTING,
                'result': None,
                'error': AppState.ERROR,
                'disctruct': AppState.DISTRUCT
            },
            AppState.ERROR: {
                'initialization': AppState.DISTRUCT,
                'input': AppState.INIT,
                'computing': AppState.INIT,
                'result': AppState.INIT,
                'error': None,
                'disctruct': None
            },
            AppState.DISTRUCT: {
                'initialization': None,
                'input': None,
                'computing': None,
                'result': None,
                'error': None,
                'disctruct': None
            }
        }

    def get_next_state(self, current_state: AppState, event: str) -> Optional[AppState]:
        """Возвращает следующее состояние или None, если переход невозможен"""
        return self.transitions.get(current_state, {}).get(event)
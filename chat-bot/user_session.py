from dataclasses import dataclass
from typing import Optional, Dict
from app import AppState
import asyncio

@dataclass
class UserSession:
    """Сессия пользователя"""
    user_id: int
    current_state: AppState = AppState.INIT
    data: Optional[tuple[str, int]] = None
    result: Optional[str] = None
    waiting_for_input: bool = False
    input_method: Optional[str] = None  # 'manual' или 'random'
    
class UserSessionManager:
    """Менеджер сессий пользователей"""
    def __init__(self):
        self.sessions: Dict[int, UserSession] = {}
        self.lock = asyncio.Lock()
    
    async def get_session(self, user_id: int) -> UserSession:
        """Получение или создание сессии пользователя"""
        async with self.lock:
            if user_id not in self.sessions:
                self.sessions[user_id] = UserSession(user_id=user_id)
            return self.sessions[user_id]
    
    async def update_session(self, user_id: int, **kwargs):
        """Обновление сессии пользователя"""
        async with self.lock:
            if user_id not in self.sessions:
                self.sessions[user_id] = UserSession(user_id=user_id)
            
            session = self.sessions[user_id]
            for key, value in kwargs.items():
                if hasattr(session, key):
                    setattr(session, key, value)
    
    async def clear_session(self, user_id: int):
        """Очистка сессии пользователя"""
        async with self.lock:
            if user_id in self.sessions:
                self.sessions[user_id] = UserSession(user_id=user_id)
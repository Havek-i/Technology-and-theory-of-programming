# auto_client.py
import time
import random
import string
from messages import Messages
from exceptions import InputError, ValidationError, TimeoutError
from server import server

class AutoCryptoClient:
    def __init__(self, client_name):
        self.client_name = client_name
        self.data = None
        self.result = None
        self.current_request_id = None
        
        # Разные типы поведения клиентов
        self.behaviors = ['quick', 'deliberate', 'erratic', 'methodical']
        self.behavior = random.choice(self.behaviors)
        
        # Список "рукотворных" текстов для реалистичности
        self.sample_texts = [
            "hello world", "python code", "secret message", "test data",
            "encryption demo", "client server", "multi threading", "queue example",
            "cyber security", "data protection", "information", "confidential"
        ]
    
    def simulate_typing(self, text, speed=0.05):
        """Эмуляция набора текста пользователем"""
        print(f"{self.client_name} вводит: ", end="", flush=True)
        for char in text:
            print(char, end="", flush=True)
            time.sleep(speed)
        print()
    
    def simulate_thinking(self, min_time=0.5, max_time=2.0):
        """Эмуляция раздумий пользователя"""
        think_time = random.uniform(min_time, max_time)
        if self.behavior == 'deliberate':
            think_time *= 1.5
        elif self.behavior == 'quick':
            think_time *= 0.5
            
        time.sleep(think_time)
    
    def show_menu_selection(self, choice, sub_choice=None):
        """Показ выбора пункта меню с эмуляцией пользовательского ввода"""
        current_time = time.strftime("%H:%M:%S")
        
        if choice == 1:
            if sub_choice == 1:
                print(f"{current_time} {self.client_name}: выбирает 'Ручной ввод данных'")
                self.simulate_thinking(0.3, 1.0)
                
                # Выбор случайного текста из samples
                text = random.choice(self.sample_texts)
                shift = random.randint(1, 10)
                
                print(f"{current_time} {self.client_name}: вводит данные...")
                self.simulate_typing(f"{text} {shift}")
                
                self.data = (text, shift)
                print(f"{current_time} {self.client_name}: {Messages.INFO['data_entered']}")
                
            elif sub_choice == 2:
                print(f"{current_time} {self.client_name}: выбирает 'Случайная генерация'")
                self.simulate_thinking(0.2, 0.8)
                
                # Генерация данных
                length = random.randint(5, 12)
                shift = random.randint(1, 15)
                text = ''.join(random.choices(string.ascii_letters, k=length))
                self.data = (text, shift)
                
                print(f"{current_time} {self.client_name}: {Messages.CONSOLE['client_generated']}")
                print(f"{current_time} {self.client_name}: сгенерировано: '{text}' сдвиг: {shift}")
                
        elif choice == 2:
            print(f"{current_time} {self.client_name}: выбирает 'Выполнить алгоритм'")
            self.simulate_thinking(0.5, 1.5)
            
        elif choice == 3:
            print(f"{current_time} {self.client_name}: выбирает 'Вывести результат'")
            self.simulate_thinking(0.2, 0.8)
    
    def send_request(self, text: str, shift: int) -> str:
        """Отправка запроса на сервер"""
        try:
            current_time = time.strftime("%H:%M:%S")
            print(f"{current_time} {self.client_name}: {Messages.CONSOLE['client_request']}")
            
            # Валидация перед отправкой
            if not text or not isinstance(text, str):
                raise ValidationError("Текст должен быть непустой строкой", None)
            
            # Отправка запроса серверу
            request_id = server.submit_request(text, shift, self.client_name)
            self.current_request_id = request_id
            
            print(f"{current_time} {self.client_name}: {Messages.INFO['waiting_server']}")
            
            # Ожидание результата с таймаутом
            start_time = time.time()
            timeout = 30
            
            while time.time() - start_time < timeout:
                result_data = server.get_result(request_id)
                if result_data:
                    if result_data['success']:
                        current_time = time.strftime("%H:%M:%S")
                        print(f"{current_time} {self.client_name}: {Messages.CONSOLE['client_result']}")
                        return result_data['result']
                    else:
                        raise InputError(f"Ошибка сервера: {result_data.get('error', 'Неизвестная ошибка')}", None)
                time.sleep(0.5)
            
            raise TimeoutError(f"Превышено время ожидания ответа ({timeout} секунд)", None)
                
        except (ValidationError, InputError, TimeoutError):
            raise
        except Exception as e:
            raise InputError(f"Неожиданная ошибка связи с сервером: {e}", e)
    
    def run_quick_session(self):
        """Быстрая сессия - все действия подряд"""
        print(f"\n{time.strftime('%H:%M:%S')} {self.client_name} начинает быструю сессию...")
        
        # 1. Ввод данных (автогенерация)
        self.show_menu_selection(1, 2)
        time.sleep(0.5)
        
        # 2. Выполнение алгоритма
        self.show_menu_selection(2)
        try:
            self.result = self.send_request(self.data[0], self.data[1])
            print(f"{time.strftime('%H:%M:%S')} {self.client_name}: {Messages.INFO['algorithm_completed']}")
        except Exception as e:
            print(f"{time.strftime('%H:%M:%S')} {self.client_name}: ошибка - {e}")
            return
        
        # 3. Показать результат
        self.show_menu_selection(3)
        print(f"{time.strftime('%H:%M:%S')} {self.client_name}: результат: {self.result}")
        
        time.sleep(1)
    
    def run_deliberate_session(self):
        """Обдуманная сессия - с паузами между действиями"""
        print(f"\n{time.strftime('%H:%M:%S')} {self.client_name} начинает обдуманную сессию...")
        
        # 1. Ввод данных (ручной ввод)
        self.show_menu_selection(1, 1)
        time.sleep(1)
        
        # Пауза перед следующим действием
        self.simulate_thinking(1.0, 3.0)
        
        # 2. Выполнение алгоритма
        self.show_menu_selection(2)
        try:
            self.result = self.send_request(self.data[0], self.data[1])
            print(f"{time.strftime('%H:%M:%S')} {self.client_name}: {Messages.INFO['algorithm_completed']}")
        except Exception as e:
            print(f"{time.strftime('%H:%M:%S')} {self.client_name}: ошибка - {e}")
            return
        
        # Пауза перед просмотром результата
        self.simulate_thinking(0.5, 2.0)
        
        # 3. Показать результат
        self.show_menu_selection(3)
        print(f"{time.strftime('%H:%M:%S')} {self.client_name}: результат: {self.result}")
        
        time.sleep(2)
    
    def run_erratic_session(self):
        """Непредсказуемая сессия - случайные действия"""
        print(f"\n{time.strftime('%H:%M:%S')} {self.client_name} начинает непредсказуемую сессию...")
        
        actions = [
            (1, 1),  # ручной ввод
            (1, 2),  # автогенерация
            (2, None),  # выполнить алгоритм
            (3, None)   # показать результат
        ]
        
        # Случайная последовательность действий
        for _ in range(random.randint(2, 4)):
            choice, sub_choice = random.choice(actions)
            self.show_menu_selection(choice, sub_choice)
            
            if choice == 1 and sub_choice == 1:
                # Ручной ввод
                text = random.choice(self.sample_texts)
                shift = random.randint(1, 8)
                self.data = (text, shift)
                print(f"{time.strftime('%H:%M:%S')} {self.client_name}: ввел: '{text}' сдвиг: {shift}")
                
            elif choice == 1 and sub_choice == 2:
                # Автогенерация
                length = random.randint(4, 10)
                shift = random.randint(1, 12)
                text = ''.join(random.choices(string.ascii_letters, k=length))
                self.data = (text, shift)
                print(f"{time.strftime('%H:%M:%S')} {self.client_name}: сгенерировал: '{text}' сдвиг: {shift}")
                
            elif choice == 2 and self.data:
                # Выполнение алгоритма
                try:
                    self.result = self.send_request(self.data[0], self.data[1])
                    print(f"{time.strftime('%H:%M:%S')} {self.client_name}: {Messages.INFO['algorithm_completed']}")
                except Exception as e:
                    print(f"{time.strftime('%H:%M:%S')} {self.client_name}: ошибка - {e}")
                    
            elif choice == 3 and self.result:
                # Показать результат
                print(f"{time.strftime('%H:%M:%S')} {self.client_name}: результат: {self.result}")
            
            time.sleep(random.uniform(0.5, 2.0))
    
    
    def run_session(self):
        """Запуск сессии в зависимости от поведения клиента"""
        behaviors_map = {
            'quick': self.run_quick_session,
            'deliberate': self.run_deliberate_session,
            'erratic': self.run_erratic_session
        }
        
        session_func = behaviors_map.get(self.behavior, self.run_quick_session)
        session_func()

def auto_client_thread(client_name):
    """Функция автоматического клиента"""
    client = AutoCryptoClient(client_name)
    
    print(f"{time.strftime('%H:%M:%S')} {client_name} подключился (поведение: {client.behavior})")
    
    # Каждый клиент выполняет 2-3 сессии
    num_sessions = random.randint(2, 3)
    
    for session_num in range(num_sessions):
        print(f"\n{time.strftime('%H:%M:%S')} {client_name} начинает сессию {session_num + 1}")
        client.run_session()
        
        # Пауза между сессиями
        if session_num < num_sessions - 1:
            pause_time = random.uniform(3, 8)
            print(f"{time.strftime('%H:%M:%S')} {client_name}: пауза {pause_time:.1f} сек...")
            time.sleep(pause_time)
    
    print(f"\n{time.strftime('%H:%M:%S')} {client_name}: завершил работу")
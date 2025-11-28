# server.py
import time
import random
import threading
from queue import Queue, Empty
from logg import server_logger
from messages import Messages
from exceptions import CryptoError, ServerError, QueueError, ValidationError

class CryptoServer:
    def __init__(self):
        self.requests_queue = Queue()
        self.results = {}
        self.request_counter = 0
        self.running = False
        self.worker_thread = None
        self.lock = threading.Lock()
        
    def encrypt_text(self, text: str, shift: int) -> str:
        """Шифрование текста с эмуляцией длительных вычислений"""
        try:
            # Валидация входных данных
            if not isinstance(text, str) or not text:
                raise ValidationError("Текст должен быть непустой строкой", None)
            
            if not isinstance(shift, int) or shift < 0:
                raise ValidationError("Сдвиг должен быть положительным целым числом", None)
            
            # Эмуляция длительных вычислений (2-5 секунд)
            processing_time = random.uniform(2, 5)
            time.sleep(processing_time)
            
            result = []
            for char in text:
                if char.isalpha():
                    base = ord('a') if char.islower() else ord('A')
                    new_char = chr((ord(char) - base + shift) % 26 + base)
                    result.append(new_char)
                else:
                    result.append(char)
                    
            return ''.join(result)
            
        except ValidationError:
            raise
        except Exception as e:
            server_logger.error(f"Критическая ошибка шифрования: {e}")
            raise CryptoError(f"Ошибка шифрования: {e}", e)
    
    def process_requests(self):
        """Обработка запросов из очереди"""
        server_logger.info("Запущен обработчик запросов")
        
        while self.running:
            try:
                # Получение запроса из очереди с таймаутом
                request = self.requests_queue.get(timeout=1.0)
                if request is None:  # Сигнал остановки
                    server_logger.info("Получен сигнал остановки обработчика")
                    break
                    
                request_id, text, shift, client_name = request
                
                # Логирование и вывод в консоль
                current_time = time.strftime("%H:%M:%S")
                print(f"{current_time} {client_name}: {Messages.CONSOLE['server_received']}")
                server_logger.info(f"Клиент {client_name}: получен запрос - текст: '{text}', сдвиг: {shift}")
                
                try:
                    # Выполнение шифрования
                    print(f"{current_time} {client_name}: {Messages.CONSOLE['server_processing']}")
                    server_logger.info(f"Клиент {client_name}: начало шифрования")
                    
                    result = self.encrypt_text(text, shift)
                    
                    # Сохранение результата с блокировкой
                    with self.lock:
                        self.results[request_id] = {
                            'success': True,
                            'result': result,
                            'client_name': client_name
                        }
                    
                    current_time = time.strftime("%H:%M:%S")
                    print(f"{current_time} {client_name}: {Messages.CONSOLE['server_completed']}")
                    server_logger.info(f"Клиент {client_name}: шифрование завершено, результат: '{result}'")
                    
                except (ValidationError, CryptoError) as e:
                    # Ошибки шифрования - сохраняем информацию об ошибке
                    with self.lock:
                        self.results[request_id] = {
                            'success': False,
                            'error': str(e),
                            'client_name': client_name
                        }
                    server_logger.error(f"Ошибка шифрования для клиента {client_name}: {e}")
                    
                except Exception as e:
                    # Непредвиденные ошибки
                    with self.lock:
                        self.results[request_id] = {
                            'success': False,
                            'error': Messages.ERROR["general_error"],
                            'client_name': client_name
                        }
                    server_logger.critical(f"Непредвиденная ошибка для клиента {client_name}: {e}")
                
                finally:
                    self.requests_queue.task_done()
                
            except Empty:
                # Таймаут очереди - нормальная ситуация, продолжаем работу
                continue
                
            except Exception as e:
                server_logger.critical(f"Критическая ошибка обработчика запросов: {e}")
                # Не прерываем цикл, продолжаем обработку
                continue
    
    def submit_request(self, text: str, shift: int, client_name: str) -> int:
        """Добавление запроса в очередь"""
        try:
            # Валидация перед добавлением в очередь
            if not isinstance(text, str) or not text.strip():
                raise ValidationError("Текст не может быть пустым", None)
            
            if not isinstance(shift, int):
                raise ValidationError("Сдвиг должен быть числом", None)
            
            with self.lock:
                request_id = self.request_counter
                self.request_counter += 1
            
            self.requests_queue.put((request_id, text, shift, client_name))
            server_logger.debug(f"Запрос {request_id} добавлен в очередь от {client_name}")
            return request_id
            
        except Exception as e:
            server_logger.error(f"Ошибка добавления запроса в очередь: {e}")
            raise QueueError(f"Ошибка отправки запроса: {e}", e)
    
    def get_result(self, request_id: int):
        """Получение результата по ID запроса"""
        try:
            with self.lock:
                return self.results.get(request_id)
        except Exception as e:
            server_logger.error(f"Ошибка получения результата {request_id}: {e}")
            return None
    
    def start(self):
        """Запуск сервера"""
        try:
            self.running = True
            self.worker_thread = threading.Thread(target=self.process_requests, daemon=True)
            self.worker_thread.start()
            server_logger.info("Сервер запущен успешно")
            print("Сервер запущен и готов к работе")
            
        except Exception as e:
            server_logger.critical(f"Ошибка запуска сервера: {e}")
            raise ServerError(f"Не удалось запустить сервер: {e}", e)
    
    def stop(self):
        """Остановка сервера"""
        try:
            self.running = False
            # Отправляем сигнал остановки
            self.requests_queue.put(None)
            
            if self.worker_thread:
                self.worker_thread.join(timeout=5.0)  # Таймаут 5 секунд
                
            server_logger.info("Сервер остановлен успешно")
            
        except Exception as e:
            server_logger.error(f"Ошибка остановки сервера: {e}")

# Глобальный экземпляр сервера
server = CryptoServer()
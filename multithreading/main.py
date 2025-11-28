# demo_showcase.py
import time
import threading
from server import server
from client import AutoCryptoClient

def main():
    """Демонстрация всех типов поведения"""
    print("=== ДЕМОНСТРАЦИЯ АВТОМАТИЧЕСКИХ КЛИЕНТОВ ===")
    
    # Запускаем сервер
    server.start()
    time.sleep(2)
    
    # Создаем клиентов с разным поведением
    clients = [
        ("Алиса", "quick"),
        ("Иван", "deliberate"), 
        ("Диана", "erratic")
    ]
    
    threads = []
    
    for client_name, behavior in clients:
        client = AutoCryptoClient(client_name)
        client.behavior = behavior
        
        thread = threading.Thread(target=client.run_session)
        thread.daemon = True
        threads.append(thread)
        
        print(f"{time.strftime('%H:%M:%S')} Запускается {client_name}")
        thread.start()
        time.sleep(3)  # Задержка между запуском клиентов
    
    # Ожидаем завершения
    for thread in threads:
        thread.join(timeout=60)
    
    server.stop()
    print(f"\n{time.strftime('%H:%M:%S')} Демонстрация завершена")

if __name__ == "__main__":
    main()
import time
import tracemalloc
from typing import List, Tuple

global GLOBAL_COUNTER

# Неэффективная функция
def process_data_inefficient(data: List[int]) -> Tuple[List[int], int, List[Tuple[int, int]]]:
    """
    Неэффективная обработка данных с использованием:
    - Глобальных переменных
    - Внешних циклов вместо list comprehension
    - Ручной проверки наличия элемента
    - Без использования enumerate
    - Неоптимальная работа с файлами
    """
    
    # 1. Использование глобальной переменной (плохая практика)
    GLOBAL_COUNTER = 0
    
    # 2. Создание нового списка через внешний цикл
    even_numbers = []
    for num in data:
        if num % 2 == 0:
            even_numbers.append(num)
            GLOBAL_COUNTER += 1
    
    # 3. Проверка наличия элемента через цикл (не используем 'in')
    max_value = max(data) if data else 0
    is_present = False
    for num in data:
        if num == max_value:
            is_present = True
            break
    
    # 4. Получение индексов через range(len())
    indexed_data = []
    for i in range(len(data)):
        if data[i] > 0:
            indexed_data.append((i, data[i]))
    
    # 5. Неоптимальная работа с файлом (без 'with')
    try:
        f = open("no_efficent_file.txt", "w")
        for num in data:
            f.write(f"{num}\n")
        f.close()
    except:
        pass
    
    return even_numbers, GLOBAL_COUNTER, indexed_data

# Эффективная функция
def process_data_efficient(data: List[int]) -> Tuple[List[int], int, List[Tuple[int, int]]]:
    """
    Эффективная обработка данных с использованием:
    - List comprehension вместо внешних циклов
    - Локальные переменные вместо глобальных
    - Использование 'in' для проверки
    - Использование enumerate для индексации
    - Использование 'with' для работы с файлами
    - Использование itertools для уникальных значений
    """
    
    # 1. Локальная переменная вместо глобальной
    counter = 0
    
    # 2. List comprehension для создания списка (быстрее и читабельнее)
    even_numbers = [num for num in data if num % 2 == 0]
    counter = len(even_numbers)
    
    # 3. Использование 'in' для проверки наличия элемента
    max_value = max(data) if data else 0
    is_present = max_value in data  # Используем ключевое слово 'in'
    
    # 4. Использование enumerate для получения индексов
    indexed_data = [(i, num) for i, num in enumerate(data) if num > 0]
    
    # 5. Использование 'with' для безопасной работы с файлом
    with open("yes_efficent_file.txt", "w") as f:
        for num in data:
            f.write(f"{num}\n")
    
    return even_numbers, counter, indexed_data

# Хэлперы
def generate_test_data(size: int = 10000) -> List[int]:
    """Генерация тестовых данных"""
    import random
    return [random.randint(-1000, 1000) for _ in range(size)]

def measure_performance(func, data: List[int], func_name: str):
    """Измерение производительности функции"""
    print(f"\n{'='*60}")
    print(f"Тестирование: {func_name}")
    
    # Очистка памяти от предыдущих измерений
    if 'GLOBAL_COUNTER' in globals():
        del globals()['GLOBAL_COUNTER']
    
    # Измерение памяти
    tracemalloc.start()
    
    # Измерение времени
    start_time = time.perf_counter()
    result = func(data)
    end_time = time.perf_counter()
    
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Проверка результатов
    even_nums, counter, indexed = result
    
    print(f"Размер данных: {len(data):,}")
    print(f"Найдено чётных чисел: {len(even_nums):,}")
    print(f"Счётчик: {counter}")
    print(f"Индексированных элементов: {len(indexed):,}")
    print(f"Время выполнения: {(end_time - start_time)*1000:.4f} мс")
    print(f"Пиковое потребление памяти: {peak / 1024:.2f} КБ")
    
    return end_time - start_time, peak, result

# Функция запуска
def main():
    """Основная функция для сравнения производительности"""
    print("СРАВНЕНИЕ ЭФФЕКТИВНОГО И НЕЭФФЕКТИВНОГО КОДА НА PYTHON")
    print("Основано на приёмах из документа 'Приёмы эффективного кода на Python'")
    
    # Генерация тестовых данных
    test_data = generate_test_data(5000)
    
    # Тестирование неэффективной функции
    time_ineff, mem_ineff, result_ineff = measure_performance(
        process_data_inefficient, test_data, "НЕЭФФЕКТИВНАЯ ФУНКЦИЯ"
    )
    
    # Тестирование эффективной функции
    time_eff, mem_eff, result_eff = measure_performance(
        process_data_efficient, test_data, "ЭФФЕКТИВНАЯ ФУНКЦИЯ"
    )
    
    # Проверка корректности результатов
    print(f"\n{'='*60}")
    print("ПРОВЕРКА КОРРЕКТНОСТИ РЕЗУЛЬТАТОВ:")
    
    # Сравнение результатов обеих функций
    if (result_ineff[0] == result_eff[0] and  # even_numbers
        result_ineff[1] == result_eff[1] and  # counter
        result_ineff[2] == result_eff[2]):    # indexed_data
        print("   Результаты обеих функций идентичны")
    else:
        print("   Результаты функций различаются!")
        print(f"  Чётные числа совпадают: {result_ineff[0] == result_eff[0]}")
        print(f"  Счётчики совпадают: {result_ineff[1] == result_eff[1]}")
        print(f"  Индексированные данные совпадают: {result_ineff[2] == result_eff[2]}")
    
    # Сравнение производительности
    print(f"\n{'='*60}")
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ:")
    print(f"{'Метрика':<25} {'Неэффективная':<15} {'Эффективная':<15} {'Ускорение':<10}")
    print(f"{'-'*25:<25} {'-'*15:<15} {'-'*15:<15} {'-'*10:<10}")
    
    print(f"{'Время (мс)':<25} {time_ineff*1000:<15.4f} {time_eff*1000:<15.4f} {time_ineff/time_eff:>9.1f}x")
    print(f"{'Память (КБ)':<25} {mem_ineff/1024:<15.2f} {mem_eff/1024:<15.2f} {mem_ineff/mem_eff:>9.1f}x")


if __name__ == "__main__":
    main()
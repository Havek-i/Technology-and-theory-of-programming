# bot.py
import asyncio
import os
from dotenv import load_dotenv
from state_machine import StateMachine
from user_session import UserSessionManager
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from log import server_logger
import general_func as gf
import helper_func as hf

# Загрузка переменных окружения
load_dotenv()

# Токен бота
API_TOKEN = os.getenv("BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в .env файле")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация автомата состояний и менеджера сессий
SM = StateMachine()
session_manager = UserSessionManager()

# Состояния FSM для обработки ввода
class InputStates(StatesGroup):
    waiting_for_data = State()

# Клавиатуры для меню
def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Основная клавиатура меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Ввести данные"), KeyboardButton(text="⚙️ Выполнить алгоритм")],
            [KeyboardButton(text="📊 Вывести результат"), KeyboardButton(text="❌ Завершить работу")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_input_method_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора метода ввода"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✍️ Самостоятельный ввод"), KeyboardButton(text="🎲 Случайная генерация")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

@dp.message(Command("start", "restart"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    server_logger.info(f"Пользователь {user_id} запустил бота")
    
    # Сбрасываем сессию пользователя
    await session_manager.clear_session(user_id)
    
    # Сбрасываем состояние автомата
    SM._restart()
    
    await message.answer(
        "🤖 Добро пожаловать в бот для шифрования Виженера!\n"
        "Используйте меню ниже для навигации:",
        reply_markup=get_main_keyboard()
    )

@dp.message(F.text == "🔙 Назад")
async def cmd_back(message: types.Message):
    """Обработчик кнопки Назад"""
    user_id = message.from_user.id
    
    # Обновляем сессию
    await session_manager.update_session(
        user_id, 
        waiting_for_input=False,
        input_method=None
    )
    
    await message.answer(
        "Возвращаюсь в главное меню:",
        reply_markup=get_main_keyboard()
    )

@dp.message(F.text == "📝 Ввести данные")
async def cmd_input(message: types.Message):
    """Обработчик выбора ввода данных"""
    user_id = message.from_user.id
    
    try:
        # Обновляем сессию
        await session_manager.update_session(
            user_id,
            waiting_for_input=True
        )
        
        # Вызываем автомат состояний
        SM.manager('input', user_id=user_id)
        
        await message.answer(
            "Выберите способ ввода данных:",
            reply_markup=get_input_method_keyboard()
        )
    except Exception as e:
        server_logger.error(f"Ошибка при выборе ввода данных: {e}")
        await message.answer(f"Ошибка: {str(e)}")

@dp.message(F.text == "✍️ Самостоятельный ввод")
async def cmd_manual_input(message: types.Message, state: FSMContext):
    """Обработчик ручного ввода"""
    user_id = message.from_user.id
    
    try:
        # Обновляем сессию
        await session_manager.update_session(
            user_id,
            input_method='manual',
            waiting_for_input=True
        )
        
        await state.set_state(InputStates.waiting_for_data)
        await message.answer(
            "✏️ Введите строку и сдвиг через пробел (например: 'hello 3'):\n"
            "⚠️ Строка должна содержать только буквы английского алфавита.",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

@dp.message(F.text == "🎲 Случайная генерация")
async def cmd_random_generate(message: types.Message):
    """Обработчик случайной генерации"""
    user_id = message.from_user.id
    
    try:
        # Обновляем сессию
        await session_manager.update_session(
            user_id,
            input_method='random',
            waiting_for_input=False
        )
        
        # Генерируем случайные данные
        random_data = gf.generating_params()
        
        # Сохраняем данные в сессию
        await session_manager.update_session(
            user_id,
            data=random_data,
            waiting_for_input=False
        )
        
        # Обновляем данные в автомате состояний
        SM.set_user_data(user_id, random_data)
        
        # Переходим в состояние INPUT
        SM.manager('input', user_id=user_id)
        
        await message.answer(
            f"✅ Данные сгенерированы:\n"
            f"📝 Текст: {random_data[0]}\n"
            f"🔢 Сдвиг: {random_data[1]}\n\n"
            f"Теперь вы можете выполнить алгоритм шифрования.",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        server_logger.error(f"Ошибка при генерации данных: {e}")
        await message.answer(f"Ошибка: {str(e)}")

@dp.message(InputStates.waiting_for_data)
async def process_manual_input(message: types.Message, state: FSMContext):
    """Обработка ручного ввода данных"""
    user_id = message.from_user.id
    
    try:
        # Парсим введенные данные
        user_input = message.text.strip()
        
        # Обрабатываем данные
        input_data = gf.input_params(user_input)
        
        # Сохраняем данные в сессию
        await session_manager.update_session(
            user_id,
            data=input_data,
            waiting_for_input=False
        )
        
        # Обновляем данные в автомате состояний
        SM.set_user_data(user_id, input_data)
        
        # Сбрасываем состояние FSM
        await state.clear()
        
        await message.answer(
            f"✅ Данные приняты:\n"
            f"📝 Текст: {input_data[0]}\n"
            f"🔢 Сдвиг: {input_data[1]}\n\n"
            f"Теперь вы можете выполнить алгоритм шифрования.",
            reply_markup=get_main_keyboard()
        )
    except ValueError as e:
        await message.answer(
            f"❌ Ошибка формата: {str(e)}\n"
            f"Пожалуйста, введите данные в формате 'текст число' (например: 'hello 3'):"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
        await state.clear()
        await message.answer(
            "Возвращаюсь в главное меню:",
            reply_markup=get_main_keyboard()
        )

@dp.message(F.text == "⚙️ Выполнить алгоритм")
async def cmd_computing(message: types.Message):
    """Обработчик запуска вычислений"""
    user_id = message.from_user.id
    
    try:
        # Получаем сессию пользователя
        session = await session_manager.get_session(user_id)
        
        # Проверяем, есть ли данные для обработки
        if session.data is None:
            await message.answer(
                "❌ Нет данных для шифрования.\n"
                "Сначала введите данные через меню '📝 Ввести данные'.",
                reply_markup=get_main_keyboard()
            )
            return
        
        # Сохраняем данные в автомате состояний
        SM.set_user_data(user_id, session.data)
        
        # Выполняем переход в состояние COMPUTING
        SM.manager('computing', user_id=user_id)
        
        # Выполняем шифрование
        encrypted = gf.crypto(string=session.data[0], shift=session.data[1])
        
        # Сохраняем результат в сессию
        await session_manager.update_session(
            user_id,
            result=encrypted
        )
        
        # Обновляем результат в автомате
        SM._result = encrypted
        
        await message.answer(
            f"✅ Шифрование выполнено успешно!\n"
            f"📝 Исходный текст: {session.data[0]}\n"
            f"🔢 Сдвиг: {session.data[1]}\n"
            f"🔐 Зашифрованный текст: {encrypted}\n\n"
            f"Теперь вы можете вывести результат.",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        server_logger.error(f"Ошибка при выполнении алгоритма: {e}")
        await message.answer(f"❌ Ошибка при шифровании: {str(e)}")

@dp.message(F.text == "📊 Вывести результат")
async def cmd_result(message: types.Message):
    """Обработчик вывода результата"""
    user_id = message.from_user.id
    
    try:
        # Получаем сессию пользователя
        session = await session_manager.get_session(user_id)
        
        # Проверяем, есть ли результат
        if session.result is None:
            await message.answer(
                "❌ Нет результата для отображения.\n"
                "Сначала выполните алгоритм шифрования через меню '⚙️ Выполнить алгоритм'.",
                reply_markup=get_main_keyboard()
            )
            return
        
        # Переходим в состояние RESULT
        SM.manager('result', user_id=user_id)
        
        # Форматируем и выводим результат
        result_text = gf.format_result_display(
            string=session.data[0] if session.data else "",
            shift=session.data[1] if session.data else 0,
            encrypted=session.result
        )
        
        await message.answer(
            result_text,
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        server_logger.error(f"Ошибка при выводе результата: {e}")
        await message.answer(f"❌ Ошибка: {str(e)}")

@dp.message(F.text == "❌ Завершить работу")
async def cmd_exit(message: types.Message):
    """Обработчик завершения работы"""
    user_id = message.from_user.id
    
    try:
        # Вызываем автомат состояний
        SM.manager('destructor', user_id=user_id)
        
        # Очищаем сессию
        await session_manager.clear_session(user_id)
        
        await message.answer(
            "👋 Завершение работы бота.\n"
            "Для перезапуска используйте команду /start",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

@dp.message()
async def process_unknown_message(message: types.Message):
    """Обработка неизвестных сообщений"""
    user_id = message.from_user.id
    
    # Проверяем, ожидаем ли мы ввод данных
    session = await session_manager.get_session(user_id)
    
    if session.waiting_for_input and session.input_method == 'manual':
        # Пользователь вводит данные, но не через правильное состояние FSM
        await message.answer(
            "Пожалуйста, используйте кнопку '✍️ Самостоятельный ввод' для ввода данных.",
            reply_markup=get_input_method_keyboard()
        )
    else:
        await message.answer(
            "Не понимаю команду. Используйте меню ниже:",
            reply_markup=get_main_keyboard()
        )

async def main():
    """Основная функция запуска бота"""
    server_logger.info("Запуск Telegram бота...")
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
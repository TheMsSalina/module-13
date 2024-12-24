from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]],
    resize_keyboard=True)

kb = InlineKeyboardMarkup()
button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формула рассчёта', callback_data='formula')
kb.add(button, button2)

class UserState(StatesGroup):
    weight = State()
    growth = State()
    age = State()

@dp.message_handler(text ='Рассчитать')
async def start_message(message):
    await message.answer('Выберите опцию:', reply_markup = kb)

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])- 161)
    await message.answer(f"Ваша норма калорий: {norma}")
    await state.finish()

@dp.callback_query_handler(text='formula')
async def get_formulas(call):
    await call.message.answer('Норма калорий = 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = menu)

@dp.message_handler(text = ['Информация'])
async def info_message(message):
    await message.answer('Информация о боте')

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

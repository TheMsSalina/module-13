from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

class UserState(StatesGroup):
    weight = State()
    growth = State()
    age = State()
    gender = State()


@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
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
'''

Я попыталась сделать, чтобы счетчик учитывал пол и применял формулу соответственно ему, но бот просто тормозится:)


@dp.message_handler(state=UserState.gender)
async def set_gender(message, state):
    await state.update_data(gender=message.text)
    await message.answer('Введите свой пол (м/ж):')
    await UserState.gender.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    for i in data.values:
        values = data.values
        if values == 'м':
            norma = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])) + 5
        else:
            norma = (10 * int(data["weight"])) + (6,25 * int(data["growth"])) - (5 * int(data["age"])) - 161
        await message.answer(f"Ваша норма калорий: {norma}")
    await state.finish()
'''

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # формула рассчёта для мужчин
    norma = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])) + 5
    await message.answer(f"Ваша норма калорий: {norma}")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
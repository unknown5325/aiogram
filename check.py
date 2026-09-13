from aiogram import Bot, Dispatcher, types
import asyncio
from os import getenv
from dotenv import load_dotenv
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.filters import Command
import requests
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


load_dotenv()
bot_token = getenv("BOT_TOKEN")

bot = Bot(token=bot_token)
dp = Dispatcher()

class Loading_states(StatesGroup):
    curr = State()
    wc = State()
    price = State()

@dp.message(Command('start'))
async def start(message):
    keyboard = [
        [types.KeyboardButton(text="/converter")],
        [types.KeyboardButton(text="/ex_rate")]
        ]
    builder = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.answer('Выберите действие: ', reply_markup=builder)
    

@dp.message(Command('converter'))
async def byn_to_other(message, state):
    new_keyboard = [
        [types.KeyboardButton(text='/close')]
    ]
    new_builder = ReplyKeyboardMarkup(keyboard=new_keyboard, resize_keyboard=True)
    await message.answer('Из какой валюты вы хотите перевести? ', reply_markup=new_builder)
    await state.set_state(Loading_states.curr)
    print(message.text)

    

@dp.message(Loading_states.curr)
async def curr_mess(message, state):
    if message.text == '/close':
        await start(message)
        await state.clear()
        return 
    print(message.text)
    currj = message.text.upper()
    await state.update_data(user_curr=currj)
    await message.answer('В какую валюту вы хотите перевести? ')
    await state.set_state(Loading_states.wc)

@dp.message(Loading_states.wc)
async def wc_mess(message, state):
    if message.text == '/close':
        await start(message)
        await state.clear()
        return 
    print(message.text)
    wcj = message.text.upper()
    await state.update_data(user_answer=wcj)
    await message.answer('Сколько вы хотите перевести? ')
    await state.set_state(Loading_states.price)

@dp.message(Loading_states.price)
async def price_mess(message, state):
    if message.text == '/close':
        await start(message)
        await state.clear()
        return 
    print(message.text)
    price = float(message.text)
    try:
        users_answer = await state.get_data()
        curr = users_answer.get('user_curr')
        response = requests.get(f'https://open.er-api.com/v6/latest/{curr}')
        data = response.json()
        wc = users_answer.get('user_answer')
        data_rates = data["rates"]
        data_wc = float(data_rates[f'{(wc.upper())}']) * price
        await message.answer(f"Результат конвертации: {data_wc:.2f} {wc}")
    
    except Exception:
        await message.answer("Sry, bot is thinking")   

@dp.message(Command('ex_rate'))
async def func_all(message):
    response = requests.get(f'https://open.er-api.com/v6/latest/byn')
    data = response.json()
    data_rates = data["rates"]
    res = '\n'.join(f'{k} : {v}' for k, v in data_rates.items())
    await message.answer(f'Вот весь список курса валют: {res}')


@dp.message()
async def func_start(message):
    print(message.text)
    await message.answer('repeat')


async def main():
    bot = Bot(token=bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
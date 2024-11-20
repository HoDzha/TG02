import asyncio
import random
import os
from gtts import gTTS
import requests

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import aiohttp
import logging
from aiogram.types import Message, FSInputFile
from consts import TOKEN, WEATHER_TOKEN

from googletrans import Translator



bot = Bot(TOKEN)
dp = Dispatcher()
loging = logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()

def init_db():
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()



@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.full_name}! Как тебя зову?')
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
     await state.update_data(name = message.text)
     await message.answer('Сколько тебе лет?')
     await state.set_state(Form.age)


@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await message.update_data(age=message.text)
    await message.answer('Из какого ты города?')
    await state.set_state(Form.city)

@dp.message(Form.city)
async def city(message: Message, state: FSMContext):
    user_data = await state.get_data()
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute("""INSERT INTO users (name, age, city) VALUES (?, ?, ?)""", (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()
    conn.close()

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_data["city"]}&appid={WEATHER_TOKEN}&units=metric&lang=ru') as response:
            if response.status == 200:
                weather_data = await response.json()
                main = weather_data['main']
                feels_like = main['feels_like']
                temperature = main['temp']
                humidity = main['humidity']
                weather = weather_data['weather'][0]
                description = weather['description']
                weather_report=(f'В городе {user_data["city"]} \n'
                                f'температура {temperature}°C, \n'
                                f'ощущается как {feels_like}°C, \n'
                                f'влажность {humidity}%, \n'
                                f'описание погоды: {description}')
                await message.answer(weather_report)
            else:
                await message.answer('Что-то пошло не так. Попробуй еще раз')
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
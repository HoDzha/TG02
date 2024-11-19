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
    await state.set_state(Form.name.state)
                         













if __name__ == '__main__':
    asyncio.run(main())
import asyncio
import random
import os
from gtts import gTTS
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command

from aiogram.types import Message, FSInputFile, CallbackQuery
from consts import HO_DZHA_BOT, WEATHER_TOKEN
import  keyboards as kb
from googletrans import Translator


bot = Bot(HO_DZHA_BOT)
dp = Dispatcher()
translator = Translator()

@dp.callback_query(F.data == "show_more")
async def show_more(callback: CallbackQuery):
    await callback.message.edit_text("Опции", reply_markup= await kb.optioins_keyboard())


@dp.callback_query(F.data =='Опция 1')
async def option1(callback: CallbackQuery):
    await callback.answer('Опция 1')

@dp.callback_query(F.data =='Опция 2')
async def option2(callback: CallbackQuery):
    await  callback.message.answer('Опция 2')


@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer(text='Динамическое меню',reply_markup=kb.inline_kb_more)







@dp.message(Command('links'))
async def links(message: Message):
    await message.answer("Ссылки", reply_markup=kb.inline_menu_kb)



@dp.message(F.text == 'Привет')
async def button1_text(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

@dp.message(F.text == 'Пока')
async def button1_text(message: Message):
    await message.answer(f"Пока, {message.from_user.full_name}!")

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Выберите команду", reply_markup=kb.menu_kb)

# @dp.message()
# async def translate_text(message: types.Message):
#     try:
#         translation = translator.translate(message.text, dest='en')
#         await message.reply(translation.text)
#     except Exception as e:
#         await message.reply(f"Произошла ошибка при переводе: {str(e)}")
async def main(dispatcher):
     await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main(dp))
import asyncio
from aiogram import Bot,  Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import requests
from googletrans import Translator

from consts import HO_DZHA_BOT

translator = Translator()
bot = Bot(token=HO_DZHA_BOT)
dp = Dispatcher()


@dp.message_handler(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Введи целое число, и получишь факт об этой цифре. \n"
        "Либо введи команду /random, чтобы получить факт о случайной цифре."
    )


@dp.message_handler(Command("random"))
async def random_command(message: Message):
    url = "http://numbersapi.com/random?json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            translation = translator.translate(data["text"], dest='ru')
            await message.reply(translation.text)
        except Exception as e:
            await message.reply(f"Ошибка при переводе: {str(e)}")
    else:
        await message.reply("Ошибка при получении данных от Numbers API.")


@dp.message_handler()
async def get_number_info(message: types.Message):
    text = message.text
    try:
        number = int(text)
        url = f"http://numbersapi.com/{number}?json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                translation = translator.translate(data["text"], dest='ru')
                await message.reply(translation.text)
            except Exception as e:
                await message.reply(f"Ошибка при переводе: {str(e)}")
        else:
            await message.reply("Ошибка при получении данных от Numbers API.")
    except ValueError:
        await message.reply("Это не целое число! Пожалуйста, введите целое число.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
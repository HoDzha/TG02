import asyncio
import random
import os
from gtts import gTTS
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command

from aiogram.types import Message, FSInputFile, CallbackQuery
from consts import TOKEN, WEATHER_TOKEN
import  keyboards as kb
from googletrans import Translator


bot = Bot(TOKEN)
dp = Dispatcher()
translator = Translator()


# Функция для получения данных о погоде
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_TOKEN,
        "units": "metric",
        "lang": "ru"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["cod"] != 200:
            return f"Ошибка: {data['message']}"
        weather_description = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (
            f"Погода в городе <b>{city}</b>:\n"
            f"🌡️ Температура: {temperature}°C\n"
            f"🤗 Ощущается как: {feels_like}°C\n"
            f"💧 Влажность: {humidity}%\n"
            f"🌬️ Ветер: {wind_speed} м/с\n"
            f"☁️ Описание: {weather_description}"
        )
    except Exception as e:
        return f"Ошибка при получении данных: {str(e)}"



@dp.callback_query(F.data == "news")
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)
    await callback.message.edit_text('Вот свежие новости!', reply_markup=await kb.test_keyboard())


@dp.message(Command('audio'))
async def audio(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('audio.m4a')
    await bot.send_audio(message.chat.id, audio)
@dp.message(Command('video'))
async def video(message: types.Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message: types.Message):
    voice = FSInputFile("sample.ogg")
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: types.Message):
    doc = FSInputFile("tgo2.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('traning'))
async def training(message: Message):
    training_list = [
       "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений \n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня: \n {rand_tr}")
    tts = gTTS(rand_tr, lang="ru")
    tts.save("training.ogg")
    await bot.send_voice(message.chat.id, FSInputFile("training.ogg"))
    os.remove('training.ogg')



@dp.message(Command('weather'))
async def weather_command(message: types.Message):
    command = message.text.strip()
    parts = command.split(" ", 1)

    if len(parts) < 2:
        await message.reply(
            "Пожалуйста, укажите город. Пример: /weather Москва"
        )
        return

    city = parts[1].strip()
    weather_info = get_weather(city)
    await message.reply(weather_info, parse_mode='HTML')


@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://cs6.livemaster.ru/storage/47/1f/e6c1defa8ea4fc9293081373656a.jpg',
            'https://cs6.livemaster.ru/storage/51/8d/e9304e78c01418b5ea956d3be36a.jpg',
            'https://cs6.livemaster.ru/storage/f1/a7/378d36a85b8e6cab15c48e25026a.jpg',
            'https://cs3.livemaster.ru/zhurnalfoto/d/a/1/150404091759.jpeg',
            'https://i.cdn01.ru/files/users/images/a0/9c/a09c2c96ab8ce875ae85ee5cfb2c0d52.jpg',
            'https://i.cdn01.ru/files/users/images/62/67/6267b7e32ed5aff57c00b0532e6af910.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(rand_photo, caption='Это супер кот')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого!', 'Cool!','Фу бяка','Кака бяка бее','Красота - страшная сила!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')


@dp.message(F.text=='Что такое ИИ')
async def aitext(message: Message):
    await message.answer('ИИ - это дох и больше текста ааа')


@dp.message(F.text == 'Тестовая кнопка 1')
async def button1_text(message: Message):
    await message.answer('кнопка 1 нажата успешно. Орешник уже летит')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды \n /start  \n /help \n /photo \n /weather \n Что такое ИИ')


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=kb.inline_keyboard_test)

@dp.message()
async def translate_text(message: types.Message):
    try:
        translation = translator.translate(message.text, dest='en')
        await message.reply(translation.text)
    except Exception as e:
        await message.reply(f"Произошла ошибка при переводе: {str(e)}")
async def main(dispatcher):
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main(dp))
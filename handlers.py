from aiogram import types, Dispatcher
import requests
from data import open_weather_token
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import datetime
import os
from TelegramBot_Loader import states_bot

# @dp.message_handler(Text(equals='Ping IP'))
async def ping_ip(message: types.Message):
    await message.answer('Введи имя хоста, либо IP для проверки доступности')
    await states_bot.ping_state.set()

# @dp.message_handler(state=states_bot.ping_state)
async def ping_ip_get(message: types.Message, state: FSMContext):
    await message.answer('5 секунд, кидаю пакеты...')
    answer = message.text
    resp = os.system('ping -n 5 ' + answer)
    if resp == 0:
        pong = ('Хост жив:)')
    else:
        pong = ('Хост не жив, упал:(')
    await message.answer(pong)
    await state.finish()

# @dp.message_handler(Text(equals='Проверка IP'))
async def out_ip(message: types.Message):
    await message.answer('Напиши IP адрес или DNS имя для которого хочешь узнать информацию')
    await states_bot.ip_state.set()

# @dp.message_handler(state=states_bot.ip_state)
async def get_ip(message: types.Message, state: FSMContext):
    try:
        ip_req = requests.get(f'http://ip-api.com/json/{message.text}')
        response = ip_req.json()
        ip_country = response['country']
        ip_city = response['city']
        ip_isp = response['isp']
        ip_org = response['org']
        await message.answer(f'Вот что я смог найти:\n'
                                f'Страна: {ip_country}\nГород: {ip_city}\nПровайдер: {ip_isp}\nОрганизация{ip_org}')
    except:
        await message.answer('Введенный IP адрес не является белым')
    await state.finish()

# @dp.message_handler(Text(equals='Точное время'))
async def get_time(message: types.Message, state: FSMContext):
    await message.answer('Определяю хде ты...')
    await states_bot.time_state.set()
    time_req = requests.get(f'http://worldtimeapi.org/api/ip')
    response = time_req.json()
    time_ip = response['client_ip']
    time_date = response['datetime']
    await message.answer(f'Твои данные:\n'
                             f'IP адрес: {time_ip}\nТочное время : {time_date}')
    await state.finish()

# @dp.message_handler(Text(equals='Погода'))
async def out_weather(message: types.Message):
    await message.answer('Напиши название города')
    await states_bot.weather_state.set()

# @dp.message_handler(state=states_bot.weather_state)
async def get_weather(message: types.Message, state: FSMContext):
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
            )
            data = r.json()

            city = data["name"]
            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму что там за погода!"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(
                data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            await message.reply(f"***{datetime.datetime.now( ).strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***"
                                )

        except:
            await message.reply("\U00002620 Проверьте название города \U00002620")
        await state.finish()

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(ping_ip, Text(equals='Ping IP'))
    dp.register_message_handler(ping_ip_get, state=states_bot.ping_state)
    dp.register_message_handler(out_ip, Text(equals='Проверка IP'))
    dp.register_message_handler(get_ip, state=states_bot.ip_state)
    dp.register_message_handler(get_time, Text(equals='Точное время'))
    dp.register_message_handler(out_weather, Text(equals='Погода'))
    dp.register_message_handler(get_weather, state=states_bot.weather_state)

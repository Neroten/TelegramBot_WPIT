from aiogram import executor, types
from TelegramBot_Loader import dp
import handlers

async def start_tgbot(_):
    print('TelegramBot запущен')

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Проверка IP', 'Точное время', 'Погода', 'Ping IP']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Выберите категорию', reply_markup=keyboard)

handlers.register_handlers(dp)

executor.start_polling(dp, on_startup=start_tgbot)
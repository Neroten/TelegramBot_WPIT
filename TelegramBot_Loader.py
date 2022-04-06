from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from data import token_bot

storage = MemoryStorage()

bot = Bot(token=token_bot)
dp = Dispatcher(bot, storage=storage)

class states_bot(StatesGroup):
    ip_state = State()
    weather_state = State()
    time_state = State()
    ping_state = State()
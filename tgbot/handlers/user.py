from aiogram import Dispatcher
from aiogram.types import Message
from ..keyboards.default.static_menu import static_keyboard

async def user_start(message: Message):
    await message.answer(f"Witaj, {message.chat.first_name}", reply_markup = static_keyboard)
    print(message)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
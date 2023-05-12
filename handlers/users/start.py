import logging
from aiogram import types
from data.config import CHANNELS
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from loader import bot, dp
from data.config import CHANNELS
from utils.misc import subscription
from api import *
# Start Command
@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message):
    user = message.from_user.id
    create_user(telegram_id=user,name=message.from_user.full_name)
    btn = InlineKeyboardMarkup(row_width=1)
    status = await subscription.check(user_id=user,
                                          channel=CHANNELS[0])
    if status:
        file = open('static/math.mp4', 'rb')
        await message.answer_animation(animation=file,caption='Testni boshlaymizmi?!')
        await message.answer(f"<b>Assalomu alaykum {message.from_user.full_name} botimizga xush kelibsiz!</b>\n"
                             f"<i>Test ishlash uchun /test buyrug'ini bosing!</i>\n\n\n"
                             f"<b><u>Muammo bo'lsa /info buyrug'idan kerakli malumotni bilib oling</u></b>")
    else:
        btn.add(InlineKeyboardButton(text="🧑‍💻 Admin",url="https://t.me/Bekhzod_Asliddinov"))
        await message.answer("<b>Sizga loyihamizga obuna bo'lmagansiz.</b>"
                         
                             "<b>Botdan foydalanish uchun Admin bilan bog'laning:</b>",reply_markup=btn)


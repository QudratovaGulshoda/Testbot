from loader import dp
from aiogram import types
import asyncio
from api import results_of_test
from telegraph.aio import Telegraph
async def create_mypage(data,title):
    telegraph = Telegraph()
    await telegraph.create_account(short_name='1337')
    response = await telegraph.create_page(
        title=title,
        html_content=data,
    )
    return response['url']

@dp.message_handler(commands='info')
async def test(message:types.Message):
    await message.answer(f"<b>Test tekshirishda agar tugmalar orqali belgilaganda muammo chiqsa,Yozma holda kiriting!</b>\n"
                         f"🧑‍💻 <i>Admin bilan bog'lanish uchun:</i> @ChatAdminMybot")
@dp.message_handler(commands='results')
async def test(message:types.Message):
    await message.answer_chat_action(action=types.ChatActions.TYPING)
    user  = message.from_user.id
    data = results_of_test(telegram_id=user)
    if data==[]:
        info = await create_mypage(title=f"{message.from_user.full_name} ning jami natijalari!",data="<p>Siz hali test ishlamapsiz😔😔😔</p>")
        await message.answer(f"Malumotni <a href='{info}'>ushbu</a> havola orqali olishingiz mumkin!")
    else:
        text = ''
        for i in data:
            text+=f"<p>Test kodi: <b>{i['test_code']}</b>.✅ To'g'ri javoblar: <b>{i['true_answers']}</b>.❌ Xato javoblar: <b>{i['false_answers']}</b>.🕐 Bajarilgan vaqt: <b>{i['date']}</b></p>"
        info = await create_mypage(title=f"{message.from_user.full_name} ning jami natijalari!",
                             data=text)
        await message.answer(f"Malumotni <a href='{info}'>ushbu</a> havola orqali olishingiz mumkin!")



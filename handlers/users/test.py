# File for get test and check test
from loader import dp,bot
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command, Text
from keyboards.default.buttons import *
from api import *
from checktest import *
from environs import Env
env =Env()
env.read_env()
url= env.str('MEDIA_URL')
file_url = 'https://bigbookuz.pythonanywhere.com/media/book-files/Xolid_Husayniy_Shamol_ortidan_yugurib.pdf'
from aiogram.dispatcher import FSMContext
# Command for get test(category)
@dp.message_handler(Command('test'))
async def test(message:types.Message):
    telegram_id = message.from_user.id
    daily_test = dailytest(telegram_id=telegram_id)
    if daily_test==400:
        await message.answer("Sizga kunlik jami <b>3</b> ta test test beriladi!\n"
                             "Siz limitdan foydalanib bo'ldiz!")
    else:
        await message.answer("Qaysi kategoriya bo'lim bo'yicha test ishlamoqchimisiz?Tanlang!",reply_markup=button_category())
# filter for category
@dp.callback_query_handler(category_callback.filter())
async def chooose_test(call:types.CallbackQuery,callback_data:dict,state:FSMContext):
    telegram_id = call.from_user.id
    category  = callback_data['choose']
    info = get_test(category=category,telegram_id=telegram_id)
    await call.answer("Tayyorlanmoqda")
    if info=='404':
        await call.message.answer("😐 Uzr bu kategoriya bo'yicha test endi tayyorlanmoqda!\n"
                                  "Yoki bu kategoriyadagi barcha testlarni ishlagansiz!")
        await call.message.delete()
    else:
        black = '◼️'
        white = '◻️'
        xabar = await bot.send_message(chat_id=call.from_user.id,text=10*white)
        for i in range(1,11):
            oq = (10-i) * white
            qora = i*black
            await xabar.edit_text(text=f"{qora}{oq}\n"
                                       f"{i*10} % tayyorlandi!")
        await xabar.delete()
        await bot.send_chat_action(chat_id=call.from_user.id,action=types.ChatActions.UPLOAD_DOCUMENT)
        text = f"ℹ️ Test kodi : <b>{info['code']}</b>\n" \
               f"🕐 Test tayyorlangan vaqt : {info['uploaded']}\n" \
               f"🔄 Test o'zgartirilgan vaqt: {info['changed']}\n" \
               f"🔢 Test soni: {len(info['answers'])}\n" \
               f"📌 Kategoriya: {info['category']}\n" \
               f"🗂 Fayl hajmi: {info['filesize']}\n\n\n" \
               f"⚠️ Testni tekshirish uchun Test javoblarni quyidagicha yuboring!\n\n" \
               f"<b>##test_kodi##1a2b3c4d......28d29b30a</b>\n" \
               f"<b>Masalan:##1002##1a2b3c4d......28d29b30a</b>"
        data= {}
        data[info['code']] = info['answers']
        await state.update_data({
            f"test":data
        })
        dailytestcreate(telegram_id=call.from_user.id)
        myfile = types.InputFile.from_url(url=url+info['file'])
        await call.message.answer_document(document=myfile,caption=text,reply_markup=regenarate(test_code=info['code']))
    await call.message.delete()
# Check Answers With Write by Hand
@dp.message_handler(Text(startswith='#'))
async def checkmytest(message:types.Message,state:FSMContext):
    answers= message.text
    stuanswers= checkformat(answers)
    if stuanswers:
        test = stuanswers['test']
        answers = stuanswers['answers']
        data = await state.get_data()
        trueanswers = data.get('test', {})
        trueanswers = trueanswers.get(test,None)
        if trueanswers==None:
            await message.answer('<b>😐 Uzr bu kodli test sizga berilmagan!!</b>')
        else:
           result = check(answers=answers,trueanswers=trueanswers)
           test_done(telegram_id=message.from_user.id,name=message.from_user.full_name,test_code=test,true_answers=result['trues'],false_answers=result['falses'])
           await message.answer(f"<b>‼️ Test kodi: {test}</b>\n\n{result['result']}")
    else:
        await message.answer(error)
# Run After Click "Testni tekshirish"
@dp.callback_query_handler(checkto.filter())
async def test(call:types.CallbackQuery,callback_data:dict,state:FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer("<b>To'g'ri javoblarni belgilang!</b>",reply_markup=checkbuttonpart_1(test_code=callback_data['test_code']))
    await call.message.delete()
# Run When "Orqaga" or "Oldinga"
@dp.callback_query_handler(next_previous.filter())
async def test(call:types.CallbackQuery,callback_data:dict,state:FSMContext):
    action = callback_data['action']
    test_code= callback_data['test_code']
    data = await state.get_data()
    answers = data.get(test_code,None)
    if action=='next':
            await call.message.edit_reply_markup(reply_markup=checkbuttonpart_2(test_code=test_code,answers=answers))
    else:
            await call.message.edit_reply_markup(reply_markup=checkbuttonpart_1(test_code=test_code,answers=answers))
# Select clicked answers
@dp.callback_query_handler(checkcallback.filter())
async def write(call:types.CallbackQuery,callback_data:dict,state:FSMContext):
    await call.answer("Javob qabul qilindi!")
    test_code =callback_data['test_code']
    answer_number=callback_data['answer_number']
    answer =callback_data['answer']
    data = await state.get_data()
    answers = data.get(test_code,{})
    answers[answer_number]=answer
    await state.update_data({
        test_code:answers
    })
    if int(answer_number)<16:
        await call.message.edit_reply_markup(reply_markup=checkbuttonpart_1(test_code=test_code,answers=answers))
    else:
        await call.message.edit_reply_markup(
            reply_markup=checkbuttonpart_2( test_code=test_code, answers=answers))
# Run after click 'Tugatish'
@dp.callback_query_handler(finish_callback.filter())
async def callme(call:types.CallbackQuery,state:FSMContext,callback_data:dict):
    test_code =  callback_data['test_code']
    data = await state.get_data()
    answers = data.get(test_code,None)
    trueanswers = data.get('test', {})
    trueanswers = trueanswers.get(test_code,None)
    if trueanswers is None:
        await call.answer('Javoblar kiritilmagan!')
    if answers is None:
        await call.answer('Javoblar kiritilmagan!')
    else:
        await call.answer(cache_time=60)
        result = check(trueanswers=trueanswers,answers=answers)
        test_done(telegram_id=call.from_user.id, name=call.from_user.full_name, test_code=test_code,
                  true_answers=result['trues'], false_answers=result['falses'])
        await call.message.answer(f"<b>‼️ Test kodi: {test_code}</b>\n\n{result['result']}")
        await state.update_data({
            test_code: {}
        })
        await call.message.delete()

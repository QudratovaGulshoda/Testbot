from api import categories
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
category_callback = CallbackData('ikb','choose')
checkto =CallbackData('ikb2','test_code')
finish_callback=CallbackData('ikb3','test_code')
checkcallback = CallbackData('ikb4','test_code','answer_number','answer')
next_previous = CallbackData('ikb5','action','test_code')
# Button for Category
def button_category():
    btn = InlineKeyboardMarkup()
    all_categories = categories()
    for category in all_categories:
        btn.add(InlineKeyboardButton(text=f"✔️ {category['name']}",callback_data=category_callback.new(choose=category['id'])))
    btn.add(InlineKeyboardButton(text="✔️ Tasodifiy test",callback_data=category_callback.new(choose='random')))
    return btn
# Button for regenarate
def regenarate(test_code):
    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton(text="📝 Testni tekshirish",callback_data=checkto.new(test_code=test_code)))
    return btn
# Buttot for check (1-15)
def checkbuttonpart_1(test_code,answers:dict=None):
    btn = InlineKeyboardMarkup(row_width=5)
    for i in range(1,16):
                if answers is  None:
                    answer=None

                else:
                    answer = answers.get(str(i))
                btn1 = InlineKeyboardButton(text=f"{i}", callback_data='1')
                btn2 = InlineKeyboardButton(text="✅ A" if answer=="A" else "A", callback_data=checkcallback.new(test_code=test_code,answer_number=i,answer="A"))
                btn3 = InlineKeyboardButton(text="✅ B" if answer== "B" else "B",
                                          callback_data=checkcallback.new(test_code=test_code,
                                                                          answer_number=i, answer="B"))
                btn4= InlineKeyboardButton(text="✅ C" if answer=="C" else "C", callback_data=checkcallback.new(test_code=test_code,answer_number=i,answer="C"))
                btn5 = InlineKeyboardButton(text="✅ D" if answer== "D" else "D",
                                          callback_data=checkcallback.new(test_code=test_code,
                                                                          answer_number=i, answer="D"))
                btn.add(btn1,btn2,btn3,btn4,btn5)
    btn.add(InlineKeyboardButton(text="➡️ Oldinga",callback_data=next_previous.new(action='next',test_code=test_code)))
    return btn
# Buttot for check (16-30)
def checkbuttonpart_2(test_code,answers=None):
    btn = InlineKeyboardMarkup(row_width=5)
    for i in range(16,31):
        if answers is None:
            answer = None
        else:
            answer = answers.get(str(i))
        btn1 = InlineKeyboardButton(text=f"{i}", callback_data='1')
        btn2 = InlineKeyboardButton(text="✅ A" if answer == "A" else "A",
                                    callback_data=checkcallback.new(test_code=test_code, answer_number=i, answer="A"))
        btn3 = InlineKeyboardButton(text="✅ B" if answer == "B" else "B",
                                    callback_data=checkcallback.new(test_code=test_code,
                                                                    answer_number=i, answer="B"))
        btn4 = InlineKeyboardButton(text="✅ C" if answer == "C" else "C",
                                    callback_data=checkcallback.new(test_code=test_code, answer_number=i, answer="C"))
        btn5 = InlineKeyboardButton(text="✅ D" if answer == "D" else "D",
                                    callback_data=checkcallback.new(test_code=test_code,
                                                                    answer_number=i, answer="D"))
        btn.add(btn1, btn2, btn3, btn4, btn5)
    btn.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=next_previous.new(action='previous',test_code=test_code)))
    btn.add(InlineKeyboardButton(text="🏁 Tugatish",callback_data=finish_callback.new(test_code=test_code)))
    return btn


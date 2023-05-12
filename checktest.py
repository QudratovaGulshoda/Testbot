import re
error = f"❗️ Xato tartibda kiritdiz!\n" \
                  f"##testkodi##to'g'rijavoblar\n" \
                  f"Misol:\n" \
                  f"##2056##1A2B3C4D5A6B...\n" \
                  f"❗️ <b>Boshqa ko'rinishlar xato hisoblanadi.Iltimos diqqatli bo'ling!</b>"
def gototrueformat(answers):
    keys = re.findall(r'\d+', answers)
    values = re.findall(r'[a-zA-Z]', answers)
    values = [x.upper() for x in values]
    results = {keys[i]: values[i] for i in range(len(keys))}
    return results
def checkformat(answers:str):
    if answers.startswith('##'):
        if answers.count('#')==4:
            try:
                cut = answers.rfind('##') + 2
                javoblar = answers[cut:]
                keys = re.findall(r'\d+', javoblar)
                values = re.findall(r'[a-zA-Z]', javoblar)
                if len(keys) == len(values):
                    data = {}
                    data['test'] =answers[2:answers.rfind('##')]
                    data['answers'] =gototrueformat(answers=javoblar)
                    return data
                else:
                    return False
            except:
                return False
        else:
            return False
    else:
        return False
def check(trueanswers,answers):
    text = ''
    tr=0
    fl = 0
    for i in trueanswers:
        if trueanswers.get(i) == answers.get(i):
            text += f"{i}.<b>{trueanswers.get(i)}</b> ✅\n"
            tr+=1
        else:
            text += f"{i}.{answers.get(i, 'Belgilanmagan')} ❌.To'gri javob: <b>{trueanswers.get(i)}</b> ✅\n"
            fl+=1
    all = tr+fl
    score = tr*100 / all
    score = "{:.2f}".format(score)

    text+='\n\n'+f"✅ To'g'ri javoblar: {tr} ta\n" \
          f"❌ Xato javoblar: {fl} ta\n" \
          f"📈 Ko'rsatkich: {score} %"
    data = {}
    data['result'] = text
    data['trues'] = tr
    data['falses']  = fl
    return data






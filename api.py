import requests
import json
from environs import Env
env = Env()
env.read_env()
BASE_URL=env.str('URL')
# Get Categories
def categories():
    response  = requests.get(url=f"{BASE_URL}/category/")
    rest = json.loads(response.text)
    return rest
# Get Category's Test
def get_test(category=None,telegram_id=None):
    if category:
       response = requests.get(url=f"{BASE_URL}/withcategory/{category}/{telegram_id}/")
       if response.status_code==204:
           rest='404'
       else:
           rest = json.loads(response.text)
    else:
        response = requests.get(url=f"{BASE_URL}/allcategory/")
        if response.status_code == 204:
            rest = '404'
        else:
            rest = json.loads(response.text)
    return rest
# Create user
def create_user(telegram_id,name=None):
    response  = requests.post(url=f"{BASE_URL}/users/",data={'telegram_id':telegram_id,'name':name})
    return response.status_code
# Get all users
def get_users():
    response = requests.get(url=f"{BASE_URL}/users/")
    data =  json.loads(response.text)
    return data
# Test Done Users
def test_done(telegram_id,name,test_code,true_answers,false_answers):
    response = requests.post(url=f"{BASE_URL}/testdone/", data={'telegram_id': telegram_id, 'name': name,'test_code':test_code,'true_answers':true_answers,'false_answers':false_answers})
    return response.status_code
# Users' results
def results_of_test(telegram_id):
    response = requests.get(url=f"{BASE_URL}/testdone/?search={telegram_id}")
    data = json.loads(response.text)
    return data
# Daily Test Status
def dailytest(telegram_id):
    response = requests.get(url=f"{BASE_URL}/daily/{telegram_id}/")
    return response.status_code
# Daily Test Create
def dailytestcreate(telegram_id):
    response = requests.get(url=f"{BASE_URL}/dailycreate/{telegram_id}/")
    return response.status_code


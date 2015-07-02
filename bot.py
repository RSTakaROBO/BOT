# -*- coding: utf-8 -*-

import requests
import json
import datetime
import time


TOKEN = 'your token'


def get_weather(forecast_type):

    if forecast_type != "now" and forecast_type != "day":
        return "nothing"

    r = requests.get('http://pogoda.onliner.by/sdapi/pogoda/api/forecast/26850')
    weather_data = r.json()
    city = weather_data["city"]
    curr_date = weather_data["today"]["date"]

    if forecast_type == "now":
        status = weather_data["now"]["phenomena"]
        curr_temp = weather_data["now"]["temperature"]
        return_string = "В " + city +" сейчас:\n👉 "+ status +"\n🌀 Температура: "+ curr_temp+"°"

    if forecast_type == "day":
        curr_day = weather_data["today"]["date"]
        morning = weather_data["today"]["morning"]["temperature"]
        day = weather_data["today"]["day"]["temperature"]
        evening = weather_data["today"]["evening"]["temperature"]
        night = weather_data["today"]["night"]["temperature"]


        return_string = "В "+city+" "+curr_date+":"+\
        "\n🌅 Утром: "+ morning +"°"+\
        "\n🌇 Днем :"+ day +"°"+\
        "\n🌄 Вечером: "+ evening+"°" +\
        "\n🌃 Ночью:  "+night+"°"

    return return_string


def get_frist_update():
    r = requests.get('https://api.telegram.org/bot'+TOKEN+'/getUpdates', auth=('user', 'pass'))
    data = r.json()
    if len(data["result"]) == 0:
        return 0
    return data["result"][0]["update_id"]

def get_upate(offset):
    r = requests.get('https://api.telegram.org/bot'+TOKEN+'/getUpdates?timeout=20&offset='+ str(offset), auth=('user', 'pass'))
    data = r.json()
    return data

def send_message(user_id, message):
    send_message_url = 'https://api.telegram.org/bot'+TOKEN+'/sendMessage?chat_id=' + str(user_id) + '&text=' + message
    r = requests.post(send_message_url, auth=('user', 'pass'))

def send_keyboard(user_id, message):
    keyboard = "{\"keyboard\":[[\"Погода сейчас\",\"Погода на день\"]],\"resize_keyboard\":false}"
    print(keyboard)
    send_message_url = 'https://api.telegram.org/bot'+TOKEN+'/sendMessage?chat_id=' + str(user_id) + '&text='+ message + '&reply_markup='+ keyboard
    r = requests.post(send_message_url, auth=('user', 'pass'))

offset = get_frist_update()

while True:

    update = get_upate(offset+1)
    if len(update["result"]) == 0:
        print("no action..."+str(datetime.datetime.now()))
        continue
    for x in range(0, len(update["result"])):
        user_id = update["result"][x]["message"]["from"]["id"]
        user_name = update["result"][x]["message"]["from"]["first_name"]
        user_message = update["result"][x]["message"]["text"].lower()
        message_to_send = ""


        if user_message == 'погода сейчас':
            print ("sending message to",user_name)
            send_message(user_id,get_weather("now"))
            continue
        if user_message == 'погода на день':
            print ("sending message to",user_name)
            send_message(user_id,get_weather("day"))
            continue
        if user_message == 'спасибо':
            print ("sending message to",user_name)
            send_message(user_id,"Пожалуйста ,"+user_name+"! :)")
            continue
        if user_message == '/start':
            print ("sending message to",user_name)
            send_keyboard(user_id,"Добро пожаловать!")
            continue
        print ("sending message to",user_name)
        send_keyboard(user_id,"Нет такой команды!")

    offset = update["result"][len(update["result"])-1]["update_id"]
    time.sleep(1)

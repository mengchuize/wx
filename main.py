from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

event_list = [["和闺蜜出门","2022年8月24日"]]

weather_list = [["冰冰！今天有雨噢，出门记着打伞！"],
                ["今天天气不错噢！冰冰有打算出门嘛！"]]

temputer_list = [["今天温度很高哦，出门记着防晒！"],
                 ["今天温度还可以，可以出门逛逛！"],
                 ["今天会很冷哦，出门要多穿衣服！"]]

days_list = ["昨晚有没有想我？",
             "想我记得找我聊天哦！",
             "有空记得给我打电话哦！",
             "我想听你唱歌呐！"]

def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])

def get_knowdays():

    next = datetime.strptime(start_date, "%Y-%m-%d")

    return (today - next).days + 1

def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    if len(words) >20:
        return get_words()
    return words.json()['data']['text']

def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

def combineTips(today_str,weather,temputer,days_str):
    
    tips_str = "锤锤的Tips\n"
    e_tips = "今天没有要紧的事情哦！好好休息一下吧！"
    w_tips = "0"
    t_tips = "0"
    d_tips = "0"
    
    for event in event_list:
        if str(event[1]) == str(today_str):
            e_tips = "别忘了今天要[" + event[0] + "]哦！"
    
    if "雨" in weather_str:
        w_tips = "·" + weather_list[0][random.randint(0,len(weather_list[0])-1)]
    else:
        w_tips = "·" + weather_list[1][random.randint(0,len(weather_list[1])-1)]

    if temputer_str > 30:
        t_tips = "·" + temputer_list[0][random.randint(0,len(temputer_list[0])-1)]
    elif temputer_str < 15:
        t_tips = "·" + temputer_list[2][random.randint(0,len(temputer_list[2])-1)]
    else:
        t_tips = "·" + temputer_list[1][random.randint(0,len(temputer_list[1])-1)] 

    d_tips = "·" + "我们已经认识" + str(days_str) + "天了，" + days_list[random.randint(0,len(days_list)-1)] 
    
    return [tips_str, e_tips, w_tips, t_tips, d_tips]

today_str =  str(today.year) + "年" + str(today.month) + "月" + str(today.day) + "日"
weather_str, temputer_str = get_weather()
days_str = get_knowdays()
tips = combineTips(today_str,weather_str,temputer_str,days_str)
words = get_words()
copyright_str = "[这里的信息仅你可见]"

data = {"time":{"value":today_str,"color":"#C0C0C0"},
        "weather":{"value":weather_str},
        "temputer":{"value":temputer_str},
        "days":{"value":days_str},
        "tips_str":{"value":tips[0],"color":"#F08080"},
        "e_tips":{"value":tips[1]},
        "w_tips":{"value":tips[2]},
        "t_tips":{"value":tips[3]},
        "d_tips":{"value":tips[4]},
        "words":{"value":words,"color":get_random_color()},
        "copyright":{"value":copyright_str,"color":"#F08080"}}
  
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

res = wm.send_template(user_id, template_id, data)

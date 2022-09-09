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

event_list = [["和姐妹吃火锅","2022年9月4日"]]

weather_list = [["冰冰！今天有雨噢，出门记着打伞！","要下雨啦！冰冰还是待在家和锤锤聊天吧！","下雨了天气凉，冰冰出门穿好衣服！"],
                ["今天天气不错噢！冰冰有打算出门嘛！","今天是个好天气呐，心情有没有更愉悦呢？","这么好的天气，不给锤锤看看天空的云嘛？"]]

temputer_list = [["今天温度很高哦，出门记着防晒！","今天超热的，冰冰乖乖待在家里吧！","这么热，冰冰又该出很多汗了吧！"],
                 ["今天温度还可以，可以出门逛逛！"],
                 ["今天会很冷哦，出门要多穿衣服！"]]

# days_list = ["“陪你把沿路感想活出了答案，陪你把独自孤单变成了勇敢...”",
#             "“等到风景都看透，也许你会陪我看细水长流。”"]

# days_list = ["“在所有人事已非的景色里，我最喜欢你。”"]
days_list = ["冰冰中秋节快乐~💗💗💗遇见你，从此凛冬散尽，星河长明。"]
def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['low']), math.floor(weather['high'])

def get_knowdays():

    next = datetime.strptime(start_date, "%Y-%m-%d")

    return (today - next).days + 1

def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']

def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

def combineTips(today_str,weather,temputer,days_str):
    
    tips_str = "锤锤的Tips🥰\n"
    e_tips = "·📆今天没有要紧的事情哦！那就多陪陪锤锤吧！"
    w_tips = "0"
    t_tips = "0"
    d_tips = "0"
    
    for event in event_list:
        if str(event[1]) == str(today_str):
            e_tips = "·📆别忘了今天要[" + event[0] + "]哦！"
    
    if "雨" in weather_str:
        w_tips = "·💧" + weather_list[0][random.randint(0,len(weather_list[0])-1)]
    else:
        w_tips = "·🌞" + weather_list[1][random.randint(0,len(weather_list[1])-1)]

    if temputer > 30:
        t_tips = "·🔥" + temputer_list[0][random.randint(0,len(temputer_list[0])-1)]
    elif temputer < 22:
        t_tips = "·🥶" + temputer_list[2][random.randint(0,len(temputer_list[2])-1)]
    else:
        t_tips = "·🌈" + temputer_list[1][random.randint(0,len(temputer_list[1])-1)] 

    d_tips = "·💕我们已经认识" + str(days_str) + "天了。" + days_list[random.randint(0,len(days_list)-1)] 
    
    return [tips_str, e_tips, w_tips, t_tips, d_tips]

today_str =  str(today.year) + "年" + str(today.month) + "月" + str(today.day) + "日"
weather_str, temputer_min_str, temputer_max_str = get_weather()
days_str = get_knowdays()
tips = combineTips(today_str,weather_str,temputer_max_str,days_str)
words = "“"  + get_words() + "”"
# copyright_str = "[这里的信息仅你可见]"
copyright_str = "[🧡冰冰专属信息🧡]"

data = {"time":{"value":today_str,"color":"#C0C0C0"},
        "weather":{"value":weather_str},
        "temputer":{"value":str(temputer_min_str) + "℃ - " + str(temputer_max_str) + "℃"},
        "days":{"value":str(days_str) + "天"},
        "tips_str":{"value":tips[0],"color":"#F08080"},
        "e_tips":{"value":tips[1]},
        "w_tips":{"value":tips[2]},
        "t_tips":{"value":tips[3]},
        "d_tips":{"value":tips[4]},
        "words":{"value":words},
        "copyright":{"value":copyright_str}}
  
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

res = wm.send_template(user_id, template_id, data)

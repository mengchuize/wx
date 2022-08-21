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

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_days():
  next = birthday
  next = datetime.strptime(birthday, "%Y-%m-%d")

  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

today_str =  str(today.year) + "年" + str(today.month) + "月" + str(today.day) + "日"
weather_str, temputer_str = get_weather()
days_str = get_days()
copyright_str = "[这里的信息仅你可见]"
others1_str = ""
others2_str = get_words()

if "雨" in weather_str:
  others1_str = others1_str + "冰冰！今天有雨噢，出门记着打伞！"
else:
  others1_str = others1_str + "今天天气不错噢！冰冰有打算出门嘛！"
  
if temputer_str > 30:
  others1_str = others1_str + "今天温度很高哦，出门记着防晒！"
else:
  others1_str = others1_str + "今天温度还可以，可以出门逛逛！"

others1_str = others1_str + "我们已经认识" + str(days_str) + "天了，昨晚有没有想我？我相信我们还会相伴更久！"
  
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)

data = {"time":{"value":today_str,"color":"#C0C0C0"},
        "weather":{"value":weather_str},
        "temputer":{"value":temputer_str},
        "days":{"value":days_str},
        "others1":{"value":others1_str},
        "others2":{"value":others2_str},
        "copyright":{"value":copyright_str,"color":"#F08080"}}

res = wm.send_template(user_id, template_id, data)

import os 
import sqlite3
import random
from utils.get_weather import *
from utils.string_utils import *

def get_weather_by_city(name):
    area_id = get_area_id(name)
    if area_id is None:
        return None, None, None, None
    dates, win_level, low_temperature, high_temperature, weather = get_weather(area_id)
    return win_level, low_temperature, high_temperature, weather    

def get_number(string):
    regex = re.compile('([0-9]+)')
    return int(regex.findall(string)[0])

def handle_weather(bot, context):
    if context['message'][:4] == '秋菜酱，':
        print('command prefix received')
        if context['message'][4:11] == 'weather':
            print('weather command received')
            msg = context['message'][11:]
            msg = msg.split(' ')
            msg = [w.replace(' ', '') for w in msg]
            msg = [w for w in msg if w != ' ' and w != '']

            if len(msg) == 0:
                name = ''
                name = '合肥'
            else:
                name = msg[0]

            win_level, low_temperature, high_temperature, weather = get_weather_by_city(name)
            if win_level is None:
                bot.send(context, '暂不支持查询该城市的天气')
                return True
            info = '今天{}最高温度为{}，最低温度为{}，风级{}，天气：{}'.format(name, high_temperature, low_temperature, win_level, weather)

            if get_number(high_temperature) > 29:
                info += '\n白天较热，请注意防暑降温'
            if get_number(low_temperature) < 16:
                info += '\n早晚温度较低，请注意保暖'
            if get_number(win_level) > 7:
                info += '\n今日的风儿甚是喧嚣，请小心被吹飞，注意树枝等可能的掉落物'
            if '雨' in weather or '雪' in weather:
                info += '\n雨雪天气请记得带伞，小心防滑'

            bot.send(context, info)
            return True
    
    return False

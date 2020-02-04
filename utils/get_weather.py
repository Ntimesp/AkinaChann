import requests
from bs4 import BeautifulSoup
import re
from pypinyin import lazy_pinyin
import os
import json

f = open(os.path.join('.', 'json', 'city.json'), 'r')
area_data = json.load(f)
f.close()

def get_area_id(name):
    if name == '':
        return '101220101'
    pyin = ''.join(lazy_pinyin(name))
    for item in area_data:
        if item['cityEn'] == pyin:
            return item['id']
    return None

    
'''
get_area_id = {
    '' : '101220101',
    '合肥' : '101220101', 
    '北京' : '101010100'
}
'''

def get_weather(area_id=101220101):
    resp = requests.get('http://www.weather.com.cn/weather/{}.shtml'.format(area_id)).text.encode('iso-8859-1').decode()
    soup = BeautifulSoup(resp,'html.parser')
    tagDate=soup.find('ul', class_="t clearfix")
    dates = tagDate.h1.string

    tagToday = soup.find('p', class_="tem")
    try:
        high_temperature = tagToday.span.string
    except AttributeError as e:
        high_temperature = tagToday.find_next('p', class_="tem").span.string

    low_temperature = tagToday.i.string
    weather = soup.find('p', class_="wea").string

    tagWind = soup.find('p',class_="win")
    win_level = tagWind.i.string

    return dates, win_level, low_temperature, high_temperature, weather


if __name__ == '__main__':
    dates, win_level, low_temperature, high_temperature, weather = get_weather()
    print('今天是：' + dates)
    print('风级：' + win_level)
    print('最低温度：' + low_temperature)
    print('最高温度：' + high_temperature)
    print('天气：' + weather)
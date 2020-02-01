import os 
import sqlite3
import random
from utils.string_utils import *
from user.user import *

image_folder_path = 'D:\\DWX-College\\language\\front\\coolQ\\CQP\\酷Q Pro\\data\\image\\imgs'
file_list = [os.path.join('imgs', o) for o in os.listdir(image_folder_path)]
max_index = len(file_list) - 1
def handle_image(bot, context):
    if context['message'][:4] == '秋菜酱，':
        print('command prefix received')
        if context['message'][4:9] == 'image':
            print('image command received')

            record = get_user_cmd_info(context['sender']['user_id'])
            user_info = get_user_info(context['sender']['user_id'])
            if user_info[2] < 2:
                bot.send(context, '权限不足')
                return False
            
            if record[1] == 0:
                if user_info[2] <= 2:
                    bot.send(context, '调用次数已达上限')
                    return False
            
            image_cmd_used(context['sender']['user_id'])
            
            _id = random.randint(0, max_index)
            msg = '[CQ:image,file={}]'.format(file_list[_id])
            
            bot.send(context, msg)
            return True
    return False

import os
import sqlite3
from utils.arg_parser import flag, parser
from user.user import *
from cqhttp import CQHttp 
import random
from commands.teach import *
from commands.answer import *
from user.user import *
from user.user_group import * 

def parse_group(string, group_id, user_id):
    authority_flag = flag('a', 'authority', 1, ['authority'], if_force_num=True)
    group_parser = parser(header_flag=None, flags_list=[authority_flag]) 
    result = group_parser.parse_args(string)

    if isinstance(result, str):
        return result
    
    result['group_id'] = group_id
    result['user_id'] = user_id
    return result

def handle_group(bot, context):
    if context['message'][:4] == '秋菜酱，':
        print('command prefix received')
        if context['message'][4:10] == 'group ':
            print('group command received')
            args = parse_group(context['message'][10:], context['group_id'], context['sender']['user_id'])
            status, content = group(args)
            if status == 'authority':
                bot.send(context, '群权限已修改为' + content)
                return True
            elif status == 'err':
                if content == 'argument':
                    bot.send(context, '参数错误')
                elif content == 'low_authority':
                    bot.send(context, '权限不足')
                else:
                    bot.send(context, 'err')
                return True
            else:
                bot.send(context, '未知错误')
                return True
            
            return True
    
    return False

def group(args):
    if args['authority'] is not None:
        if get_user_info(args['user_id'])[2] < 3:
            return 'err', 'low_authority'
        try:
            args['authority'] = int(args['authority'])
            if args['authority'] < 0:
                return 'err', 'argument'
        except:
            return 'err', 'argument'
        
        lib = sqlite3.connect(os.path.join('database', 'data.db'))

        cursor = lib.cursor()

        cursor.execute('UPDATE user_group SET authority=? WHERE group_id=?', (args['authority'], args['group_id']))

        lib.commit()
        lib.close()
        return 'authority', str(args['authority'])
    
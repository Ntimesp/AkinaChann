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

def handle_info(bot, context):
    msg = context['message'].replace(' ', '')
    if msg != '我的信息' and msg != '本群信息':
        return False
    
    if msg == '本群信息':
        record = get_user_group_info(context['group_id'])
        bot.send(context, '本群信息\n群号：%s\n权限：%s' % (record[0], record[2]))
        return True

    record = get_user_info(context['sender']['user_id'])
    cmd_record = get_user_cmd_info(context['sender']['user_id'])
    bot.send(context, '你的信息\n称呼：%s\n权限：%s\nimage命令调用次数：%d' % (record[1], record[2], cmd_record[1]))
    

    return True
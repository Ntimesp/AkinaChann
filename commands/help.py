import os
import sqlite3
from utils.arg_parser import flag, parser
from user.user import *
from cqhttp import CQHttp 
import random
from commands.teach import *
from commands.answer import *
from user.user import *

def show_doc(bot, context, docname):
    print('docname: ', docname)
    filename = os.path.join('.', 'docs', docname + '.txt')
    print('filename: ', filename)
    if not os.path.exists(filename):
        bot.send(context, '未找到该指令')
        return 
    
    f = open(filename, 'r')
    reply = ''
    for line in f:
        reply += line
    bot.send(context, reply) 

def handle_help(bot, context):
    if context['message'][:4] == '秋菜酱，':
        print('command prefix received')
        if context['message'][4:9] == 'help ':
            print('help command received')
            msg = context['message'][9:]
            msg = msg.split(' ')
            msg = [w.replace(' ', '') for w in msg]
            msg = [w for w in msg if w != ' ' and w != '']
            if len(msg) == 0:
                # show help doc 
                # will be updated next time
                return False
            
            docname = msg[0]
            show_doc(bot, context, docname)
            return True
    
    return False
            

            

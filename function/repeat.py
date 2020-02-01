from cqhttp import CQHttp 
import random
from commands.teach import *
from commands.answer import *
from user.user import *
from user.user_group import *
from commands.info import *
from commands.commands import *


def handle_repeat(bot, context, repeat_prob):
    repeat_forbidden_list = ["我的图鉴"]
    if random.random() > repeat_prob:
        return False
    
    msg = context['message']
    if msg in repeat_forbidden_list:
        return False
    
    if '\n' in msg:
        return False
    
    bot.send(context, msg)
    return True

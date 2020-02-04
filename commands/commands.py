from cqhttp import CQHttp 
import random
from commands.teach import *
from commands.answer import *
from user.user import *
from commands.info import *
from commands.help import *
from commands.group import *
from commands.weather import *
#from commands.image import *

def handle_reply(bot, context):
    reply = answer(context['message'], context['sender']['nickname'], context['group_id'])
    if reply != False:
        bot.send(context, reply)
        return True
    return False


def handle_commands(bot, context):
    if handle_reply(bot, context):
        return True

    if handle_help(bot, context):
        return True
    
    if handle_group(bot, context):
        return True
    
    if handle_teach(bot, context):
        return True

    if handle_info(bot, context):
        return True
    
    if handle_weather(bot, context):
        return True
    
    # if handle_image(bot, context):
    #     return True
    
    return False
from cqhttp import CQHttp 
import random
from commands.teach import *
from commands.answer import *
from user.user import *
from user.user_group import *
from commands.info import *
from commands.commands import *
from function.repeat import *

bot = CQHttp(api_root='http://127.0.0.1:5700')

repeat_prob = 0.05

@bot.on_message()
def handle_msg(context):
    # show context in console
    print(context)

    # detect user
    
    detect_user_group(context['group_id'])
    detect_user(context['sender']['user_id'], context['group_id'])

    # handle commands
    if handle_commands(bot, context):
        return 

    # handle repeat
    if handle_repeat(bot, context, repeat_prob):
        return 

# checkdate()
bot.run(host='0.0.0.0', port=8080)
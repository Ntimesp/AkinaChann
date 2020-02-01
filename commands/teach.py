import os
import sqlite3
from utils.arg_parser import flag, parser
from user.user import *
from cqhttp import CQHttp 
import random
from commands.teach import *
from commands.answer import *
from user.user import *

def handle_teach(bot, context):
    if context['message'][:4] == '秋菜酱，':
        print('command prefix received')
        if context['message'][4:9] == 'teach':
            print('teach command received')
            args = parse_teach(context['message'][9:], context['sender'])
            print(args)
            if isinstance(args, str):
                if args == 'unknown_flags_or_too_many_arguments':
                    bot.send(context, '未知命令或参数过多')
                    return True
                bot.send(context, 'err info: ' + args)
                return True 
            else:
                cmdtype, content = teach(args, context['sender'], context['group_id'])
                if cmdtype == 'add':
                    bot.send(context, '问答已添加。问答编号为' + str(content))
                    return True
                elif cmdtype == 'err':
                    if content == 'already_exists':
                        bot.send(context, '问答已存在')
                        return True
                    if content == 'low_authority':
                        bot.send(context, '权限不足')
                        return True 
                    if content == 'no_QA':
                        bot.send(context, '问答未找到')
                        return True
                    if content == 'too_few_arguments':
                        bot.send(context, '参数过少')
                        return True
                    bot.send(context, '参数错误')
                    return True
                elif cmdtype == 'query':
                    if len(content):
                        bot.send(context, '相关问答如下：\n' + query_format_string(content))
                    return True
                elif cmdtype == 'delete':
                    bot.send(context, '问答已删除')
                    return True
                elif cmdtype == 'update':
                    bot.send(context, '编号为' + str(content) + '的问题已更新。')
    
    return False

def parse_teach(string, sender):
    header_flag = flag(None, None, 2, ['question', 'answer'], if_force_num=False)
    delete_flag = flag('d', 'delete', 1, ['delete'], if_force_num=True)
    query_flag = flag('q', 'query', 1, ['query'], if_force_num=True)
    global_flag = flag('g', 'global', 0, ['global'], if_force_num=True)
    update_flag = flag('u', 'update', 1, ['update'], if_force_num=True)
    teach_parser = parser(header_flag=header_flag, flags_list=[delete_flag, query_flag, global_flag, update_flag])  
    result = teach_parser.parse_args(string)

    if isinstance(result, str):
        return result
    
    result['sender'] = sender['user_id']
    return result

def teach(args, sender, group_id):
    lib = sqlite3.connect(os.path.join('database', 'data.db'))
    
    cursor = lib.cursor()

    if args['question'] is not None:
        if args['answer'] is not None:
            # add question and answer and return the code
            if args['global'] is not None:
                if get_user_info(sender['user_id'])[2] < 3:
                    lib.close()
                    return 'err', 'low_authority'
                
                exists = cursor.execute('SELECT * FROM teach where question=? AND answer=?', (args['question'], args['answer'])).fetchall()

                if len(exists):
                    lib.close()
                    return 'err', 'already_exists' # already exists
                cursor.execute('INSERT INTO teach VALUES(?, ?, ?, ?)', (args['question'], args['answer'], args['sender'], 'global'))
                index = cursor.lastrowid
                print(index)
                lib.commit()
                lib.close()
            else:
                exists = cursor.execute('SELECT * FROM teach WHERE question=? AND answer=? AND (env=? OR env=?)', (args['question'], args['answer'], group_id, 'global')).fetchall()
                if len(exists):
                    lib.close()
                    return 'err', 'already_exists' # already exists
                cursor.execute('INSERT INTO teach VALUES(?, ?, ?, ?)', (args['question'], args['answer'], args['sender'], group_id))
                index = cursor.lastrowid
                print(index)
                lib.commit()
                lib.close()
            
            return 'add', index
        else:
            if args['update'] is not None:
                new_answer = args['question']
                if get_user_info(sender['user_id'])[2] >= 3:
                    exists = cursor.execute('SELECT * FROM teach WHERE rowid=?', (args['update'],)).fetchall()
                else:
                    exists = cursor.execute('SELECT * FROM teach WHERE rowid=? AND author=?', (args['update'], sender['user_id'])).fetchall()
                if not len(exists):
                    lib.close()
                    return 'err', 'no_QA'
                
                cursor.execute('UPDATE teach SET answer=? WHERE rowid=?', (new_answer, args['update']))
                lib.commit()
                lib.close()
                return 'update', args['update']
                

            lib.close()
            return 'err', 'too_few_arguments' # too few argument 
    else:
        if args['answer'] is not None:
            lib.close()
            return 'err', 'too_few_arguments' # too few argument
    
    if args['delete'] is not None:
        if get_user_info(sender['user_id'])[2] >= 3:
            exists = cursor.execute('SELECT * FROM teach where rowid=?', (args['delete'],)).fetchall()
            if not len(exists):
                lib.close()
                return 'err', 'no_QA'
            cursor.execute('DELETE FROM teach WHERE rowid=?', (args['delete'],))
            lib.commit()
            lib.close()
            # delete answer and return
            return 'delete', args['delete']
        else:
            return 'err', 'low_authority'
    
    if args['query'] is not None:
        records = cursor.execute('SELECT rowid, question, answer FROM teach WHERE question=? OR answer=?', (args['query'], args['query'])).fetchall()

        if not len(records):
            lib.close()
            return 'err', 'no_QA'

        lib.close()
        return 'query', records
        # query and return 

def query_format_string(list):
    ret = ''
    for record in list:
        id, q, a = record[0], record[1], record[2]
        ret += (str(id) + '.' + '问题：' + record[1] + ';  ' + '回答：' + record[2] + '\n')
    return ret

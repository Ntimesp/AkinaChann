

def handle_teach(bot, context):
    if context['message'][:4] == '秋菜酱，':
        print('command prefix received')
        if context['message'][4:9] == 'test ':
            print('test command received')
            args = parse_teach(context['message'][9:], context['sender'])
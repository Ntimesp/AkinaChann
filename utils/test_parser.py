from arg_parser import flag, parser

header_flag = flag(None, None, 2, ['question', 'answer'], if_force_num=True)
delete_flag = flag('d', 'delete', 1, ['delete'], if_force_num=True)
query_flag = flag('q', 'query', 1, ['query'], if_force_num=True)
teach_parser = parser(header_flag=header_flag, flags_list=[delete_flag, query_flag])

while True:
    string = input('msg:')
    result = teach_parser.parse_args(string)
    print(result)

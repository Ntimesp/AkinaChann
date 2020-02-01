class flag():
    def __init__(self, short_flag, long_flag, args_num, args_name_list, if_force_num):
        self.short_flag = short_flag
        self.long_flag = long_flag
        self.args_num = args_num
        self.args_name_list = args_name_list
        self.if_force_num = if_force_num
        try:
            assert args_num >= 0
            assert args_name_list != []
            assert short_flag is None or len(short_flag) == 1
            assert long_flag != 'header'
        except:
            print('attribute error in class flag')

class parser(): 
    def __init__(self, header_flag=None, flags_list=[]):
        self.header = header_flag
        self.flags = flags_list
    
    def parse_args(self, string):
        args = dict()
        arg_name_list = [name for flag in self.flags for name in flag.args_name_list]
        if self.header is not None:
            arg_name_list += self.header.args_name_list 
        for key in arg_name_list:
            args[key] = None

        args_cnt = 0
        args_num = 0
        if_force_num = None
        if self.header is not None:
            wait_status = 'arg_or_flag'
            flag_status = self.header.args_name_list
            args_num = self.header.args_num
            if_force_num = self.header.if_force_num
        else:
            wait_status = 'flag'
            flag_status = None 
        
        words = string.split(' ')
        words = [word.replace(' ', '') for word in words]
        words = [word for word in words if word != '' and word != ' ']
        
        for word in words:

            if wait_status == 'arg_or_flag' or wait_status == 'flag':
                this_flag = None
                for flag in self.flags:
                    if word == '-' + flag.short_flag:
                        this_flag = flag
                        break
                    elif word == '--' + flag.long_flag:
                        this_flag = flag
                        break
                
                if this_flag is None:
                    if wait_status != 'arg_or_flag':
                        return 'unknown_flags_or_too_many_arguments'
                
                if this_flag is not None:
                    if this_flag.args_num == 0:
                        args[this_flag.args_name_list[0]] = True
                        wait_status = 'flag'
                        continue
                    
                    wait_status = 'arg'
                    flag_status = this_flag.args_name_list
                    args_num = this_flag.args_num
                    if_force_num = this_flag.if_force_num
                    args_cnt = 0
                    continue

            # wait_status == 'arg'
            args[flag_status[args_cnt]] = word 
            args_cnt += 1
            if args_cnt == args_num:
                wait_status = 'flag'
                flag_status = None 
                args_num = None 
                args_cnt = 0
                if_force_num = None
                continue 
            if if_force_num == False:
                wait_status = 'arg_or_flag' 
            else:
                wait_status = 'arg'
        
        return args
        
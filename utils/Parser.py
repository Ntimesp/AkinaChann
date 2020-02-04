import re

def parse_value(string, value_type='str'):
    '''
    parse a value string with the given value type.
    if value_type has some value other than 'string' or 'int', None will be returned.
    '''
    if value_type == 'str':
        return string

    if value_type == 'int':
        for char in string:
            if char > '9' or char < '0':
                return None
        
        return int(string)
    
    return None
    
def split_spaces(string):
    '''
    split the string by one or few spaces
    '''
    if string == '':
        return []
    
    arr = string.split(' ')
    length = len(arr)
    i = 0
    while (i < length):
        if arr[i] == '':
            del arr[i]
            length -= 1
        else:
            i += 1
    return arr


class Flag:
    def __init__(self, long, short, optional=False):
        '''
        A flag or option class in a command.

        long : long term, long='global' means '--global'\n
        short : short term, short='g' means '-g'; if the flag doesn't have a short term, you can just set it to an empty str ''.\n
        optional : whether the flag is optional or not
        '''
        assert len(short) == 1
        self.long = long
        self.short = short 
        self.optional = optional
        self.filled = False
    
    def copy(self):
        return Flag(self.long, self.short, self.optional)
    
    @classmethod
    def create_from_string(cls, string):
        '''
        Create a flag or option class from a pattern string.
        '''
        optional = False
        if string[0] == '[' and string[-1] == ']':
            optional = True
            string = string[1:-1]

        if string[0] == '(' and string[-1] == ')':
            string = string[1:-1]
        
        terms = string.split('|')
        if len(terms) != 1 and len(terms) != 2:
            return
        
        if len(terms) == 1:
            # only long term or short term
            string = string.replace(' ', '')
            if string[:2] == '--':
                # long
                long = string[2:]
                short = ''
            elif string[:1] == '-':
                # short
                short = string[1:]
                long = ''
            else:
                return
        
        if len(terms) == 2:
            # long and short
            long_term = terms[0].replace(' ', '')
            short_term = terms[1].replace(' ', '')
            if long_term[:1] == '-' and short_term[:2] == '--':
                tmp = long_term
                long_term = short_term
                short_term = tmp
            if long_term[:2] == '--' and short_term[:1] == '-':
                # long and short
                long = long_term[2:]
                short = short_term[1:]
            else:
                return

        return cls(long, short, optional)
    
    def fill(self):
        self.filled = True
    
    def is_filled(self):
        return self.filled

class flags_dict:
    def __init__(self):
        self.long_dict = dict()
        self.short_dict = dict()
    
    def add_flag(self, flag):
        if flag.short != '':
            self.short_dict[flag.short] = flag
        if flag.long != '':
            self.long_dict[flag.long] = flag
    
    def copy(self):
        ret = flags_dict()
        if self.long_dict is None:
            ret.long_dict = None
        else:
            ret.long_dict = self.long_dict.copy()
        
        if self.short_dict is None:
            ret.short_dict = None
        else:
            ret.short_dict = self.short_dict.copy()
        
        return ret
        
class ArgPattern:
    def __init__(self, name, pattern):
        '''
        A pattern of a command.

        name : the name of the pattern\n
        pattern : it is a string, expressed the pattern of a command like '[--global | -g] <question:str> <answer:str>'; '[]' means optional flag or argument.; Types of arguments include 'str' and 'int'
        '''
        self.name = name
        self.pattern = pattern
        self.optional_flags = flags_dict()
        self.compulsory_flag = None
        self.optional_arg = None # if there is an optional argument, it will be a dict like ['name':'aaa','type': 'xxx','value': 'xxxxx']
        self.compulsory_args = list() # [['answer', 'str', 'xxxx'], ...]
        # read the pattern
        self.split_into_flags(pattern)


    def split_into_flags(self, pattern):
        '''
        split the pattern string into flags, then set self.optional_flags and compulsory_flags right.
        '''
        opt_flags_ptn = re.compile('\[[^\[\]]*\]')
        cpl_flags_ptn = re.compile('\([^\(\)]*\)')
        opt_arg_ptn = re.compile('\[<[^\[\]<>]*>\]')
        cpl_args_ptn = re.compile('<[^<>]*>')

        opt_arg = opt_arg_ptn.findall(pattern)
        pattern = opt_arg_ptn.sub('', pattern)

        cpl_args = cpl_args_ptn.findall(pattern)
        pattern = cpl_args_ptn.sub('', pattern)

        opt_flags = opt_flags_ptn.findall(pattern)

        cpl_flags = cpl_flags_ptn.findall(pattern)
        pattern = cpl_flags_ptn.sub('', pattern)

        res_flags = split_spaces(pattern)
        cpl_flags += res_flags
        
        for flag in opt_flags:
            self.optional_flags.add_flag(Flag.create_from_string(flag))
        
        assert len(cpl_flags) < 2
        if len(cpl_flags):
            self.compulsory_flag = (Flag.create_from_string(cpl_flags[0]))
        
        for arg in cpl_args:
            words = arg[1:-1].split(':')
            arg_name = words[0].replace(' ', '')
            arg_type = words[1].replace(' ', '')
            assert (arg_type == 'str') or (arg_type == 'int')
            self.compulsory_args.append([arg_name, arg_type, None])
        
        assert len(opt_arg) < 2

        if len(opt_arg):
            words = opt_arg[0][2:-2].split(':')
            arg_name = words[0].replace(' ', '')
            arg_type = words[1].replace(' ', '')
            assert (arg_type == 'str') or (arg_type == 'int')
            self.optional_arg = {'name': arg_name, 'type': arg_type, 'value': None}
        
        return 
    
    def parse(self, string):
        optional_flags = self.optional_flags.copy()
        if self.compulsory_flag is None:
            compulsory_flag = None
        else:
            compulsory_flag = self.compulsory_flag.copy()
        
        if self.optional_arg is None:
            optional_arg = None
        else:
            optional_arg = self.optional_arg.copy()
        compulsory_args = self.compulsory_args.copy()

        filled_args = 0

        # in next update, quotes will be considered in str argument, str like 'a sentence with spaces' will be supported
        words = split_spaces(string)

        for word in words:
            if word[:2] == '--':
                word = word[2:]
                if word in optional_flags.long_dict:
                    optional_flags.long_dict[word].fill()
                    continue
                
                if compulsory_flag is not None and word == compulsory_flag.long:
                    compulsory_flag.fill()
                    continue
                return None

            if word[0] == '-':                    
                word = word[1:]
                # argument
                for char in word:
                    if compulsory_flag is not None and char == compulsory_flag.short:
                        compulsory_flag.fill()
                        continue
                    if char in optional_flags.short_dict:
                        optional_flags.short_dict[char].fill()
                        continue
                    return None
                continue 
            
            if len(compulsory_args) > filled_args:
                compulsory_args[filled_args][2] = parse_value(word, compulsory_args[filled_args][1])
                filled_args += 1
            elif len(compulsory_args) == filled_args and (not optional_arg is None):
                optional_arg['value'] = parse_value(word, optional_arg['type'])
                filled_args += 1
            else:
                return None
        
        result_flags = dict()
        result_args = dict()
        # check if the syntax is correct and return the dict
        if compulsory_flag is not None and not(compulsory_flag.is_filled()):
            return None
        
        if compulsory_flag is not None:
            name = compulsory_flag.long if compulsory_flag.long != '' else compulsory_flag.short
            result_flags[name] = True

        for (name, flag) in optional_flags.long_dict:
            name = name if name != '' else flag.short
            result_flags[name] = flag.is_filled()
        
        for arg in compulsory_args:
            if arg[2] is None:
                return None
            result_args[arg[0]] = arg[2]
        
        if optional_arg is not None and optional_arg['value'] is not None:
            result_args[optional_arg['name']] = optional_arg['value']
        
        return (self.name, result_flags, result_args)
                        
class ArgParser:
    def __init__(self, name):
        '''
        A parser class for a command.\n
        name : the name of the parser. 
        '''
        self.name = name
        self.patterns = []
    
    def add_pattern(self, pattern):
        self.patterns.append(pattern)
    
    def parse(self, string):
        name_len = len(self.name)
        if string[:name_len] != self.name:
            return None
        string = string[name_len:]

        for pattern in self.patterns:
            result = pattern.parse(string)
            if result is not None:
                return result
        
        return None
                

'''
\space; means a space
\\ means a '\'
so examine '\\'first, and then cut the string by '\\', replace ' ' by '\space' in each substring
''' 
def str_convert_esc(string):
    result = ''
    str_list = []
    while (string.find('\\\\') > 0):
        pos = string.find('\\\\')
        str_list.append(string[:pos])
        string = string[pos+2:]
    
    str_list.append(string)

    for string in str_list[:-1]:
        string = string.replace('\\space;', ' ')
        result += string
        result += '\\'

    result += str_list[-1].replace('\\space;', ' ')
    
    return result

    

        

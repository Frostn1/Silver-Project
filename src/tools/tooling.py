def isInteger(number):
    return number.isnumeric()

def isNumber(number):
    return isInteger(number) or (number.count('.') == 1 and
    isInteger(number[:number.index('.')]) and isInteger(number[number.index('.') + 1:]))

def isString(string):
    return string[0] == '\'' and string[-1] == '\'' or string[0] == '"' and string[-1] == '"'
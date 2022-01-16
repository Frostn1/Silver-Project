
SUCCESS = '\033[92m' #LIGHT_GREEN
WARNING = '\033[93m' #YELLOW
FAIL = '\033[91m' #RED
RESET = '\033[0m' #RESET COLOR
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def formatP(color, string):
    print(f"{color}{string}{RESET}", end = '')
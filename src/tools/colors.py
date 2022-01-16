class bcolors:
    SUCCESS = '\033[92m' #LIGHT_GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

def formatP(color, string):
    print(f"{color}{string}{bcolors.RESET}")
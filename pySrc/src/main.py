import sys
import lexer

def checkFile(file_t):
    if file_t[file_t.index(".")+1:] != "si":
        print('error: file extension doesn\'t match\n')
        exit(0)
        

def readFile(file_t):
    try:
        with open(file_t) as srcCode:
            src = srcCode.readlines()
            src = list(map(lambda s: s.strip(), src))
            return ''.join(src)
    except:
        print('error : file doesn\'t exists\n')
        exit(0)
def main(args):
    if len(args) == 0:
        print('error : missing file\n')
        exit(0)
    lexedTerms = lexer.lexer(readFile(args[0]))
    print('lexed :',lexedTerms)
    # print(readFile(args[0]))



if __name__ == '__main__':
    main(sys.argv[1:])
import sys
import lexer
def main(argv : list):
    if len(argv) < 2:
        raise Exception("file error : missing file")
    if argv[1] == "" :
        raise Exception("file error : file path empty")
    with open(argv[1], "r") as fileP:
        if not fileP.readable():
            raise Exception("file error : file not readable")
        fileContent = fileP.read()
        lex = lexer.Lexer(fileContent)
        lex.lexify()

if __name__ == "__main__":
    main(sys.argv)
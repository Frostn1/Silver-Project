import sys
import lexer as _lexer


def main(argv : list):
    if len(argv) < 2:
        raise Exception("file error : missing file")
    if argv[1] == "" :
        raise Exception("file error : file path empty")
    with open(argv[1], "r") as fileP:
        if not fileP.readable():
            raise Exception("file error : file not readable")
        fileContent = fileP.read()
        lex = _lexer.Lexer(fileContent, argv[1])
        lex.lexify()
        # lex.printStructs()
        par = _lexer.Parser()
        par.parse(lex)
        # par.printData()
        ast = _lexer.AST(par)
        ast.semanticAnalysis()
        # ast.printData(ast.data)
        gen = _lexer.GEN(ast)
        gen.generateCode()
if __name__ == "__main__":
    main(sys.argv)
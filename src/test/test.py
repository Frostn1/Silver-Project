import argparse
from src.tools.colors import *
import os.path
from os import path as pathModule
from src.app.link import *
from src.app.lexer import Lexer, Parser, AST, GEN   

SILVER_VERSION = '1.0.0'

class Tester():
    def __init__(self, paths=[]) -> None:
        self.paths = { path : 0 for path in paths }
        self.numOfTests = 0

        # -----------------

        self.passed = 0
        self.failed = 0


    def getDirPaths(self, dirName):
        full_path = []

        for path in os.listdir(dirName):
            full_path.append(os.path.join(dirName, path))
        return full_path


    def checkPaths(self):
        for path in self.paths.keys():
            if pathModule.exists(path):
                print("Path exists")
                self.paths[path] = 1
                if not pathModule.isfile(path):
                    self.paths[path] = 2
        self.numOfTests = len([key for key in self.paths.keys() if self.paths[key]])



    def formatStart(self):
        self.checkPaths()
        formatP(HEADER, f"Running tests for Silver v{SILVER_VERSION}")
        formatP(BOLD, f"\tTotal of {self.numOfTests} test")


    def startTesting(self, paths):
        for path in paths:
            if (path in self.paths.keys() and (self.paths[path] == 2 and self.paths[path])):
                self.startTesting(self.getDirPaths(path))
            else:
                try:
                    print("Current path", path)
                    with open(path, "r") as fileP:
                        if not fileP.readable():
                            raise Exception("file error : file not readable")
                        fileContent = fileP.read()
                        print("CONTENT", fileContent)
                        lex = Lexer(fileContent, path)
                        lex.lexify()
                        lex.printStructs()
                        par = Parser()
                        par.parse(lex)
                        par.printData()
                        ast = AST(par)
                        ast.semanticAnalysis()
                        gen = GEN(ast)
                        gen.generateCode()
                except Exception as e:
                    print("ERROR", e)
                    raise e

class TestCallback(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is None:
            raise ValueError("0 nargs not allowed")
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        tester = Tester(values)
        tester.formatStart()
        tester.startTesting(tester.paths.keys())
        # print('%r %r %r' % (namespace, values, option_string))
        setattr(namespace, self.dest, values)




def main():
    parser = argparse.ArgumentParser(prog='py -m src.test.test')
    parser.add_argument('--test',help='Run test on folders and/or .si files' , nargs='+', action=TestCallback)
    parser.add_argument('--version', action='version', version=f'Silver-Test v{SILVER_VERSION}')
    args = parser.parse_args()
    
if __name__ == "__main__":
    main()
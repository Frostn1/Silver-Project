import argparse
from re import VERBOSE
from src.tools.colors import *
import os.path
from os import path as pathModule
from src.app.lexer import *
import time
from  src.tools.consts import *

parser = argparse.ArgumentParser(prog='py -m src.test.test')
VERBOSE_FLAG = False
FORCE_FLAG = False
TEST_VALUES = []

class Tester():
    def __init__(self, paths=[]) -> None:
        self.paths = { path : 0 for path in paths }
        self.numOfTests = 0

        # -----------------

        self.passed = 0
        self.failed = 0
        self.times = 0

        # -----------------

    def getDirPaths(self, dirName):
        full_path = []

        for path in os.listdir(dirName):
            full_path.append(os.path.join(dirName, path))
        return full_path


    def checkPaths(self):
        for path in self.paths.keys():
            if pathModule.exists(path):
                self.paths[path] = int(path.endswith('.si'))
                if not pathModule.isfile(path):
                    self.paths[path] = 2
        self.numOfTests = len([key for key in self.paths.keys() if self.paths[key]])



    def formatStart(self):
        self.checkPaths()
        formatP(BOLD, f"Running tests for Silver v{SILVER_VERSION}\n")
        formatP(RESET, f"Total of {self.numOfTests} test cases given\n\n")
        self.numOfTests = 0

    def outTest(self, path, status, timeElapsed):

        formatP(BOLD, f"{path} ... ")
        if status == "Passed":
            formatP(SUCCESS, f"{status}")
            self.times += timeElapsed
            self.passed += 1
        else:
            formatP(FAIL, f"{status}")
            self.failed += 1
        formatP(RESET, f"; in %.3fs\n" % timeElapsed)


    def startTesting(self, paths):
        for path in paths:
            if (path in self.paths.keys() and self.paths[path] == 2) or pathModule.isdir(path):
                self.startTesting(self.getDirPaths(path))
            elif path.endswith('si'):
                try:
                    self.numOfTests += 1
                    with open(path, "r") as fileP:
                        if not fileP.readable():
                            raise Exception("file error : file not readable")
                        currentTime = time.time()
                        fileContent = fileP.read()
                        lex = Lexer(fileContent, path)
                        lex.lexify()
                        par = Parser()
                        par.parse(lex)
                        ast = AST(par)
                        ast.semanticAnalysis()
                        gen = GEN(ast)
                        gen.generateCode()

                        self.outTest(path, "Passed", time.time() - currentTime)
                except Exception as msg:
                    self.outTest(path, "Failed", -1)
                    if VERBOSE_FLAG:
                        formatP(RESET, f'\t{msg}\n')


    def cleanFiles(self, paths):
        for path in paths:
            if (path in self.paths.keys() and self.paths[path] == 2) or pathModule.isdir(path):
                self.cleanFiles(self.getDirPaths(path))
            elif not path.endswith('si'):
                os.remove(path)
    
    def endTest(self):
        if not FORCE_FLAG:
            self.cleanFiles(self.paths.keys())
        print()
        formatP(UNDERLINE, "Test ended")

        formatP(RESET, f" - {self.numOfTests} cases\n\n")
        if self.passed:
            formatP(BOLD, f"{self.passed} ")
            formatP(SUCCESS, "Passed ")

        if self.failed:
            formatP(BOLD, f"{self.failed} ")
            formatP(FAIL, "Failed ")
            
        if self.passed:
            formatP(BOLD, "\nAverage time of ")
            formatP(WARNING, "%.3f" % (self.times / (self.passed))) 

    def testValues(values):
        for value in values:
            tester = Tester(value)
            tester.formatStart()
            tester.startTesting(tester.paths.keys())
            tester.endTest()

class TestCallback(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is None:
            raise ValueError("0 nargs not allowed")
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        TEST_VALUES.append(values)  
        setattr(namespace, self.dest, values)
        return
        




def main():
    global VERBOSE_FLAG, FORCE_FLAG
    parser.add_argument('--version', help='Returns the version of the current Silver', action='version', version=f'Silver-Test v{SILVER_VERSION}')
    parser.add_argument('--verbose', help='Outputs failed cases errors inline', action='store_true', default=False)
    parser.add_argument('--force', '-f', help='Forces to keep output files from exports', action='store_true', default=False)
    parser.add_argument('--test',help='Run test on folders and/or .si files' , nargs='+', action=TestCallback)
    args = parser.parse_args()
    VERBOSE_FLAG = args.verbose
    FORCE_FLAG = args.force
    Tester.testValues(TEST_VALUES)
    
if __name__ == "__main__":
    main()

# 

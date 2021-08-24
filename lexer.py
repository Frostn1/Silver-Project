import struct as _struct
import chunk as _chunk
import link as _link
import json

class GEN:
    def __init__(self, ast):
        self.ast = ast
    def generateCode(self):
        for export in self.ast.par.exports:
            if export.exportName == "json":
                self.jsonGEN()
    def jsonGEN(self):
        self.ast.par.filePath = self.ast.par.filePath.strip("\\").strip(".\\")
        fileContent = ""
        with open(self.ast.par.filePath[:self.ast.par.filePath.index(".")]+".json", "w") as fileP:
            if not fileP.writable() :
                raise Exception("gen error : can't create export file")
            else:
                fileContent += '{'
                # fileP.write("{")
                # print("hello", self.ast.data)
                for index,data in enumerate(self.ast.data.keys()):
                    if index > 0:
                        fileContent += ','
                        # fileP.write(',')
                    fileContent += str(data).replace("'",'"')
                    # fileP.write(str(data).replace("'",'"'))
                    fileContent += ':'
                    # fileP.write(":")
                    if isinstance(self.ast.data[data], list):
                        # print(self.ast.data[data][0][1])
                        fileContent += str(self.ast.data[data][0][1]).replace("'",'"')
                        # fileP.write(str(self.ast.data[data][0][1]).replace("'",'"'))
                    else:
                        fileContent += str(self.ast.data[data]).replace("'",'"')
                        # fileP.write(str(self.ast.data[data]).replace("'",'"'))
                # fileP.write("}")
                fileContent += '}'
                fileContent = eval(fileContent)
                json.dump(fileContent, fileP, indent=4)
        print("Opened File")
class AST:
    def __init__(self, par):
        self.data = par.data
        self.par = par
    def semanticAnalysis(self):
        structNames = [i.structName for i in self.par.structs]
        for index, structPair in enumerate(self.par.data["'ano'"]):
            if structPair[0] not in structNames:
                raise Exception("parser error : struct type `"+structPair[0]+"` not expected")
            else:
                self.missingArgs("'ano'", index, structPair)

        for index, key in enumerate(self.par.data.keys()):
            if key != "'ano'":
                # print(key, "->", self.par.data[key])
                if isinstance(self.par.data[key], list):
                    if self.par.data[key][0][0] not in structNames:
                        raise Exception("parser error : struct type `"+structPair[0]+"` not expected")
                    else:
                        self.missingArgs(key, 0, self.par.data[key][0])
        

    def missingArgs(self, address ,index ,pair):
        validStructs = []
        for i in self.par.structs :
            if i.structName == pair[0] : 
                validStructs.append(i)
        currentArgs = validStructs[0].idens
        argsLeft = set(currentArgs) - set(pair[1]) 
        if len(argsLeft):
            callbackValues = []
            for i in self.par.structs :
                if i.structName == pair[0] : 
                    callbackValues = i.callbacks.keys()
            for arg in argsLeft:
                if arg in callbackValues:
                    pass
                    # print("This value has dynamic ->", arg)
                    # TODO : Value Dynamic
                else:
                    self.data[address][index][1][arg] = ""

    def printData(self, data):
        for key in data.keys():
            print(key, " -> ", data[key])
    def functionDynamic(self, values, functionCall):
        '''
        TODO: Create Function Dynamic
        '''
        pass

class Parser:
    def __init__(self):
        self.data = {"'ano'":[]}
        self.exports = []
        self.links = []
    def parse(self, lexer):
        self.filePath = lexer.filePath
        self.structs = lexer.structs
        self.exports = lexer.exports
        self.links = lexer.links
        self.restrcutureData(lexer)
    def restrcutureData(self, lexer):
        for chunk in lexer.chunks:
            for data in chunk.ano:
                if "[" in data:
                    typeName = data[:data.index("[")]
                    if typeName not in [i.structName for i in lexer.structs]:
                        raise Exception("parser error : struct type `"+typeName+"` not expected")
                    else:
                        fields = {}
                        for field in data[data.index("[")+1:data.index("]")].split("|"):
                            fields[field.split("=")[0].strip().strip("'").strip('"')] = field.split("=")[1].strip().strip("'").strip('"')
                        self.data["'ano'"].append((typeName,fields))
            for key in chunk.chunkDict.keys():
                data = chunk.chunkDict[key]
                if "[" in data:
                    typeName = data[:data.index("[")]
                    if typeName not in [i.structName for i in lexer.structs]:
                        raise Exception("parser error : struct type `"+typeName+"` not expected")
                    else:
                        fields = {}
                        self.data[key.strip().strip('"')] = []
                        for field in data[data.index("[")+1:data.index("]")].split("|"):
                            fields[field.split("=")[0].strip().strip('"')] = field.split("=")[1].strip().strip("'").strip('"')
                        self.data[key.strip().strip('"')].append((typeName,fields))
                else:
                    self.data[key.strip().strip('"')] = data
                # print(key," -> ",  chunk.chunkDict[key])
    
    def printData(self):
        for key in self.data.keys():
            print(key, " -> ", self.data[key])

    def printStructs(self):
        for struct in self.structs:
            print("[Name]", struct.structName)
            print("[Idens] =>")
            for iden in struct.idens:
                print("\t",iden, end="")
                if iden in struct.callbacks.keys():
                    print(" => [Callback]")
                    print("\t[Func Name]", struct.callbacks[iden].name)
                    print("\t[Func Args] =>")
                    for arg in struct.callbacks[iden].args:
                        print("\t\t",arg)
                else:
                    print()
class Lexer:
    def __init__(self, content, filePath):
        self.filePath = filePath
        self.index = 0
        self.content = content
        self.structs = []
        self.chunks = []
        self.links = []
        self.exports = []
    def lexify(self):
        while self.index < len(self.content):
            if self.content[self.index] == "<":
                self.structs.append(_struct.Struct())
                self.index = self.structs[-1].detectStructs(self.content, self.index)

            elif self.content[self.index] == "{":
                self.chunks.append(_chunk.Chunk())
                self.index = self.chunks[-1].detectData(self.content, self.index)

            elif self.content[self.index] == "(":
                self.links.append(_link.Link())
                self.index = self.links[-1].detectLinks(self.content, self.index)

            elif self.content[self.index] == "#":
                self.exports.append(_link.Export())
                self.index = self.exports[-1].detectExports(self.content, self.index)

            else :
                self.index += 1
            
    def printStructs(self):
        for struct in self.structs:
            print("[Name]", struct.structName)
            print("[Idens] =>")
            for iden in struct.idens:
                print("\t",iden, end="")
                if iden in struct.callbacks.keys():
                    print(" => [Callback]")
                    print("\t[Func Name]", struct.callbacks[iden].name)
                    print("\t[Func Args] =>")
                    for arg in struct.callbacks[iden].args:
                        print("\t\t",arg)
                else:
                    print()
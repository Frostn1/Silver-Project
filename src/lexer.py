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
            elif export.exportName == "raw":
                self.rawGEN()
            elif export.exportName == "yaml":
                self.yamlGEN()
    def jsonGEN(self):
        self.ast.par.filePath = self.ast.par.filePath.strip("\\").strip(".\\")
        fileContent = ""
        if "ano" in self.ast.data.keys() and self.ast.data["ano"] == []:
            self.ast.data.pop("ano")
        with open(self.ast.par.filePath[:self.ast.par.filePath.index(".")]+".json", "w") as fileP:
            if not fileP.writable() :
                raise Exception("gen error : can't create export file")
            else:
                fileContent += '{'
                for index,data in enumerate(self.ast.data.keys()):
                    if index > 0:
                        fileContent += ','
                    fileContent += '"' + str(data) + '"'
                    fileContent += ':'
                    if isinstance(self.ast.data[data], list):
                        length = False
                        if len(self.ast.data[data]) > 1 or len(self.ast.data[data]) == 0:
                            length = True
                            fileContent += '['
                        for index1, section in enumerate(self.ast.data[data]):
                            if index1 > 0:
                                fileContent += ','
                            fileContent += str(section[1]).replace("'",'"')
                        if length:
                            fileContent += ']'
                            length = False
                    else:
                        fileContent += str(self.ast.data[data]).replace("'",'"')
                fileContent += '}'
                fileContent = eval(fileContent)
                json.dump(fileContent, fileP, indent=4)
    def rawGEN(self):
        self.ast.par.filePath = self.ast.par.filePath.strip("\\").strip(".\\")
        fileContent = ""
        if "ano" in self.ast.data.keys() and self.ast.data["ano"] == []:
            self.ast.data.pop("ano")
        with open(self.ast.par.filePath[:self.ast.par.filePath.index(".")]+".txt", "w") as fileP:
            if not fileP.writable() :
                raise Exception("gen error : can't create export file")
            else:
                fileContent += '{\n'
                for index,data in enumerate(self.ast.data.keys()):
                    if index:
                        fileContent += ',\n'
                    fileContent += '\t' + str(data)
                    fileContent += ' : '
                    if isinstance(self.ast.data[data], list):
                        length = False
                        if len(self.ast.data[data]) > 1 or len(self.ast.data[data]) == 0:
                            length = True
                            fileContent += '['
                        for index1, section in enumerate(self.ast.data[data]):
                            if index1:
                                fileContent += ','
                            fileContent += '[ ' + str(list(section[1].values())).replace("'",'').replace('"','')[1:-1] + ' ]'
                        if length:
                            fileContent += ']'
                            length = False
                    else:
                        fileContent += str(self.ast.data[data]).replace("'",'').replace('"','')
                fileContent += '\n}'
                fileP.write(fileContent)
    def yamlGEN(self):
        self.ast.par.filePath = self.ast.par.filePath.strip("\\").strip(".\\")
        fileContent = ""
        if "ano" in self.ast.data.keys() and self.ast.data["ano"] == []:
            self.ast.data.pop("ano")
        with open(self.ast.par.filePath[:self.ast.par.filePath.index(".")]+".yaml", "w") as fileP:
            if not fileP.writable() :
                raise Exception("gen error : can't create export file")
            else:
                if len(self.ast.data.keys()) > 1:
                    fileContent += '- '
                for index,data in enumerate(self.ast.data.keys()):
                    if index:
                        fileContent += '\n- '
                    fileContent += str(data)
                    fileContent += ': '
                    if isinstance(self.ast.data[data], list):
                        length = False
                        if len(self.ast.data[data]) > 1 or len(self.ast.data[data]) == 0:
                            length = True
                            fileContent += '\n    - '
                        for index1, section in enumerate(self.ast.data[data]):
                            if index1:
                                fileContent += '\n    - '
                            fileFormat = "\n    - " + "\n    - ".join([str(i[0]) + ': ' + str(i[1]) for i in section[1].items()])
                            fileContent += fileFormat
                        if length:
                            length = False
                    else:
                        fileContent += str(self.ast.data[data]).replace("'",'').replace('"','')
                fileP.write(fileContent)

class AST:
    def __init__(self, par):
        self.data = par.data
        self.par = par
    def semanticAnalysis(self):
        structNames = [i.structName for i in self.par.structs]
        for index, structPair in enumerate(self.par.data["ano"]):
            if structPair[0] not in structNames:
                raise Exception("parser error : struct type `"+structPair[0]+"` not expected")
            else:
                self.missingArgs("ano", index, structPair)

        for index, key in enumerate(self.par.data.keys()):
            if key != "ano":
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
            addtionalData = []
            for i in self.par.structs :
                if i.structName == pair[0] :
                    callbackValues = i.callbacks
                    addtionalData.append(i)
            for arg in argsLeft:
                if arg in callbackValues.keys():
                    # Dynamic value gather
                    self.data[address][index][1][arg] = self.functionDynamic(callbackValues[arg].expr, callbackValues[arg].name, self.data[address][index])
                else:
                    self.data[address][index][1][arg] = ""

    def printData(self, data):
        for key in data.keys():
            print(key, " -> ", data[key])
    def functionDynamic(self, expression, argName, structsData):

        validOperators = ['+','-','*','/','(',')']
        index = 0
        length = len(expression)
        finalExp = ""
        while index < length:
            semi = index
            currentSlice = ""

            # Get current iden and save it in currentSlice
            while semi < length and expression[semi] not in validOperators:
                currentSlice += expression[semi]
                semi += 1
            index = semi
            currentSlice = currentSlice.strip()

            # Identifiy currentSlice
            if currentSlice in self.data.keys():
                finalExp += self.data[currentSlice]
            elif '.' in currentSlice and currentSlice[:currentSlice.index('.')] in [i.structName for i in self.par.structs]:
                fieldName = currentSlice[currentSlice.index('.')+1:]
                finalExp += structsData[1][fieldName]
            elif currentSlice.isnumeric() or ('.' in currentSlice and 
                currentSlice[:currentSlice.index('.')].isnumeric() and
                currentSlice[currentSlice.index('.')+1:].isnumeric()):
                finalExp += currentSlice
            elif (currentSlice[0] == '\'' and currentSlice[-1] == '\'') or (currentSlice[0] == '"' and currentSlice[-1] == '"'):
                finalExp += currentSlice
            else:
                print("ERROR OCCURED", currentSlice)
            if semi != length:
                finalExp += expression[semi]
            index += 1
        return str(eval(finalExp))
        
class Parser:
    def __init__(self):
        self.data = {"ano":[]}
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
                            try:
                                fields[field.split("=")[0].strip().strip("'").strip('"')] = field.split("=")[1].strip().strip("'").strip('"')
                            except:
                                raise Exception("parser error : missing `=` at data chunk")
                        self.data["ano"].append((typeName,fields))
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

            # Removing links from the language and moving the calculation to a lambda function in the struct itself
            # elif self.content[self.index] == "(":
            #     self.links.append(_link.Link())
            #     self.index = self.links[-1].detectLinks(self.content, self.index)

            elif self.content[self.index] == "e":
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

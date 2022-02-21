from email.contentmanager import raw_data_manager
from xml.dom.expatbuilder import FilterCrutch
import src.app.struct as _struct
import src.app.link as _link 
import src.app.chunk as _chunk
import json
from src.tools import consts
from src.tools import tooling

class GEN:
    def __init__(self, ast):
        self.ast = ast
        self.exportFuncs = {'json' : self.jsonGEN, 'raw' : self.rawGEN, 'yaml' : self.yamlGEN, 'base' : self.baseGEN}
    def generateCode(self):
        # Clear empty ano
        if self.ast.data["ano"] == []:
            self.ast.data.pop("ano")

        # Check for all exports
        for export in self.ast.par.exports:
            self.exportFuncs[export.exportName]()
    
    def baseGEN(self):
        def baseWRITE(dataDict, fileContent, listFlag):
            if isinstance(dataDict, list):
                fileContent += ' [ '
                for index, data in enumerate(dataDict):
                    if index:
                        fileContent += ', '
                    fileContent = baseWRITE(data, fileContent, True)
                fileContent += ' ] : List'
            elif type(dataDict) == tuple:
                if not listFlag:
                    fileContent += ' : '
                fileContent += f'{dataDict[0]}'
            else:
                if not listFlag:
                    fileContent += ' : '
                if tooling.isString(dataDict) :
                    fileContent += 'Text'
                elif tooling.isNumber(dataDict) :
                    fileContent += 'Number'
                elif tooling.isBoolean(dataDict) :
                    fileContent += 'Bool'
            return fileContent
        

        # -------------------------

        self.ast.par.filePath = self.ast.par.filePath.strip("\\").strip(".\\")
        fileContent = ""
        with open(self.ast.par.filePath[:self.ast.par.filePath.index(".")]+".base", "w") as fileP:
            if not fileP.writable() :
                raise Exception("gen error : can't create export file")
            else:
                for struct in self.ast.par.structs:
                    fileP.write(str(struct) + '\n')
                fileContent += '[ '
                for index,data in enumerate(self.ast.data.keys()):
                    if index:
                        fileContent += ', '
                    fileContent += str(data)
                    fileContent = baseWRITE(self.ast.data[data], fileContent, False)
                fileContent += ' ]'
                fileP.write(fileContent)

    def jsonGEN(self):
        def jsonWRITE(dataDict, fileContent):
            if isinstance(dataDict, list):
                fileContent += '['
                for index, data in enumerate(dataDict):
                    if index:
                        fileContent += ','
                    fileContent = jsonWRITE(data, fileContent)
            elif type(dataDict) == tuple:
                keys = [i.idens for i in self.ast.par.structs if i.structName == dataDict[0]][0]
                fileContent += str(dict(sorted(dataDict[1].items(), key= lambda x : keys.index(x[0])))).replace("'",'"')
            else:
                fileContent += str(dataDict).replace("'",'"')
            
            if isinstance(dataDict, list):
                fileContent += ']'
            return fileContent

        # ----------------------------

        self.ast.par.filePath = self.ast.par.filePath.strip("\\").strip(".\\")
        fileContent = ""
        with open(self.ast.par.filePath[:self.ast.par.filePath.index(".")]+".json", "w") as fileP:
            if not fileP.writable() :
                raise Exception("gen error : can't create export file")
            else:
                fileContent += '{'
                for index,data in enumerate(self.ast.data.keys()):
                    if index:
                        fileContent += ','
                    fileContent += '"' + str(data) + '":'
                    fileContent = jsonWRITE(self.ast.data[data], fileContent)
                fileContent += '}'
                fileContent = eval(fileContent)
                json.dump(fileContent, fileP, indent=4)


    def rawGEN(self):

        def rawWRITE(dataDict, fileContent):
            if isinstance(dataDict, list):
                fileContent += '[ '
                for index, data in enumerate(dataDict):
                    if index:
                        fileContent += ', '
                    fileContent = rawWRITE(data, fileContent)
            elif type(dataDict) == tuple:
                keys = [i.idens for i in self.ast.par.structs if i.structName == dataDict[0]][0]
                preDict = dict(sorted(dataDict[1].items(), key= lambda x : keys.index(x[0])))
                fileContent += '[ ' + str(list(preDict.values())).replace("'",'').replace('"','')[1:-1] + ' ]'
            else:
                fileContent += " " + str(dataDict).replace("'",'').replace('"','')
            
            if isinstance(dataDict, list):
                fileContent += ' ]'
            return fileContent

        # ------------------------

        self.ast.par.filePath = self.ast.par.filePath.strip("\\").strip(".\\")
        fileContent = ""
        with open(self.ast.par.filePath[:self.ast.par.filePath.index(".")]+".txt", "w") as fileP:
            if not fileP.writable() :
                raise Exception("gen error : can't create export file")
            else:
                fileContent += '{\n'
                for index,data in enumerate(self.ast.data.keys()):
                    if index:
                        fileContent += ',\n'
                    fileContent += '\t' + str(data) + ' : '
                    fileContent = rawWRITE(self.ast.data[data], fileContent)
                fileContent += '\n}'
                fileP.write(fileContent)


    def yamlGEN(self):


        def yamlWRITE(dataDict, fileContent):
            if isinstance(dataDict, list):
                for index, data in enumerate(dataDict):
                    fileContent += '\n    - '
                    fileContent = yamlWRITE(data, fileContent)
            elif type(dataDict) == tuple:
                keys = [i.idens for i in self.ast.par.structs if i.structName == dataDict[0]][0]
                preDict = dict(sorted(dataDict[1].items(), key= lambda x : keys.index(x[0])))
                fileContent += "\n    - ".join([str(i[0]) + ': ' + str(i[1]) for i in preDict.items()])
            else:
                fileContent += str(dataDict).replace("'",'').replace('"','')
            return fileContent

        # ------------------------------

        self.ast.par.filePath = self.ast.par.filePath.strip("\\").strip(".\\")
        fileContent = ""
        with open(self.ast.par.filePath[:self.ast.par.filePath.index(".")]+".yaml", "w") as fileP:
            if not fileP.writable() :
                raise Exception("gen error : can't create export file")
            else:
                if len(self.ast.data.keys()) > 1:
                    fileContent += '- '
                for index,data in enumerate(self.ast.data.keys()):
                    if index:
                        fileContent += '\n- '
                    fileContent += str(data) + ': '
                    fileContent = yamlWRITE(self.ast.data[data], fileContent)
                fileP.write(fileContent)

class AST:
    def __init__(self, par):
        self.data = par.data
        self.par = par
    def semanticAnalysis(self):
        structNames = [i.structName for i in self.par.structs]
        for index, structPair in enumerate(self.par.data["ano"]):
            if type(structPair) == tuple and structPair[0] not in structNames:
                raise Exception("zparser error : struct type `"+structPair[0]+"` not expected")
            elif type(structPair) == tuple:
                self.missingArgs("ano", index, structPair)

        for index, key in enumerate(self.par.data.keys()):
            if key != "ano":
                # print("KEY",key, self.par.data[key])
                if isinstance(self.par.data[key], list):
                    for pairIndex, pair in enumerate(self.par.data[key]):
                        if type(pair) == tuple and pair[0] not in structNames:
                            raise Exception("eparser error : struct type `"+pair[0]+"` not expected")
                        elif type(pair) == tuple:
                            # print("PAIR", pair)
                            self.missingArgs(key, pairIndex, pair)
        

    def missingArgs(self, address ,index ,pair):
        validStructs = [i for i in self.par.structs if i.structName == pair[0]]
        currentArgs = validStructs[0].idens
        argsLeft = set(currentArgs) - set(pair[1]) 
        if len(argsLeft):
            callbackValues = []
            addtionalData = []
            for i in self.par.structs :
                if i.structName == pair[0] :
                    callbackValues = i.callbacks
                    addtionalData.append(i)
            dynamicSave = []

            for arg in argsLeft:
                if arg in callbackValues.keys():
                    valueFlagCheck = self.functionDynamic(callbackValues[arg].expr, callbackValues[arg].name, self.data[address][index])
                    
                    # Dynamic value gather
                    if valueFlagCheck == -1:
                        dynamicSave.append([address, index, arg])
                        continue
                    self.data[address][index][1][arg] = valueFlagCheck
                else:
                    self.data[address][index][1][arg] = ""
            for save in dynamicSave:
                if save[2] in callbackValues.keys():
                    valueFlagCheck = self.functionDynamic(callbackValues[save[2]].expr, callbackValues[save[2]].name, self.data[address][index])
                # Second Run Dynamic value gather
                if valueFlagCheck == -1:
                    dynamicSave.append([save[0], save[1], save[2]])
                    continue
                self.data[save[0]][save[1]][1][save[2]] = valueFlagCheck

    def printData(self, data):
        for key in data.keys():
            print(key, " -> ", data[key])
    def functionDynamic(self, expression, argName, structsData):

        index = 0
        length = len(expression)
        finalExp = ""
        while index < length:
            semi = index
            currentSlice = ""

            # Get current iden and save it in currentSlice
            while semi < length and expression[semi] not in consts.BASIC_ARITHMETIC:
                currentSlice += expression[semi]
                semi += 1
            index = semi
            currentSlice = currentSlice.strip()

            # Identifiy currentSlice

            if currentSlice in self.data.keys():
                finalExp += self.data[currentSlice]
            elif '.' in currentSlice and currentSlice[:currentSlice.index('.')] in [i.structName for i in self.par.structs]:
                fieldName = currentSlice[currentSlice.index('.')+1:]
                if fieldName not in [i for i in self.par.structs if i.structName == currentSlice[:currentSlice.index('.')]][0].idens:
                    raise Exception(f"semantic error : failed to calculate delta;\n{fieldName} is not a valid field name in {currentSlice[:currentSlice.index('.')]} struct;\nvalid Fields are {', '.join([i for i in structsData[1].keys()])}")  
                elif fieldName not in structsData[1].keys():
                    finalExp += ""
                else:
                    finalExp += structsData[1][fieldName]
            elif currentSlice.isnumeric() or ('.' in currentSlice and 
                currentSlice[:currentSlice.index('.')].isnumeric() and
                currentSlice[currentSlice.index('.')+1:].isnumeric()):
                finalExp += currentSlice
            elif (currentSlice[0] == '\'' and currentSlice[-1] == '\'') or (currentSlice[0] == '"' and currentSlice[-1] == '"'):
                finalExp += currentSlice
            else:
                raise Exception(f"semantic error : unknown identifier < {currentSlice} > referenced in delta of `{argName}`;on `{structsData[0]}` structs")
            if semi != length:
                finalExp += expression[semi]
            index += 1
        if finalExp[-1] in consts.BASIC_ARITHMETIC:
            return ""
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

    def findData(self, key, data, lexer):
        print('FIND', key, data)
        if "[" in data:
            typeName = data[:data.index("[")]
            print("TYPE", typeName)
            if typeName != '' and typeName not in [i.structName for i in lexer.structs]:
                raise Exception(f"parser error : struct type `{typeName}` not expected")
            elif typeName == '':
                values = self.newGet(data, lexer)[0]
                if key == 'ano':
                    self.data["ano"].append(values)
                else:
                    self.data[key.strip().strip('"')] = values
            else:

                values = self.newGet(data, lexer)
                print("VALUES =>", values)
                fields = {}
                self.data[key.strip().strip('"')] = []
                for field in data[data.index("[")+1:data.index("]")].split("|"):
                    fields[field.split("=")[0].strip().strip('"')] = field.split("=")[1].strip().strip("'").strip('"')
                if key == 'ano':
                    self.data["ano"].append((typeName,fields))
                else:
                    self.data[key.strip().strip('"')] = (typeName,fields)
        else:
            if tooling.isNumber(data) or tooling.isString(data) or tooling.isBoolean(data):
                if key == 'ano':
                    self.data["ano"].append(data)
                else:
                    self.data[key.strip().strip('"')] = data
            else:
                message = f"'{key}' : {data}"
                raise Exception(f'parser error : unknown identifer < {data} > refernenced in value;\nin line < {message} >')

    def restrcutureData(self, lexer):        
        for chunk in lexer.chunks:
            for data in chunk.ano:
                self.findData('ano',data,lexer)

            for key in chunk.chunkDict.keys():
                data = chunk.chunkDict[key]
                self.findData(key,data,lexer)
                
    


    def newGet(self, data, lexer):
        current = ''
        index = 0
        fields = {}
        values = []
        while index < len(data):
            if data[index] in consts.EMPTY_SPACE:
                index += 1
                continue
            if data[index] == '[' and current not in [i.structName for i in lexer.structs]:
                current = ''
                values.append(self.newGet(data[index + 1:], lexer))
                bracketCount = 0
                dowhile = True
                while index < len(data) and bracketCount or dowhile:
                    if data[index] == '[':
                        bracketCount += 1
                    elif data[index] == ']':
                        bracketCount -= 1
                    index += 1
                    dowhile = False
                if index == len(data):
                    index -= 1
            elif data[index] == '[' and current:
                if current not in [i.structName for i in lexer.structs]:
                    raise Exception(f"parser error : struct type `{current}` not expected")
                bracketCount = 0
                dowhile = True
                while index < len(data) and bracketCount or dowhile:
                    if data[index] == '[':
                        bracketCount += 1
                    elif data[index] == ']':
                        bracketCount -= 1
                    current += data[index]
                    index += 1
                    dowhile = False
                if index == len(data):
                    index -= 1
                print("CURRENT", current, current[current.index("[")+1:current.index("]")].split("|"))
                structName = current[:current.index('[')]
                readFlag = False
                levelCounter = 0
                rawData = ""
                fieldName = ""
                for char in current[current.index('[') + 1:]:
                    if char == '=' and not readFlag :
                        readFlag = not readFlag
                    elif char == '|' and readFlag and not levelCounter:
                        readFlag = not readFlag
                        print('Field Name ->',fieldName)
                        # print('Raw Data ->', rawData)
                        # print('Level Counter ->', levelCounter)
                        fieldName = rawData = ""
                        print('Extracted Data', self.newGet(rawData, lexer))
                        # use newGet function on raw data and insert it into the fields list

                    elif char == '[' and readFlag:
                        rawData += char
                        levelCounter += 1
                    elif char == ']' and readFlag:
                        if levelCounter:
                            rawData += char
                            levelCounter -= 1
                    elif not readFlag:
                        fieldName += char
                    elif readFlag:
                        rawData += char
                print('Field Name ->',fieldName)
                # print('Raw Data ->', rawData)
                # print('Level Counter ->', levelCounter)
                print('Extracted Data', self.newGet(rawData, lexer))
                for field in current[current.index("[")+1:current.index("]")].split("|"):
                    fields[field.split("=")[0].strip().strip('"')] = field.split("=")[1].strip().strip("'").strip('"')
                values.append((current[:current.index('[')],fields))
                return values
            elif data[index] == ']':
                return values

            elif data[index] == '"' or data[index] == '\'':
                starter = data[index]
                index += 1
                foundString = "'"
                while index < len(data) and data[index] != starter:
                    foundString += data[index]
                    index += 1
                foundString += "'"
                values.append(foundString)
                index += 1
                current = ''

            elif data[index].isnumeric():
                endNumber = ''
                while index < len(data) and data[index] not in consts.EMPTY_SPACE and data[index] != ']':
                    endNumber += data[index]
                    index += 1
                if not tooling.isNumber(endNumber):
                    raise Exception(f'lexer error : failed while lexing terms, < {data} > is not a valid number value')
                values.append(endNumber)
                index -= 1
                current = ''

            elif data[index].lower() in ['t','f']:
                endNumber = ''
                while index < len(data) and data[index] not in consts.EMPTY_SPACE and data[index] != ']':
                    endNumber += data[index]
                    index += 1
                if not tooling.isBoolean(endNumber):
                    raise Exception(f'lexer error : failed while lexing terms, < {data} > is not a valid number value')
                values.append(endNumber)
                index -= 1
                current = ''
            if index < len(data) and data[index] not in consts.EMPTY_SPACE:
                current += data[index]
            index += 1
        # print('GOT TO END',values)
        return values

    def getData(self, data, lexer):

        def skipZero(string, index):
            while index < len(string) and string[index] in consts.EMPTY_SPACE:
                index += 1
            return index
        
        print('DATA', data)
        if "[" in data:
            typeName = data[:data.index("[")]
            if typeName != '' and typeName not in [i.structName for i in lexer.structs]:
                raise Exception("parser error : struct type `"+typeName+"` not expected")
            elif typeName == '':
                data = data[1:].strip()
                values = []
                index = 0
                current = ''
                keyword = ""
                while index < len(data) and current != ']':
                    index = skipZero(data, index)
                    current = data[index]
                    keyword += current
                    if current == '[' and keyword != '' and keyword[:-1] in [i.structName for i in lexer.structs]:
                        index = skipZero(data, index)
                        current = data[index]
                        structWORD = keyword[:-1]
                        while index < len(data) and current != ']':
                            structWORD += current
                            index += 1
                            current = data[index]
                        structWORD += ']'
                        # `structWORD` will hold the struct creation line
                        # Call getData again to get the value of structs creation
                        values.append(self.getData(structWORD, lexer)[0])
                        index += 1
                        if index >= len(data):
                            raise Exception(f'lexer error : failed while lexing terms, unclosed lbracket ( `]` ) at < {data} >')
                        current = data[index]
                        keyword = ""
                    elif current == '"' or current == '\'':
                        starter = current
                        index += 1
                        current = data[index]
                        foundString = "'"
                        while index < len(data) and current != starter:
                            foundString += current
                            index += 1
                            current = data[index]
                        foundString += "'"
                        values.append(foundString)
                        keyword = ""
                    elif current.isnumeric():
                        endNumber = ""

                        while index < len(data) and current not in consts.EMPTY_SPACE and current != ']':
                            endNumber += current
                            index += 1
                            if index >= len(data):
                                raise Exception(f'lexer error : failed while lexing terms, unclosed lbracket ( `]` ) at < {data} >')
                            current = data[index]
                        values.append(endNumber)
                        keyword = ""
                    else:
                        endExp = ""
                        while index < len(data) and current not in consts.EMPTY_SPACE and current not in ['[',']']:
                            endExp += current
                            index += 1
                            if index >= len(data):
                                raise Exception(f'lexer error : failed while lexing terms, unclosed lbracket ( `]` ) at < {data} >')
                            current = data[index]
                        
                        
                        
                        if tooling.isBoolean(endExp):
                            values.append(endExp)
                            keyword = ""
                        else:
                            keyword = keyword[:-1] + endExp
                            index -= 1
                        # else :
                        #     raise Exception(f'eparser error : unknown identifer < {endExp} > refernenced in value;\nin line < {data} >')
                    if index + 1 < len(data):
                        index += 1
                if current != ']':
                    raise Exception(f'lexer error : failed while lexing terms, unclosed lbracket ( `]` ) at < {data} >')
                return values

            else:
                fields = {}
                values = []
                for field in data[data.index("[")+1:data.index("]")].split("|"):
                    fields[field.split("=")[0].strip().strip('"')] = field.split("=")[1].strip().strip("'").strip('"')
                values.append((typeName,fields))
                return values
        else:
            print("Got here", data)
            return data
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
                    print("\t\t",struct.callbacks[iden].expr)
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
                    print("\t\t",struct.callbacks[iden].expr)
                else:
                    print()

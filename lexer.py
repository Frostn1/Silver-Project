import struct as _struct
import chunk as _chunk
import link as _link

class AST:
    def __init__(self):
        self.data = ""
    def semanticAnalysis(self, par):
        # par.printData()
        structNames = [i.structName for i in par.structs]
        for index, structPair in enumerate(par.data["ano"]):
            if structPair[0] not in structNames:
                raise Exception("parser error : struct type `"+structPair[0]+"` not expected")
            else:
                validStructs = []
                for i in par.structs :
                    if i.structName == structPair[0] : 
                        validStructs.append(i)
                currentArgs = validStructs[0].idens
                argsLeft = set(currentArgs) - set(structPair[1]) 
                if len(argsLeft):
                    callbackValues = []
                    for i in par.structs :
                        if i.structName == structPair[0] : 
                            callbackValues = i.callbacks.keys()
                    for arg in argsLeft:
                        if arg in callbackValues:
                            pass
                            # print("This value has dynamic ->", arg)
                            # TODO : Value Dynamic
                        else:
                            par.data["ano"][index][1][arg] = ""
        self.data = par.data
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
        self.data = {"ano":[]}
        self.exports = []
        self.links = []
    def parse(self, lexer):
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
                        self.data["ano"].append((typeName,fields))
            for key in chunk.chunkDict.keys():
                data = chunk.chunkDict[key]
                if "[" in data:
                    typeName = data[:data.index("[")]
                    if typeName not in [i.structName for i in lexer.structs]:
                        raise Exception("parser error : struct type `"+typeName+"` not expected")
                    else:
                        fields = {}
                        self.data[key.strip().strip("'").strip('"')] = []
                        for field in data[data.index("[")+1:data.index("]")].split("|"):
                            fields[field.split("=")[0].strip().strip("'").strip('"')] = field.split("=")[1].strip().strip("'").strip('"')
                        self.data[key.strip().strip("'").strip('"')].append((typeName,fields))
                else:
                    self.data[key.strip().strip("'").strip('"')] = data
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
    def __init__(self, content):
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
                # print("current index is", self.index)
                # print("here",[i.idens for i in self.structs])

            elif self.content[self.index] == "{":
                # print("Index is", self.index)
                self.chunks.append(_chunk.Chunk())
                self.index = self.chunks[-1].detectData(self.content, self.index)

            elif self.content[self.index] == "(":
                # print("Index is", self.index)
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
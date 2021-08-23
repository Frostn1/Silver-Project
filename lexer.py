import struct as _struct
class Lexer:
    def __init__(self, content):
        self.index = 0
        self.content = content
        self.structs = []
        # self.data
    def lexify(self):
        for char in self.content:
            if char == "<":
                self.structs.append(_struct.Struct())
                self.index = self.structs[-1].detectStructs(self.content, self.index)
                print("current index is", self.index)
                
            else :
                self.index += 1
            
    def printStructs(self):
        for struct in self.structs:
            print("[Name]", struct.structName)
            print("[Idens] =>")
            for iden in struct.idens:
                print("\t",iden, end="")
                if iden in struct.callbacks.keys():
                    print("=> [Callback]")
                    print("\t[Func Name]", struct.callbacks[iden].name)
                    print("\t[Func Args] =>")
                    for arg in struct.callbacks[iden].args:
                        print("\t\t",arg)
                else:
                    print()
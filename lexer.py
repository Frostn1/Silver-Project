import struct
class Lexer:
    def __init__(self, content):
        self.index = 0
        self.content = content
        self.stru = struct.Struct()
        self.keysDict = {'<':self.stru.detectStructs}
        # self.data
    def lexify(self):
        for char in self.content:
            if char in self.keysDict.keys():
                self.index = self.keysDict[char](self.content, self.index)
                print("current index is", self.index)
            else :
                self.index += 1
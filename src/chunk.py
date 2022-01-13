class Chunk:
    def __init__(self):
        self.chunkDict = {}
        self.ano = []
    def detectData(self, content, currentIndex):
        startIndex = currentIndex
        enderFlag = False
        for char in content[currentIndex:]:
            if char == '}' and currentIndex > 0 and content[currentIndex - 1] != '=':
                enderFlag = True
                break
            currentIndex += 1
        if not enderFlag:
            raise Exception("lexer error : expecting `}`")
        chunks = [i.strip() for i in content[startIndex + 1 : currentIndex].split(",")]
        for chunk in chunks:
            if chunk == "":
                raise Exception("chunk error : chunk line can't be empty; trailing `,` in end of chunk")
            elif ":" not in chunk:
                raise Exception("chunk error : expecting `:`")
            elif chunk.count(":") > 1:
                raise Exception("chunk error : not expecting another `:`")
            else:
                dataName, data = [i.strip() for i in chunk.split(":")]
                if dataName == "ano":
                    self.ano.append(data)
                else :
                    print("DATA:", data)
                    self.chunkDict[dataName[1:-1]] = data
        return currentIndex

class Link:
    def __init__(self):
        self.linkedFiles = []
    def detectLinks(self, content, currentIndex):
        startIndex = currentIndex
        enderFlag = False
        for char in content[currentIndex:]:
            if char == ')' and currentIndex > 0 and content[currentIndex - 1] != '=':
                enderFlag = True
                break
            currentIndex += 1
        if not enderFlag:
            raise Exception("lexer error : expecting `)`")
        self.linkedFiles = [i.strip().strip("'").strip('"') for i in content[content.index(":")+1:currentIndex].split("|")]
        return currentIndex

class Export:
    def __init__(self):
        self.validExports = ['json', 'raw', 'yaml', 'base']
        self.exportName = ""
    def detectExports(self, content : str, currentIndex : int):
        currentIndex += 1
        if content[currentIndex-1: currentIndex + 5] != "export":
            raise Exception("lexer error : expecting `export` symbol instead got `"+content[currentIndex-1: currentIndex + 5]+"`")
        currentIndex += 6
        exportName = ""
        while currentIndex < len(content) and content[currentIndex] != "\n":
            if content[currentIndex] != " ":
                exportName  += content[currentIndex]
            currentIndex += 1
        self.exportName = exportName
        if exportName not in self.validExports:
            raise Exception("lexer error : invalid export type `"+exportName+"`")
        return currentIndex

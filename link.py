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
        print("Links", self.linkedFiles)
        return currentIndex

class Export:
    def __init__(self):
        super().__init__()
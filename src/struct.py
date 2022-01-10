# < person:
#     first name,
#     last name,
#     year of birth,
#     age => (currentYear - person.year of birth),
#     email
# >
# < nameOfStruct : idenList >
class Callback:
    def __init__(self, name : str, expression : str):
        self.name = name
        self.expr = expression
    
    def solveExpression(self, data):
        pass
    
class Struct:
    def __init__(self):
        self.callbacks = {}
        self.idens = []
        self.structName = ""
    def detectStructs(self, content, currentIndex):
        startIndex = currentIndex
        enderFlag = False
        for char in content[currentIndex:]:
            if char == '>' and currentIndex > 0 and content[currentIndex - 1] != '=':
                enderFlag = True
                break
            currentIndex += 1
        if not enderFlag:
            raise Exception("lexer error : expecting `>`")
        self.structName = content[startIndex+1:startIndex+content[startIndex+1:].index(":")+1].strip()
        structIden = [i.strip() for i in content[startIndex+content[startIndex:].index(":") + 1 : currentIndex].split(",")]
        for iden in structIden:
            if "=>" in iden:
                print(iden)
                call = str(iden[iden.index("=>")+2:].strip())
                funcName = str(iden[:iden.index("=>")].strip())
                funcArgs = call[call.index("(")+1:call[::-1].index(")")]
                self.callbacks[iden[:iden.index("=>")].strip()] = Callback(funcName, funcArgs)
                self.idens.append(iden[:iden.index("=>")].strip())
            else:
                self.idens.append(iden)
        return currentIndex
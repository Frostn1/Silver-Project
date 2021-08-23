# < person:
#     first name,
#     last name,
#     year of birth,
#     age => calAge(currentYear | person.year of birth),
#     email
# >
# < nameOfStruct : idenList >

class Callback:
    def __init__(self, name : str, args : list):
        self.name = name
        self.args = args
    
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
        self.structName = content[1:content.index(":")]
        structIden = [i.strip() for i in content[content.index(":") + 1 : currentIndex].split(",")]
        for iden in structIden:
            if "=>" in iden:
                call = str(iden[iden.index("=>")+2:].strip())
                funcName = call[:call.index("(")]
                funcArgs = [i.strip() for i in call[call.index("(")+1:call.index(")")].split("|")]
                self.callbacks[iden[:iden.index("=>")].strip()] = Callback(funcName, funcArgs)
                self.idens.append(iden[:iden.index("=>")].strip())
        return currentIndex
# < person:
#     first name,
#     last name,
#     year of birth,
#     age => calAge(currentYear,person.year of birth),
#     email
# >
# < nameOfStruct : idenList >
class Struct:
    def __init__(self):
        pass
    def detectStructs(self, content, currentIndex):
        enderFlag = False
        for char in content[currentIndex:]:
            if char == '>' and currentIndex > 0 and content[currentIndex-1] != '=':
                enderFlag = True
                break
            print(char, end="")
            currentIndex += 1
        if not enderFlag:
            raise Exception("lexer error : expecting `>`")
        return currentIndex
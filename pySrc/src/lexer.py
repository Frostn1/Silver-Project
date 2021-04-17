import links
import structures
import functioncalls
import data


def lexer(src : str):
    lexemes = []
    counter = 0
    while counter < len(src):
        if src[counter] == '#':
            package = links.lexLinkFile(src,counter)
            lexemes.append(package[0])
            counter += package[1]
        elif src[counter] == '<':
            package = structures.lexStructsFile(src,counter)
            lexemes.append(package[0])
            counter += package[1]
        counter += 1
    return lexemes

def removeWhiteSpace(txt : str, index : int):
    while txt[index] == ' ':
        index += 1
    return index
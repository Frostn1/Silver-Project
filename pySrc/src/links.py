import utils

def lexLinkFile(src : str, index : int):
    index += 1
    index = utils.removeWhiteSpace(src,index) 
    linkCounter = 0
    links = ['l','i','n','k']
    while linkCounter < 4:
        if src[linkCounter+index] != links[linkCounter]:
            print('error : unmatched .link.')
            exit(0)
        linkCounter += 1
    index += linkCounter
    index = utils.removeWhiteSpace(src,index)
    
    if src[index] != ':':
        print('error : missing .:.')
        exit(0)
    index += 1
    index = utils.removeWhiteSpace(src,index)
    if src[index] != '\'':
        print('error : missing .\'.')
        exit(0)
    index += 1
    fileName = ''
    while src[index] != '\'' and len(fileName) < 25:
        fileName += src[index]
        index += 1
    if src[index] != '\'':
        print('error : missing .\'.')
        exit(0)
    index += 1
    index = utils.removeWhiteSpace(src,index)
    
    return ['link',fileName], index


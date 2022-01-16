# import lexer as _lexer
class Parser:
    def __init__(self):
        self.data = {"ano":[]}
    
    def parse(self, lexer : _lexer.Lexer):
        for chunk in lexer.chunks:
            for data in chunk.ano:
                if "[" in data:
                    typeName = data[:data.index("[")]
                    print(typeName)
                    if typeName not in [i.structName for i in lexer.structs]:
                        raise Exception("parser error : struct type `"+typeName+"` not expected")
                    else:
                        
                        print("data",data[data.index("[")+1:data.index("]")])
                        fields = {}
                        for field in data[data.index("[")+1:data.index("]")].split("|"):
                            fields[field.split("=")[0].strip().strip("'").strip('"')] = field.split("=")[1].strip().strip("'").strip('"')
                        print("fields",fields)

import Utils
import Tokenizer

class Symbol(object):
    def __init__(self,text,geometry):
        self.text = text
        self.geometry = geometry

    def __str__(self):
        return '(Symbol \'' + self.text + '\')'

    def getText(self):
        return self.text

    def getGeometry(self):
        return self.geometry

class Func(object):
    def __init__(self,argnames,body,geometry):
        self.argnames = argnames
        self.body = body
        self.geometry = geometry

    def __str__(self):
        return '(Func [' + ' '.join(map(str,self.argnames)) + '] ' + str(self.body) + ')'

    def getArgNames(self):
        return self.argnames

    def getArgName(self,index):
        return self.argnames[index]

    def getBody(self):
        return self.body

    def getGeometry(self):
        return self.geometry

class Dict(object):
    def __init__(self,keyvalues,geometry):
        self.keyvalues = keyvalues
        self.geometry = geometry

    def __str__(self):
        return '(Dict [' + ' '.join(map(lambda x: '(' + ' '.join(map(str,x[0])) + ' -> ' + str(x[1]) + ')',self.keyvalues)) + '])'

    def getKeyValues(self):
        return self.keyvalues

    def getKeyValue(self,index):
        return self.keyvalues[index]

    def getGeometry(self):
        return self.geometry

class Call(object):
    def __init__(self,called,arguments,geometry):
        self.called = called
        self.arguments = arguments
        self.geometry = geometry

    def __str__(self):
        return '(Func ' + str(self.called) + ' [' + ' '.join(map(str,self.arguments)) + '])'

    def getCalled(self):
        return self.called

    def getArguments(self):
        return self.arguments

    def getArgument(self,index):
        return self.argument[index]

    def getGeometry(self):
        return self.geometry

def parse(tokens,pos):
    if isinstance(tokens[pos],Tokenizer.Symbol):
        return (pos + 1,Symbol(tokens[pos].getText(),tokens[pos].getGeometry()))
    if isinstance(tokens[pos],Tokenizer.FuncBeg):
        pass
    if isinstance(tokens[pos],Tokenizer.DictBeg):
        init_geometry = tokens[pos].getGeometry()
        full_entries = []
        one_entry = []
        pos = pos + 1

        while not isinstance(tokens[pos],Tokenizer.DictEnd):
            if isinstance(tokens[pos],Tokenizer.Column):
                if len(one_entry) == 1:
                    raise Exception('Dictionary invalid syntax #1!')
                elif len(one_entry) == 0:
                    one_entry = []
                    pos = pos + 1
                else:
                    full_entries.append((one_entry[:-1],one_entry[-1]))
                    one_entry = []
                    pos = pos + 1
            else:
                (pos,new_entry) = parse(tokens,pos)
                one_entry.append(new_entry)

        if len(one_entry) == 1:
            raise Exception('Dictionary invalid syntax #2!')
        elif len(one_entry) == 0:
            pass
        else:
            full_entries.append((one_entry[:-1],one_entry[-1]))

        new_geometry = Utils.TextGeometry(init_geometry.getAbsBeg(),tokens[pos].getGeometry().getAbsEnd(),
                                          init_geometry.getRelBeg()[0],init_geometry.getRelBeg()[1],
                                          tokens[pos].getGeometry().getRelEnd()[0],tokens[pos].getGeometry().getRelEnd()[1])

        return (pos + 1,Dict(full_entries,new_geometry))
    if isinstance(tokens[pos],Tokenizer.CallBeg):
        init_geometry = tokens[pos].getGeometry()
        (pos,called) = parse(tokens,pos + 1)
        arguments = []

        while not isinstance(tokens[pos],Tokenizer.CallEnd):
            (pos,new_argument) = parse(tokens,pos)
            arguments.append(new_argument)

        new_geometry = Utils.TextGeometry(init_geometry.getAbsBeg(),tokens[pos].getGeometry().getAbsEnd(),
                                          init_geometry.getRelBeg()[0],init_geometry.getRelBeg()[1],
                                          tokens[pos].getGeometry().getRelEnd()[0],tokens[pos].getGeometry().getRelEnd()[1])

        return (pos + 1,Call(called,arguments,new_geometry))

    raise Exception('Invalid tokens!')

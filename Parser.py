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
    pass

class Dict(object):
    pass

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
        pass
    if isinstance(tokens[pos],Tokenizer.CallBeg):
        init_geometry = tokens[pos].getGeometry()
        (pos,called) = parse(tokens,pos + 1)
        arguments = []

        while not isinstance(tokens[pos],Tokenizer.CallEnd):
            (pos,new_argument) = parse(tokens,pos)
            arguments.append(new_argument)

        new_geometry = Utils.TextGeometry(init_geometry.getAbsBeg(),arguments[-1].getGeometry().getAbsEnd(),
                                          init_geometry.getRelBeg()[0],init_geometry.getRelBeg()[1],
                                          arguments[-1].getGeometry().getRelEnd()[0],arguments[-1].getGeometry().getRelEnd()[1])

        return (pos + 1,Call(called,arguments,new_geometry))

    raise Exception('Invalid tokens!')

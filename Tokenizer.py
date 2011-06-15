import re

import Stream

class TkAtom(object):
    def __init__(self,text,geometry):
        assert(isinstance(text,str))
        assert(isinstance(geometry,Stream.Geometry))

        self.__text = str(text)
        self.__geometry = geometry.clone()

    def __str__(self):
        return 'TkAtom \'' + self.__text + '\''

    def __repr__(self):
        return str(self)

    @property
    def text(self):
        return self.__text

    @property
    def geometry(self):
        return self.__geometry

class CallBeg(TkAtom):
    def __str__(self):
        return 'CallBeg'

class CallEnd(TkAtom):
    def __str__(self):
        return 'CallEnd'

class Dollar(TkAtom):
    def __str__(self):
        return 'Dollar'

class Boolean(TkAtom):
    def __str__(self):
        return 'Boolean "' + self.text + '"'

class Number(TkAtom):
    def __str__(self):
        return 'Number "' + self.text + '"'

class Symbol(TkAtom):
    def __str__(self):
        return 'Symbol "' + self.text + '"'

class String(TkAtom):
    def __str__(self):
        return 'String "' + self.text + '"'

class StringEval(TkAtom):
    def __str__(self):
        return 'StringEval "' + self.text + '"'

class FuncBeg(TkAtom):
    def __str__(self):
        return 'FuncBeg'

class FuncEnd(TkAtom):
    def __str__(self):
        return 'FuncEnd'

class FuncName(TkAtom):
    def __str__(self):
        return 'FuncName'

class FuncStar(TkAtom):
    def __str__(self):
        return 'FuncStar'

class FuncPlus(TkAtom):
    def __str__(self):
        return 'FuncPlus'

class BlockBeg(TkAtom):
    def __str__(self):
        return 'BlockBeg'

class BlockEnd(TkAtom):
    def __str__(self):
        return 'BlockEnd'

class DictBeg(TkAtom):
    def __str__(self):
        return 'DictBeg'

class DictEnd(TkAtom):
    def __str__(self):
        return 'DictEnd'

class DictBar(TkAtom):
    def __str__(self):
        return 'DictBar'

class CommonEqual(TkAtom):
    def __str__(self):
        return 'CommonEqual'

def tokenize(stream):
    assert(isinstance(stream,Stream.Buffer))

    local_stream = stream.clone()

    tokens = []
    parsers = [(CallBeg,re.compile(r'[(]'),0),
               (CallEnd,re.compile(r'[)]'),0),
               (Dollar,re.compile(r'[$]'),0),
               (Boolean,re.compile(r'#T|#F'),0),
               (Number,re.compile(r'-?[0-9]+(\.[0-9]+)?'),0),
               (Symbol,re.compile(r'[a-zA-Z_]([a-zA-Z0-9-_\?]|:)*'),0),
               (String,re.compile(r'[\']([^\']*)[\']'),1),
               (StringEval,re.compile(r'[`]([^`]*)[`]'),1),
               (FuncBeg,re.compile(r'[[]'),0),
               (FuncEnd,re.compile(r'[]]'),0),
               (FuncName,re.compile(r'[!]'),0),
               (FuncStar,re.compile(r'[*]'),0),
               (FuncPlus,re.compile(r'[+]'),0),
               (BlockBeg,re.compile(r'[{]'),0),
               (BlockEnd,re.compile(r'[}]'),0),
               (DictBeg,re.compile(r'[<]'),0),
               (DictEnd,re.compile(r'[>]'),0),
               (DictBar,re.compile(r'[|]'),0),
               (CommonEqual,re.compile(r'[=]'),0),
               (None,re.compile(r'\s+'),0)]

    while not local_stream.finished:
        for tokenType,reobject,group in parsers:
            res = local_stream.tryConsume(reobject,group)

            if res:
                if tokenType:
                    tokens.append(tokenType(res[0],res[1]))
                break
        else:
            raise Exception('Invalid character at line %d : column %d' % \
                                (local_stream.relPos.row,local_stream.relPos.col))

    return tokens

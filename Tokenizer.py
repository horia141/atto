import re

import Stream

class Token(object):
    def __init__(self,text,geometry):
        assert(isinstance(text,str))
        assert(isinstance(geometry,Stream.Geometry))

        self.__text = text
        self.__geometry = geometry.clone()

    def __str__(self):
        return 'Token \'' + self.__text + '\''

    def __repr__(self):
        return 'Token(' + repr(self.__text) + ',' + repr(self.__geometry) + ')'

    @property
    def text(self):
        return self.__text

    @property
    def geometry(self):
        return self.__geometry

class CallBeg(Token):
    def __str__(self):
        return 'CallBeg'

    def __repr__(self):
        return 'CallBeg(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class CallEnd(Token):
    def __str__(self):
        return 'CallEnd'

    def __repr__(self):
        return 'CallEnd(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Column(Token):
    def __str__(self):
        return 'Column'

    def __repr__(self):
        return 'Column(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Dollar(Token):
    def __str__(self):
        return 'Dollar'

    def __repr__(self):
        return 'Dollar(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Equal(Token):
    def __str__(self):
        return 'Equal'

    def __repr__(self):
        return 'Equal(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Star(Token):
    def __str__(self):
        return 'Star'

    def __repr__(self):
        return 'Star(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Plus(Token):
    def __str__(self):
        return 'Plus'

    def __repr__(self):
        return 'Plus(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Symbol(Token):
    def __str__(self):
        return 'Symbol \'' + self.text + '\''

    def __repr__(self):
        return 'Symbol(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class FuncBeg(Token):
    def __str__(self):
        return 'FuncBeg'

    def __repr__(self):
        return 'FuncBeg(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class FuncEnd(Token):
    def __str__(self):
        return 'FuncEnd'

    def __repr__(self):
        return 'FuncEnd(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class DictBeg(Token):
    def __str__(self):
        return 'DictBeg'

    def __repr__(self):
        return 'DictBeg(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class DictEnd(Token):
    def __str__(self):
        return 'DictEnd'

    def __repr__(self):
        return 'DictEnd(' + repr(self.text) + ',' + repr(self.geometry) + ')'

def tokenize(stream):
    assert(isinstance(stream,Stream.Buffer))

    local_stream = stream.clone()

    tokens = []
    parsers = [(CallBeg,re.compile(r'[(]')),
               (CallEnd,re.compile(r'[)]')),
               (Column,re.compile(r'[|]')),
               (Dollar,re.compile(r'[$]')),
               (Equal,re.compile(r'[=]')),
               (Star,re.compile(r'[*]')),
               (Plus,re.compile(r'[+]')),
               (Symbol,re.compile(r'[a-zA-Z0-9-_]+')),
               (Symbol,re.compile(r'[<]([^>]+)[>]')),
               (FuncBeg,re.compile(r'[[]')),
               (FuncEnd,re.compile(r'[]]')),
               (DictBeg,re.compile(r'[{]')),
               (DictEnd,re.compile(r'[}]')),
               (None,re.compile(r'\s+'))]

    while not local_stream.finished:
        for tokenType,reobject in parsers:
            res = local_stream.tryConsume(reobject)

            if res:
                if tokenType:
                    tokens.append(tokenType(res[0],res[1]))
                break
        else:
            raise Exception('Invalid character at line %d : column %d' % \
                                (local_stream.relPos.row,local_stream.relPos.col))

    return tokens

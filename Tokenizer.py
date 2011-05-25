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
        return 'Tokenizer.TkAtom(' + repr(self.__text) + ',' + repr(self.__geometry) + ')'

    @property
    def text(self):
        return self.__text

    @property
    def geometry(self):
        return self.__geometry

class CallBeg(TkAtom):
    def __str__(self):
        return 'CallBeg'

    def __repr__(self):
        return 'Tokenizer.CallBeg(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class CallEnd(TkAtom):
    def __str__(self):
        return 'CallEnd'

    def __repr__(self):
        return 'Tokenizer.CallEnd(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class CallEqual(TkAtom):
    def __str__(self):
        return 'CallEqual'

    def __repr__(self):
        return 'Tokenizer.CallEqual(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Symbol(TkAtom):
    def __str__(self):
        return 'Symbol \'' + self.text + '\''

    def __repr__(self):
        return 'Tokenizer.Symbol(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class FuncBeg(TkAtom):
    def __str__(self):
        return 'FuncBeg'

    def __repr__(self):
        return 'Tokenizer.FuncBeg(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class FuncEnd(TkAtom):
    def __str__(self):
        return 'FuncEnd'

    def __repr__(self):
        return 'Tokenizer.FuncEnd(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class FuncStar(TkAtom):
    def __str__(self):
        return 'FuncStar'

    def __repr__(self):
        return 'Tokenizer.FuncStar(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class FuncPlus(TkAtom):
    def __str__(self):
        return 'FuncPlus'

    def __repr__(self):
        return 'Tokenizer.FuncPlus(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class DictBeg(TkAtom):
    def __str__(self):
        return 'DictBeg'

    def __repr__(self):
        return 'Tokenizer.DictBeg(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class DictEnd(TkAtom):
    def __str__(self):
        return 'DictEnd'

    def __repr__(self):
        return 'Tokenizer.DictEnd(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class DictColumn(TkAtom):
    def __str__(self):
        return 'DictColumn'

    def __repr__(self):
        return 'Tokenizer.DictColumn(' + repr(self.text) + ',' + repr(self.geometry) + ')'

def tokenize(stream):
    assert(isinstance(stream,Stream.Buffer))

    local_stream = stream.clone()

    tokens = []
    parsers = [(CallBeg,re.compile(r'[(]')),
               (CallEnd,re.compile(r'[)]')),
               (CallEqual,re.compile(r'[=]')),
               (Symbol,re.compile(r'[a-zA-Z0-9~`!@#$%^&_\-;"\'|\\,.?/]+')),
               (Symbol,re.compile(r'[<]([^>]+)[>]')),
               (FuncBeg,re.compile(r'[[]')),
               (FuncEnd,re.compile(r'[]]')),
               (FuncStar,re.compile(r'[*]')),
               (FuncPlus,re.compile(r'[+]')),
               (DictBeg,re.compile(r'[{]')),
               (DictEnd,re.compile(r'[}]')),
               (DictColumn,re.compile(r'[:]')),
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

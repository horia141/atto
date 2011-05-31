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

class CallDollar(TkAtom):
    def __str__(self):
        return 'CallDollar'

    def __repr__(self):
        return 'Tokenizer.CallDollar(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class LookupSep(TkAtom):
    def __str__(self):
        return 'LookupSep'

    def __repr__(self):
        return 'Tokenizer.Lookup(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Boolean(TkAtom):
    def __str__(self):
        return 'Boolean "' + self.text + '"'

    def __repr__(self):
        return 'Tokenizer.Boolean(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Number(TkAtom):
    def __str__(self):
        return 'Number "' + self.text + '"'

    def __repr__(self):
        return 'Tokenizer.Number(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class Symbol(TkAtom):
    def __str__(self):
        return 'Symbol "' + self.text + '"'

    def __repr__(self):
        return 'Tokenizer.Symbol(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class String(TkAtom):
    def __str__(self):
        return 'String "' + self.text + '"'

    def __repr__(self):
        return 'Tokenizer.String(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class StringEval(TkAtom):
    def __str__(self):
        return 'StringEval "' + self.text + '"'

    def __repr__(self):
        return 'Tokenizer.StringEval(' + repr(self.text) + ',' + repr(self.geometry) + ')'

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

class BlockBeg(TkAtom):
    def __str__(self):
        return 'BlockBeg'

    def __repr__(self):
        return 'Tokenizer.BlockBeg(' + repr(self.text) + ',' + repr(self.geometry) + ')'

class BlockEnd(TkAtom):
    def __str__(self):
        return 'BlockEnd'

    def __repr__(self):
        return 'Tokenizer.BlockEnd(' + repr(self.text) + ',' + repr(self.geometry) + ')'

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

class DictBar(TkAtom):
    def __str__(self):
        return 'DictBar'

    def __repr__(self):
        return 'Tokenizer.DictBar(' + repr(self.text) + ',' + repr(self.geometry) + ')'

def tokenize(stream):
    assert(isinstance(stream,Stream.Buffer))

    local_stream = stream.clone()

    tokens = []
    parsers = [(CallBeg,re.compile(r'[(]'),0),
               (CallEnd,re.compile(r'[)]'),0),
               (CallEqual,re.compile(r'[=]'),0),
               (CallDollar,re.compile(r'[$]'),0),
               (LookupSep,re.compile(r'[:]'),0),
               (Boolean,re.compile(r'#T|#F'),0),
               (Number,re.compile(r'[0-9]+'),0),
               (Symbol,re.compile(r'[a-zA-Z_][a-zA-Z0-9-_]*'),0),
               (String,re.compile(r'[\']([^\']*)[\']'),1),
               (StringEval,re.compile(r'[`]([^`]*)[`]'),1),
               (FuncBeg,re.compile(r'[[]'),0),
               (FuncEnd,re.compile(r'[]]'),0),
               (FuncStar,re.compile(r'[*]'),0),
               (FuncPlus,re.compile(r'[+]'),0),
               (BlockBeg,re.compile(r'[{]'),0),
               (BlockEnd,re.compile(r'[}]'),0),
               (DictBeg,re.compile(r'[<]'),0),
               (DictEnd,re.compile(r'[>]'),0),
               (DictBar,re.compile(r'[|]'),0),
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

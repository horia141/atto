import re

import Utils

class Token(object):
    def __init__(self,text,abs_beg,abs_end,rel_beg,rel_end):
        self.text = text
        self.geometry = Utils.TextGeometry(abs_beg,abs_end,rel_beg[0],rel_beg[1],rel_end[0],rel_end[1])

    def __str__(self):
        return 'Token \'' + self.text + '\''

    def getText(self):
        return self.text

    def getGeometry(self):
        return self.geometry

class CallBeg(Token):
    def __str__(self):
        return 'CallBeg'

class CallEnd(Token):
    def __str__(self):
        return 'CallEnd'

class Column(Token):
    def __str__(self):
        return 'Column'

class Dollar(Token):
    def __str__(self):
        return 'Dollar'

class Star(Token):
    def __str__(self):
        return 'Star'

class Plus(Token):
    def __str__(self):
        return 'Plus'

class Symbol(Token):
    def __str__(self):
        return 'Symbol \'' + self.text + '\''

class FuncBeg(Token):
    def __str__(self):
        return 'FuncBeg'

class FuncEnd(Token):
    def __str__(self):
        return 'FuncEnd'

class DictBeg(Token):
    def __str__(self):
        return 'DictBeg'

class DictEnd(Token):
    def __str__(self):
        return 'DictEnd'

def tokenize(input_string):
    def to_rel(pos):
        abs = 0
        row = 0
        col = 0

        while abs < pos:
            if input_string[abs] == '\n':
                row = row + 1
                col = 0
            else:
                col = col + 1

            abs = abs + 1

        return (row,col)

    tokens = []
    pos = 0

    callbeg = re.compile(r'[(]')
    callend = re.compile(r'[)]')
    column = re.compile(r'[|]')
    dollar = re.compile(r'[$]')
    star = re.compile(r'[*]')
    plus = re.compile(r'[+]')
    symbol = re.compile(r'([a-zA-Z0-9-_]+)|[<]([^>]+)[>]')
    funcbeg = re.compile(r'[[]')
    funcend = re.compile(r'[]]')
    dictbeg = re.compile(r'[{]')
    dictend = re.compile(r'[}]')
    space = re.compile(r'\s+')

    while pos < len(input_string):
        m = callbeg.match(input_string,pos)

        if m:
            tokens.append(CallBeg(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = callend.match(input_string,pos)

        if m:
            tokens.append(CallEnd(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = column.match(input_string,pos)

        if m:
            tokens.append(Column(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue
        
        m = dollar.match(input_string,pos)

        if m:
            tokens.append(Dollar(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = star.match(input_string,pos)

        if m:
            tokens.append(Star(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = plus.match(input_string,pos)

        if m:
            tokens.append(Plus(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = symbol.match(input_string,pos)

        if m:
            if m.group(1):
                tokens.append(Symbol(m.group(1),pos,m.end(),to_rel(pos),to_rel(m.end())))
            else:
                tokens.append(Symbol(m.group(2),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = funcbeg.match(input_string,pos)

        if m:
            tokens.append(FuncBeg(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = funcend.match(input_string,pos)

        if m:
            tokens.append(FuncEnd(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = dictbeg.match(input_string,pos)

        if m:
            tokens.append(DictBeg(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = dictend.match(input_string,pos)

        if m:
            tokens.append(DictEnd(m.group(),pos,m.end(),to_rel(pos),to_rel(m.end())))
            pos = m.end()
            continue

        m = space.match(input_string,pos)

        if m:
            pos = m.end()
            continue

        raise Exception('Invalid characters!')

    return tokens

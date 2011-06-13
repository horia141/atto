import re

import Stream
import Tokenizer

class PsAtom(object):
    def __init__(self,geometry):
        assert(isinstance(geometry,Stream.Geometry))

        self.__geometry = geometry.clone()

    def __str__(self):
        return 'PsAtom'

    def __repr__(self):
        return 'Parser.PsAtom(' + repr(self.__geometry) + ')'

    @property
    def geometry(self):
        return self.__geometry

class CallNamedArg(object):
    def __init__(self,name,value):
        assert(isinstance(name,PsAtom))
        assert(isinstance(value,PsAtom))

        self.__name = name.clone()
        self.__value = value.clone()

    def __str__(self):
        return str(self.__name) + '=' + str(self.__value)

    def __repr__(self):
        return 'Parser.CallNamedArg(' + repr(self.__name) + ',' + repr(self.__value) + ')'

    def clone(self):
        return CallNamedArg(self.__name,self.__value)

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

class Call(PsAtom):
    def __init__(self,action,order_args,named_args,geometry):
        assert(isinstance(action,PsAtom))
        assert(isinstance(order_args,list))
        assert(all(map(lambda x: isinstance(x,PsAtom),order_args)))
        assert(isinstance(named_args,list))
        assert(all(map(lambda x: isinstance(x,CallNamedArg),named_args)))

        super(Call,self).__init__(geometry)

        self.__action = action.clone()
        self.__order_args = map(lambda x: x.clone(),order_args)
        self.__named_args = map(lambda x: x.clone(),named_args)

    def __str__(self):
        return '(' + str(self.__action) + \
                (' ' + ' '.join(map(str,self.__order_args)) if self.__order_args else '') + \
                (' ' + ' '.join(map(str,self.__named_args)) if self.__named_args else '') + ')'

    def __repr__(self):
        return 'Parser.Call(' + repr(self.__action) + ',' + \
                           '[' + ','.join(map(repr,self.__order_args)) + '],' + \
                           '[' + ','.join(map(repr,self.__named_args)) + '],' + \
                           repr(self.geometry) + ')'

    def clone(self):
        return Call(self.__action,self.__order_args,self.__named_args,self.geometry)

    @property
    def action(self):
        return self.__action

    @property
    def orderArgs(self):
        return self.__order_args

    @property
    def namedArgs(self):
        return self.__named_args

class Self(PsAtom):
    def __init__(self,text,geometry):
        assert(isinstance(text,str))
        
        super(Self,self).__init__(geometry)

        self.__text = str(text)

    def __str__(self):
        return self.__text

    def __repr__(self):
        return 'Parser.Self(' + repr(self.__text) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return Self(self.__text,self.geometry)

    @property
    def text(self):
        return self.__text

class Boolean(PsAtom):
    def __init__(self,text,geometry):
        assert(isinstance(text,str))
        
        super(Boolean,self).__init__(geometry)

        self.__text = str(text)

    def __str__(self):
        return self.__text

    def __repr__(self):
        return 'Parser.Boolean(' + repr(self.__text) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return Boolean(self.__text,self.geometry)

    @property
    def text(self):
        return self.__text

class Number(PsAtom):
    def __init__(self,text,geometry):
        assert(isinstance(text,str))
        
        super(Number,self).__init__(geometry)

        self.__text = str(text)

    def __str__(self):
        return self.__text

    def __repr__(self):
        return 'Parser.Number(' + repr(self.__text) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return Number(self.__text,self.geometry)

    @property
    def text(self):
        return self.__text

class Symbol(PsAtom):
    def __init__(self,text,geometry):
        assert(isinstance(text,str))

        super(Symbol,self).__init__(geometry)

        self.__text = str(text)

    def __str__(self):
        return self.__text

    def __repr__(self):
        return 'Parser.Symbol(' + repr(self.__text) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return Symbol(self.__text,self.geometry)

    @property
    def text(self):
        return self.__text

class String(PsAtom):
    def __init__(self,text,geometry):
        assert(isinstance(text,str))

        super(String,self).__init__(geometry)

        self.__text = str(text)

    def __str__(self):
        return '\'' + self.__text + '\''

    def __repr__(self):
        return 'Parser.String(' + repr(self.__text) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return String(self.__text,self.geometry)

    @property
    def text(self):
        return self.__text

class StringEval(PsAtom):
    def __init__(self,text,geometry):
        assert(isinstance(text,str))

        super(StringEval,self).__init__(geometry)

        self.__text = str(text)

    def __str__(self):
        return '`' + self.__text + '`'

    def __repr__(self):
        return 'Parser.StringEval(' + repr(self.__text) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return Symbol(self.__text,self.geometry)

    @property
    def text(self):
        return self.__text

class FuncArg(object):
    def __init__(self,name,default):
        assert(isinstance(name,PsAtom))
        assert(default == None or isinstance(default,PsAtom))

        self.__name = name.clone()
        self.__default = default.clone() if default != None else None

    def __str__(self):
        return str(self.__name) + \
               ('=' + str(self.__default) if self.__default else '')

    def __repr__(self):
        return 'Parser.FuncArg(' + repr(self.__name) + ',' + \
                                   repr(self.__default) + ')'

    def clone(self):
        return FuncArg(self.__name,self.__default)

    @property
    def name(self):
        return self.__name

    @property
    def hasDefault(self):
        return self.__default != None

    @property
    def default(self):
        return self.__default

class Func(PsAtom):
    def __init__(self,order,order_defs,order_var,named,named_defs,named_var,body,geometry):
        assert(isinstance(order,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),order)))
        assert(isinstance(order_defs,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),order_defs)))
        assert(order_var == None or isinstance(order_var,PsAtom))
        assert(isinstance(named,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),named)))
        assert(isinstance(named_defs,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),named_defs)))
        assert(named_var == None or isinstance(named_var,PsAtom))
        assert(isinstance(body,PsAtom))

        super(Func,self).__init__(geometry)

        self.__order = map(lambda x: x.clone(),order)
        self.__order_defs = map(lambda x: x.clone(),order_defs)
        self.__order_var = order_var.clone() if order_var else None
        self.__named = map(lambda x: x.clone(),named)
        self.__named_defs = map(lambda x: x.clone(),named_defs)
        self.__named_var = named_var.clone() if named_var else None
        self.__body = body.clone()

    def __str__(self):
        def spIfNNil(ls):
            return ' ' if len(ls) > 0 else ''

        return '[' + ' '.join(map(str,self.__order)) + spIfNNil(self.__order) + \
                     ' '.join(map(str,self.__order_defs)) + spIfNNil(self.__order_defs) + \
                     (str(self.__order_var) + '* ' if self.__order_var else '') + \
                     ' '.join(map(lambda x: str(x) + '!',self.__named)) + spIfNNil(self.__named) + \
                     ' '.join(map(lambda x: str(x) + '!',self.__named_defs)) + spIfNNil(self.__named_defs) + \
                     (str(self.__named_var) + '+ ' if self.__named_var else '') + \
                     str(self.__body) + ']'

    def __repr__(self):
        return 'Parser.Func(' + repr(self.__order) + ',' + \
                                repr(self.__order_defs) + ',' + \
                                repr(self.__order_var) + ',' + \
                                repr(self.__named) + ',' + \
                                repr(self.__named_defs) + ',' + \
                                repr(self.__named_var) + ',' + \
                                repr(self.__body) + ',' + \
                                repr(self.geometry) + ')'

    def clone(self):
        return Func(self.__order,self.__order_defs,self.__order_var,
                    self.__named,self.__named_defs,self.__named_var,
                    self.__body,self.geometry)

    @property
    def order(self):
        return self.__order

    @property
    def orderDefs(self):
        return self.__order_defs

    @property
    def hasOrderVar(self):
        return self.__order_var != None

    @property
    def orderVar(self):
        return self.__order_var

    @property
    def named(self):
        return self.__named

    @property
    def namedDefs(self):
        return self.__named_defs

    @property
    def hasNamedVar(self):
        return self.__named_var != None

    @property
    def namedVar(self):
        return self.__named_var

    @property
    def body(self):
        return self.__body

class Dict(PsAtom):
    def __init__(self,keyvalues,geometry):
        assert(isinstance(keyvalues,list))
        assert(all(map(lambda x: isinstance(x,tuple),keyvalues)))
        assert(all(map(lambda x: isinstance(x[0],PsAtom),keyvalues)))
        assert(all(map(lambda x: isinstance(x[1],PsAtom),keyvalues)))

        super(Dict,self).__init__(geometry)

        self.__keyvalues = map(lambda x: (x[0].clone(),x[1].clone()),keyvalues)

    def __str__(self):
        return '<' + ' '.join(map(lambda x: str(x[0]) + ' ' + str(x[1]),self.__keyvalues)) + '>'

    def __repr__(self):
        return 'Parser.Dict(' + repr(self.__keyvalues) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return Dict(self.__keyvalues,self.geometry)

    @property
    def keyvalues(self):
        return self.__keyvalues

def parse(tokens,pos=0):
    assert(isinstance(tokens,list))
    assert(all(map(lambda x: isinstance(x,Tokenizer.TkAtom),tokens)))
    assert(isinstance(pos,int))
    assert(pos < len(tokens))

    full_geometry = tokens[pos].geometry
    values = []

    while True:
        if isinstance(tokens[pos],Tokenizer.CallBeg):
            init_geometry = tokens[pos].geometry
            (pos,action) = parse(tokens,pos+1)
            order_args = []
            named_args = []
    
            while not isinstance(tokens[pos],Tokenizer.CallEnd):
                (pos,new_arg) = parse(tokens,pos)
    
                if isinstance(tokens[pos],Tokenizer.CommonEqual):
                    (pos,value) = parse(tokens,pos+1)
                    named_args.append(CallNamedArg(new_arg,value))
                else:
                    order_args.append(new_arg)
    
            geometry = init_geometry.expandTo(tokens[pos].geometry)
            values.append(Call(action,order_args,named_args,geometry))
        elif isinstance(tokens[pos],Tokenizer.CallEnd):
            raise Exception('Invalid ")" character!')
        elif isinstance(tokens[pos],Tokenizer.Dollar):
            values.append(Self(tokens[pos].text,tokens[pos].geometry))
        elif isinstance(tokens[pos],Tokenizer.Boolean):
            values.append(Boolean(tokens[pos].text,tokens[pos].geometry))
        elif isinstance(tokens[pos],Tokenizer.Number):
            values.append(Number(tokens[pos].text,tokens[pos].geometry))
        elif isinstance(tokens[pos],Tokenizer.Symbol):
            values.append(Symbol(tokens[pos].text,tokens[pos].geometry))
        elif isinstance(tokens[pos],Tokenizer.String):
            values.append(String(tokens[pos].text,tokens[pos].geometry))
        elif isinstance(tokens[pos],Tokenizer.StringEval):
            values.append(StringEval(tokens[pos].text,tokens[pos].geometry))
        elif isinstance(tokens[pos],Tokenizer.FuncBeg):
            def testSyntax(token):
                if isinstance(token,Tokenizer.CommonEqual) or \
                   isinstance(token,Tokenizer.FuncName) or \
                   isinstance(token,Tokenizer.FuncStar) or \
                   isinstance(token,Tokenizer.FuncPlus):
                    raise Exception('Invalid syntax for function call!')

            FUNC_ORDER = 0
            FUNC_ORDER_DEFS = 1
            FUNC_ORDER_VAR = 2
            FUNC_NAMED = 3
            FUNC_NAMED_DEFS = 4
            FUNC_NAMED_VAR = 5
            FUNC_STOP = 6

            init_geometry = tokens[pos].geometry
            pos = pos + 1
            cpos = 0
            order = []
            order_defs = []
            order_var = None
            named = []
            named_defs = []
            named_var = None
            body = None
            contents = []
            state = FUNC_ORDER

            while not isinstance(tokens[pos],Tokenizer.FuncEnd):
                if isinstance(tokens[pos],Tokenizer.CommonEqual):
                    contents.append(tokens[pos])
                    pos = pos + 1
                elif isinstance(tokens[pos],Tokenizer.FuncName):
                    contents.append(tokens[pos])
                    pos = pos + 1
                elif isinstance(tokens[pos],Tokenizer.FuncStar):
                    contents.append(tokens[pos])
                    pos = pos + 1
                elif isinstance(tokens[pos],Tokenizer.FuncPlus):
                    contents.append(tokens[pos])
                    pos = pos + 1
                else:
                    (pos,new_item) = parse(tokens,pos)
                    contents.append(new_item)

            if len(contents) < 1:
                raise Exception('Invalid empty function!')

            testSyntax(contents[-1])

            body = contents[-1]
            del contents[-1]

            while cpos < len(contents) and state != FUNC_STOP :
                if state == FUNC_ORDER:
                    if cpos + 3 < len(contents) and \
                       isinstance(contents[cpos+1],Tokenizer.CommonEqual) and \
                       isinstance(contents[cpos+3],Tokenizer.FuncName):
                        testSyntax(contents[cpos])
                        testSyntax(contents[cpos+2])
                        state = FUNC_NAMED_DEFS
                        named_defs.append(FuncArg(contents[cpos],contents[cpos+2]))
                        cpos = cpos + 4
                    elif cpos + 2 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.CommonEqual):
                        testSyntax(contents[cpos])
                        testSyntax(contents[cpos+2])
                        state = FUNC_ORDER_DEFS
                        order_defs.append(FuncArg(contents[cpos],contents[cpos+2]))
                        cpos = cpos + 3
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncName):
                        testSyntax(contents[cpos])
                        state = FUNC_NAMED
                        named.append(FuncArg(contents[cpos],None))
                        cpos = cpos + 2
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncStar):
                        testSyntax(contents[cpos])
                        state = FUNC_ORDER_VAR
                        order_var = contents[cpos]
                        cpos = cpos + 2
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncPlus):
                        testSyntax(contents[cpos])
                        state = FUNC_NAMED_VAR
                        named_var = contents[cpos]
                        cpos = cpos + 2
                    elif cpos < len(contents):
                        testSyntax(contents[cpos])
                        state = FUNC_ORDER
                        order.append(FuncArg(contents[cpos],None))
                        cpos = cpos + 1
                    else:
                        state = FUNC_STOP
                elif state == FUNC_ORDER_DEFS:
                    if cpos + 3 < len(contents) and \
                       isinstance(contents[cpos+1],Tokenizer.CommonEqual) and \
                       isinstance(contents[cpos+3],Tokenizer.FuncName):
                        testSyntax(contents[cpos])
                        testSyntax(contents[cpos+2])
                        state = FUNC_NAMED_DEFS
                        named_defs.append(FuncArg(contents[cpos],contents[cpos+2]))
                        cpos = cpos + 4
                    elif cpos + 2 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.CommonEqual):
                        testSyntax(contents[cpos])
                        testSyntax(contents[cpos+2])
                        state = FUNC_ORDER_DEFS
                        order_defs.append(FuncArg(contents[cpos],contents[cpos+2]))
                        cpos = cpos + 3
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncName):
                        testSyntax(contents[cpos])
                        state = FUNC_NAMED
                        named.append(FuncArg(contents[cpos],None))
                        cpos = cpos + 2
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncStar):
                        testSyntax(contents[cpos])
                        state = FUNC_ORDER_VAR
                        order_var = contents[cpos]
                        cpos = cpos + 2
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncPlus):
                        testSyntax(contents[cpos])
                        state = FUNC_NAMED_VAR
                        named_var = contents[cpos]
                        cpos = cpos + 2
                    elif cpos < len(contents):
                        raise Exception('Cannot use order arguments after default ones!')
                    else:
                        state = FUNC_STOP
                elif state == FUNC_ORDER_VAR:
                    if cpos + 3 < len(contents) and \
                       isinstance(contents[cpos+1],Tokenizer.CommonEqual) and \
                       isinstance(contents[cpos+3],Tokenizer.FuncName):
                        testSyntax(contents[cpos])
                        testSyntax(contents[cpos+2])
                        state = FUNC_NAMED_DEFS
                        named_defs.append(FuncArg(contents[cpos],contents[cpos+2]))
                        cpos = cpos + 4
                    elif cpos + 2 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.CommonEqual):
                        raise Exception('Cannot use order arguments (with default) after variable one!')
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncName):
                        testSyntax(contents[cpos])
                        state = FUNC_NAMED
                        named.append(FuncArg(contents[cpos],None))
                        cpos = cpos + 2
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncStar):
                        raise Exception('Only one variable order argument allowed!')
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncPlus):
                        testSyntax(contents[cpos])
                        state = FUNC_NAMED_VAR
                        named_var = contents[cpos]
                        cpos = cpos + 2
                    elif cpos < len(contents):
                        raise Exception('Cannot use order arguments after variable one!')
                    else:
                        state = FUNC_STOP
                elif state == FUNC_NAMED:
                    if cpos + 3 < len(contents) and \
                       isinstance(contents[cpos+1],Tokenizer.CommonEqual) and \
                       isinstance(contents[cpos+3],Tokenizer.FuncName):
                        testSyntax(contents[cpos])
                        testSyntax(contents[cpos+2])
                        state = FUNC_NAMED_DEFS
                        named_defs.append(FuncArg(contents[cpos],contents[cpos+2]))
                        cpos = cpos + 4
                    elif cpos + 2 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.CommonEqual):
                        raise Exception('Cannot use order arguments (with default) after named ones!')
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncName):
                        testSyntax(contents[cpos])
                        state = FUNC_NAMED
                        named.append(FuncArg(contents[cpos],None))
                        cpos = cpos + 2
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncStar):
                        raise Exception('Cannot use variable order argument after named ones!')
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncPlus):
                        testSyntax(contents[cpos])
                        state = FUNC_NAMED_VAR
                        named_var = contents[cpos]
                        cpos = cpos + 2
                    elif cpos < len(contents):
                        raise Exception('Cannot use order arguments after named ones!')
                    else:
                        state = FUNC_STOP
                elif state == FUNC_NAMED_DEFS:
                    if cpos + 3 < len(contents) and \
                       isinstance(contents[cpos+1],Tokenizer.CommonEqual) and \
                       isinstance(contents[cpos+3],Tokenizer.FuncName):
                        testSyntax(contents[cpos])
                        testSyntax(contents[cpos+2])
                        state = FUNC_NAMED_DEFS
                        named_defs.append(FuncArg(contents[cpos],contents[cpos+2]))
                        cpos = cpos + 4
                    elif cpos + 2 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.CommonEqual):
                        raise Exception('Cannot use order arguments (with default) after named ones!')
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncName):
                        raise Exception('Cannot use named arguments after default named arguments!')
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncStar):
                        raise Exception('Cannot use variable order argument after named ones!')
                    elif cpos + 1 < len(contents) and \
                         isinstance(contents[cpos+1],Tokenizer.FuncPlus):
                        testSyntax(contents[cpos])
                        state = FUNC_NAMED_VAR
                        named_var = contents[cpos]
                        cpos = cpos + 2
                    elif cpos < len(contents):
                        raise Exception('Cannot use order arguments after default ones!')
                    else:
                        state = FUNC_STOP
                elif state == FUNC_NAMED_VAR:
                    if cpos < len(contents):
                        raise Exception('Invalid argument after named variable one!')
                    else:
                        state = FUNC_STOP
                else:
                    raise Exception('Critical Error: Invalid Func FSM Path!')

            if cpos != len(contents):
                raise Exception('Invalid syntax for function call!')

            geometry = init_geometry.expandTo(tokens[pos].geometry)
            values.append(Func(order,order_defs,order_var,named,named_defs,named_var,body,geometry))
        elif isinstance(tokens[pos],Tokenizer.FuncEnd):
            raise Exception('Invalid "]" character!')
        elif isinstance(tokens[pos],Tokenizer.FuncName):
            raise Exception('Invalid "!" character!')
        elif isinstance(tokens[pos],Tokenizer.FuncStar):
            raise Exception('Invalid "*" character!')
        elif isinstance(tokens[pos],Tokenizer.FuncPlus):
            raise Exception('Invalid "+" character!')
        elif isinstance(tokens[pos],Tokenizer.BlockBeg):
            init_geometry = tokens[pos].geometry
            (pos,action) = parse(tokens,pos+1)
            order_args = []
            named_args = []
    
            while not isinstance(tokens[pos],Tokenizer.BlockEnd):
                (pos,new_arg) = parse(tokens,pos)
    
                if isinstance(tokens[pos],Tokenizer.CommonEqual):
                    (pos,value) = parse(tokens,pos+1)
                    named_args.append(CallNamedArg(new_arg,value))
                else:
                    order_args.append(new_arg)
    
            geometry = init_geometry.expandTo(tokens[pos].geometry)
            body = Call(action,order_args,named_args,geometry)
            values.append(Func([],[],None,[],[],None,body,geometry))
        elif isinstance(tokens[pos],Tokenizer.BlockEnd):
            raise Exception('Invalid "}" character!')
        elif isinstance(tokens[pos],Tokenizer.DictBeg):
            init_geometry = tokens[pos].geometry
            pos = pos+1
            keyvalues = []
    
            while not isinstance(tokens[pos],Tokenizer.DictEnd):
                (pos,key) = parse(tokens,pos)
                (pos,value) = parse(tokens,pos)
    
                keyvalues.append((key,value))
    
            geometry = init_geometry.expandTo(tokens[pos].geometry)
            values.append(Dict(keyvalues,geometry))
        elif isinstance(tokens[pos],Tokenizer.DictEnd):
            raise Exception('Invalid ">" character!')
        elif isinstance(tokens[pos],Tokenizer.DictBar):
            raise Exception('Invalid "|" character!')
        elif isinstance(tokens[pos],Tokenizer.CommonEqual):
            raise Exception('Invalid "=" character!')
        else:
            raise Exception('Invalid syntax!')

        pos = pos + 1

        if pos < len(tokens) and isinstance(tokens[pos],Tokenizer.DictBar):
            pos = pos + 1
        else:
            break

    if len(values) == 1:
        return (pos,values[0])
    else:
        no_geom = Stream.Geometry(0,Stream.RelPos(0,0),0,Stream.RelPos(0,0))
        build_kvs = [(Symbol('Length',no_geom),
                      Number(str(len(values)),no_geom))]

        for i in range(0,len(values)):
            build_kvs.append((Number(str(i),no_geom),values[i]))

        geometry = full_geometry.expandTo(tokens[pos-1].geometry)
        return (pos,Dict(build_kvs,geometry))

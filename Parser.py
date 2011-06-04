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
    def default(self):
        return self.__default

class Func(PsAtom):
    def __init__(self,reqargs,defargs,optargs,vararg_name,vararg_minone,body,geometry):
        assert(isinstance(reqargs,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),reqargs)))
        assert(isinstance(defargs,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),defargs)))
        assert(isinstance(optargs,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),optargs)))
        assert(vararg_name == None or isinstance(vararg_name,PsAtom))
        assert((vararg_name == None and vararg_minone == None) or \
               (vararg_name != None and isinstance(vararg_minone,bool)))
        assert(isinstance(body,PsAtom))

        super(Func,self).__init__(geometry)

        self.__reqargs = map(lambda x: x.clone(),reqargs)
        self.__defargs = map(lambda x: x.clone(),defargs)
        self.__optargs = map(lambda x: x.clone(),optargs)
        self.__vararg_name = vararg_name.clone() if vararg_name else None
        self.__vararg_minone = vararg_minone
        self.__body = body.clone()

    def __str__(self):
        if self.__vararg_name:
            return '[' + ' '.join(map(str,self.__reqargs)) + \
                        (' ' if self.__reqargs != [] else '') + \
                         ' '.join(map(str,self.__defargs)) + \
                        (' ' if self.__defargs != [] else '') + \
                         ' '.join(map(lambda x: str(x) + '?',self.__optargs)) + \
                        (' ' if self.__optargs != [] else '') + \
                        str(self.__vararg_name) + ('+ ' if self.__vararg_minone else '* ') + \
                        str(self.__body) + ']'
        else:
            return '[' + ' '.join(map(str,self.__reqargs)) + \
                        (' ' if self.__reqargs != [] else '') + \
                         ' '.join(map(str,self.__defargs)) + \
                        (' ' if self.__defargs != [] else '') + \
                         ' '.join(map(lambda x: str(x) + '?',self.__optargs)) + \
                        (' ' if self.__optargs != [] else '') + \
                        str(self.__body) + ']'

    def __repr__(self):
        return 'Parser.Func(' + '[' + ','.join(map(repr,self.__reqargs)) + '],' + \
                                '[' + ','.join(map(repr,self.__defargs)) + '],' + \
                                '[' + ','.join(map(repr,self.__optargs)) + '],' + \
                                 repr(self.__vararg_name) + ',' + \
                                 repr(self.__vararg_minone) + ',' + \
                                 repr(self.__body) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return Func(self.__reqargs,self.__defargs,self.__optargs,
                    self.__vararg_name,self.__vararg_minone,
                    self.__body,self.geometry)

    @property
    def reqargs(self):
        return self.__reqargs

    @property
    def defargs(self):
        return self.__defargs

    @property
    def optargs(self):
        return self.__optargs

    @property
    def hasVararg(self):
        return self.__vararg_name != None

    @property
    def varargName(self):
        return self.__vararg_name

    @property
    def varargMinOne(self):
        return self.__vararg_minone

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
            ARGST_REQ = 0
            ARGST_DEF = 1
            ARGST_OPT = 2
            ARGST_VAR = 3
            ARGST_END = 4

            init_geometry = tokens[pos].geometry
            pos = pos + 1
            cpos = 0
            reqargs = []
            defargs = []
            optargs = []
            vararg_name = None
            vararg_minone = None
            body = None
            contents = []
            state = ARGST_REQ

            while not isinstance(tokens[pos],Tokenizer.FuncEnd):
                if isinstance(tokens[pos],Tokenizer.CommonEqual):
                    contents.append(tokens[pos])
                    pos = pos + 1
                elif isinstance(tokens[pos],Tokenizer.FuncOptional):
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

            if not isinstance(contents[-1],Tokenizer.CommonEqual) and \
               not isinstance(contents[-1],Tokenizer.FuncOptional) and \
               not isinstance(contents[-1],Tokenizer.FuncStar) and \
               not isinstance(contents[-1],Tokenizer.FuncPlus):
                body = contents[-1]
                del contents[-1]
            else:
                raise Exception('Invalid body!')

            while state == ARGST_REQ:
                if cpos + 3 < len(contents) and \
                   isinstance(contents[cpos+1],Tokenizer.CommonEqual) and \
                   isinstance(contents[cpos+3],Tokenizer.FuncOptional):
                    state = ARGST_OPT
                    optargs.append(FuncArg(contents[cpos],contents[cpos+2]))
                    cpos = cpos + 4
                elif cpos + 2 < len(contents) and \
                     isinstance(contents[cpos+1],Tokenizer.CommonEqual):
                    state = ARGST_DEF
                    defargs.append(FuncArg(contents[cpos],contents[cpos+2]))
                    cpos = cpos + 3
                elif cpos + 1 < len(contents) and \
                     isinstance(contents[cpos+1],Tokenizer.FuncStar):
                    state = ARGST_VAR
                    vararg_name = contents[cpos]
                    vararg_minone = False
                    cpos = cpos + 2
                elif cpos + 1 < len(contents) and \
                     isinstance(contents[cpos+1],Tokenizer.FuncPlus):
                    state = ARGST_VAR
                    vararg_name = contents[cpos]
                    vararg_minone = True
                    cpos = cpos + 2
                elif cpos < len(contents):
                    state = ARGST_REQ
                    reqargs.append(FuncArg(contents[cpos],None))
                    cpos = cpos + 1
                else:
                    state = ARGST_END

            while state == ARGST_DEF:
                if cpos + 3 < len(contents) and \
                   isinstance(contents[cpos+1],Tokenizer.CommonEqual) and \
                   isinstance(contents[cpos+3],Tokenizer.FuncOptional):
                    state = ARGST_OPT
                    optargs.append(FuncArg(contents[cpos],contents[cpos+2]))
                    cpos = cpos + 4
                elif cpos + 2 < len(contents) and \
                     isinstance(contents[cpos+1],Tokenizer.CommonEqual):
                    state = ARGST_DEF
                    defargs.append(FuncArg(contents[cpos],contents[cpos+2]))
                    cpos = cpos + 3
                elif cpos + 1 < len(contents) and \
                     isinstance(contents[cpos+1],Tokenizer.FuncStar):
                    state = ARGST_VAR
                    vararg_name = contents[cpos]
                    vararg_minone = False
                    cpos = cpos + 2
                elif cpos + 1 < len(contents) and \
                     isinstance(contents[cpos+1],Tokenizer.FuncPlus):
                    state = ARGST_VAR
                    vararg_name = contents[cpos]
                    vararg_minone = True
                    cpos = cpos + 2
                elif cpos < len(contents):
                    raise Exception('Cannot have normal argument after default one!')
                else:
                    state = ARGST_END

            while state == ARGST_OPT:
                if cpos + 3 < len(contents) and \
                   isinstance(contents[cpos+1],Tokenizer.CommonEqual) and \
                   isinstance(contents[cpos+3],Tokenizer.FuncOptional):
                    state = ARGST_OPT
                    optargs.append(FuncArg(contents[cpos],contents[cpos+2]))
                    cpos = cpos + 4
                elif cpos + 1 < len(contents) and \
                     isinstance(contents[cpos+1],Tokenizer.FuncStar):
                    state = ARGST_VAR
                    vararg_name = contents[cpos]
                    vararg_minone = False
                    cpos = cpos + 2
                elif cpos + 1 < len(contents) and \
                     isinstance(contents[cpos+1],Tokenizer.FuncPlus):
                    state = ARGST_VAR
                    vararg_name = contents[cpos]
                    vararg_minone = True
                    cpos = cpos + 2
                elif cpos < len(contents):
                    raise Exception('Cannot have normal or default argument after optional one!')
                else:
                    state = ARGST_END

            while state == ARGST_VAR:
                if cpos < len(contents):
                    raise Exception('Cannot have more than one variable argument1')
                else:
                    state = ARGST_END

            assert(state == ARGST_END)

            geometry = init_geometry.expandTo(tokens[pos].geometry)
            values.append(Func(reqargs,defargs,optargs,vararg_name,vararg_minone,body,geometry))
        elif isinstance(tokens[pos],Tokenizer.FuncEnd):
            raise Exception('Invalid "]" character!')
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
            values.append(Func([],[],[],None,None,body,geometry))
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

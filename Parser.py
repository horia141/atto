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
    def __init__(self,name,default,optional):
        assert(isinstance(name,PsAtom))
        assert(default == None or isinstance(default,PsAtom))
        assert(isinstance(optional,bool))

        self.__name = name.clone()
        self.__default = default.clone() if default != None else default
        self.__optional = optional

    def __str__(self):
        return str(self.__name) + \
               ('=' + str(self.__default) if self.__default else '') + \
               ('?' if self.__optional else '')

    def __repr__(self):
        return 'Parser.FuncArg(' + repr(self.__name) + ',' + \
                                   repr(self.__default) + ',' + \
                                   repr(self.__optional) + ')'

    def clone(self):
        return FuncArg(self.__name,self.__default,self.__optional)

    @property
    def name(self):
        return self.__name

    @property
    def default(self):
        return self.__default

    @property
    def optional(self):
        return self.__optional

class Func(PsAtom):
    def __init__(self,arg_names,vararg_name,vararg_minone,body,geometry):
        assert(isinstance(arg_names,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),arg_names)))
        assert(vararg_name == None or isinstance(vararg_name,PsAtom))
        assert((vararg_name == None and vararg_minone == None) or \
               (vararg_name != None and isinstance(vararg_minone,bool)))
        assert(isinstance(body,PsAtom))

        super(Func,self).__init__(geometry)

        self.__arg_names = map(lambda x: x.clone(),arg_names)
        self.__vararg_name = vararg_name.clone() if vararg_name else None
        self.__vararg_minone = vararg_minone
        self.__body = body.clone()

    def __str__(self):
        if self.__vararg_name:
            return '[' + ' '.join(map(str,self.__arg_names)) + \
                        (' ' if self.__arg_names != [] else '') + \
                        str(self.__vararg_name) + ('+ ' if self.__vararg_minone else '* ') + \
                        str(self.__body) + ']'
        else:
            return '[' + ' '.join(map(str,self.__arg_names)) + \
                        (' ' if self.__arg_names != [] else '') + \
                        str(self.__body) + ']'

    def __repr__(self):
        return 'Parser.Func(' + '[' + ','.join(map(repr,self.__arg_names)) + '],' + \
                                 repr(self.__vararg_name) + ',' + \
                                 repr(self.__vararg_minone) + ',' + \
                                 repr(self.__body) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return Func(self.__arg_names,self.__vararg_name,self.__vararg_minone,
                    self.__body,self.geometry)

    @property
    def argNames(self):
        return self.__arg_names

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
            init_geometry = tokens[pos].geometry
            pos = pos + 1
            contents = []
            vararg_name = None
            vararg_minone = None
    
            while not isinstance(tokens[pos],Tokenizer.FuncEnd):
                new_item_name = None

                (pos,new_item_name) = parse(tokens,pos)

                if isinstance(tokens[pos],Tokenizer.CommonEqual):
                    (pos,new_item_default) = parse(tokens,pos+1)

                    if isinstance(tokens[pos],Tokenizer.FuncOptional):
                        pos = pos + 1
                        contents.append(FuncArg(new_item_name,new_item_default,True)) 
                    else:
                        contents.append(FuncArg(new_item_name,new_item_default,False)) 

                    if isinstance(tokens[pos],Tokenizer.FuncEnd):
                        raise Exception('Missing function body!')
                elif isinstance(tokens[pos],Tokenizer.FuncStar) or \
                     isinstance(tokens[pos],Tokenizer.FuncPlus):
                    vararg_name = new_item_name
    
                    if isinstance(tokens[pos],Tokenizer.FuncStar):
                        vararg_minone = False
                    else:
                        vararg_minone = True
    
                    pos = pos + 1
                    (pos,body) = parse(tokens,pos)
                    contents.append(FuncArg(body,None,False))

                    if not isinstance(tokens[pos],Tokenizer.FuncEnd):
                        raise Exception('Invalid function syntax #2!')
                else:
                    contents.append(FuncArg(new_item_name,None,False))

            if len(contents) == 0:
                raise Exception('Invalid function syntax!')

            geometry = init_geometry.expandTo(tokens[pos].geometry)
            values.append(Func(contents[:-1],vararg_name,vararg_minone,contents[-1].name,geometry))
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
            values.append(Func([],None,None,body,geometry))
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

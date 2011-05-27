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

class Lookup(PsAtom):
    def __init__(self,names,geometry):
        assert(isinstance(names,list))
        assert(all(map(lambda x: isinstance(x,PsAtom),names)))

        super(Lookup,self).__init__(geometry)

        self.__names = map(lambda x: x.clone(),names)

    def __str__(self):
        return ':' +  ':'.join(map(str,self.__names))

    def __repr__(self):
        return 'Parser.Lookup(' + '[' + ','.join(map(repr,self.__names)) + '])'

    def clone(self):
        return Lookup(self.__names,self.geometry)

    @property
    def names(self):
        return self.__names

class Symbol(PsAtom):
    def __init__(self,text,geometry):
        assert(isinstance(text,str))

        super(Symbol,self).__init__(geometry)

        self.__text = str(text)

    def __str__(self):
        if re.search('\s',self.__text):
            return '{' + self.__text + '}'
        else:
            return self.__text

    def __repr__(self):
        return 'Parser.Symbol(' + repr(self.__text) + ',' + repr(self.geometry) + ')'

    def clone(self):
        return Symbol(self.__text,self.geometry)

    @property
    def text(self):
        return self.__text

class Func(PsAtom):
    def __init__(self,arg_names,vararg_name,vararg_minone,body,geometry):
        assert(isinstance(arg_names,list))
        assert(all(map(lambda x: isinstance(x,PsAtom),arg_names)))
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

class DictKeysValue(object):
    def __init__(self,keys,value):
        assert(isinstance(keys,list))
        assert(all(map(lambda x: isinstance(x,PsAtom),keys)))
        assert(isinstance(value,PsAtom))

        self.__keys = map(lambda x: x.clone(),keys)
        self.__value = value.clone()

    def __str__(self):
        return ' '.join(map(str,self.__keys)) + ' ' + str(self.__value)

    def __repr__(self):
        return 'Parser.DictKeysValue(' + repr(self.__keys) + ',' + \
                                        repr(self.__value) + ')'

    def clone(self):
        return DictKeysValue(self.__keys,self.__value)

    @property
    def keys(self):
        return self.__keys

    @property
    def value(self):
        return self.__value

class Dict(PsAtom):
    def __init__(self,keysvalues,geometry):
        assert(isinstance(keysvalues,list))
        assert(all(map(lambda x: isinstance(x,DictKeysValue),keysvalues)))

        super(Dict,self).__init__(geometry)

        self.__keysvalues = map(lambda x: x.clone(),keysvalues)

    def __str__(self):
        return '{' + '|'.join(map(str,self.__keysvalues)) + '}'

    def __repr__(self):
        return 'Parser.Dict(' + '[' + ','.join(map(repr,self.__keysvalues)) + '],' + \
                                      repr(self.geometry) + ')'

    def clone(self):
        return Dict(self.__keysvalues,self.geometry)

    @property
    def keysvalues(self):
        return self.__keysvalues

def parse(tokens,pos=0):
    assert(isinstance(tokens,list))
    assert(all(map(lambda x: isinstance(x,Tokenizer.TkAtom),tokens)))
    assert(isinstance(pos,int))
    assert(pos < len(tokens))

    if isinstance(tokens[pos],Tokenizer.CallBeg):
        init_geometry = tokens[pos].geometry
        (pos,action) = parse(tokens,pos+1)
        order_args = []
        named_args = []

        while not isinstance(tokens[pos],Tokenizer.CallEnd):
            (pos,new_arg) = parse(tokens,pos)

            if isinstance(tokens[pos],Tokenizer.CallEqual):
                (pos,value) = parse(tokens,pos+1)
                named_args.append(CallNamedArg(new_arg,value))
            else:
                order_args.append(new_arg)

        geometry = init_geometry.expandTo(tokens[pos].geometry)
        return (pos+1,Call(action,order_args,named_args,geometry))
    elif isinstance(tokens[pos],Tokenizer.CallEnd):
        raise Exception('Invalid ")" character!')
    elif isinstance(tokens[pos],Tokenizer.CallEqual):
        return (pos+1,Symbol(tokens[pos].text,tokens[pos].geometry))
    elif isinstance(tokens[pos],Tokenizer.Lookup):
        init_geometry = tokens[pos].geometry
        names = []

        while pos+1 < len(tokens) and \
              isinstance(tokens[pos],Tokenizer.Lookup) and \
              not isinstance(tokens[pos+1],Tokenizer.Lookup):
            (pos,current_name) = parse(tokens,pos+1)
            names.append(current_name)

        if len(names) == 0:
            raise Exception('Invalid lookup syntax!')

        geometry = init_geometry.expandTo(tokens[pos-1].geometry)
        return (pos,Lookup(names,geometry))
    elif isinstance(tokens[pos],Tokenizer.Symbol):
        return (pos+1,Symbol(tokens[pos].text,tokens[pos].geometry))
    elif isinstance(tokens[pos],Tokenizer.FuncBeg):
        init_geometry = tokens[pos].geometry
        pos = pos + 1
        contents = []
        vararg_name = None
        vararg_minone = None

        while not isinstance(tokens[pos],Tokenizer.FuncEnd):
            (pos,new_item) = parse(tokens,pos)

            if isinstance(tokens[pos],Tokenizer.FuncStar) or \
               isinstance(tokens[pos],Tokenizer.FuncPlus):
                vararg_name = new_item

                if isinstance(tokens[pos],Tokenizer.FuncStar):
                    vararg_minone = False
                else:
                    vararg_minone = True

                pos = pos + 1
                (pos,body) = parse(tokens,pos)
                contents.append(body)

                if not isinstance(tokens[pos],Tokenizer.FuncEnd):
                    raise Exception('Invalid function syntax #2!')
            else:
                contents.append(new_item)

        if len(contents) == 0:
            raise Exception('Invalid function syntax!')

        geometry = init_geometry.expandTo(tokens[pos].geometry)
        return (pos+1,Func(contents[:-1],vararg_name,vararg_minone,contents[-1],geometry))
    elif isinstance(tokens[pos],Tokenizer.FuncEnd):
        raise Exception('Invalid "]" character!')
    elif isinstance(tokens[pos],Tokenizer.FuncStar):
        return (pos+1,Symbol(tokens[pos].text,tokens[pos].geometry))
    elif isinstance(tokens[pos],Tokenizer.FuncPlus):
        return (pos+1,Symbol(tokens[pos].text,tokens[pos].geometry))
    elif isinstance(tokens[pos],Tokenizer.DictBeg):
        init_geometry = tokens[pos].geometry
        pos = pos+1
        keysvalues = []

        while not isinstance(tokens[pos],Tokenizer.DictEnd):
            keysvalue = []

            while not isinstance(tokens[pos],Tokenizer.Column) and \
                  not isinstance(tokens[pos],Tokenizer.DictEnd):
                (pos,newkey) = parse(tokens,pos)
                keysvalue.append(newkey)

            if len(keysvalue) < 2:
                raise Exception('Invalid dictionary format!')

            if isinstance(tokens[pos],Tokenizer.Column):
                pos = pos + 1

            keysvalues.append(DictKeysValue(keysvalue[:-1],keysvalue[-1]))

        geometry = init_geometry.expandTo(tokens[pos].geometry)
        return (pos+1,Dict(keysvalues,geometry))
    elif isinstance(tokens[pos],Tokenizer.DictEnd):
        raise Exception('Invalid "}" character!')
    elif isinstance(tokens[pos],Tokenizer.Column):
        return (pos+1,Symbol(tokens[pos].text,tokens[pos].geometry))
    else:
        raise Exception('Invalid syntax!')

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

class DictKeyValue(object):
    def __init__(self,key,value):
        assert(isinstance(key,PsAtom))
        assert(isinstance(value,PsAtom))

        self.__key = key.clone()
        self.__value = value.clone()

    def __str__(self):
        return str(self.__key) + ' ' + str(self.__value)

    def __repr__(self):
        return 'Parser.DictKeyValue(' + repr(self.__key) + ',' + \
                                        repr(self.__value) + ')'

    def clone(self):
        return DictKeyValue(self.__key,self.__value)

    @property
    def key(self):
        return self.__key

    @property
    def value(self):
        return self.__value

class Dict(PsAtom):
    def __init__(self,keyvalues,geometry):
        assert(isinstance(keyvalues,list))
        assert(all(map(lambda x: isinstance(x,DictKeyValue),keyvalues)))

        super(Dict,self).__init__(geometry)

        self.__keyvalues = map(lambda x: x.clone(),keyvalues)

    def __str__(self):
        return '{' + ' '.join(map(str,self.__keyvalues)) + '}'

    def __repr__(self):
        return 'Parser.Dict(' + '[' + ','.join(map(repr,self.__keyvalues)) + '],' + \
                                      repr(self.geometry) + ')'

    def clone(self):
        return Dict(self.__keyvalues,self.geometry)

    @property
    def keyvalues(self):
        return self.__keyvalues

def parse(tokens,pos=0,in_list=False):
    assert(isinstance(tokens,list))
    assert(all(map(lambda x: isinstance(x,Tokenizer.TkAtom),tokens)))
    assert(isinstance(pos,int))
    assert(pos < len(tokens))

    full_geometry = tokens[pos].geometry
    built_list = []

    while True: # Ugh!
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
            built_list.append(Call(action,order_args,named_args,geometry))
        elif isinstance(tokens[pos],Tokenizer.CallEnd):
            raise Exception('Invalid ")" character!')
        elif isinstance(tokens[pos],Tokenizer.CallEqual):
            built_list.append(Symbol(tokens[pos].text,tokens[pos].geometry))
        elif isinstance(tokens[pos],Tokenizer.Symbol):
            built_list.append(Symbol(tokens[pos].text,tokens[pos].geometry))
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
            built_list.append(Func(contents[:-1],vararg_name,vararg_minone,contents[-1],geometry))
        elif isinstance(tokens[pos],Tokenizer.FuncEnd):
            raise Exception('Invalid "]" character!')
        elif isinstance(tokens[pos],Tokenizer.FuncStar):
            built_list.append(Symbol(tokens[pos].text,tokens[pos].geometry))
        elif isinstance(tokens[pos],Tokenizer.FuncPlus):
            built_list.append(Symbol(tokens[pos].text,tokens[pos].geometry))
        elif isinstance(tokens[pos],Tokenizer.DictBeg):
            init_geometry = tokens[pos].geometry
            pos = pos+1
            keyvalues = []

            while not isinstance(tokens[pos],Tokenizer.DictEnd):
                (pos,key) = parse(tokens,pos)
                (pos,value) = parse(tokens,pos)

                keyvalues.append(DictKeyValue(key,value))

            geometry = init_geometry.expandTo(tokens[pos].geometry)
            built_list.append(Dict(keyvalues,geometry))
        elif isinstance(tokens[pos],Tokenizer.DictEnd):
            raise Exception('Invalid "}" character!')
        elif isinstance(tokens[pos],Tokenizer.DictColumn):
            built_list.append(Symbol(tokens[pos].text,tokens[pos].geometry))
        else:
            raise Exception('Invalid syntax!')

        pos = pos + 1

        if in_list:
            break
        else:
            if pos < len(tokens) and \
               isinstance(tokens[pos],Tokenizer.DictColumn):
                pos = pos + 1
            else:
                break

    if len(built_list) == 1:
        return (pos,built_list[0])
    else:
        new_keyvalues = []
        nogeom = Stream.Geometry(0,Stream.RelPos(0,0),
                                 0,Stream.RelPos(0,0))

        new_keyvalues.append(DictKeyValue(Symbol('Length',nogeom),
                                          Symbol(str(len(built_list)),nogeom)))

        for i in range(0,len(built_list)):
            new_keyvalues.append(DictKeyValue(Symbol(str(i),nogeom),built_list[i]))

        geometry = full_geometry.expandTo(tokens[pos-1].geometry)
        return (pos,Dict(new_keyvalues,geometry))

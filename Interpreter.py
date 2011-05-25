import re

import Stream
import Tokenizer
import Parser

class InAtom(object):
    pass

class Symbol(InAtom):
    def __init__(self,text):
        assert(isinstance(text,str))

        self.__text = str(text)

    def __str__(self):
        if re.search('\s',self.__text):
            return '{' + self.__text + '}'
        else:
            return self.__text

    def __repr__(self):
        return 'Interpreter.Symbol(' + repr(self.__text) + ')'

    def __eq__(self,other):
        if isinstance(other,Symbol):
            return self.__text == other.__text
        else:
            return False

    def clone(self):
        return Symbol(self.__text)

    @property
    def text(self):
        return self.__text

class Func(InAtom):
    def __init__(self,arg_names,vararg_name,vararg_minone,body,env):
        assert(isinstance(arg_names,list))
        assert(all(map(lambda x: isinstance(x,str),arg_names)))
        assert(vararg_name == None or isinstance(vararg_name,str))
        assert((vararg_name == None and vararg_minone == None) or \
               (vararg_name != None and isinstance(vararg_minone,bool)))
        assert(isinstance(body,Parser.PsAtom))
        assert(isinstance(env,dict))
        assert(all(map(lambda x: isinstance(x,str),env.keys())))
        assert(all(map(lambda x: isinstance(x,InAtom),env.keys())))

        self.__arg_names = map(lambda x: str(x),arg_names)
        self.__vararg_name = str(vararg_name) if vararg_name else None
        self.__vararg_minone = vararg_minone
        self.__body = body.clone()
        self.__env = dict(env)

    def __str__(self):
        s_env = '{' + ','.join(map(lambda x: str(x) + ':' + str(self.__env[x]),
                                   self.__env.keys())) + '}'

        if self.__vararg_name:
            return '[' + ' '.join(map(str,self.__arg_names)) + \
                        (' ' if self.__arg_names != [] else '') + \
                        str(self.__vararg_name) + ('+ ' if self.__vararg_minone else '* ') + \
                        str(self.__body) + ' ' + s_env + ']'
        else:
            return '[' + ' '.join(map(str,self.__arg_names)) + \
                        (' ' if self.__arg_names != [] else '') + \
                        str(self.__body) + ' ' + s_env + ']'

    def __repr__(self):
        return 'Interpreter.Func(' + '[' + ','.join(map(repr,self.__arg_names)) + '],' + \
                                     repr(self.__vararg_name) + ',' + \
                                     repr(self.__vararg_minone) + ',' + \
                                     repr(self.__body) + ',' + repr(self.__env) + ')'

    def __eq__(self,other):
        return False

    def clone(self):
        return Func(self.__arg_name,self.__vararg_name,self.__vararg_minone,
                    self.__body,self.__env)

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

    @property
    def env(self):
        return self.__env

class DictKeyValue(object):
    def __init__(self,key,value):
        assert(isinstance(key,InAtom))
        assert(isinstance(value,InAtom))

        self.__key = key.clone()
        self.__value = value.clone()

    def __str__(self):
        return str(self.__key) + ' ' + str(self.__value)

    def __repr__(self):
        return 'Interpreter.DictKeyValue(' + repr(self.__key) + ',' + \
                                             repr(self.__value) + ')'

    def __eq__(self,other):
        if isinstance(other,DictKeyValue):
            return self.__key == other.__key and \
                   self.__value == other.__value
        else:
            return False

    def clone(self):
        return DictKeyValue(self.__key,self.__value)

    @property
    def key(self):
        return self.__key

    @property
    def value(self):
        return self.__value

class Dict(InAtom):
    def __init__(self,keyvalues):
        assert(isinstance(keyvalues,list))
        assert(all(map(lambda x: isinstance(x,DictKeyValue),keyvalues)))

        self.__keyvalues = map(lambda x: x.clone(),keyvalues)

    def __str__(self):
        return '{' + ' '.join(map(str,self.__keyvalues)) + '}'

    def __repr__(self):
        return 'Parser.Dict(' + '[' + ','.join(map(repr,self.__keyvalues)) + '])'

    def __eq__(self,other):
        if isinstance(other,Dict):
            if len(self.__keyvalues) == len(other.__keyvalues):
                for kv in self.__keyvalues:
                    if kv not in other.__keyvalues:
                        return False

                return True
            else:
                return False
        else:
            return False

    def clone(self):
        return Dict(self.__keyvalues)

    @property
    def keyvalues(self):
        return self.__keyvalues

def interpret(atom,args,env):
    assert(isinstance(atom,Parser.PsAtom))
    assert(isinstance(args,dict))
    assert(all(map(lambda x: isinstance(x,str),args.keys())))
    assert(all(map(lambda x: isinstance(x,InAtom),args.values())))
    assert(isinstance(env,dict))
    assert(all(map(lambda x: isinstance(x,str),env.keys())))
    assert(all(map(lambda x: isinstance(x,InAtom),env.values())))

    if isinstance(atom,Parser.Call):
        fn = interpret(atom.action,args,env)

        if isinstance(fn,Symbol):
            if fn.text in args:
                func = args[fn.text]
            elif fn.text in env:
                func = env[fn.text]
            else:
                raise Exception('Unknown function "' + fn.text + '"!')
        elif isinstance(fn,Func):
            func = fn
        elif isinstance(fn,Dict):
            func = fn
        else:
            pass

        if isinstance(func,Symbol):
            if len(atom.orderArgs) == 0 and len(atom.namedArgs) == 0:
                return func
            else:
                raise Exception('Cannot apply symbol "' + func.text + '"!')
        if isinstance(func,Func):
            new_args = dict([(name,None) for name in func.argNames])

            for nv in atom.namedArgs:
                name = interpret(nv.name,args,env)
                value = interpret(nv.value,args,env)

                if not isinstance(name,Symbol):
                    raise Exception('Named argument must be a Symbol!')

                if name.text not in new_args:
                    raise Exception('Invalid argument "' + name.text + '"!')

                new_args[name.text] = value

            idx = 0

            for name in func.argNames:
                if new_args[name] == None:
                    if idx < len(atom.orderArgs):
                        value = interpret(atom.orderArgs[idx],args,env)
                        new_args[name] = value
                        idx = idx + 1
                    else:
                        raise Exception('Too few arguments in call to function!')

            # We have varargs
            if idx < len(atom.orderArgs):
                raise Exception('Too many arguments in call to function!')

            return interpret(func.body,new_args,func.env)
        if isinstance(func,Dict):
            if len(atom.orderArgs) == 1 and len(atom.namedArgs) == 0:
                key = interpret(atom.orderArgs[0],args,env)

                for kv in func.keyvalues:
                    if key == kv.key:
                        return kv.value

                raise Exception('Cannot find key "' + key.text + '" in dictionary!')
            else:
                raise Exception('Invalid form of dictionary access!')

        raise Exception('Should not be here!')
    if isinstance(atom,Parser.Symbol):
        return Symbol(atom.text)
    if isinstance(atom,Parser.Func):
        arg_names = []
        vararg_name = None
        vararg_minone = None

        for arg_name in atom.argNames:
            name = interpret(arg_name,args,env)

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anyhting but Symbol!')

            arg_names.append(name.text)

        if atom.hasVararg:
            name = interpret(atom.varargName,args,env)

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anyhting but Symbol!')

            vararg_name = name.text
            vararg_minone = atom.varargMinOne

        return Func(arg_names,vararg_name,vararg_minone,atom.body,env)
    if isinstance(atom,Parser.Dict):
        keyvalues = []

        for kv in atom.keyvalues:
            key = interpret(kv.key,args,env)
            value = interpret(kv.value,args,env)

            keyvalues.append(DictKeyValue(key,value))

        return Dict(keyvalues)

    raise Exception('Shouln\'t have gotten here!')

import re
import inspect

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
            return '`' + self.__text + '`'
        else:
            return self.__text

    def __repr__(self):
        return 'Interpreter.Symbol(' + repr(self.__text) + ')'

    def __eq__(self,other):
        if not isinstance(other,Symbol):
            return False

        return self.__text == other.__text

    def clone(self):
        return Symbol(self.__text)

    @property
    def text(self):
        return self.__text

class BuiltIn(InAtom):
    def __init__(self,func):
        assert(hasattr(func,'__call__'))

        arginfo = inspect.getargspec(func)

        self.__arg_names = arginfo.args
        self.__vararg_name = arginfo.varargs
        self.__vararg_minone = False
        self.__func = func

    def __str__(self):
        return '[' + ' '.join(map(str,self.__arg_names)) + \
                     (' ' if len(self.__arg_names) > 0 else '') + \
                     (str(self.__vararg_name) + \
                      ('+ ' if self.__vararg_minone else '* ') if self.__vararg_name else '') + \
                     '<<BuiltIn "' + self.__func.__name__ + '">>]'

    def __repr__(self):
        fullname = inspect.getmodule(self.__func) + '.' + self.__func.__name__
        return 'Interpreter.BuiltIn(' + fullname + ')'

    def __eq__(self,other):
        return False

    def clone(self):
        return BuiltIn(self.__func)

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
    def func(self):
        return self.__func

class Func(InAtom):
    def __init__(self,arg_names,vararg_name,vararg_minone,body,env):
        assert(isinstance(arg_names,list))
        assert(all(map(lambda x: isinstance(x,str),arg_names)))
        assert(vararg_name == None or isinstance(vararg_name,str))
        assert((vararg_name == None and vararg_minone == None) or \
                vararg_name != None and isinstance(vararg_minone,bool))
        assert(isinstance(body,Parser.PsAtom))
        assert(isinstance(env,list))
        assert(all(map(lambda x: isinstance(x,dict),env)))
        assert(all(map(lambda x: all(map(lambda y: isinstance(y,str),x.keys())),env)))
        assert(all(map(lambda x: all(map(lambda y: isinstance(y,InAtom),x.values())),env)))

        self.__arg_names = map(lambda x: str(x),arg_names)
        self.__vararg_name = str(vararg_name) if vararg_name else None
        self.__vararg_minone = vararg_minone
        self.__body = body.clone()
        self.__env = map(lambda x: dict([(str(y),x[y].clone()) for y in x]),env)

    def __str__(self):
        return '[' + ' '.join(map(str,self.__arg_names)) + \
                     (' ' if len(self.__arg_names) > 0 else '') + \
                     (str(self.__vararg_name) + \
                      ('+ ' if self.__vararg_minone else '* ') if self.__vararg_name else '') + \
                     str(self.__body) + ']'

    def __repr__(self):
        return 'Interpreter.Func(' + repr(self.__arg_names) + ',' + repr(self.__vararg_name) + \
                                     repr(self.__vararg_minone) + ',' + repr(self.__body) + \
                                     repr(self.__env) + ')'

    def __eq__(self,other):
        return False

    def clone(self):
        return Func(self.__arg_names,self.__vararg_name,self.__vararg_minone,
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

class Dict(InAtom):
    def __init__(self,keyvalues):
        assert(isinstance(keyvalues,list))
        assert(all(map(lambda x: isinstance(x,tuple),keyvalues)))
        assert(all(map(lambda x: isinstance(x[0],InAtom),keyvalues)))
        assert(all(map(lambda x: isinstance(x[1],InAtom),keyvalues)))

        self.__keyvalues = map(lambda x: (x[0].clone(),x[1].clone()),keyvalues)

    def __str__(self):
        return '<' + ' '.join(map(lambda x: str(x[0]) + ' ' + str(x[1]),self.__keyvalues)) + '>'

    def __repr__(self):
        return 'Interpreter.Dict(' + repr(self.__keyvalues) + ')'

    def __eq__(self,other):
        if not isinstance(other,Dict):
            return False

        if len(self.__keyvalues) != len(other.__keyvalues):
            return False

        for (key,value) in self.__keyvalues:
            for (okey,ovalue) in self.__keyvalues:
                if key == okey:
                    break
            else:
                return False

        return True

    def lookup(self,key):
        assert(isinstance(key,InAtom))

        for (k,v) in self.__keyvalues:
            if key == k:
                return v

        raise Exception('Cannot find key "' + str(key) + '"!')

    def lookupS(self,key):
        assert(isinstance(key,str))

        for (k,v) in self.__keyvalues:
            if isinstance(k,Symbol) and key == k.text:
                return v

        raise Exception('Cannot find key "' + key + '"!')

    def clone(self):
        return Dict(self.__keyvalues)

    @property
    def keyvalues(self):
        return self.__keyvalues

def interpret(atom,env):
    assert(isinstance(atom,Parser.PsAtom))
    assert(isinstance(env,list))
    assert(all(map(lambda x: isinstance(x,dict),env)))
    assert(all(map(lambda x: all(map(lambda y: isinstance(y,str),x.keys())),env)))
    assert(all(map(lambda x: all(map(lambda y: isinstance(y,InAtom),x.values())),env)))

    if isinstance(atom,Parser.Call):
        action = interpret(atom.action,env)

        if isinstance(action,Symbol):
            for one_env in reversed(env):
                if action.text in one_env:
                    fn = one_env[action.text]
                    break
            else:
                raise Exception('Couldn\'t find name "' + action.text + '"!')
        elif isinstance(action,Func):
            fn = action
        elif isinstance(action,Dict):
            fn = action
        else:
            raise Exception('Now, this shouldn\'t really happen!')

        if isinstance(fn,Symbol):
            raise Exception('Cannot call a symbol!')
        elif isinstance(fn,BuiltIn) or isinstance(fn,Func):
            args = dict([(name,None) for name in fn.argNames])
            total_arg_cnt = len(atom.namedArgs) + len(atom.orderArgs)

            if fn.hasVararg:
                if fn.varargMinOne:
                    if len(args) >= total_arg_cnt:
                        raise Exception('Invalid number of arguments!')
                else:
                    if len(args) > total_arg_cnt:
                        raise Exception('Invalid number of arguments!')
            else:
                if len(args) != total_arg_cnt:
                    raise Exception('Invalid number of arguments!')

            for named_arg in atom.namedArgs:
                named_name = interpret(named_arg.name,env)

                if not isinstance(named_name,Symbol):
                    raise Exception('Invalid argument name type!')

                if named_name.text not in args:
                    raise Exception('Invalid argument name "' + named_name.text + '"!')

                if args[named_name.text] != None:
                    raise Exception('Argument "' + named_name.text + '" was specified twice!')

                args[named_name.text] = interpret(named_arg.value,env)

            carg = 0

            for order_args in fn.argNames:
                if args[order_args] == None:
                    args[order_args] = interpret(atom.orderArgs[carg],env)
                    carg = carg + 1

            if isinstance(fn,BuiltIn):
                inorder_args = [args[arg_name] for arg_name in fn.argNames]

                if fn.hasVararg:
                    vararg_i = 0
                    vararg_cnt = total_arg_cnt - len(args)

                    while vararg_i < vararg_cnt:
                        inorder_args.append(interpret(atom.orderArgs[carg],env))
                        vararg_i = vararg_i + 1
                        carg = carg + 1

                return fn.func(*inorder_args)
            else:
                if fn.hasVararg:
                    vararg_i = 0
                    vararg_cnt = total_arg_cnt - len(args)
                    vararg_kvs = [(Symbol('Length'),Symbol(str(vararg_cnt)))]
        
                    while vararg_i < vararg_cnt:
                        vararg_kvs.append((Symbol(str(vararg_i)),
                                           interpret(atom.orderArgs[carg],env)))
                        vararg_i = vararg_i + 1
                        carg = carg + 1
        
                    args[fn.varargName] = Dict(vararg_kvs)
    
                new_env = fn.env
                new_env.append(args)
    
                return interpret(fn.body,new_env)
        elif isinstance(fn,Dict):
            if len(atom.orderArgs) == 1 and len(atom.namedArgs) == 0:
                return fn.lookup(interpret(atom.orderArgs[0],env))
            else:
                raise Exception('Invalid syntax for dictionary lookup!')
        else:
            raise Exception('This again, should not be the case!')
    elif isinstance(atom,Parser.Lookup):
        for one_env in reversed(env):
            if atom.name.text in one_env:
                return one_env[atom.name.text]

        raise Exception('Can\'t find name "' + atom.name.text + '"!')
    elif isinstance(atom,Parser.Symbol):
        return Symbol(atom.text)
    elif isinstance(atom,Parser.Func):
        arg_names = []
        vararg_name = None
        vararg_minone = None

        for arg_name in atom.argNames:
            name = interpret(arg_name,env)

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but Symbol!')

            arg_names.append(name.text)

        if atom.hasVararg:
            name = interpret(atom.varargName,env)

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but Symbol!')

            vararg_name = name.text
            vararg_minone = atom.varargMinOne

        return Func(arg_names,vararg_name,vararg_minone,atom.body,env)
    elif isinstance(atom,Parser.Dict):
        keyvalues = []

        for item in atom.keyvalues:
            keyvalues.append((interpret(item.key,env),
                              interpret(item.value,env)))

        return Dict(keyvalues)
    else:
        raise Exception('Invalid atom!')

import re
import inspect
import numbers

import Stream
import Tokenizer
import Parser

class InAtom(object):
    pass

class Boolean(InAtom):
    def __init__(self,value):
        assert(isinstance(value,bool))

        self.__value = value

    def __str__(self):
        return '#T' if self.__value else '#F'

    def __repr__(self):
        return 'Interpreter.Boolean(' + repr(self.__value) + ')'

    def __eq__(self,other):
        if not isinstance(other,Boolean):
            return False

        return self.__value == other.__value

    def clone(self):
        return Boolean(self.__value)

    @property
    def value(self):
        return self.__value

class Number(InAtom):
    def __init__(self,value):
        assert(isinstance(value,numbers.Number))

        self.__value = value

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return 'Interpreter.Number(' + repr(self.__value) + ')'

    def __eq__(self,other):
        if not isinstance(other,Number):
            return False

        return self.__value == other.__value

    def clone(self):
        return Number(self.__value)

    @property
    def value(self):
        return self.__value

class Symbol(InAtom):
    def __init__(self,value):
        assert(isinstance(value,str))

        self.__value = str(value)

    def __str__(self):
        return self.__value

    def __repr__(self):
        return 'Interpreter.Symbol(' + repr(self.__value) + ')'

    def __eq__(self,other):
        if not isinstance(other,Symbol):
            return False

        return self.__value == other.__value

    def clone(self):
        return Symbol(self.__value)

    @property
    def value(self):
        return self.__value

class String(InAtom):
    def __init__(self,value):
        assert(isinstance(value,str))

        self.__value = str(value)

    def __str__(self):
        return '\'' + self.__value + '\''

    def __repr__(self):
        return 'Interpreter.String(' + repr(self.__value) + ')'

    def __eq__(self,other):
        if not isinstance(other,String):
            return False

        return self.__value == other.__value

    def clone(self):
        return String(self.__value)

    @property
    def value(self):
        return self.__value

class FuncArg(object):
    def __init__(self,name,default):
        assert(isinstance(name,str))
        assert(default == None or isinstance(default,InAtom))

        self.__name = str(name)
        self.__default = default.clone() if default != None else None

    def __str__(self):
        return self.__name + \
               ('=' + str(self.__default) if self.__default else '')

    def __repr__(self):
        return 'Interpreter.FuncArg(' + repr(self.__name) + ',' + \
                                        repr(self.__default) + ')'

    def clone(self):
        return FuncArg(self.__name,self.__default)

    @property
    def name(self):
        return self.__name

    @property
    def default(self):
        return self.__default

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
        fullname = inspect.getmodule(self.__func).__name__ + '.' + self.__func.__name__
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
    def __init__(self,reqarg_names,optarg_names,vararg_name,vararg_minone,body,env):
        assert(isinstance(reqarg_names,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),reqarg_names)))
        assert(isinstance(optarg_names,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),optarg_names)))
        assert(vararg_name == None or isinstance(vararg_name,str))
        assert((vararg_name == None and vararg_minone == None) or \
                vararg_name != None and isinstance(vararg_minone,bool))
        assert(isinstance(body,Parser.PsAtom))
        assert(isinstance(env,list))
        assert(all(map(lambda x: isinstance(x,dict),env)))
        assert(all(map(lambda x: all(map(lambda y: isinstance(y,str),x.keys())),env)))
        assert(all(map(lambda x: all(map(lambda y: isinstance(y,InAtom),x.values())),env)))

        self.__reqarg_names = map(lambda x: x.clone(),reqarg_names)
        self.__optarg_names = map(lambda x: x.clone(),optarg_names)
        self.__vararg_name = str(vararg_name) if vararg_name else None
        self.__vararg_minone = vararg_minone
        self.__body = body.clone()
        self.__env = map(lambda x: dict([(str(y),x[y].clone()) for y in x]),env)

    def __str__(self):
        if self.__vararg_name:
            return '[' + ' '.join(map(str,self.__reqarg_names)) + \
                        (' ' if self.__reqarg_names != [] else '') + \
                         ' '.join(map(lambda x: str(x) + '?',self.__optarg_names)) + \
                        (' ' if self.__optarg_names != [] else '') + \
                        str(self.__vararg_name) + ('+ ' if self.__vararg_minone else '* ') + \
                        str(self.__body) + ']'
        else:
            return '[' + ' '.join(map(str,self.__reqarg_names)) + \
                        (' ' if self.__reqarg_names != [] else '') + \
                         ' '.join(map(lambda x: str(x) + '?',self.__optarg_names)) + \
                        (' ' if self.__optarg_names != [] else '') + \
                        str(self.__body) + ']'

    def __repr__(self):
        return 'Interpreter.Func(' + '[' + ','.join(map(repr,self.__reqarg_names)) + '],' + \
                                     '[' + ','.join(map(repr,self.__optarg_names)) + '],' + \
                                     repr(self.__vararg_name) + ',' + \
                                     repr(self.__vararg_minone) + ',' + \
                                     repr(self.__body) + ',' + repr(self.__env) + ')'

    def __eq__(self,other):
        return False

    def clone(self):
        return Func(self.__reqarg_names,self.__optarg_names,
                    self.__vararg_name,self.__vararg_minone,
                    self.__body,self.__env)

    @property
    def reqargNames(self):
        return self.__reqarg_names

    @property
    def optargNames(self):
        return self.__optarg_names

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

    def lookupV(self,key):
        for (k,v) in self.__keyvalues:
            if isinstance(k,Boolean) or isinstance(k,Number) or \
               isinstance(k,Symbol) or isinstance(k,String):
                if key == k.value:
                    return v

        raise Exception('Cannot find key "' + key + '"!')

    def clone(self):
        return Dict(self.__keyvalues)

    @property
    def keyvalues(self):
        return self.__keyvalues

def interpret(atom,env,curr_func):
    assert(isinstance(atom,Parser.PsAtom))
    assert(isinstance(env,list))
    assert(all(map(lambda x: isinstance(x,dict),env)))
    assert(all(map(lambda x: all(map(lambda y: isinstance(y,str),x.keys())),env)))
    assert(all(map(lambda x: all(map(lambda y: isinstance(y,InAtom),x.values())),env)))
    assert(curr_func == None or isinstance(curr_func,Func))
    
    if isinstance(atom,Parser.Call):
        action = interpret(atom.action,env,curr_func)

        if isinstance(action,Boolean):
            raise Exception('Cannot call a boolean!')
        elif isinstance(action,Number):
            raise Exception('Cannot call a number!')
        elif isinstance(action,Symbol):
            for one_env in reversed(env):
                if action.value in one_env:
                    fn = one_env[action.value]
                    break
            else:
                raise Exception('Couldn\'t find name "' + action.value + '"!')
        elif isinstance(action,String):
            raise Exception('Cannot call a string!')
        elif isinstance(action,Func):
            fn = action
        elif isinstance(action,Dict):
            fn = action
        else:
            raise Exception('Should not have gotten here!')

        if isinstance(fn,Boolean):
            if len(atom.orderArgs) == 0 and len(atom.namedArgs) == 0:
                return fn
            else:
                raise Exception('Cannot apply arguments to a boolean!')
        elif isinstance(fn,Number):
            if len(atom.orderArgs) == 0 and len(atom.namedArgs) == 0:
                return fn
            else:
                raise Exception('Cannot apply arguments to a number!')
        elif isinstance(fn,Symbol):
            if len(atom.orderArgs) == 0 and len(atom.namedArgs) == 0:
                return fn
            else:
                raise Exception('Cannot apply arguments to a symbol!')
        elif isinstance(fn,String):
            if len(atom.orderArgs) == 0 and len(atom.namedArgs) == 0:
                return fn
            else:
                raise Exception('Cannot apply arguments to a string!')
        elif isinstance(fn,Func) or isinstance(fn,BuiltIn):
            if len(atom.orderArgs) == 0 and len(atom.namedArgs) == 0:
                return fn
            else:
                reqargs = dict([(arg.name,(arg.default,False)) for arg in fn.reqargNames])
                optargs = dict([(arg.name,(arg.default,False)) for arg in fn.optargNames])
                used_opt_names = 0

                for named_arg in atom.namedArgs:
                    named_name = interpret(named_arg.name,env,curr_func)

                    if not isinstance(named_name,Symbol):
                        raise Exception('Invalid argument name type!')

                    if named_name.value in reqargs:
                        if reqargs[named_name.value][1]:
                            raise Exception('Argument "' + named_name.value + '" was used twice!')

                        reqargs[named_name.value] = (interpret(named_arg.value,env,curr_func),True)
                    elif named_name.value in optargs:
                        if optargs[named_name.value][1]:
                            raise Exception('Argument "' + named_name.value + '" was used twice!')

                        optargs[named_name.value] = (interpret(named_arg.value,env,curr_func),True)
                        used_opt_names = used_opt_names + 1
                    else:
                        raise Exception('Invalid argument name "' + named_name.value + '"!')

                carg = 0

                for order_args in fn.reqargNames:
                    if reqargs[order_args.name][0] == None or \
                       (reqargs[order_args.name][0] != None and reqargs[order_args.name][1] == False):
                        if carg >= len(atom.orderArgs):
                            raise Exception('Too few arguments!')

                        reqargs[order_args.name] = (interpret(atom.orderArgs[carg],env,curr_func),True)
                        carg = carg + 1

                if isinstance(fn,BuiltIn):
                    pass
                else:
                    if fn.hasVararg:
                        vararg_i = carg
                        vararg_kvs = [(Symbol('Length'),Symbol(str(vararg_cnt)))]

                        while vararg_i < len(atom.orderArgs):
                            vararg_kvs.append((Symbol(str(vararg_i - carg)),
                                               interpret(atom.orderArgs[vararg_i],env,curr_func)))
                            vararg_i = vararg_i + 1

                        reqargs[fn.varargName] = (Dict(vararg_kvs),True)
                    else:
                        if len(fn.reqargNames) != len(atom.orderArgs) + len(atom.namedArgs) - used_opt_names:
                            raise Exception('Too many arguments!')

                    args = {}

                    for reqarg_name,(reqarg_value,reqarg_used) in reqargs.iteritems():
                        if not reqarg_value:
                            raise Exception('Argument "' + reqarg_name + '" has no value!')

                        args[reqarg_name] = reqarg_value

                    for optarg_name,(optarg_value,optarg_used) in optargs.iteritems():
                        if not optarg_value:
                            raise Exception('Argument "' + optarg_name + '" has no value!')

                        args[optarg_name] = optarg_value

                    new_env = [dict([(k,v.clone()) for (k,v) in e.iteritems()]) for e in fn.env]
                    new_env.append(args)

                    return interpret(fn.body,new_env,fn)
        elif isinstance(fn,Dict):
            if len(atom.orderArgs) == 0 and len(atom.namedArgs) == 0:
                return fn
            elif len(atom.orderArgs) == 1 and len(atom.namedArgs) == 0:
                return fn.lookup(interpret(atom.orderArgs[0],env,curr_func))
            else:
                raise Exception('Cannot apply more than one argument to a dictionary!')
        else:
            raise Exception('Should not have gotten here!')
    elif isinstance(atom,Parser.Boolean):
        if atom.text == '#T':
            return Boolean(True)
        else:
            return Boolean(False)
    elif isinstance(atom,Parser.Number):
        return Number(float(atom.text))
    elif isinstance(atom,Parser.Symbol):
        return Symbol(atom.text)
    elif isinstance(atom,Parser.String):
        return String(atom.text)
    elif isinstance(atom,Parser.StringEval):
        raise Exception('Execution path not yet implemented!')
    elif isinstance(atom,Parser.Self):
        return curr_func
    elif isinstance(atom,Parser.Func):
        reqarg_names = []
        optarg_names = []
        vararg_name = None
        vararg_minone = None

        names = set()

        for reqarg_name in atom.reqargNames:
            name = interpret(reqarg_name.name,env,curr_func)
            default = interpret(reqarg_name.default,env,curr_func) if reqarg_name.default else None
            
            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but a Symbol!')

            if name.value in names:
                raise Exception('Argument "' + name.value + '" is used twice!')

            reqarg_names.append(FuncArg(name.value,default))
            names.add(name.value)

        for optarg_name in atom.optargNames:
            name = interpret(optarg_name.name,env,curr_func)
            default = interpret(optarg_name.default,env,curr_func) if optarg_name.default else None
            
            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but a Symbol!')

            if name.value in names:
                raise Exception('Argument "' + name.value + '" is used twice!')

            optarg_names.append(FuncArg(name.value,default))
            names.add(name.value)

        if atom.hasVararg:
            name = interpret(atom.varargName,env,curr_func)

            if not isinstance(name,Symbol):
                raise Exception('Variable argument name can\'t be anython but a Symbol!')

            if name.value in names:
                raise Exception('Argument "' + name.value + '" is used twice!')

            vararg_name = name.value
            vararg_minone = atom.varargMinOne

        return Func(reqarg_names,optarg_names,vararg_name,vararg_minone,atom.body,env)
    elif isinstance(atom,Parser.Dict):
        keyvalues = []

        for (key,value) in atom.keyvalues:
            keyvalues.append((interpret(key,env,curr_func),
                              interpret(value,env,curr_func)))

        return Dict(keyvalues)
    else:
        raise Exception('Should not have gotten here!')

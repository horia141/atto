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
    def hasDefault(self):
        return self.__default != None

    @property
    def default(self):
        return self.__default

class Func(InAtom):
    def __init__(self,order,order_defs,order_var,named,named_defs,named_var,body,env):
        assert(isinstance(order,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),order)))
        assert(isinstance(order_defs,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),order_defs)))
        assert(order_var == None or isinstance(order_var,str))
        assert(isinstance(named,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),named)))
        assert(isinstance(named_defs,list))
        assert(all(map(lambda x: isinstance(x,FuncArg),named_defs)))
        assert(named_var == None or isinstance(named_var,str))
        assert(isinstance(body,Parser.PsAtom))
        assert(isinstance(env,dict))
        assert(all(map(lambda x: isinstance(x,str),env.iterkeys())))
        assert(all(map(lambda x: isinstance(x,InAtom),env.itervalues())))

        self.__order = map(lambda x: x.clone(),order)
        self.__order_defs = map(lambda x: x.clone(),order_defs)
        self.__order_var = str(order_var) if order_var else None
        self.__named = map(lambda x: x.clone(),named)
        self.__named_defs = map(lambda x: x.clone(),named_defs)
        self.__named_var = str(named_var) if named_var else None
        self.__body = body.clone()
        self.__env = dict([(str(k),v.clone()) for (k,v) in env.iteritems()])

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
        return 'Interpreter.Func(' + repr(self.__order) + ',' + \
                                     repr(self.__order_defs) + ',' + \
                                     repr(self.__order_var) + ',' + \
                                     repr(self.__named) + ',' + \
                                     repr(self.__named_defs) + ',' + \
                                     repr(self.__named_var) + ',' + \
                                     repr(self.__body) + ',' + \
                                     repr(self.__env) + ')'

    def __eq__(self,other):
        return False

    def apply(self,order_args,named_args):
        assert(isinstance(order_args,list))
        assert(all(map(lambda x: isinstance(x,InAtom),order_args)))
        assert(isinstance(named_args,dict))
        assert(all(map(lambda x: isinstance(x,str),named_args.keys())))
        assert(all(map(lambda x: isinstance(x,InAtom),named_args.values())))

        order = dict([(arg.name,arg.default) for arg in self.__order])
        order_defs = dict([(arg.name,arg.default) for arg in self.__order_defs])
        order_var = {}
        order_pos = 0

        named = dict([(arg.name,arg.default) for arg in self.__named])
        named_defs = dict([(arg.name,arg.default) for arg in self.__named_defs])
        named_var = {}
        named_var_kvs = []
        named_pos = 0

        if len(order_args) < len(self.__order):
            raise Exception('Can\'t cover order arguments!')

        if len(order_args) > len(self.__order) + len(self.__order_defs) and not self.hasOrderVar:
            raise Exception('Too many order arguments!')

        if len(named_args) < len(self.__named):
            raise Exception('Can\'t cover named arguments!')

        if len(named_args) > len(self.__named) + len(self.__named_defs) and not fn.hasNamedVar:
            raise Exception('Too many named arguments!')

        for arg in self.__order:
            order[arg.name] = order_args[order_pos]
            order_pos = order_pos + 1

        for arg in self.__order_defs:
            if order_pos < len(order_args):
                order_defs[arg.name] = order_args[order_pos]
                order_pos = order_pos + 1
            else:
                break

        if self.hasOrderVar:
            var_kvs = [(Symbol('Length'),Number(len(order_args) - order_pos))]

            for i in range(order_pos,len(order_args)):
                var_kvs.append((Number(i - order_pos),order_args[i]))

            order_var[self.__order_var] = Dict(var_kvs)

        for (name,value) in named_args.iteritems():
            # These cases are mutually exclusive and are the only four possibilities
            # given our assumptions about Call and Func.
            if name in named:
                named[name] = value
            elif name in named_defs:
                named_defs[name] = value
            elif fn.hasNamedVar:
                named_var_kvs.append((Symbol(name),value))
            else:
                raise Exception('Function does not have argument "' + name + '"!')

        if self.hasNamedVar:
            named_var[self.__named_var] = Dict(named_var_kvs)

        new_env = dict([(str(k),v.clone()) for (k,v) in self.__env.iteritems()])
        new_env.update(order)
        new_env.update(order_defs)
        new_env.update(order_var)
        new_env.update(named)
        new_env.update(named_defs)
        new_env.update(named_var)
    
        return interpret(self.__body,new_env,self)

    def curry(self,va):
        pass

    def orderInject(self,order_arg):
        assert(isinstance(order_arg,str))

        self.__order.insert(0,FuncArg(order_arg,None))

    def namedInject(self,named_arg):
        assert(isinstance(named_arg,str))

        self.__named.insert(0,FuncArg(named_arg,None))

    def clone(self):
        return Func(self.__order,self.__order_defs,self.__order_var,
                    self.__named,self.__named_defs,self.__named_var,
                    self.__body,self.__env)

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

    @property
    def env(self):
        return self.__env

class BuiltIn(InAtom):
    def __init__(self,func):
        assert(hasattr(func,'__call__'))

        BUILTIN_ORDER = 0
        BUILTIN_ORDER_VAR = 1
        BUILTIN_NAMED = 2
        BUILTIN_NAMED_VAR = 3
        BUILTIN_STOP = 4

        arginfo = inspect.getargspec(func)
        state = BUILTIN_ORDER
        order = []
        order_var = None
        named = []
        named_var = None
        pos = 0

        assert(arginfo.varargs == None)
        assert(arginfo.keywords == None)
        assert(arginfo.defaults == None)

        while pos < len(arginfo.args) and state != BUILTIN_STOP:
            if state == BUILTIN_ORDER:
                if arginfo.args[pos].endswith('_star'):
                    state = BUILTIN_ORDER_VAR
                    order_var = arginfo.args[pos]
                    pos = pos + 1
                elif arginfo.args[pos].endswith('_bang'):
                    state = BUILTIN_NAMED
                    named.append(FuncArg(arginfo.args[pos],None))
                    pos = pos + 1
                elif arginfo.args[pos].endswith('_plus'):
                    state = BUILTIN_NAMED_VAR
                    named_var = arginfo.args[pos]
                    pos = pos + 1
                else:
                    state = BUILTIN_ORDER
                    order.append(FuncArg(arginfo.args[pos],None))
                    pos = pos + 1
            elif state == BUILTIN_ORDER_VAR:
                if arginfo.args[pos].endswith('_star'):
                    raise Exception('Only one variable order argument allowed!')
                elif arginfo.args[pos].endswith('_bang'):
                    state = BUILTIN_NAMED
                    named.append(FuncArg(arginfo.args[pos],None))
                    pos = pos + 1
                elif arginfo.args[pos].endswith('_plus'):
                    state = BUILTIN_NAMED_VAR
                    named_var = arginfo.args[pos]
                    pos = pos + 1
                else:
                    raise Exception('Cannot use order arguments after variable one!')
            elif state == BUILTIN_NAMED:
                if arginfo.args[pos].endswith('_star'):
                    raise Exception('Cannot use variable order argument after named ones!')
                elif arginfo.args[pos].endswith('_bang'):
                    state = BUILTIN_NAMED
                    named.append(FuncArg(arginfo.args[pos],None))
                    pos = pos + 1
                elif arginfo.args[pos].endswith('_plus'):
                    state = BUILTIN_NAMED_VAR
                    named_var = arginfo.args[pos]
                    pos = pos + 1
                else:
                    raise Exception('Cannot use order arguments after named ones!')
            elif state == BUILTIN_NAMED_VAR:
                raise Exception('Invalid argument after named variable one!')
            else:
                raise Exception('Critical Error: Invalid BuiltIn FSM Path!')

        self.__order = order
        self.__order_var = order_var
        self.__named = named
        self.__named_var = named_var
        self.__func = func

    def __str__(self):
        def spIfNNil(ls):
            return ' ' if len(ls) > 0 else ''

        return '[' + ' '.join(map(str,self.__order)) + spIfNNil(self.__order) + \
                     (str(self.__order_var) + '* ' if self.__order_var else '') + \
                     ' '.join(map(str,self.__named)) + spIfNNil(self.__named) + \
                     (str(self.__named_var) + '* ' if self.__named_var else '') + \
                     '<<BuiltIn "' + self.__func.__name__ + '">>]'

    def __repr__(self):
        fullname = inspect.getmodule(self.__func).__name__ + '.' + self.__func.__name__
        return 'Interpreter.BuiltIn(' + fullname + ')'

    def __eq__(self,other):
        return False

    def clone(self):
        return BuiltIn(self.__func)

    @property
    def order(self):
        return self.__order

    @property
    def orderDefs(self):
        return []

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
        return []

    @property
    def hasNamedVar(self):
        return self.__named_var != None

    @property
    def namedVar(self):
        return self.__named_var

    @property
    def func(self):
        return self.__func

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

    def lookupWNone(self,key):
        assert(isinstance(key,InAtom))

        for (k,v) in self.__keyvalues:
            if key == k:
                return v

        return None

    def lookup(self,key):
        assert(isinstance(key,InAtom))

        for (k,v) in self.__keyvalues:
            if key == k:
                return v

        raise Exception('Cannot find key "' + str(key) + '"!')

    def update(self,key,value):
        assert(isinstance(key,InAtom))
        assert(isinstance(value,InAtom))

        for i in range(0,len(self.__keyvalues)):
            if self.__keyvalues[i][0] == key:
                self.__keyvalues[i] = (key,value)
                break
        else:
            self.__keyvalues.append((key,value))

        return self

    def clone(self):
        return Dict(self.__keyvalues)

    @property
    def keyvalues(self):
        return self.__keyvalues

    @property
    def keys(self):
        return [k for (k,v) in self.__keyvalues]

    @property
    def values(self):
        return [v for (k,v) in self.__keyvalues]

def interpret(atom,env,curr_func):
    assert(isinstance(atom,Parser.PsAtom))
    assert(isinstance(env,dict))
    assert(all(map(lambda x: isinstance(x,str),env.iterkeys())))
    assert(all(map(lambda x: isinstance(x,InAtom),env.itervalues())))
    assert(curr_func == None or isinstance(curr_func,Func))
    
    if isinstance(atom,Parser.Call):
        action = interpret(atom.action,env,curr_func)

        if isinstance(action,Boolean):
            raise Exception('Cannot call a boolean!')
        elif isinstance(action,Number):
            raise Exception('Cannot call a number!')
        elif isinstance(action,Symbol):
            if action.value in env:
                fn = env[action.value]
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
                order = dict([(arg.name,arg.default) for arg in fn.order])
                order_defs = dict([(arg.name,arg.default) for arg in fn.orderDefs])
                order_var = {}
                order_pos = 0

                named = dict([(arg.name,arg.default) for arg in fn.named])
                named_defs = dict([(arg.name,arg.default) for arg in fn.namedDefs])
                named_var = {}
                named_var_kvs = []
                named_pos = 0

                if len(atom.orderArgs) < len(order):
                    raise Exception('Can\'t cover order arguments!')

                if len(atom.orderArgs) > len(order) + len(order_defs) and not fn.hasOrderVar:
                    raise Exception('Too many order arguments!')

                if len(atom.namedArgs) < len(named):
                    raise Exception('Can\'t cover named arguments!')

                if len(atom.namedArgs) > len(named) + len(named_defs) and not fn.hasNamedVar:
                    raise Exception('Too many named arguments!')

                for arg in fn.order:
                    order[arg.name] = interpret(atom.orderArgs[order_pos],env,curr_func)
                    order_pos = order_pos + 1

                for arg in fn.orderDefs:
                    if order_pos < len(atom.orderArgs):
                        order_defs[arg.name] = interpret(atom.orderArgs[order_pos],env,curr_func)
                        order_pos = order_pos + 1
                    else:
                        break

                if fn.hasOrderVar:
                    var_kvs = [(Symbol('Length'),Number(len(atom.orderArgs) - order_pos))]

                    for i in range(order_pos,len(atom.orderArgs)):
                        var_kvs.append((Number(i - order_pos),interpret(atom.orderArgs[i],env,curr_func)))

                    order_var[fn.orderVar] = Dict(var_kvs)

                for arg in atom.namedArgs:
                    name = interpret(arg.name,env,curr_func)

                    if not isinstance(name,Symbol):
                        raise Exception('Named argument name isn\'t Symbol!')

                    # These cases are mutually exclusive and are the only four possibilities
                    # given our assumptions about Call and Func.
                    if name.value in named:
                        named[name.value] = interpret(arg.value,env,curr_func)
                    elif name.value in named_defs:
                        named_defs[name.value] = interpret(arg.value,env,curr_func) 
                    elif fn.hasNamedVar:
                        named_var_kvs.append((Symbol(name.value),interpret(arg.value,env,curr_func)))
                    else:
                        raise Exception('Function does not have argument "' + name.value + '"!')

                if fn.hasNamedVar:
                    named_var[fn.namedVar] = Dict(named_var_kvs)
                    
                if isinstance(fn,Func):
                    new_env = dict([(str(k),v.clone()) for (k,v) in fn.env.iteritems()])
                    new_env.update(order)
                    new_env.update(order_defs)
                    new_env.update(order_var)
                    new_env.update(named)
                    new_env.update(named_defs)
                    new_env.update(named_var)
    
                    return interpret(fn.body,new_env,fn)
                else:
                    new_env = {}
                    new_env.update(order)
                    new_env.update(order_defs)
                    new_env.update(order_var)
                    new_env.update(named)
                    new_env.update(named_defs)
                    new_env.update(named_var)

                    return fn.func(**new_env)
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
        def evalArg(arg,target,names):
            name = interpret(arg.name,env,curr_func)
            default = interpret(arg.default,env,curr_func) if arg.hasDefault else None

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but a Symbol!')

            if name.value in names:
                raise Exception('Argument "' + name.value + '" is used twice!')

            target.append(FuncArg(name.value,default))
            names.add(name.value)

        order = []
        order_defs = []
        order_var = None
        named = []
        named_defs = []
        named_var = None

        names = set()

        for order_arg in atom.order:
            evalArg(order_arg,order,names)

        for order_arg in atom.orderDefs:
            evalArg(order_arg,order_defs,names)

        if atom.hasOrderVar:
            name = interpret(atom.orderVar,env,curr_func)

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but a Symbol!')

            if name.value in names:
                raise Exception('Argument "' + name.value + '" is used twice!')

            order_var = name.value

        for named_arg in atom.named:
            evalArg(named_arg,named,names)

        for named_arg in atom.namedDefs:
            evalArg(named_arg,named_defs,names)

        if atom.hasNamedVar:
            name = interpret(atom.namedVar,env,curr_func)

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but a Symbol!')

            if name.value in names:
                raise Exception('Argument "' + name.value + '" is used twice!')

            named_var = name.value

        return Func(order,order_defs,order_var,named,named_defs,named_var,atom.body,env)
    elif isinstance(atom,Parser.Dict):
        keyvalues = []

        for (key,value) in atom.keyvalues:
            keyvalues.append((interpret(key,env,curr_func),
                              interpret(value,env,curr_func)))

        return Dict(keyvalues)
    else:
        raise Exception('Should not have gotten here!')

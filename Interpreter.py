import re
import inspect
import numbers

import Stream
import Tokenizer
import Parser

class InAtom(object):
    def __init__(self):
        pass

    def __str__(self):
        raise Exception('Invalid call to "__str__" for InAtom object!')

    def __repr__(self):
        return str(self)

class Boolean(InAtom):
    def __init__(self,value):
        assert(isinstance(value,bool))

        super(Boolean,self).__init__()

        self.__value = value

    def __str__(self):
        return '#T' if self.__value else '#F'

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

        super(Number,self).__init__()

        self.__value = value

    def __str__(self):
        return str(self.__value)

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

        super(Symbol,self).__init__()

        self.__value = value

    def __str__(self):
        return self.__value

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

        super(String,self).__init__()

        self.__value = value

    def __str__(self):
        return '\'' + self.__value + '\''

    def __eq__(self,other):
        if not isinstance(other,String):
            return False

        return self.__value == other.__value

    def clone(self):
        return String(self.__value)

    @property
    def value(self):
        return self.__value

class Argument(object):
    def __init__(self,name,default):
        assert(isinstance(name,str))
        assert(default == None or isinstance(default,InAtom))

        self.__name = name
        self.__default = default

    def __str__(self):
        return self.__name + \
               ('=' + str(self.__default) if self.__default else '')

    def __repr__(self):
        return str(self)

    def clone(self):
        return Argument(self.__name,self.__default)

    @property
    def name(self):
        return self.__name

    @property
    def hasDefault(self):
        return self.__default != None

    @property
    def default(self):
        return self.__default

class Callable(InAtom):
    def __init__(self,order,order_defs,order_var,named,named_defs,named_var):
        assert(isinstance(order,list))
        assert(all(map(lambda x: isinstance(x,Argument),order)))
        assert(isinstance(order_defs,list))
        assert(all(map(lambda x: isinstance(x,Argument),order_defs)))
        assert(order_var == None or isinstance(order_var,str))
        assert(isinstance(named,list))
        assert(all(map(lambda x: isinstance(x,Argument),named)))
        assert(isinstance(named_defs,list))
        assert(all(map(lambda x: isinstance(x,Argument),named_defs)))
        assert(named_var == None or isinstance(named_var,str))

        super(Callable,self).__init__()

        self.__order = order
        self.__order_defs = order_defs
        self.__order_var = order_var
        self.__named = named
        self.__named_defs = named_defs
        self.__named_var = named_var

    def __str__(self):
        def spIfNNil(ls):
            return ' ' if len(ls) > 0 else ''

        return '[' + ' '.join(map(str,self.__order)) + spIfNNil(self.__order) + \
                     ' '.join(map(str,self.__order_defs)) + spIfNNil(self.__order_defs) + \
                     (str(self.__order_var) + '* ' if self.__order_var else '') + \
                     ' '.join(map(lambda x: str(x) + '!',self.__named)) + spIfNNil(self.__named) + \
                     ' '.join(map(lambda x: str(x) + '!',self.__named_defs)) + spIfNNil(self.__named_defs) + \
                     (str(self.__named_var) + '+ ' if self.__named_var else '') + \
                     str(self._sp_str()) + ']'

    def __eq__(self,other):
        return False

    def _sp_str(self):
        raise Exception('Invalid call to "_sp_str" for Callable object!')

    def _sp__apply(self,order,order_defs,order_var,named,named_defs,named_var):
        raise Exception('Invalid call to "_sp_apply" for Callable object!')

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

        if len(named_args) > len(self.__named) + len(self.__named_defs) and not self.hasNamedVar:
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
            elif self.hasNamedVar:
                named_var_kvs.append((Symbol(name),value))
            else:
                raise Exception('Function does not have argument "' + name + '"!')

        if self.hasNamedVar:
            named_var[self.__named_var] = Dict(named_var_kvs)

        if not all(map(lambda x: isinstance(x,InAtom),named.itervalues())):
            raise Exception('Can\'t cover all named arguments!')

        return self._sp_apply(order,order_defs,order_var,named,named_defs,named_var)

    def curry(self,va):
        raise Exception('Invalid call to "curry" for Callable object!')

    def orderInject(self,order_arg):
        raise Exception('Invalid call to "orderInject" for Callable object!')

    def namedInject(self,named_arg):
        raise Exception('Invalid call to "namedInject" for Callable object!')

    def envHasKey(self,key):
        raise Exception('Invalid call to "envHasKey" for Callable object!')

    def envGet(self,key):
        raise Exception('Invalid call to "envGet" for Callable object!')

    def envSet(self,key,value):
        raise Exception('Invalid call to "envSet" for Callable object!')

    def clone(self):
        raise Exception('Invalid call to "clone" for Callable object!')

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

class Func(Callable):
    def __init__(self,order,order_defs,order_var,named,named_defs,named_var,body,env):
        assert(isinstance(order,list))
        assert(all(map(lambda x: isinstance(x,Argument),order)))
        assert(isinstance(order_defs,list))
        assert(all(map(lambda x: isinstance(x,Argument),order_defs)))
        assert(order_var == None or isinstance(order_var,str))
        assert(isinstance(named,list))
        assert(all(map(lambda x: isinstance(x,Argument),named)))
        assert(isinstance(named_defs,list))
        assert(all(map(lambda x: isinstance(x,Argument),named_defs)))
        assert(named_var == None or isinstance(named_var,str))
        assert(isinstance(body,Parser.PsAtom))
        assert(isinstance(env,dict))
        assert(all(map(lambda x: isinstance(x,str),env.iterkeys())))
        assert(all(map(lambda x: isinstance(x,InAtom),env.itervalues())))

        super(Func,self).__init__(order,order_defs,order_var,named,named_defs,named_var)

        self.__body = body
        self.__env = dict(env)

    def _sp_str(self):
        return str(self.__body)

    def _sp_apply(self,order,order_defs,order_var,named,named_defs,named_var):
        new_env = dict(self.__env)
        new_env.update(order)
        new_env.update(order_defs)
        new_env.update(order_var)
        new_env.update(named)
        new_env.update(named_defs)
        new_env.update(named_var)
    
        return interpret(self.__body,new_env)

    def orderInject(self,order_arg):
        assert(isinstance(order_arg,str))

        self.__order.insert(0,Argument(order_arg,None))

    def namedInject(self,named_arg):
        assert(isinstance(named_arg,str))

        self.__named.insert(0,Argument(named_arg,None))

    def envHasKey(self,key):
        assert(isinstance(key,str))

        return key in self.__env

    def envGet(self,key):
        assert(isinstance(key,str))

        if key in self.__env:
            return self.__env[key]
        else:
            return None

    def envSet(self,key,value):
        assert(isinstance(key,str))
        assert(isinstance(value,InAtom))

        self.__env[key] = value

        return self

    def clone(self):
        return Func(self.order,self.orderDefs,self.orderVar,
                    self.named,self.namedDefs,self.namedVar,
                    self.__body,self.__env)

    @property
    def body(self):
        return self.__body

    @property
    def env(self):
        return self.__env

class BuiltIn(Callable):
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
                    named.append(Argument(arginfo.args[pos],None))
                    pos = pos + 1
                elif arginfo.args[pos].endswith('_plus'):
                    state = BUILTIN_NAMED_VAR
                    named_var = arginfo.args[pos]
                    pos = pos + 1
                else:
                    state = BUILTIN_ORDER
                    order.append(Argument(arginfo.args[pos],None))
                    pos = pos + 1
            elif state == BUILTIN_ORDER_VAR:
                if arginfo.args[pos].endswith('_star'):
                    raise Exception('Only one variable order argument allowed!')
                elif arginfo.args[pos].endswith('_bang'):
                    state = BUILTIN_NAMED
                    named.append(Argument(arginfo.args[pos],None))
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
                    named.append(Argument(arginfo.args[pos],None))
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

        super(BuiltIn,self).__init__(order,[],order_var,named,[],named_var)

        self.__func = func

    def _sp_str(self):
        return '<<BuiltIn "' + self.__func.__name__ + '">>'

    def _sp_apply(self,order,order_defs,order_var,named,named_defs,named_var):
        new_env = {}
        new_env.update(order)
        new_env.update(order_defs)
        new_env.update(order_var)
        new_env.update(named)
        new_env.update(named_defs)
        new_env.update(named_var)

        return self.__func(**new_env)

    def clone(self):
        return BuiltIn(self.__func)

    @property
    def func(self):
        return self.__func

class Dict(InAtom):
    def __init__(self,keyvalues):
        assert(isinstance(keyvalues,list))
        assert(all(map(lambda x: isinstance(x,tuple),keyvalues)))
        assert(all(map(lambda x: isinstance(x[0],InAtom),keyvalues)))
        assert(all(map(lambda x: isinstance(x[1],InAtom),keyvalues)))

        super(Dict,self).__init__()

        self.__keyvalues = keyvalues

    def __str__(self):
        return '<' + ' '.join(map(lambda x: str(x[0]) + ' ' + str(x[1]),self.__keyvalues)) + '>'

    def __eq__(self,other):
        if not isinstance(other,Dict):
            return False

        if len(self.__keyvalues) != len(other.__keyvalues):
            return False

        for (key,value) in self.__keyvalues:
            for (okey,ovalue) in other.__keyvalues:
                if key == okey:
                    break
            else:
                return False

        return True

    def hasKey(self,key):
        assert(isinstance(key,InAtom))

        for (k,v) in self.__keyvalues:
            if key == k:
                return True

        return False

    def get(self,key):
        assert(isinstance(key,InAtom))

        for (k,v) in self.__keyvalues:
            if key == k:
                return v

        return None

    def set(self,key,value):
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

def interpret(atom,env):
    assert(isinstance(atom,Parser.PsAtom))
    assert(isinstance(env,dict))
    assert(all(map(lambda x: isinstance(x,str),env.iterkeys())))
    assert(all(map(lambda x: isinstance(x,InAtom),env.itervalues())))
    
    if isinstance(atom,Parser.Call):
        action = interpret(atom.action,env)

        if isinstance(action,Symbol):
            if action.value in env:
                fn = env[action.value]
            else:
                raise Exception('Couldn\'t find name "' + action.value + '"!')
        elif isinstance(action,Callable):
            fn = action
        elif isinstance(action,Dict):
            fn = action
        else:
            raise Exception('Cannot call object of that type!')

        if len(atom.orderArgs) == 0 and len(atom.namedArgs) == 0:
            return fn

        if isinstance(fn,Callable):
            order_args = []
            named_args = {}

            for arg in atom.orderArgs:
                order_args.append(interpret(arg,env))

            for arg in atom.namedArgs:
                name = interpret(arg.name,env)

                if not isinstance(name,Symbol):
                    raise Exception('Named argument name isn\'t a Symbol!')

                if name.value in named_args:
                    raise Exception('Named argument "' + name.value + '" appears more than once!')

                named_args[name.value] = interpret(arg.value,env)

            return fn.apply(order_args,named_args)
        elif isinstance(fn,Dict):
            if len(atom.orderArgs) == 1 and len(atom.namedArgs) == 0:
                return fn.get(interpret(atom.orderArgs[0],env))
            else:
                raise Exception('Cannot apply more than one argument to a dictionary!')
        else:
            raise Exception('Cannot apply arguments to an object of that type!')
    elif isinstance(atom,Parser.Boolean):
        if atom.text == '#T':
            return Boolean(True)
        elif atom.text == '#F':
            return Boolean(False)
        else:
            raise Exception('Critical Error: Invalid boolean value "' + atom.text + '"!')
    elif isinstance(atom,Parser.Number):
        return Number(float(atom.text))
    elif isinstance(atom,Parser.Symbol):
        return Symbol(atom.text)
    elif isinstance(atom,Parser.String):
        return String(atom.text)
    elif isinstance(atom,Parser.StringEval):
        raise Exception('Execution path not yet implemented!')
    elif isinstance(atom,Parser.Func):
        def evalArg(arg,target,names):
            name = interpret(arg.name,env)
            default = interpret(arg.default,env) if arg.hasDefault else None

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but a Symbol!')

            if name.value in names:
                raise Exception('Argument "' + name.value + '" is used twice!')

            target.append(Argument(name.value,default))
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
            name = interpret(atom.orderVar,env)

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
            name = interpret(atom.namedVar,env)

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but a Symbol!')

            if name.value in names:
                raise Exception('Argument "' + name.value + '" is used twice!')

            named_var = name.value

        return Func(order,order_defs,order_var,named,named_defs,named_var,atom.body,env)
    elif isinstance(atom,Parser.Dict):
        keyvalues = []

        for (key,value) in atom.keyvalues:
            keyvalues.append((interpret(key,env),
                              interpret(value,env)))

        return Dict(keyvalues)
    else:
        raise Exception('Should not have gotten here!')

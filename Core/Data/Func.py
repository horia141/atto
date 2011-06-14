import Interpreter
import Core.Utils

from Core.Utils import isFunc
from Core.Utils import testFunc
from Core.Utils import testSymbol
from Core.Utils import testBoolean
from Core.Utils import argStarAsList
from Core.Utils import argPlusAsDict

def IsFunc(f):
    assert(isinstance(f,Interpreter.InAtom))

    return Interpreter.Boolean(isFunc(f))

def Apply(f,va_star,va_plus):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))
    assert(isinstance(va_plus,Interpreter.InAtom))

    testFunc(f,'Apply')

    return f.apply(argStarAsList(va_star),
                   argPlusAsDict(va_plus))

def Curry(f,va_star,va_plus):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))
    assert(isinstance(va_plus,Interpreter.InAtom))

    testFunc(f,'Curry')

    new_f = f.clone()

    return new_f.curry(argStarAsList(va_star),
                       argPlusAsDict(va_plus))

def Inject(f,arg,named):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(arg,Interpreter.InAtom))
    assert(isinstance(named,Interpreter.InAtom))

    testFunc(f,'Inject')
    testSymbol(arg,'Inject')
    testBoolean(named,'Boolean')

    new_f = f.clone()

    if named.value:
        new_f.namedInject(arg.value)
    else:
        new_f.orderInject(arg.value)

    return new_f

def EnvHasKey(f,key):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    testFunc(f,'EnvHasKey')
    testSymbol(key,'EnvHasKey')

    return Interpreter.Boolean(f.envHasKey(key.value))

def EnvGet(f,key):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    testFunc(f,'EnvGet')
    testSymbol(key,'EnvGet')

    v = f.envGet(key.value)

    if v:
        return v.clone()
    else:
        raise Exception('Environment does not have key "' + key.value + '"!')

def EnvSet(f,key,value,va_star):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))
    assert(isinstance(value,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    testFunc(f,'EnvSet')
    testSymbol(key,'EnvSet')

    va = argStarAsList(va_star)

    if len(va) % 2 != 0:
        raise Exception('<<BuiltIn "EnvSet">> must be called with an even number of argument!')

    new_f = f.clone().envSet(key.value,value)

    for i in range(0,len(va),2):
        testSymbol(va[i],'EnvSet')
        new_f.envSet(va[i].value,va[i+1])

    return new_f

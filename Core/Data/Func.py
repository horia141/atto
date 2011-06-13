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

def Curry(f,va_star,va_plus):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))
    assert(isinstance(va_plus,Interpreter.InAtom))

    testFunc(f,'Curry')

    new_f = f.clone()

    return new_f.curry(argStarAsList(va_star),
                       argPlusAsDict(va_plus))

def EnvHasKey(f):
    pass

def EnvGet(f):
    pass

def EnvSet(f):
    pass

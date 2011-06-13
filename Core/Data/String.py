import Interpreter
import Core.Utils

from Core.Utils import isString
from Core.Utils import testString
from Core.Utils import argStarAsList

def IsString(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(isString(a))

def Cat(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    testString(a,'Cat')
    testString(b,'Cat')

    va = argStarAsList(va_star)

    map(lambda x: testString(x,'Cat'),va)

    return Interpreter.String(a.value + b.value + ''.join(map(lambda x: x.value,va)))

import Interpreter
import Core.Utils

from Core.Utils import isBoolean
from Core.Utils import testBoolean
from Core.Utils import argStarAsList

def IsBoolean(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(isBoolean(a))

def Not(a):
    assert(isinstance(a,Interpreter.InAtom))

    testBoolean(a,'Not')

    return Interpreter.Boolean(not a.value)

def And(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    testBoolean(a,'And')
    testBoolean(b,'And')

    res = a.value and b.value
    va = argStarAsList(va_star)

    map(lambda x: testBoolean(x,'And'),va)

    for i in va:
        res = res and i.value

    return Interpreter.Boolean(res)

def Or(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    testBoolean(a,'Or')
    testBoolean(b,'Or')

    res = a.value or b.value
    va = argStarAsList(va_star)

    map(lambda x: testBoolean(x,'Or'),va)

    for i in va:
        res = res or i.value

    return Interpreter.Boolean(res)

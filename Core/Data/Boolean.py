import Interpreter
import Core.Utils

from Core.Utils import isBoolean
from Core.Utils import testBoolean
from Core.Utils import testBooleanVar

def IsBoolean(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(isBoolean(a))

def Not(a):
    assert(isinstance(a,Interpreter.InAtom))

    testBoolean(a,'Not')

    return Interpreter.Boolean(not a.value)

def And(a,b,*va):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))

    testBoolean(a,'And')
    testBoolean(b,'And')
    testBooleanVar(va,'And')

    res = a.value and b.value

    for i in va:
        res = res and i.value

    return Interpreter.Boolean(res)

def Or(a,b,*va):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))

    testBoolean(a,'Or')
    testBoolean(b,'Or')
    testBooleanVar(va,'Or')

    res = a.value or b.value

    for i in va:
        res = res or i.value

    return Interpreter.Boolean(res)

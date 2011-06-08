import Interpreter
import Core.Utils

from Core.Utils import isString
from Core.Utils import testString
from Core.Utils import testStringVar

def IsString(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(isString(a))

def Cat(a,b,*va):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))

    testString(a,'Add')
    testString(b,'Add')
    testStringVar(va,'Add')

    return Interpreter.String(a.value + b.value + ''.join(map(lambda x: x.value,va)))

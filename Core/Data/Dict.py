import Interpreter
import Core.Utils

from Core.Utils import isDict
from Core.Utils import testDict
from Core.Utils import buildArray

def IsDict(d):
    assert(isinstance(d,Interpreter.InAtom))

    return Interpreter.Boolean(isDict(d))

def HasKey(d,key):
    assert(isinstance(d,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    testDict(d,'HasKey')

    try:
        d.lookup(key)
        return Interpreter.Boolean(True)
    except Exception,e:
        # Should use a proper error here. Don't
        # want to stop the good exeptions from going
        # up.
        return Interpreter.Boolean(False)

def Get(d,key):
    assert(isinstance(d,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    testDict(d,'Get')

    return d.lookup(key).clone()

def Set(d,key,value,*va):
    assert(isinstance(d,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))
    assert(isinstance(value,Interpreter.InAtom))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))

    testDict(d,'Set')

    if len(va) % 2 != 0:
        raise Exception('<<BuiltIn "Set">> must be called with an even number of argument!')

    new_d = d.clone().update(key,value)

    for i in range(0,len(va),2):
        new_d.update(va[i],va[i+1])

    return new_d

def Keys(d):
    assert(isinstance(d,Interpreter.InAtom))

    testDict(d,'Keys')

    return buildArray([k for (k,v) in d.keyvalues])

def Values(d):
    assert(isinstance(d,Interpreter.InAtom))

    testDict(d,'Values')

    return buildArray([v for (k,v) in d.keyvalues])

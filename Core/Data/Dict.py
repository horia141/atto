import Interpreter
import Core.Utils

from Core.Utils import isDict
from Core.Utils import testDict
from Core.Utils import buildArray
from Core.Utils import argStarAsList

def IsDict(d):
    assert(isinstance(d,Interpreter.InAtom))

    return Interpreter.Boolean(isDict(d))

def HasKey(d,key):
    assert(isinstance(d,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    testDict(d,'HasKey')

    return Interpreter.Boolean(d.haskey(key))

def Get(d,key):
    assert(isinstance(d,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    testDict(d,'Get')

    v = d.get(key)

    if v:
        return v.clone()
    else:
        raise Exception('Dictionary does not have key "' + str(key) + '"!')

def Set(d,key,value,va_star):
    assert(isinstance(d,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))
    assert(isinstance(value,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    testDict(d,'Set')

    va = argStarAsList(va_star)

    if len(va) % 2 != 0:
        raise Exception('<<BuiltIn "Set">> must be called with an even number of argument!')

    new_d = d.clone().set(key,value)

    for i in range(0,len(va),2):
        new_d.set(va[i],va[i+1])

    return new_d

def Keys(d):
    assert(isinstance(d,Interpreter.InAtom))

    testDict(d,'Keys')

    return buildArray(d.keys)

def Values(d):
    assert(isinstance(d,Interpreter.InAtom))

    testDict(d,'Values')

    return buildArray(d.values)

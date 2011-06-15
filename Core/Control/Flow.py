import Interpreter
import Core.Utils

from Core.Utils import testBoolean
from Core.Utils import testSymbol
from Core.Utils import isFunc
from Core.Utils import isBlock
from Core.Utils import argStarAsList

def If(test,caseT,caseF):
    assert(isinstance(test,Interpreter.InAtom))
    assert(isinstance(caseT,Interpreter.InAtom))
    assert(isinstance(caseF,Interpreter.InAtom))

    testBoolean(test,'If')

    if test.value:
        if isBlock(caseT):
            return caseT.apply([],{})
        else:
            return caseT
    else:
        if isBlock(caseF):
            return caseF.apply([],{})
        else:
            return caseF

def Let(va_star):
    assert(isinstance(va_star,Interpreter.InAtom))

    va = argStarAsList(va_star)

    if len(va) < 3 or len(va) % 2 == 0:
        raise Exception('<<BuiltIn "Let">> must be called with an odd number (>= 3) of arguments!')

    body = va[-1]
    del va[-1]
    names = va[0::2]
    values = va[1::2]

    map(lambda x: testSymbol(x,'Let'),names)

    new_kv = dict(zip(map(lambda x: x.value,names),values))

    for i in range(0,len(values)):
        if isFunc(values[i]):
            values[i] = values[i].clone()

            for (k,v) in new_kv.iteritems():
                values[i].envSet(k,v)

    if isFunc(body):
        body = body.clone()

        for (k,v) in new_kv.iteritems():
            body.envSet(k,v)

    if isBlock(body):
        return body.apply([],{})

    return body

def Seq(va_star):
    pass

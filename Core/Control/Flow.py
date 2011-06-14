import Interpreter
import Core.Utils

from Core.Utils import testBoolean
from Core.Utils import isBlock

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
    pass

def Seq(va_star):
    pass

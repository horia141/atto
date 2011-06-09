import Interpreter
import Core.Utils

from Core.Utils import testBoolean
from Core.Utils import isBlock

def If(test,caseT,caseF):
    assert(isinstance(test,Interpreter.InAtom))
    assert(isinstance(caseT,Interpreter.InAtom))
    assert(isinstance(caseF,Interpreter.InAtom))

    testBoolean(test)

    if test.value:
        if isBlock(testT):
            return $eval_somehow_testT$
        else:
            return testT
    else:
        if isBlock(testF):
            return $eval_somehow_testF$
        else:
            return testF

import Interpreter
import Core.Utils

from Core.Utils import isSymbol

def IsSymbol(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(isSymbol(a))

import Interpreter
import BuiltIns.Utils

from BuiltIns.Utils import isSymbol

def IsSymbol(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(isSymbol(a))

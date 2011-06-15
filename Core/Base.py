import Interpreter
import Core.Utils

from Core.Utils import isBoolean
from Core.Utils import isNumber
from Core.Utils import isSymbol
from Core.Utils import isString
from Core.Utils import isFunc
from Core.Utils import isDict

def Type(x):
    assert(isinstance(x,Interpreter.InAtom))

    if isBoolean(x):
        return Interpreter.Symbol('Boolean')
    if isNumber(x):
        return Interpreter.Symbol('Number')
    if isSymbol(x):
        return Interpreter.Symbol('Symbol')
    if isString(x):
        return Interpreter.Symbol('String')
    if isFunc(x):
        return Interpreter.Symbol('Func')
    if isDict(x):
        return Interpreter.Symbol('Dict')

    raise Exception('Critical Error: Invalid control path!')

def Eq(x,y):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(y,Interpreter.InAtom))

    return Interpreter.Boolean(x == y)

def Neq(x,y):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(y,Interpreter.InAtom))

    return Interpreter.Boolean(x != y)

def SameType(x,y):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(y,Interpreter.InAtom))

    return Interpreter.Boolean(isinstance(x,y.__class__))

def Module():
    pass

def Define():
    pass

def Import():
    pass

def Export():
    pass

def UTests():
    pass

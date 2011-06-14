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
    if isNumber(x):
        return Interpreter.Symbol('Symbol')
    if isNumber(x):
        return Interpreter.Symbol('String')
    if isNumber(x):
        return Interpreter.Symbol('Func')
    if isNumber(x):
        return Interpreter.Symbol('Dict')

    raise Exception('Critical Error: Invalid control path!')

def Equal(x):
    pass

def NotEqual(x):
    pass

def SameType(x):
    pass

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

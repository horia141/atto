import Interpreter
import BuiltIns.Utils
from BuiltIns.Utils import makeNumber
from BuiltIns.Utils import getNumber

def Add(a,b,*va):
    a = getNumber(a)
    b = getNumber(b)

    res = a + b

    for i in va:
        res = res + getNumber(i)

    return makeNumber(res)

def Sub(a,b,*va):
    a = getNumber(a)
    b = getNumber(b)

    res = a - b

    for i in va:
        res = res - getNumber(i)

    return makeNumber(res)

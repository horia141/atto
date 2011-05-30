import numbers

import Interpreter

def makeString(string):
    assert(isinstance(string,str))

    return Interpreter.Symbol(str)

def getString(obj):
    assert(isinstance(obj,Interpreter.InAtom))

    if not isinstance(obj,Interpreter.Symbol):
        raise Exception('Expected symbol!')

    return obj.text

def makeNumber(number):
    assert(isinstance(number,numbers.Number))

    return Interpreter.Symbol(str(number))

def getNumber(obj):
    if not isinstance(obj,Interpreter.Symbol):
        raise Exception('Expected symbol!')

    try:
        return float(obj.text)
    except ValueError,e:
        raise Exception('Expected number!')

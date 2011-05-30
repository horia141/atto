import Interpreter

def checkSymbol(obj):
    if not isinstance(obj,Interpreter.Symbol):
        raise Exception('Excepected symbol!')

def checkNumber(obj):
    checkSymbol(obj)

    try:
        int(obj.text)
    except ValueError,e:
        raise Exception('Expected number!')

def checkFunc(obj):
    if not isinstance(obj,Interpreter.Func):
        raise Exception('Excepected function!')

def checkThunk(obj):
    checkFunc(obj)

    if not len(obj.argNames) == 0 or obj.hasVararg:
        raise Exception('Expected a thunk!')

def checkDict(obj):
    if not isinstance(obj,Interpreter.Dict):
        raise Exception('Excepected function!')

def checkVarargArray(obj):
    pass

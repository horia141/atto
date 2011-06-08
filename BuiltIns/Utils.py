import Interpreter

def isBoolean(x):
    return isinstance(x,Interpreter.Boolean)

def testBoolean(x,m):
    if not isBoolean(x):
        raise Exception('Expected boolean in <<BuiltIn "' + m + '">>!')

def testBooleanVar(va,m):
    map(lambda x: testBoolean(x,m),va)

def isNumber(x):
    return isinstance(x,Interpreter.Number)

def testNumber(x,m):
    if not isNumber(x):
        raise Exception('Expected number in <<BuiltIn "' + m + '">>!')

def testNumberVar(va,m):
    map(lambda x: testNumber(x,m),va)

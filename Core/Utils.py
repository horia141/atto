import Stream
import Interpreter

def isBoolean(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.Boolean)

def testBoolean(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isBoolean(x):
        raise Exception('Expected boolean in <<BuiltIn "' + m + '">>!')

def testBooleanVar(va,m):
    assert(isinstance(va,tuple))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))
    assert(isinstance(m,str))

    map(lambda x: testBoolean(x,m),va)

def isNumber(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.Number)

def testNumber(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isNumber(x):
        raise Exception('Expected number in <<BuiltIn "' + m + '">>!')

def testNumberVar(va,m):
    assert(isinstance(va,tuple))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))
    assert(isinstance(m,str))

    map(lambda x: testNumber(x,m),va)

def isSymbol(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.Symbol)

def testSymbol(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isSymbol(x):
        raise Exception('Expected symbol in <<BuiltIn "' + m + '">>!')

def testSymbolVar(va,m):
    assert(isinstance(va,tuple))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))
    assert(isinstance(m,str))

    map(lambda x: testSymbol(x,m),va)

def isString(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.String)

def testString(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isString(x):
        raise Exception('Expected string in <<BuiltIn "' + m + '">>!')

def testStringVar(va,m):
    assert(isinstance(va,tuple))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))
    assert(isinstance(m,str))

    map(lambda x: testString(x,m),va)

def isDict(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.Dict)

def testDict(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isDict(x):
        raise Exception('Expected dict in <<BuiltIn "' + m + '">>!')

def testDictVar(va,m):
    assert(isinstance(va,tuple))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))
    assert(isinstance(m,str))

    map(lambda x: testDict(x,m),va)

def isFunc(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.Func)

def testFunc(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isFunc(x):
        raise Exception('Expected func in <<BuiltIn "' + m + '">>!')

def testFuncVar(va,m):
    assert(isinstance(va,tuple))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))
    assert(isinstance(m,str))

    map(lambda x: testFunc(x,m),va)

def buildArray(l):
    assert(isinstance(l,list))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),l)))

    kvs = [(Interpreter.Symbol('Length'),
            Interpreter.Number(len(l)))]

    for i in range(0,len(l)):
        kvs.append((Interpreter.Number(float(i)),l[i]))

    return Interpreter.Dict(kvs)

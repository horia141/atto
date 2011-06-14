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

def isNumber(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.Number)

def testNumber(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isNumber(x):
        raise Exception('Expected number in <<BuiltIn "' + m + '">>!')

def isSymbol(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.Symbol)

def testSymbol(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isSymbol(x):
        raise Exception('Expected symbol in <<BuiltIn "' + m + '">>!')

def isString(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.String)

def testString(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isString(x):
        raise Exception('Expected string in <<BuiltIn "' + m + '">>!')

def isDict(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.Dict)

def testDict(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isDict(x):
        raise Exception('Expected dict in <<BuiltIn "' + m + '">>!')

def isFunc(x):
    assert(isinstance(x,Interpreter.InAtom))

    return isinstance(x,Interpreter.Func)

def testFunc(x,m):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(m,str))

    if not isFunc(x):
        raise Exception('Expected func in <<BuiltIn "' + m + '">>!')

def argStarAsList(arg_star):
    assert(isinstance(arg_star,Interpreter.Dict))

    length = arg_star.get(Interpreter.Symbol('Length'))
    assert(length)
    new_ls = []

    for i in range(0,length.value):
        new_item = arg_star.get(Interpreter.Number(i))
        assert(new_item)
        new_ls.append(new_item)

    return new_ls

def argPlusAsDict(arg_plus):
    assert(isinstance(arg_plus,Interpreter.Dict))
    assert(all(map(lambda x: isinstance(x,Interpreter.Symbol),arg_plus.keys)))

    new_dict = {}

    for (k,v) in arg_plus.keyvalues:
        new_dict[k.value] = v

    return new_dict

def buildArray(l):
    assert(isinstance(l,list))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),l)))

    kvs = [(Interpreter.Symbol('Length'),
            Interpreter.Number(len(l)))]

    for i in range(0,len(l)):
        kvs.append((Interpreter.Number(float(i)),l[i]))

    return Interpreter.Dict(kvs)

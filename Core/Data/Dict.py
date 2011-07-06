import Interpreter
import Application
import Utils

def GetModule():
    return Application.Module(
        'Core:Data:Dict',
        {'is-dict?':  Interpreter.BuiltIn(IsDict),
         'has-key?':  Interpreter.BuiltIn(HasKey),
         'get':       Interpreter.BuiltIn(Get),
         'set':       Interpreter.BuiltIn(Set),
         'keys':      Interpreter.BuiltIn(Keys),
         'values':    Interpreter.BuiltIn(Values)},
        {},['is-dict?','has-key?','get','set','keys','values'])

def IsDict(d):
    assert(isinstance(d,Interpreter.InAtom))

    return Interpreter.Boolean(Utils.isDict(d))

def HasKey(d,key):
    assert(isinstance(d,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    Utils.testDict(d,'HasKey')

    return Interpreter.Boolean(d.hasKey(key))

def Get(d,key):
    assert(isinstance(d,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    Utils.testDict(d,'Get')

    v = d.get(key)

    if v:
        return v
    else:
        raise Exception('Dictionary does not have key "' + str(key) + '"!')

def Set(d,key,value,va_star):
    assert(isinstance(d,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))
    assert(isinstance(value,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    Utils.testDict(d,'Set')

    va = Utils.argStarAsList(va_star)

    if len(va) % 2 != 0:
        raise Exception('<<BuiltIn "Set">> must be called with an even number of argument!')

    new_d = d.clone().set(key,value)

    for i in range(0,len(va),2):
        new_d.set(va[i],va[i+1])

    return new_d

def Keys(d):
    assert(isinstance(d,Interpreter.InAtom))

    Utils.testDict(d,'Keys')

    return Utils.buildArray(d.keys)

def Values(d):
    assert(isinstance(d,Interpreter.InAtom))

    Utils.testDict(d,'Values')

    return Utils.buildArray(d.values)

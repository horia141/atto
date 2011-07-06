import Interpreter
import Application
import Utils

def GetModule():
    return Application.Module(
        'Core:Data:Boolean',
        {'is-boolean?':  Interpreter.BuiltIn(IsBoolean),
         'not':          Interpreter.BuiltIn(Not), 
         'and':          Interpreter.BuiltIn(And),
         'or':           Interpreter.BuiltIn(Or)},
        {},['is-boolean?','not','and','or'])

def IsBoolean(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(Utils.isBoolean(a))

def Not(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testBoolean(a,'Not')

    return Interpreter.Boolean(not a.value)

def And(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    Utils.testBoolean(a,'And')
    Utils.testBoolean(b,'And')

    res = a.value and b.value
    va = Utils.argStarAsList(va_star)

    map(lambda x: Utils.testBoolean(x,'And'),va)

    for i in va:
        res = res and i.value

    return Interpreter.Boolean(res)

def Or(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    Utils.testBoolean(a,'Or')
    Utils.testBoolean(b,'Or')

    res = a.value or b.value
    va = Utils.argStarAsList(va_star)

    map(lambda x: Utils.testBoolean(x,'Or'),va)

    for i in va:
        res = res or i.value

    return Interpreter.Boolean(res)

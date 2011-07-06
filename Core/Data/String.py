import Interpreter
import Application
import Utils

def GetModule():
    return Application.Module(
        'Core:Data:String',
        {'is-string?':  Interpreter.BuiltIn(IsString),
         'cat':         Interpreter.BuiltIn(Cat)},
        {},['is-string?','cat'])

def IsString(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(Utils.isString(a))

def Cat(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    Utils.testString(a,'Cat')
    Utils.testString(b,'Cat')

    va = Utils.argStarAsList(va_star)

    map(lambda x: Utils.testString(x,'Cat'),va)

    return Interpreter.String(a.value + b.value + ''.join(map(lambda x: x.value,va)))

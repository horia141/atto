import Interpreter
import Application
import Utils

def GetModule():
    return Application.Module(
        'Core:Data:Func',
        {'is-func?':      Interpreter.BuiltIn(IsFunc),
         'apply':         Interpreter.BuiltIn(Apply),
         'curry':         Interpreter.BuiltIn(Curry),
         'inject':        Interpreter.BuiltIn(Inject),
         'env-has-key?':  Interpreter.BuiltIn(EnvHasKey),
         'env-get':       Interpreter.BuiltIn(EnvGet),
         'env-set':       Interpreter.BuiltIn(EnvSet)},
        {},['is-func?','apply','curry','inject','env-has-key?','env-get',
            'env-set'])

def IsFunc(f):
    assert(isinstance(f,Interpreter.InAtom))

    return Interpreter.Boolean(Utils.isFunc(f))

def Apply(f,va_star,va_plus):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))
    assert(isinstance(va_plus,Interpreter.InAtom))

    Utils.testFunc(f,'Apply')

    return f.apply(Utils.argStarAsList(va_star),
                   Utils.argPlusAsDict(va_plus))

def Curry(f,va_star,va_plus):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))
    assert(isinstance(va_plus,Interpreter.InAtom))

    Utils.testFunc(f,'Curry')

    new_f = f.clone()

    return new_f.curry(Utils.argStarAsList(va_star),
                       Utils.argPlusAsDict(va_plus))

def Inject(f,arg,named):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(arg,Interpreter.InAtom))
    assert(isinstance(named,Interpreter.InAtom))

    Utils.testFunc(f,'Inject')
    Utils.testSymbol(arg,'Inject')
    Utils.testBoolean(named,'Boolean')

    new_f = f.clone()


    if named.value:
        new_f.namedInject(arg.value)
    else:
        new_f.orderInject(arg.value)

    return new_f

def EnvHasKey(f,key):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    Utils.testFunc(f,'EnvHasKey')
    Utils.testSymbol(key,'EnvHasKey')

    return Interpreter.Boolean(f.envHasKey(key.value))

def EnvGet(f,key):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))

    Utils.testFunc(f,'EnvGet')
    Utils.testSymbol(key,'EnvGet')

    v = f.envGet(key.value)

    if v:
        return v.clone()
    else:
        raise Exception('Environment does not have key "' + key.value + '"!')

def EnvSet(f,key,value,va_star):
    assert(isinstance(f,Interpreter.InAtom))
    assert(isinstance(key,Interpreter.InAtom))
    assert(isinstance(value,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    Utils.testFunc(f,'EnvSet')
    Utils.testSymbol(key,'EnvSet')

    va = Utils.argStarAsList(va_star)

    if len(va) % 2 != 0:
        raise Exception('<<BuiltIn "EnvSet">> must be called with an even number of argument!')

    new_f = f.clone().envSet(key.value,value)

    for i in range(0,len(va),2):
        Utils.testSymbol(va[i],'EnvSet')
        new_f.envSet(va[i].value,va[i+1])

    return new_f

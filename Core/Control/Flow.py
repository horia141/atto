import Interpreter
import Application
import Utils

def GetModule():
    return Application.Module(
        'Core:Control:Flow',
        {'if':   Interpreter.BuiltIn(If),
         'let':  Interpreter.BuiltIn(Let)},
        {},['if','let'])

def If(test,caseT,caseF):
    assert(isinstance(test,Interpreter.InAtom))
    assert(isinstance(caseT,Interpreter.InAtom))
    assert(isinstance(caseF,Interpreter.InAtom))

    Utils.testBoolean(test,'If')

    if test.value:
        if Utils.isBlock(caseT):
            return caseT.apply([],{})
        else:
            return caseT
    else:
        if Utils.isBlock(caseF):
            return caseF.apply([],{})
        else:
            return caseF

def Let(va_star):
    assert(isinstance(va_star,Interpreter.InAtom))

    va = Utils.argStarAsList(va_star)

    if len(va) < 3 or len(va) % 2 == 0:
        raise Exception('<<BuiltIn "Let">> must be called with an odd number (>= 3) of arguments!')

    body = va[-1]
    del va[-1]
    names = va[0::2]
    values = map(lambda x: x.clone(),va[1::2])

    map(lambda x: Utils.testSymbol(x,'Let'),names)

    new_kv = dict(zip(map(lambda x: x.value,names),values))

    for i in range(0,len(values)):
        if Utils.isFunc(values[i]):
            for (k,v) in new_kv.iteritems():
                values[i].envSet(k,v)

    if Utils.isFunc(body):
        body = body.clone()

        for (k,v) in new_kv.iteritems():
            body.envSet(k,v)

    if Utils.isBlock(body):
        return body.apply([],{})

    return body

def Seq(va_star):
    pass

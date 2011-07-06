import math

import Interpreter
import Application
import Utils

def GetModule():
    return Application.Module(
        'Core:Data:Number',
        {'pi':          Interpreter.Number(3.1415926535897931),
         'e':           Interpreter.Number(2.7182818284590451),
         'is-number?':  Interpreter.BuiltIn(IsNumber),
         'add':         Interpreter.BuiltIn(Add),
         'inc':         Interpreter.BuiltIn(Inc),
         'sub':         Interpreter.BuiltIn(Sub),
         'dec':         Interpreter.BuiltIn(Dec),
         'mul':         Interpreter.BuiltIn(Mul),
         'div':         Interpreter.BuiltIn(Div),
         'mod':         Interpreter.BuiltIn(Mod),
         'lt':          Interpreter.BuiltIn(Lt),
         'lte':         Interpreter.BuiltIn(Lte),
         'gt':          Interpreter.BuiltIn(Gt),
         'gte':         Interpreter.BuiltIn(Gte),
         'sin':         Interpreter.BuiltIn(Sin),
         'cos':         Interpreter.BuiltIn(Cos),
         'tan':         Interpreter.BuiltIn(Tan),
         'ctg':         Interpreter.BuiltIn(Ctg),
         'asin':        Interpreter.BuiltIn(ASin),
         'acos':        Interpreter.BuiltIn(ACos),
         'atan':        Interpreter.BuiltIn(ATan),
         'actg':        Interpreter.BuiltIn(ACtg),
         'rad2deg':     Interpreter.BuiltIn(Rad2Deg),
         'deg2rad':     Interpreter.BuiltIn(Deg2Rad),
         'exp':         Interpreter.BuiltIn(Exp),
         'log':         Interpreter.BuiltIn(Log),
         'ln':          Interpreter.BuiltIn(Ln),
         'lg':          Interpreter.BuiltIn(Lg),
         'sqrt':        Interpreter.BuiltIn(Sqrt),
         'pow':         Interpreter.BuiltIn(Pow),
         'abs':         Interpreter.BuiltIn(Abs),
         'ceill':       Interpreter.BuiltIn(Ceill),
         'floor':       Interpreter.BuiltIn(Floor)},
        {},['pi','e','is-number?','add','inc','sub','dec','mul','div','mod',
            'lt','lte','gt','gte','sin','cos','tan','ctg','asin','acos','actg',
            'rad2deg','deg2rad','exp','log','ln','lg','sqrt','pow','abs','ceill',
            'floor'])

def IsNumber(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(Utils.isNumber(a))

def Add(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    Utils.testNumber(a,'Add')
    Utils.testNumber(b,'Add')

    res = a.value + b.value
    va = Utils.argStarAsList(va_star)

    map(lambda x: Utils.testNumber(x,'Add'),va)

    for i in va:
        res = res + i.value

    return Interpreter.Number(res)

def Inc(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Inc')

    return Interpreter.Number(a.value + 1)

def Sub(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    Utils.testNumber(a,'Sub')
    Utils.testNumber(b,'Sub')

    res = a.value - b.value
    va = Utils.argStarAsList(va_star)

    map(lambda x: Utils.testNumber(x,'Sub'),va)

    for i in va:
        res = res - i.value

    return Interpreter.Number(res)

def Dec(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Dec')

    return Interpreter.Number(a.value - 1)

def Mul(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    Utils.testNumber(a,'Mul')
    Utils.testNumber(b,'Mul')

    res = a.value * b.value
    va = Utils.argStarAsList(va_star)

    map(lambda x: Utils.testNumber(x,'Mul'),va)

    for i in va:
        res = res * i.value

    return Interpreter.Number(res)

def Div(a,b,va_star):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(isinstance(va_star,Interpreter.InAtom))

    Utils.testNumber(a,'Div')
    Utils.testNumber(b,'Div')

    res = a.value / b.value
    va = Utils.argStarAsList(va_star)

    map(lambda x: Utils.testNumber(x,'Div'),va)

    for i in va:
        res = res / i.value

    return Interpreter.Number(res)

def Mod(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    Utils.testNumber(a,'Mod')
    Utils.testNumber(b,'Mod')

    res = math.fmod(a.value,b.value)

    return Interpreter.Number(res)

def Lt(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    Utils.testNumber(a,'Lt')
    Utils.testNumber(b,'Lt')

    res = a.value < b.value

    return Interpreter.Boolean(res)

def Lte(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    Utils.testNumber(a,'Lte')
    Utils.testNumber(b,'Lte')

    res = a.value <= b.value

    return Interpreter.Boolean(res)

def Gt(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    Utils.testNumber(a,'Gt')
    Utils.testNumber(b,'Gt')

    res = a.value > b.value

    return Interpreter.Boolean(res)

def Gte(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    Utils.testNumber(a,'Gte')
    Utils.testNumber(b,'Gte')

    res = a.value >= b.value

    return Interpreter.Boolean(res)

def Sin(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Sin')

    return Interpreter.Number(math.sin(a.value))

def Cos(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Cos')

    return Interpreter.Number(math.cos(a.value))

def Tan(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Sin')

    return Interpreter.Number(math.tan(a.value))

def Ctg(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Ctg')

    return Interpreter.Number(1/math.tan(a.value))

def ASin(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'ASin')

    return Interpreter.Number(math.asin(a.value))

def ACos(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'ACos')

    return Interpreter.Number(math.acos(a.value))

def ATan(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'ATan')

    return Interpreter.Number(math.atan(a.value))

def ACtg(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'ACtg')

    return Interpreter.Number(math.pi / 2 - math.atan(a.value))

def Rad2Deg(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Rad2Deg')

    return Interpreter.Number(math.degrees(a.value))

def Deg2Rad(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Deg2Rad')

    return Interpreter.Number(math.radians(a.value))

def Exp(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Exp')

    return Interpreter.Number(math.exp(a.value))

def Log(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    Utils.testNumber(a,'Log')
    Utils.testNumber(b,'Log')

    return Interpreter.Number(math.log(a.value,b.value))

def Ln(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Ln')

    return Interpreter.Number(math.log(a.value,math.e))

def Lg(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Lg')

    return Interpreter.Number(math.log(a.value,10))

def Sqrt(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Sqrt')

    return Interpreter.Number(math.sqrt(a.value))

def Pow(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    Utils.testNumber(a,'Pow')
    Utils.testNumber(b,'Pow')

    return Interpreter.Number(math.pow(a.value,b.value))

def Abs(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Abs')

    return Interpreter.Number(math.fabs(a.value))

def Ceill(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Ceill')

    return Interpreter.Number(math.ceil(a.value))

def Floor(a):
    assert(isinstance(a,Interpreter.InAtom))

    Utils.testNumber(a,'Floor')

    return Interpreter.Number(math.floor(a.value))

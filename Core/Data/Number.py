import math

import Interpreter
import Core.Utils

from Core.Utils import isNumber
from Core.Utils import testNumber
from Core.Utils import testNumberVar

def IsNumber(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(isNumber(a))

def Add(a,b,*va):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))

    testNumber(a,'Add')
    testNumber(b,'Add')
    testNumberVar(va,'Add')

    res = a.value + b.value

    for i in va:
        res = res + i.value

    return Interpreter.Number(res)

def Inc(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Inc')

    return Interpreter.Number(a.value + 1)

def Sub(a,b,*va):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))

    testNumber(a,'Sub')
    testNumber(b,'Sub')
    testNumberVar(va,'Sub')

    res = a.value - b.value

    for i in va:
        res = res - i.value

    return Interpreter.Number(res)

def Dec(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Dec')

    return Interpreter.Number(a.value - 1)

def Mul(a,b,*va):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))

    testNumber(a,'Mul')
    testNumber(b,'Mul')
    testNumberVar(va,'Mul')

    res = a.value * b.value

    for i in va:
        res = res * i.value

    return Interpreter.Number(res)

def Div(a,b,*va):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))
    assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),va)))

    testNumber(a,'Div')
    testNumber(b,'Div')
    testNumberVar(va,'Div')

    res = a.value / b.value

    for i in va:
        res = res / i.value

    return Interpreter.Number(res)

def Mod(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    testNumber(a,'Mod')
    testNumber(b,'Mod')

    res = math.fmod(a.value,b.value)

    return Interpreter.Number(res)

def Lt(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    testNumber(a,'Lt')
    testNumber(b,'Lt')

    res = a.value < b.value

    return Interpreter.Boolean(res)

def Lte(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    testNumber(a,'Lte')
    testNumber(b,'Lte')

    res = a.value <= b.value

    return Interpreter.Boolean(res)

def Gt(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    testNumber(a,'Gt')
    testNumber(b,'Gt')

    res = a.value > b.value

    return Interpreter.Boolean(res)

def Gte(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    testNumber(a,'Gte')
    testNumber(b,'Gte')

    res = a.value >= b.value

    return Interpreter.Boolean(res)

def Sin(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Sin')

    return Interpreter.Number(math.sin(a.value))

def Cos(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Cos')

    return Interpreter.Number(math.cos(a.value))

def Tan(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Sin')

    return Interpreter.Number(math.tan(a.value))

def Ctg(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Ctg')

    return Interpreter.Number(1/math.tan(a.value))

def ASin(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'ASin')

    return Interpreter.Number(math.asin(a.value))

def ACos(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'ACos')

    return Interpreter.Number(math.acos(a.value))

def ATan(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'ATan')

    return Interpreter.Number(math.atan(a.value))

def ACtg(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'ACtg')

    return Interpreter.Number(math.pi / 2 - math.atan(a.value))

def Rad2Deg(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Rad2Deg')

    return Interpreter.Number(math.degrees(a.value))

def Deg2Rad(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Deg2Rad')

    return Interpreter.Number(math.radians(a.value))

def Exp(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Exp')

    return Interpreter.Number(math.exp(a.value))

def Log(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    testNumber(a,'Log')
    testNumber(b,'Log')

    return Interpreter.Number(math.log(a.value,b.value))

def Ln(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Ln')

    return Interpreter.Number(math.log(a.value,math.e))

def Lg(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Lg')

    return Interpreter.Number(math.log(a.value,10))

def Sqrt(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Sqrt')

    return Interpreter.Number(math.sqrt(a.value))

def Pow(a,b):
    assert(isinstance(a,Interpreter.InAtom))
    assert(isinstance(b,Interpreter.InAtom))

    testNumber(a,'Pow')
    testNumber(b,'Pow')

    return Interpreter.Number(math.pow(a.value,b.value))

def Abs(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Abs')

    return Interpreter.Number(math.fabs(a.value))

def Ceill(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Ceill')

    return Interpreter.Number(math.ceil(a.value))

def Floor(a):
    assert(isinstance(a,Interpreter.InAtom))

    testNumber(a,'Floor')

    return Interpreter.Number(math.floor(a.value))

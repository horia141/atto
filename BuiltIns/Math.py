import Interpreter
import BuiltIns.Utils

def Add(a,b,*va):
    res = a.value + b.value

    for i in va:
        res = res + i.value

    return Interpreter.Number(res)

def Sub(a,b,*va):
    res = a.value - b.value

    for i in va:
        res = res - i.value

    return Interpreter.Number(res)

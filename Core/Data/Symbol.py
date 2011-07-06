import Interpreter
import Application
import Utils

def GetModule():
    return Application.Module(
        'Core:Data:Symbol',
        {'is-symbol?':  Interpreter.BuiltIn(IsSymbol)},
        {},['is-symbol?'])

def IsSymbol(a):
    assert(isinstance(a,Interpreter.InAtom))

    return Interpreter.Boolean(Utils.isSymbol(a))

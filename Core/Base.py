import Interpreter
import Application
import Core.Utils

from Core.Utils import isBoolean
from Core.Utils import isNumber
from Core.Utils import isSymbol
from Core.Utils import testSymbol
from Core.Utils import isString
from Core.Utils import isFunc
from Core.Utils import isDict
from Core.Utils import argStarAsList

def Type(x):
    assert(isinstance(x,Interpreter.InAtom))

    if isBoolean(x):
        return Interpreter.Symbol('Boolean')
    if isNumber(x):
        return Interpreter.Symbol('Number')
    if isSymbol(x):
        return Interpreter.Symbol('Symbol')
    if isString(x):
        return Interpreter.Symbol('String')
    if isFunc(x):
        return Interpreter.Symbol('Func')
    if isDict(x):
        return Interpreter.Symbol('Dict')

    raise Exception('Critical Error: Invalid control path!')

def SameType(x,y):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(y,Interpreter.InAtom))

    return Interpreter.Boolean(isinstance(x,y.__class__))

def Eq(x,y):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(y,Interpreter.InAtom))

    return Interpreter.Boolean(x == y)

def Neq(x,y):
    assert(isinstance(x,Interpreter.InAtom))
    assert(isinstance(y,Interpreter.InAtom))

    return Interpreter.Boolean(x != y)

def Case(x,cases_star):
    pass

def Id(x):
    assert(isinstance(x,Interpreter.InAtom))

    return x

def Module(name,directives_star):
    assert(isinstance(name,Interpreter.InAtom))
    assert(isinstance(directives_star,Interpreter.InAtom))

    testSymbol(name,'Module')

    directives = argStarAsList(directives_star)

    c_type = Interpreter.Symbol('Type')
    c_define = Interpreter.Symbol('Define')
    c_import = Interpreter.Symbol('Import')
    c_export = Interpreter.Symbol('Export')

    defines = {}
    imports = {}
    exports = []

    for directive in directives:
        t = directive.get(c_type)

        if t == c_define:
            defines[directive.get(Interpreter.Symbol('Name')).value] = directive.get(Interpreter.Symbol('Value'))
        elif t == c_import:
            imports[directive.get(Interpreter.Symbol('Module'))] = \
                (directive.get(Interpreter.Symbol('As')).value,
                 map(lambda x: x.value,argStarAsList(directive.get(Interpreter.Symbol('Names')))))
        elif t == c_export:
            exports.extend(map(lambda x: x.value,argStarAsList(directive.get(Interpreter.Symbol('Names')))))
        else:
            raise Exception('Invalid module directive type!')

    return Application.Module(name.value,defines,imports,exports)

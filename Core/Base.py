import Interpreter
import Application
import Utils

def GetModule():
    def xapply(block):
        assert(isinstance(block,Interpreter.InAtom))

        Utils.testBlock(block,'xapply')
        return block.apply([],{})

    lenv = {'xapply':Interpreter.BuiltIn(xapply)}

    return Application.Module(
        'Core:Base',
        {'type':        Interpreter.BuiltIn(Type),
         'same-type?':  Interpreter.BuiltIn(SameType),
         'eq?':         Interpreter.BuiltIn(Eq),
         'neq?':        Interpreter.BuiltIn(Neq),
         'case':        Interpreter.BuiltIn(Case),
         'id':          Interpreter.BuiltIn(Id),
         'module':      Interpreter.BuiltIn(Module),
         'define':      Application.fastInterpret('[name value <Type Define Name (name) Value (value)>]',{}),
         'import':      Application.fastInterpret('[module names* as=full! <Type Import Module (xapply (module)) Names (names) As (as)>]',lenv),
         'export':      Application.fastInterpret('[names* <Type Export Names (names)>]',{})},
        {},['type','same-type?','eq?','neq?','case','id','module','define','import','export'])

def Type(x):
    assert(isinstance(x,Interpreter.InAtom))

    if Utils.isBoolean(x):
        return Interpreter.Symbol('Boolean')
    if Utils.isNumber(x):
        return Interpreter.Symbol('Number')
    if Utils.isSymbol(x):
        return Interpreter.Symbol('Symbol')
    if Utils.isString(x):
        return Interpreter.Symbol('String')
    if Utils.isFunc(x):
        return Interpreter.Symbol('Func')
    if Utils.isDict(x):
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

    Utils.testSymbol(name,'Module')

    directives = Utils.argStarAsList(directives_star)

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
                 map(lambda x: x.value,Utils.argStarAsList(directive.get(Interpreter.Symbol('Names')))))
        elif t == c_export:
            exports.extend(map(lambda x: x.value,Utils.argStarAsList(directive.get(Interpreter.Symbol('Names')))))
        else:
            raise Exception('Invalid module directive type!')

    return Application.Module(name.value,defines,imports,exports)

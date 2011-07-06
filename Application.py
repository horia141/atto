import Stream
import Tokenizer
import Parser
import Interpreter

import Core.Utils
import Core.Base
import Core.Data.Boolean
import Core.Data.Number
import Core.Data.Symbol
import Core.Data.String
import Core.Data.Func
import Core.Data.Dict
import Core.Control.Flow

class ModuleCache(object):
    def __init__(self):
        self.__cache = {}

    def add(self,module):
        assert(isinstance(module,Module))

        self.__cache[module.name] = module

    def lookup(self,mod_name,def_name):
        assert(isinstance(mod_name,str))
        assert(isinstance(def_name,str))

        if mod_name not in self.__cache:
            raise Exception('Can\'t find module "' + mod_name + '"!')

        return self.__cache[mod_name].lookup(def_name)

    def resolve(self):
        for (modname,module) in self.__cache.iteritems():
            new_env = {}

            for (def_name,def_value) in module.defines.iteritems():
                if def_name in new_env:
                    raise Exception('Define "' + def_name + '" is defined more than once!')

                new_env[def_name] = def_value

            for (im_mod,(im_newname,im_names)) in module.imports.iteritems():
                if im_newname == 'none':
                    addname = ''
                elif im_newname == 'full':
                    addname = im_mod.name
                else:
                    addname = im_newname

                for im_name in im_names:
                    if im_name not in im_mod.exports:
                        raise Exception('Module "' + im_mod.name + '" does not export "' + im_name + '"!')

                    fullname = addname + ':' + im_name if addname else im_name

                    if fullname in new_env:
                        raise Exception('Define "' + fullname + '" is imported more than once or is already defined!')

                    new_env[fullname] = im_mod.defines[im_name]

            for (defname,define) in module.defines.iteritems():
                if isinstance(define,Interpreter.Func):
                    for (name,value) in new_env.iteritems():
                        define.envSet(name,value)

class ApAtom(Interpreter.InAtom):
    pass

class Module(ApAtom):
    def __init__(self,name,defines,imports,exports):
        assert(isinstance(name,str))
        assert(isinstance(defines,dict))
        assert(all(map(lambda x: isinstance(x,str),defines.keys())))
        assert(all(map(lambda x: isinstance(x,Interpreter.InAtom),defines.values())))
        assert(isinstance(imports,dict))
        assert(all(map(lambda x: isinstance(x,Module),imports.keys())))
        assert(all(map(lambda x: isinstance(x,tuple) and len(x) == 2,imports.values())))
        assert(all(map(lambda x: isinstance(x[0],str),imports.values())))
        assert(all(map(lambda x: isinstance(x[1],list),imports.values())))
        assert(all(map(lambda x: all(map(lambda y: isinstance(y,str),x[1])),imports.values())))
        assert(isinstance(exports,list))
        assert(all(map(lambda x: isinstance(x,str),exports)))
        assert(all(map(lambda x: x in defines.keys(),exports)))

        self.__name = name
        self.__defines = defines
        self.__imports = imports
        self.__exports = exports

    def __hash__(self):
        return hash(self.name)

    def lookup(self,def_name):
        assert(isinstance(def_name,str))

        if def_name not in self.__defines:
            raise Exception('Can\'t find name "' + def_name + '"!')

        return self.__defines[def_name]

    @property
    def name(self):
        return self.__name

    @property
    def defines(self):
        return self.__defines

    @property
    def imports(self):
        return self.__imports

    @property
    def exports(self):
        return self.__exports

class Data(ApAtom):
    pass

class View(ApAtom):
    pass

class Task(ApAtom):
    pass

def fasti(program):
    a = Stream.Buffer(program)
    b = Tokenizer.tokenize(a)
    c = Parser.parse(b)

    return Interpreter.interpret(c[1],{})

def doit(program):
    basic_env = {'type':                     Interpreter.BuiltIn(Core.Base.Type),
                 'same-type?':               Interpreter.BuiltIn(Core.Base.SameType),
                 'eq?':                      Interpreter.BuiltIn(Core.Base.Eq),
                 'neq?':                     Interpreter.BuiltIn(Core.Base.Neq),
                 'case':                     Interpreter.BuiltIn(Core.Base.Case),
                 'id':                       Interpreter.BuiltIn(Core.Base.Id),
                 'module':                   Interpreter.BuiltIn(Core.Base.Module),
                 'define':                   fasti('[name value <Type Define Name (name) Value (value)>]'),
                 'import':                   fasti('[module names* as=full! <Type Import Module (module) Names (names) As (as)>]'),
                 'export':                   fasti('[names* <Type Export Names (names)>]'),
                 'Core:Data:Boolean':
                     Module('Core:Data:Boolean',
                            {'is-boolean?':  Interpreter.BuiltIn(Core.Data.Boolean.IsBoolean),
                             'not':          Interpreter.BuiltIn(Core.Data.Boolean.Not), 
                             'and':          Interpreter.BuiltIn(Core.Data.Boolean.And),
                             'or':           Interpreter.BuiltIn(Core.Data.Boolean.Or)},
                            {},['is-boolean?','not','and','or']),
                 'Core:Data:Number':
                     Module('Core:Data:Number',
                            {'pi':           Interpreter.Number(3.1415926535897931),
                             'e':            Interpreter.Number(2.7182818284590451),
                             'is-number?':   Interpreter.BuiltIn(Core.Data.Number.IsNumber),
                             'add':          Interpreter.BuiltIn(Core.Data.Number.Add),
                             'inc':          Interpreter.BuiltIn(Core.Data.Number.Inc),
                             'sub':          Interpreter.BuiltIn(Core.Data.Number.Sub),
                             'dec':          Interpreter.BuiltIn(Core.Data.Number.Dec),
                             'mul':          Interpreter.BuiltIn(Core.Data.Number.Mul),
                             'div':          Interpreter.BuiltIn(Core.Data.Number.Div),
                             'mod':          Interpreter.BuiltIn(Core.Data.Number.Mod),
                             'lt':           Interpreter.BuiltIn(Core.Data.Number.Lt),
                             'lte':          Interpreter.BuiltIn(Core.Data.Number.Lte),
                             'gt':           Interpreter.BuiltIn(Core.Data.Number.Gt),
                             'gte':          Interpreter.BuiltIn(Core.Data.Number.Gte),
                             'sin':          Interpreter.BuiltIn(Core.Data.Number.Sin),
                             'cos':          Interpreter.BuiltIn(Core.Data.Number.Cos),
                             'tan':          Interpreter.BuiltIn(Core.Data.Number.Tan),
                             'ctg':          Interpreter.BuiltIn(Core.Data.Number.Ctg),
                             'asin':         Interpreter.BuiltIn(Core.Data.Number.ASin),
                             'acos':         Interpreter.BuiltIn(Core.Data.Number.ACos),
                             'atan':         Interpreter.BuiltIn(Core.Data.Number.ATan),
                             'actg':         Interpreter.BuiltIn(Core.Data.Number.ACtg),
                             'rad2deg':      Interpreter.BuiltIn(Core.Data.Number.Rad2Deg),
                             'deg2rad':      Interpreter.BuiltIn(Core.Data.Number.Deg2Rad),
                             'exp':          Interpreter.BuiltIn(Core.Data.Number.Exp),
                             'log':          Interpreter.BuiltIn(Core.Data.Number.Log),
                             'ln':           Interpreter.BuiltIn(Core.Data.Number.Ln),
                             'lg':           Interpreter.BuiltIn(Core.Data.Number.Lg),
                             'sqrt':         Interpreter.BuiltIn(Core.Data.Number.Sqrt),
                             'pow':          Interpreter.BuiltIn(Core.Data.Number.Pow),
                             'abs':          Interpreter.BuiltIn(Core.Data.Number.Abs),
                             'ceill':        Interpreter.BuiltIn(Core.Data.Number.Ceill),
                             'floor':         Interpreter.BuiltIn(Core.Data.Number.Floor)},
                            {},['pi','e','is-number?','add','inc','sub','dec','mul','div','mod',
                                'lt','lte','gt','gte','sin','cos','tan','ctg','asin','acos','actg',
                                'rad2deg','deg2rad','exp','log','ln','lg','sqrt','pow','abs','ceill',
                                'floor']),
                 'Core:Data:Symbol':
                     Module('Core:Data:Symbol',
                            {'is-symbol?':   Interpreter.BuiltIn(Core.Data.Symbol.IsSymbol)},
                            {},['is-symbol?']),
                 'Core:Data:String':
                     Module('Core:Data:String',
                            {'is-string?':   Interpreter.BuiltIn(Core.Data.String.IsString),
                             'cat':          Interpreter.BuiltIn(Core.Data.String.Cat)},
                            {},['is-string?','cat']),
                 'Core:Data:Func':
                     Module('Core:Data:Func',
                            {'is-func?':     Interpreter.BuiltIn(Core.Data.Func.IsFunc),
                             'apply':        Interpreter.BuiltIn(Core.Data.Func.Apply),
                             'curry':        Interpreter.BuiltIn(Core.Data.Func.Curry),
                             'inject':       Interpreter.BuiltIn(Core.Data.Func.Inject),
                             'env-has-key?': Interpreter.BuiltIn(Core.Data.Func.EnvHasKey),
                             'env-get':      Interpreter.BuiltIn(Core.Data.Func.EnvGet),
                             'env-set':      Interpreter.BuiltIn(Core.Data.Func.EnvSet)},
                            {},['is-func?','apply','curry','inject','env-has-key?','env-get',
                                'env-set']),
                 'Core:Data:Dict':
                     Module('Core:Data:Dict',
                            {'is-dict?':     Interpreter.BuiltIn(Core.Data.Dict.IsDict),
                             'has-key?':     Interpreter.BuiltIn(Core.Data.Dict.HasKey),
                             'get':          Interpreter.BuiltIn(Core.Data.Dict.Get),
                             'set':          Interpreter.BuiltIn(Core.Data.Dict.Set),
                             'keys':         Interpreter.BuiltIn(Core.Data.Dict.Keys),
                             'values':       Interpreter.BuiltIn(Core.Data.Dict.Values)},
                            {},['is-dict?','has-key?','get','set','keys','values']),
                 'Core:Control:Flow':
                     Module('Core:Control:Flow',
                            {'if':           Interpreter.BuiltIn(Core.Control.Flow.If),
                             'let':          Interpreter.BuiltIn(Core.Control.Flow.Let)},
                            {},['if','let'])}

    a = Stream.Buffer(program)
    b = Tokenizer.tokenize(a)
    mc = ModuleCache()
    pos = 0

    while pos < len(b):
        (pos,c) = Parser.parse(b,pos)
        new_mod = Interpreter.interpret(c,basic_env)

        if not isinstance(new_mod,Module):
            raise Exception('Stop messing around!')

        mc.add(new_mod)
        basic_env[new_mod.name] = new_mod

    mc.resolve()
    return mc.lookup('Main','Start').apply([],{})

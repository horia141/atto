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
    def __init__(self):
        pass

    def __str__(self):
        raise Exception('Invalid call to "__str__" for ApAtom object!')

    def __repr__(self):
        return str(self)

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

        super(Module,self).__init__()

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

def fastInterpret(program):
    a = Stream.Buffer(program)
    b = Tokenizer.tokenize(a)
    c = Parser.parse(b)

    return Interpreter.interpret(c[1],{})

def moduleName(name):
    name_parts = name.split('.')

    if len(name_parts) > 1:
        return (name,[name_parts[-1]])
    else:
        return (name,[])

def run(program):
    basic_env = {}
    flatten_modules = frozenset(['Core.Base'])
    builtin_modules = ['Core.Base',
                       'Core.Data.Boolean',
                       'Core.Data.Number',
                       'Core.Data.Symbol',
                       'Core.Data.String',
                       'Core.Data.Func',
                       'Core.Data.Dict',
                       'Core.Control.Flow']

    for builtin_module_name in builtin_modules:
        (bef,aft) = moduleName(builtin_module_name)
        mod = __import__(bef,fromlist=aft)

        if not 'GetModule' in mod.__dict__:
            raise Exception('Python module "' + builtin_module_name + '" does not contain a valid Atto module!')

        attoMod = mod.GetModule()

        if not isinstance(attoMod,Module):
            raise Exception('Python module "' + builtin_module_name + '" does not contain a valid Atto module!')

        basic_env[attoMod.name] = attoMod

        if builtin_module_name in flatten_modules:
            for export in attoMod.exports:
                basic_env[export] = attoMod.lookup(export)

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

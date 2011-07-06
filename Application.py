import getopt
import os
import os.path

import Stream
import Tokenizer
import Parser
import Interpreter

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

def run(argv):
    mc = ModuleCache()
    toplevel_env = {}
    start = 'Main:Start'
    flatten_modules = frozenset(['./Core/Base.py'])
    source_names = ['./Core/Base.py',
                    './Core/Data/Boolean.py',
                    './Core/Data/Number.py',
                    './Core/Data/Symbol.py',
                    './Core/Data/String.py',
                    './Core/Data/Func.py',
                    './Core/Data/Dict.py',
                    './Core/Control/Flow.py']

    # Parse "command-line" arguments.

    try:
        opts,args = getopt.gnu_getopt(argv[1:],'hs:',['help','start='])
    except getopt.GetoptError,err:
        print str(err)
        _usage()
        return 2

    for name,value in opts:
        if name in ('-h','--help'):
            _usage()
            return 1
        elif name in ('-s','--start'):
            start = value
        else:
            assert False

    source_names.extend(args)

    # Load atto and builtin modules.

    try:
        for source_name in source_names:
            (root,ext) = os.path.splitext(source_name)

            if ext == '.py':
                f = open(source_name,'r')
                text = f.read()
                f.close()

                hack = compile(text,source_name,mode='exec')
                mod = eval('(eval(hack),GetModule() if "GetModule" in globals() else None)',{'hack':hack})[1]

                if not mod or not isinstance(mod,Module):
                    raise Exception('Python module "' + source_name + '" does not contain a valid Atto module!')

                toplevel_env[mod.name] = mod
                mc.add(mod)

                if source_name in flatten_modules:
                    for export in mod.exports:
                        toplevel_env[export] = mod.lookup(export)
            elif ext == '.atto':
                f = open(source_name,'r')
                text = f.read()
                f.close()

                buff = Stream.Buffer(text)
                tokens = Tokenizer.tokenize(buff)
                pos = 0

                while pos < len(tokens):
                    (pos,c) = Parser.parse(tokens,pos)
                    mod = Interpreter.interpret(c,toplevel_env)

                    if not isinstance(mod,Module):
                        raise Exception('Source "' + source_name + '" does not contain a valid Atto module!')

                    toplevel_env[mod.name] = mod
                    mc.add(mod)
            else:
                raise Exception('Unrecognized source path "' + source_name + '"!')
    except Exception,e:
        print e
        return 1

    # Execute the scripts starting at the function specifed
    # by "start".

    mc.resolve()
    (start_mod,start_func) = _moduleName(start)
    print mc.lookup(start_mod,start_func).apply([],{})

    return 0

def _moduleName(name):
    name_parts = name.split(':')
    return (':'.join(name_parts[:-1]),name_parts[-1])

def _usage():
    pass

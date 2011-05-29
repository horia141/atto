import re

import Stream
import Tokenizer
import Parser

class InAtom(object):
    pass

class Symbol(InAtom):
    def __init__(self,text):
        assert(isinstance(text,str))

        self.__text = str(text)

    def __str__(self):
        if re.search('\s',self.__text):
            return '`' + self.__text + '`'
        else:
            return self.__text

    def __repr__(self):
        return 'Interpreter.Symbol(' + repr(self.__text) + ')'

    def __eq__(self):
        if not isinstance(other,Symbol):
            return False

        return self.__text == other.__text

    def clone(self):
        return Symbol(self.__text)

    @property
    def text(self):
        return self.__text

class Func(InAtom):
    def __init__(self,arg_names,vararg_name,vararg_minone,body,env):
        assert(isinstance(arg_names,list))
        assert(all(map(lambda x: isinstance(x,str),arg_names)))
        assert(vararg_name == None or isinstance(vararg_name,str))
        assert((vararg_name == None and vararg_minone == None) or \
                vararg_name != None and isinstance(vararg_minone,bool))
        assert(isinstance(body,Parser.PsAtom))
        assert(isinstance(env,list))
        assert(all(map(lambda x: isinstance(x,dict),env)))
        assert(all(map(lambda x: all(map(lambda y: isinstance(y,str),x.keys())),env)))
        assert(all(map(lambda x: all(map(lambda y: isinstance(y,InAtom),x.values())),env)))

        self.__arg_names = map(lambda x: str(x),arg_names)
        self.__vararg_name = str(vararg_name) if vararg_name else None
        self.__vararg_minone = vararg_minone
        self.__body = body.clone()
        self.__env = map(lambda x: dict([(str(y),x[y].clone()) for y in x]),env)

    def __str__(self):
        return '[' + ' '.join(map(str,self.__arg_names)) + \
                     (' ' if len(self.__arg_names) > 0 else '') + \
                     (str(self.__vararg_name) + \
                      ('+ ' if self.__vararg_minone else '* ') if self.__vararg_name else '') + \
                     str(self.__body) + ']'

    def __repr__(self):
        return 'Interpreter.Func(' + repr(self.__arg_names) + ',' + repr(self.__vararg_name) + \
                                     repr(self.__vararg_minone) + ',' + repr(self.__body) + \
                                     repr(self.__env) + ')'

    def __eq__(self,other):
        return Flase

    def clone(self):
        return Func(self.__arg_names,self.__vararg_name,self.__vararg_minone,
                    self.__body,self.__env)

    @property
    def argNames(self):
        return self.__arg_names

    @property
    def hasVararg(self):
        return self.__vararg_name != None

    @property
    def varargName(self):
        return self.__vararg_name

    @property
    def varargMinOne(self):
        return self.__vararg_minone

    @property
    def body(self):
        return self.__body

    @property
    def env(self):
        return self.__env

class Dict(InAtom):
    def __init__(self,keyvalues):
        assert(isinstance(keyvalues,list))
        assert(all(map(lambda x: isinstance(x,tuple),keyvalues)))
        assert(all(map(lambda x: isinstance(x[0],InAtom),keyvalues)))
        assert(all(map(lambda x: isinstance(x[1],InAtom),keyvalues)))

        self.__keyvalues = map(lambda x: (x[0].clone(),x[1].clone()),keyvalues)

    def __str__(self):
        return '<' + ' '.join(map(lambda x: str(x[0]) + ' ' + str(x[1]),self.__keyvalues)) + '>'

    def __repr__(self):
        return 'Interpreter.Dict(' + repr(self.__keyvalues) + ')'

    def __eq__(self,other):
        if not isinstance(other,Dict):
            return False

        if len(self.__keyvalues) != len(other.__keyvalues):
            return False

        search_dict = dict(other.__keyvalues)

        for (key,value) in self.__keyvalues:
            if key not in search_dict:
                return False

        return True

    def clone(self):
        return Dict(self.__keyvalues)

    @property
    def keyvalues(self):
        return self.__keyvalues

def interpret(atom,env):
    assert(isinstance(atom,Parser.PsAtom))
    assert(isinstance(env,list))
    assert(all(map(lambda x: isinstance(x,dict),env)))
    assert(all(map(lambda x: all(map(lambda y: isinstance(y,str),x.keys())),env)))
    assert(all(map(lambda x: all(map(lambda y: isinstance(y,InAtom),x.values())),env)))

    if isinstance(atom,Parser.Call):
        action = interpter(atom.action,env)

        if isinstance(action,Symbol):
            for one_env in reversed(env):
                if action.text in one_env:
                    fn = one_env[action.text]
                    break
            else:
                raise Exception('Couldn\'t find name "' + action.text + '"!')
        elif isinstance(action,Func):
            fn = action
        elif isinstance(action,Dict):
            fn = action
        else:
            raise Exception('Now, this shouldn\'t really happen!')

        if isinstance(fn,Symbol):
            pass
        elif isinstance(fn,Func):
            pass
        elif isinstance(fn,Dict):
            pass
        else:
            raise Exception('This again, should not be the case!')
    elif isinstance(atom,Parser.Lookup):
        for one_env in reversed(env):
            if atom.names[0].text in one_env:
                return one_env[atom.names[0].text]

        raise Exception('Can\'t find name "' + atom.names[0].text + '"!')
    elif isinstance(atom,Parser.Symbol):
        return Symbol(atom.text)
    elif isinstance(atom,Parser.Func):
        arg_names = []
        vararg_name = None
        vararg_minone = None

        for arg_name in atom.argNames:
            name = interpret(arg_name,env)

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but Symbol!')

            arg_names.append(name.text)

        if atom.hasVararg:
            name = interpret(atom.varargName,env)

            if not isinstance(name,Symbol):
                raise Exception('Argument name can\'t be anything but Symbol!')

            vararg_name = name.text
            vararg_minone = atom.varargMinOne

        return Func(arg_names,vararg_name,vararg_minone,atom.body,env)
    elif isinstance(atom,Parser.Dict):
        keyvalues = []

        for item in atom.keyvalues:
            keyvalues.append((interpret(item.key,env),
                              interpret(item.value,env)))

        return Dict(keyvalues)
    else:
        raise Exception('Invalid atom!')

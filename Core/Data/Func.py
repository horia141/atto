import Interpreter
import Core.Utils

from Core.Utils import isFunc
from Core.Utils import testFunc

def IsFunc(f):
    assert(isinstance(f,Interpreter.InAtom))

    return Interpreter.Boolean(isFunc(f))

def Apply(f,*args):
    pass

def Inject(f,arg):
    pass

def Curry(f,*args):
    pass

def ExtendEnv(f,*args):
    pass

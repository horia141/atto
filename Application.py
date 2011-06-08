import Stream
import Tokenizer
import Parser
import Interpreter
import BuiltIns.Utils
import BuiltIns.Boolean
import BuiltIns.Number

def doit(program):
    a = Stream.Buffer(program)
    b = Tokenizer.tokenize(a)
    c = Parser.parse(b)

    basic_env = {'is-boolean?':Interpreter.BuiltIn(BuiltIns.Boolean.IsBoolean),
                 'not':        Interpreter.BuiltIn(BuiltIns.Boolean.Not), 
                 'and':        Interpreter.BuiltIn(BuiltIns.Boolean.And),
                 'or':         Interpreter.BuiltIn(BuiltIns.Boolean.Or),
                 'pi':         Interpreter.Number(3.1415926535897931),
                 'e':          Interpreter.Number(2.7182818284590451),
                 'is-number?': Interpreter.BuiltIn(BuiltIns.Number.IsNumber),
                 'add':        Interpreter.BuiltIn(BuiltIns.Number.Add),
                 'inc':        Interpreter.BuiltIn(BuiltIns.Number.Inc),
                 'sub':        Interpreter.BuiltIn(BuiltIns.Number.Sub),
                 'dec':        Interpreter.BuiltIn(BuiltIns.Number.Dec),
                 'mul':        Interpreter.BuiltIn(BuiltIns.Number.Mul),
                 'div':        Interpreter.BuiltIn(BuiltIns.Number.Div),
                 'mod':        Interpreter.BuiltIn(BuiltIns.Number.Mod),
                 'lt':         Interpreter.BuiltIn(BuiltIns.Number.Lt),
                 'lte':        Interpreter.BuiltIn(BuiltIns.Number.Lte),
                 'gt':         Interpreter.BuiltIn(BuiltIns.Number.Gt),
                 'gte':        Interpreter.BuiltIn(BuiltIns.Number.Gte),
                 'sin':        Interpreter.BuiltIn(BuiltIns.Number.Sin),
                 'cos':        Interpreter.BuiltIn(BuiltIns.Number.Cos),
                 'tan':        Interpreter.BuiltIn(BuiltIns.Number.Tan),
                 'ctg':        Interpreter.BuiltIn(BuiltIns.Number.Ctg),
                 'asin':       Interpreter.BuiltIn(BuiltIns.Number.ASin),
                 'acos':       Interpreter.BuiltIn(BuiltIns.Number.ACos),
                 'atan':       Interpreter.BuiltIn(BuiltIns.Number.ATan),
                 'actg':       Interpreter.BuiltIn(BuiltIns.Number.ACtg),
                 'rad2deg':    Interpreter.BuiltIn(BuiltIns.Number.Rad2Deg),
                 'deg2rad':    Interpreter.BuiltIn(BuiltIns.Number.Deg2Rad),
                 'exp':        Interpreter.BuiltIn(BuiltIns.Number.Exp),
                 'log':        Interpreter.BuiltIn(BuiltIns.Number.Log),
                 'ln':         Interpreter.BuiltIn(BuiltIns.Number.Ln),
                 'lg':         Interpreter.BuiltIn(BuiltIns.Number.Lg),
                 'sqrt':       Interpreter.BuiltIn(BuiltIns.Number.Sqrt),
                 'pow':        Interpreter.BuiltIn(BuiltIns.Number.Pow),
                 'abs':        Interpreter.BuiltIn(BuiltIns.Number.Abs),
                 'ceill':      Interpreter.BuiltIn(BuiltIns.Number.Ceill),
                 'floor':      Interpreter.BuiltIn(BuiltIns.Number.Floor)}

    return Interpreter.interpret(c[1],[basic_env],None)

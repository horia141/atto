import Stream
import Tokenizer
import Parser
import Interpreter

import Core.Utils
import Core.Data.Boolean
import Core.Data.Number
import Core.Data.Symbol
import Core.Data.String
import Core.Data.Func
import Core.Data.Dict
import Core.Control.Flow

def doit(program):
    a = Stream.Buffer(program)
    b = Tokenizer.tokenize(a)
    c = Parser.parse(b)

    basic_env = {'is-boolean?':     Interpreter.BuiltIn(Core.Data.Boolean.IsBoolean),
                 'not':             Interpreter.BuiltIn(Core.Data.Boolean.Not), 
                 'and':             Interpreter.BuiltIn(Core.Data.Boolean.And),
                 'or':              Interpreter.BuiltIn(Core.Data.Boolean.Or),
                 'pi':              Interpreter.Number(3.1415926535897931),
                 'e':               Interpreter.Number(2.7182818284590451),
                 'is-number?':      Interpreter.BuiltIn(Core.Data.Number.IsNumber),
                 'add':             Interpreter.BuiltIn(Core.Data.Number.Add),
                 'inc':             Interpreter.BuiltIn(Core.Data.Number.Inc),
                 'sub':             Interpreter.BuiltIn(Core.Data.Number.Sub),
                 'dec':             Interpreter.BuiltIn(Core.Data.Number.Dec),
                 'mul':             Interpreter.BuiltIn(Core.Data.Number.Mul),
                 'div':             Interpreter.BuiltIn(Core.Data.Number.Div),
                 'mod':             Interpreter.BuiltIn(Core.Data.Number.Mod),
                 'lt':              Interpreter.BuiltIn(Core.Data.Number.Lt),
                 'lte':             Interpreter.BuiltIn(Core.Data.Number.Lte),
                 'gt':              Interpreter.BuiltIn(Core.Data.Number.Gt),
                 'gte':             Interpreter.BuiltIn(Core.Data.Number.Gte),
                 'sin':             Interpreter.BuiltIn(Core.Data.Number.Sin),
                 'cos':             Interpreter.BuiltIn(Core.Data.Number.Cos),
                 'tan':             Interpreter.BuiltIn(Core.Data.Number.Tan),
                 'ctg':             Interpreter.BuiltIn(Core.Data.Number.Ctg),
                 'asin':            Interpreter.BuiltIn(Core.Data.Number.ASin),
                 'acos':            Interpreter.BuiltIn(Core.Data.Number.ACos),
                 'atan':            Interpreter.BuiltIn(Core.Data.Number.ATan),
                 'actg':            Interpreter.BuiltIn(Core.Data.Number.ACtg),
                 'rad2deg':         Interpreter.BuiltIn(Core.Data.Number.Rad2Deg),
                 'deg2rad':         Interpreter.BuiltIn(Core.Data.Number.Deg2Rad),
                 'exp':             Interpreter.BuiltIn(Core.Data.Number.Exp),
                 'log':             Interpreter.BuiltIn(Core.Data.Number.Log),
                 'ln':              Interpreter.BuiltIn(Core.Data.Number.Ln),
                 'lg':              Interpreter.BuiltIn(Core.Data.Number.Lg),
                 'sqrt':            Interpreter.BuiltIn(Core.Data.Number.Sqrt),
                 'pow':             Interpreter.BuiltIn(Core.Data.Number.Pow),
                 'abs':             Interpreter.BuiltIn(Core.Data.Number.Abs),
                 'ceill':           Interpreter.BuiltIn(Core.Data.Number.Ceill),
                 'floor':           Interpreter.BuiltIn(Core.Data.Number.Floor),
                 'is-symbol?':      Interpreter.BuiltIn(Core.Data.Symbol.IsSymbol),
                 'is-string?':      Interpreter.BuiltIn(Core.Data.String.IsString),
                 'cat':             Interpreter.BuiltIn(Core.Data.String.Cat),
                 'is-func?':        Interpreter.BuiltIn(Core.Data.Func.IsFunc),
                 'apply':           Interpreter.BuiltIn(Core.Data.Func.Apply),
                 'curry':           Interpreter.BuiltIn(Core.Data.Func.Curry),
                 'inject':          Interpreter.BuiltIn(Core.Data.Func.Inject),
                 'env-has-key?':    Interpreter.BuiltIn(Core.Data.Func.EnvHasKey),
                 'env-get':         Interpreter.BuiltIn(Core.Data.Func.EnvGet),
                 'env-set':         Interpreter.BuiltIn(Core.Data.Func.EnvSet),
                 'is-dict?':        Interpreter.BuiltIn(Core.Data.Dict.IsDict),
                 'has-key?':        Interpreter.BuiltIn(Core.Data.Dict.HasKey),
                 'get':             Interpreter.BuiltIn(Core.Data.Dict.Get),
                 'set':             Interpreter.BuiltIn(Core.Data.Dict.Set),
                 'keys':            Interpreter.BuiltIn(Core.Data.Dict.Keys),
                 'values':          Interpreter.BuiltIn(Core.Data.Dict.Values),
                 'if':              Interpreter.BuiltIn(Core.Control.Flow.If)}

    return Interpreter.interpret(c[1],basic_env,None)

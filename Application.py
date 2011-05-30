import Stream
import Tokenizer
import Parser
import Interpreter
import BuiltIns.Utils
import BuiltIns.Math

def doit(program):
    a = Stream.Buffer(program)
    b = Tokenizer.tokenize(a)
    c = Parser.parse(b)

    basic_env = {'add':Interpreter.BuiltIn(BuiltIns.Math.Add)}

    return Interpreter.interpret(c[1],[basic_env])

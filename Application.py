import Stream
import Tokenizer
import Parser
import Interpreter
import BuiltIns

def doit(program):
    a = Stream.Buffer(program)
    b = Tokenizer.tokenize(a)
    c = Parser.parse(b)

    basic_env = {'add':Interpreter.BuiltIn(BuiltIns.Add)}

    return Interpreter.interpret(c[1],[basic_env])

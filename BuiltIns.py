import Interpreter

def Add(a,b,*va):
    if not isinstance(a,Interpreter.Symbol):
        raise Exception('Invalid argument for builtin "add"!')

    if not isinstance(a,Interpreter.Symbol):
        raise Exception('Invalid argument for builtin "add"!')

    try:
        res = int(a.text) + int(b.text)

        for i in range(0,len(va)):
            res = res + int(va[i].text)
    except ValueError,e:
            raise Exception('Invalid argument for builtin "add"!')

    return Interpreter.Symbol(str(res))

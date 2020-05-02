"""
This is a tiny Scheme interpreter borrowed heavily from Peter Norvig's lis.py
interpreter. This particluar version only supports the lambda calculus. That
technically makes it Turing complete, if you're willing to fight Church encoded
data.
"""

def main():
    while True:
        try:
            print(eval(read()))

        except KeyboardInterrupt:
            break

        except Exception as e:
            print(e)


def read():
    "Read in user input and parse."
    return parse(input("> "))

def parse(input):
    "Parse user input into Python list."
    return read_from_tokens(tokenize(input))

def tokenize(string):
    "Split string into tokens."
    return string.replace("(", " ( ").replace(")", " ) ").split()

def read_from_tokens(tokens):
    "Convert list of tokens into Python list of rudimentary types."

    if len(tokens) == 0:
        raise SyntaxError("Unexpect EOF")

    token = tokens.pop(0)

    if "(" == token:
        lst = []

        while tokens[0] != ")":
            lst.append(read_from_tokens(tokens))

        tokens.pop(0) # Pop off the trailing ")"

        return lst

    elif ")" == token:
        raise SyntaxError("Unexpected ')'")

    else:
        return atom(token)

def atom(token):
    "Convert strings into their appropriate datatypes."

    try:
        return int(token)
    
    except ValueError:
        try:
            return float(token)

        except ValueError:
            return str(token)



class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args): 
        return eval(self.body, Env(self.parms, args, self.env))

class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        return self if (var in self) else self.outer.find(var)

def standard_env():
    return Env()

global_env = standard_env()

def eval(expression, env=global_env):
    "Evaluate the input program"

    if isinstance(expression, str):
        return env.find(expression)[expression]

    elif not isinstance(expression, list):
        return expression

    elif expression[0] == "define":
        (_, var, exp) = expression
        env[var] = eval(exp, env)

    elif expression[0] == "lambda" or expression[0] == "\\":
        (_, params, body) = expression
        return Procedure(params, body, env)

    else:
        proc = eval(expression[0], env)
        args = [ eval(exp, env) for exp in expression[1:] ]
        return proc(*args)



if __name__ == "__main__":
    main()
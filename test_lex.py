from peco import *

ws = many(eat(r'\s+|#.+'))
pos = lambda s: s._replace(stack=s.stack + (s.pos,))


def token(tag, expr, f=lambda x: x):
    return seq(cite(eat(expr)), pos, to(lambda x, p: (tag, f(x), p - len(x))))


scan = alt(
    token('num', r'0[xX][a-fA-F0-9]+', lambda x: int(x, 16)),
    token('num', r'\d+', int),
    token('str', r'"[^"]*"', lambda x: x[1:-1]),
    token('op', r'[+\-*/=;()]'),
    token('id', r'\w+')
)

main = seq(group(many(seq(ws, scan))), ws)


def test():
    src = '''
    # comment
    a = 0xff;
    b = 42 + 1;
    print("hello");
    '''
    tokens = ((('id', 'a', 19), ('op', '=', 21), ('num', 255, 23),
               ('op', ';', 27), ('id', 'b', 33), ('op', '=', 35),
               ('num', 42, 37), ('op', '+', 40), ('num', 1, 42),
               ('op', ';', 43), ('id', 'print', 49), ('op', '(', 54),
               ('str', 'hello', 55), ('op', ')', 62), ('op', ';', 63)),)
    s = parse(src, main)
    assert s.ok and s.stack == tokens

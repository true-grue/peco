from peco import *

expr = lambda s: expr(s)
ws = many(space)

atom = seq(cite(letter), to(lambda x: x))
func = seq(sym('λ'), ws, atom, ws, sym('.'), ws, expr,
           to(lambda arg, body: ('func', arg, body)))

part = alt(seq(sym('('), ws, expr, ws, sym(')')), expr)
appl = seq(part, ws, part, to(lambda a, b: ('apply', a, b)))
expr = left(alt(func, appl, atom))


def test():
    x = 'λb. λg. λa.b( ga)'.strip()
    y = (('func', 'b', ('func', 'g', ('func', 'a', ('apply', 'b', ('apply', 'g', 'a'))))),)
    s = parse(x, expr)
    assert s.ok and s.stack == y

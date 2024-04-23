from peco import *

ws = many(space)
expr = lambda s: expr(s)
tok = lambda f: memo(seq(ws, f))
skip = lambda c: tok(sym(c))

atom = tok(cite(letter))
func = seq(skip('λ'), atom, skip('.'), expr,
           to(lambda arg, body: ('func', arg, body)))

part = alt(seq(skip('('), expr, skip(')')), expr)
appl = seq(part, part, to(lambda a, b: ('apply', a, b)))
expr = left(alt(func, appl, atom))


def test():
    x = ' λb. λg. λa.b( ga)  '
    y = (('func', 'b', ('func', 'g', ('func', 'a', ('apply', 'b', ('apply', 'g', 'a'))))),)
    s = parse(x, seq(expr, ws))
    assert s.ok and s.stack == y

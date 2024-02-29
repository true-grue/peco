from peco import *

ws = many(space)
tok = lambda f: memo(seq(ws, f))
skip = lambda c: tok(sym(c))
op = lambda c: tok(cite(sym(c)))

mkvar = to(lambda x: ('var', x))
mknum = to(lambda x: ('num', x))
mkbop = to(lambda a, o, b: (o, a, b))

var = seq(cite(seq(letter, many(alt(letter, digit)))), mkvar)
num = seq(cite(some(digit)), mknum)

expr = lambda s: expr(s)
term = lambda s: term(s)

factor = alt(
    seq(skip('('), expr, skip(')')),
    tok(var),
    tok(num)
)

expr = left(alt(
    seq(expr, op('+'), term, mkbop),
    seq(expr, op('-'), term, mkbop),
    term
))

term = left(alt(
    seq(term, op('*'), factor, mkbop),
    seq(term, op('/'), factor, mkbop),
    factor
))


def test():
    x = '  (foo+ bar)*4 - (12/ a) '
    y = (('-', ('*', ('+', ('var', 'foo'), ('var', 'bar')), ('num', '4')),
         ('/', ('num', '12'), ('var', 'a'))),)
    s = parse(x, seq(expr, ws))
    assert s.ok and s.stack == y

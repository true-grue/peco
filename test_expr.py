from peco import *

ws = eat(r'\s*')
token = lambda f: memo(seq(ws, f))
tok = lambda c: token(push(eat(c)))
skip = lambda c: token(eat(c))

mkvar = to(lambda x: ('var', x))
mknum = to(lambda x: ('num', x))
mkbop = to(lambda a, o, b: (o, a, b))

var = seq(tok(r'[a-zA-Z][a-zA-Z0-9]*'), mkvar)
num = seq(tok(r'\d+'), mknum)

expr = lambda s: expr(s)
term = lambda s: term(s)

factor = alt(
    seq(skip(r'\('), expr, skip(r'\)')),
    var,
    num
)

expr = left(alt(
    seq(expr, tok(r'\+'), term, mkbop),
    seq(expr, tok(r'-'), term, mkbop),
    term
))

term = left(alt(
    seq(term, tok(r'\*'), factor, mkbop),
    seq(term, tok(r'/'), factor, mkbop),
    factor
))

main = seq(expr, ws)


def test():
    x = '  (foo+ bar)*4 - (12/ a) '
    y = (('-', ('*', ('+', ('var', 'foo'), ('var', 'bar')), ('num', '4')),
         ('/', ('num', '12'), ('var', 'a'))), None)
    s = parse(x, main)
    assert s.ok and s.stack == y
    err_x = '(b*b - 3* a*c )) + a'
    err_y = '               ^'
    s = parse(err_x, main)
    assert not s.ok and ' ' * s.glob['err'] + '^' == err_y

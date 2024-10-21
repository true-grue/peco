from peco import *

ws = eat(r'\s*')
scan = lambda f: memo(seq(ws, f))
skip = lambda c: scan(eat(c))
tok = lambda c: scan(cite(eat(c)))

mkfun = to(lambda arg, body: ('fun', arg, body))
mkapp = to(lambda func, arg: ('app', func, arg))

expr = lambda s: expr(s)
atom = tok(r'[a-zA-Z]')
func = seq(skip('λ'), atom, skip('.'), expr, mkfun)
appl = seq(expr, expr, mkapp)

pars = seq(skip(r'\('), expr, skip(r'\)'))
expr = left(alt(func, appl, atom, pars))


def test():
    x = ' λb. λg. (λa.b g(a))  '
    y = (('fun', 'b',
          ('fun', 'g',
           ('fun', 'a',
            ('app', 'b',
             ('app', 'g', 'a'))))),)
    s = parse(x, seq(expr, ws))
    assert s.ok and s.stack == y

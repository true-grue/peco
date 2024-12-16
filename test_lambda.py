from peco import *

ws = eat(r'\s*')
token = lambda f: memo(seq(ws, f))
tok = lambda c: token(push(eat(c)))
skip = lambda c: token(eat(c))

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
             ('app', 'g', 'a'))))), None)
    s = parse(x, seq(expr, ws))
    assert s.ok and s.stack == y

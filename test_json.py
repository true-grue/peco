from peco import *

ws = many(space)
tok = lambda f: memo(seq(ws, f))
skip = lambda c: tok(sym(c))
op = lambda c: tok(cite(sym(c)))

int_part = alt(seq(range_of('1', '9'), many(digit)), sym('0'))
frac = seq(sym('.'), some(digit))
exp = seq(one_of('eE'), opt(one_of('-+')), some(digit))
number = seq(cite(seq(opt(sym('-')), int_part, opt(frac), opt(exp))),
             to(lambda x: float(x)))
uhex = alt(digit, range_of('a', 'f'), range_of('A', 'F'))
uXXXX = seq(sym('u'), uhex, uhex, uhex, uhex)
escaped = seq(sym('\\'), alt(one_of('"\\/bfnrt'), uXXXX))
string = seq(sym('"'), cite(many(alt(non(one_of('"\\')), escaped))), sym('"'))

value = lambda s: value(s)

true = seq(skip('true'), to(lambda: True))
false = seq(skip('false'), to(lambda: False))
null = seq(skip('null'), to(lambda: None))
array = group(seq(skip('['), opt(list_of(value, skip(','))), skip(']')))
member = group(seq(tok(string), skip(':'), value))
obj = seq(skip('{'), group(opt(list_of(member, skip(',')))), skip('}'),
          to(lambda x: dict(x)))
value = alt(tok(number), tok(string), true, false, null, obj, array)
json = seq(alt(obj, array), ws)


def test():
    x = '{ "Object":{"Zoom": false, "Property1":{"Property2":' \
        '{"Color":[0,153,255,0]},"Width":40}} }'
    y = ({'Object': {'Zoom': False, 'Property1': {'Property2': {'Color':
         (0.0, 153.0, 255.0, 0.0)}, 'Width': 40.0}}},)
    s = parse(x, json)
    assert s.ok and s.stack == y

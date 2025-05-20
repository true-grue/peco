from peco import *

mknum = to(lambda x: float(x))
mktrue = to(lambda: True)
mkfalse = to(lambda: False)
mknone = to(lambda: None)
mkobj = to(lambda x: dict(x))

ws = eat(r'\s*')
scan = lambda f: memo(seq(ws, f))
skip = lambda c: scan(eat(c))

number = seq(push(eat(r'-?([1-9]\d+|0)(\.\d+)?((e|E)(-\+)*\d)?')), mknum)
uXXXX = eat(r'u(\d|[a-f]|[A-F]){4}')
escaped = seq(eat(r'\\'), alt(eat(r'["\\/bfnrt]'), uXXXX))
string = seq(eat('"'), push(many(alt(eat(r'[^"\\]'), escaped))), eat('"'))

true = seq(skip('true'), mktrue)
false = seq(skip('false'), mkfalse)
null = seq(skip('null'), mknone)

value = lambda s: value(s)

array = group(seq(skip(r'\['), opt(list_of(value, skip(','))), skip(']')))
member = group(seq(scan(string), skip(':'), value))
obj = seq(skip('{'), group(opt(list_of(member, skip(',')))), skip('}'), mkobj)
value = alt(scan(number), scan(string), true, false, null, obj, array)
json = seq(alt(obj, array), ws)


def test():
    x = '{ "Object":{"Zoom": false, "Property1":{"Property2":' \
        '{"Color":[0,153,255,-0]},"Width":40}} }'
    y = ({'Object': {'Zoom': False, 'Property1': {'Property2': {'Color':
         (0.0, 153.0, 255.0, -0.0)}, 'Width': 40.0}}}, None)
    s = parse(x, json)
    assert s.ok and s.stack == y

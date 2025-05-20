from peco import *

mknum = to(lambda n: float(n))
mkstr = to(lambda s: s[1:-1])
mkarr = to(lambda a: list(a))
mkobj = to(lambda o: dict(o))

ws = many(eat(r'\s+|#.+'))
token = lambda f: memo(seq(ws, f))
tok = lambda c: token(push(eat(c)))
skip = lambda c: token(eat(c))

num = seq(tok(r'[-+]?\d+'), mknum)
string = seq(tok(r'"[^"]*"'), mkstr)
name = tok(r'[_a-zA-Z][_a-zA-Z0-9]*')

val = lambda s: val(s)
array = seq(skip(r'\['), group(many(val)), skip(r'\]'), mkarr)
item = group(seq(name, skip(r'='), val))
obj = seq(skip(r'{'), group(many(item)), skip(r'}'), mkobj)
val = alt(num, string, array, obj)

main = seq(group(many(item)), ws, mkobj)


def test():
    src = '''
    # comment
    vm = {
        ip = [192 168 44 44]
        memory = 1024
        synced_folders = [{
            host_path = "data/"
            guest_path = "/var/www"
            type = "default"
        }]
    }
    log = "conf.log"
    '''
    obj = ({'vm': {'ip': [192.0, 168.0, 44.0, 44.0], 'memory': 1024.0,
           'synced_folders': [{'host_path': 'data/', 'guest_path': '/var/www',
           'type': 'default'}]}, 'log': 'conf.log'}, None)
    s = parse(src, main)
    assert s.ok and s.stack == obj

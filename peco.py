from collections import namedtuple

State = namedtuple('State', 'data pos ok stack glob')


def eat(f, size=1):
    def parse(s):
        new_pos = s.pos + size
        if new_pos <= len(s.data) and f(s.data[s.pos:new_pos]):
            s.glob['pos'] = max(s.glob['pos'], new_pos)
            return s._replace(pos=new_pos)
        return s._replace(ok=False)
    return parse


def seq(*funcs):
    def parse(s):
        for f in funcs:
            if not (s := f(s)).ok:
                return s
        return s
    return parse


def alt(*funcs):
    def parse(s):
        for f in funcs:
            if (new_s := f(s)).ok:
                return new_s
        return new_s
    return parse


def many(f):
    def parse(s):
        while True:
            if not (new_s := f(s)).ok:
                return s
            s = new_s
    return parse


def cite(f):
    def parse(s):
        pos = s.pos
        if not (s := f(s)).ok:
            return s
        return s._replace(stack=s.stack + (s.data[pos:s.pos],))
    return parse


def to(f):
    n = f.__code__.co_argcount

    def parse(s):
        pos = len(s.stack) - n
        return s._replace(stack=s.stack[:pos] + (f(*s.stack[pos:]),))
    return parse


def group(f):
    def parse(s):
        stack = s.stack
        if not (s := f(s)).ok:
            return s
        return s._replace(stack=stack + (s.stack[len(stack):],))
    return parse


def peek(f):
    def parse(s):
        return s._replace(ok=f(s).ok)
    return parse


def npeek(f):
    def parse(s):
        return s._replace(ok=not f(s).ok)
    return parse


def memo(f):
    def parse(s):
        key = f, s.pos
        tab = s.glob['tab']
        if key not in tab:
            tab[key] = f(s)
        return tab[key]
    return parse


def left(f):
    def parse(s):
        key = f, s.pos
        tab = s.glob['tab']
        if key not in tab:
            tab[key] = s._replace(ok=False)
            pos = s.pos
            while (s := f(s._replace(pos=pos))).pos > tab[key].pos:
                tab[key] = s
        return tab[key]
    return parse


def parse(data, f):
    s = f(State(data, 0, True, (), dict(tab={}, pos=0)))
    return s._replace(ok=s.ok and s.pos == len(s.data))


sym = lambda x: eat(lambda y: x == y, len(x))
dot = eat(lambda _: True)
space = eat(str.isspace)
digit = eat(str.isdigit)
letter = eat(str.isalpha)
one_of = lambda chars: eat(lambda c: c in chars)
range_of = lambda a, b: eat(lambda c: a <= c <= b)
empty = lambda s: s
opt = lambda f: alt(f, empty)
some = lambda f: seq(f, many(f))
non = lambda f: seq(npeek(f), dot)
list_of = lambda f, d: seq(f, many(seq(d, f)))

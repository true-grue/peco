# Author: Peter Sovietov
import re
from collections import namedtuple

__all__ = 'Peco Stack eat seq alt many push to group peek npeek memo left ' \
		  'parse empty opt some list_of'.split()

Peco = namedtuple('Peco', 'text pos ok stack glob')

Stack = namedtuple('Stack', 'car cdr', defaults=(None,))

def _till(stack, till):
    if stack == till:
        return ()
    if stack.cdr == till:
        return (stack.car,)
    acc = []
    while stack != till:
        acc.append(stack.car)
        stack = stack.cdr
    acc.reverse()
    return tuple(acc)


def _split(stack, n):
    if n == 0:
        return (), stack
    if n == 1:
        return (stack.car,), stack.cdr
    acc = []
    while n > 0:
        acc.append(stack.car)
        stack = stack.cdr
        n -= 1
    acc.reverse()
    return tuple(acc), stack


def eat(expr):
    code = re.compile(expr)

    def parse(s):
        if (m := code.match(s.text[s.pos:])) is None:
            return s._replace(ok=False)
        pos = s.pos + len(m.group())
        s.glob['err'] = max(s.glob['err'], pos)
        return s._replace(pos=pos)
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
        while (new_s := f(s)).ok:
            s = new_s
        return s
    return parse


def push(f):
    def parse(s):
        pos = s.pos
        if not (s := f(s)).ok:
            return s
        return s._replace(stack=Stack(s.text[pos:s.pos], s.stack))
    return parse


def to(f):
    n = f.__code__.co_argcount

    def parse(s):
        args, stack = _split(s.stack, n)
        return s._replace(stack=Stack(f(*args), stack))
    return parse


def group(f):
    def parse(s):
        stack = s.stack
        if not (s := f(s)).ok:
            return s
        grp = _till(s.stack, stack)
        return s._replace(stack=Stack(grp, stack))
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


def parse(text, f, **kwargs):
    glob = dict(err=0, tab={}) | (kwargs or {})
    s = f(Peco(text, 0, True, None, glob))
    return s._replace(ok=s.ok and s.pos == len(s.text))


empty = lambda s: s
opt = lambda f: alt(f, empty)
some = lambda f: seq(f, many(f))
list_of = lambda f, d: seq(f, many(seq(d, f)))

# Author: Peter Sovietov
from peco import alt as old_alt, seq


class Cut(Exception):
    pass


def alt(*funcs):
    f = old_alt(*funcs)

    def parse(s):
        try:
            return f(s)
        except Cut:
            return s._replace(ok=False)
    return parse


def cut(*funcs):
    f = seq(*funcs)

    def parse(s):
        if (s := f(s)).ok:
            return s
        raise Cut
    return parse

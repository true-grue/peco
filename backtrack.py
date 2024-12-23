# Author: Peter Sovietov
class Backtrack(Exception):
    pass


def back(f):
    def parse(s):
        try:
            return f(s)
        except Backtrack:
            return s._replace(ok=False)
    return parse


def track(f):
    def parse(s):
        if (s := f(s)).ok:
            return s
        raise Backtrack
    return parse

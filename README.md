# peco

peco: tiny parser combinators library written in pure Python.

### Getting Started

A **parser** in peco is a function `parse: State -> State` accepting a parser state and returning a new parser state:

```python
State = namedtuple('State', 'data pos ok stack glob')
```

Every `State` instance consists of the following fields:
1. `data` contains the original sequence, the sequence can be represented by a string, a list of tokens, etc.
2. `pos` contains the current integer offset.
3. `ok` is a flag indicating whether a parser has been successfully applied to the given `State` or not.
4. `glob` contains the shared context, e.g. the mutable data that might be required by a specific parser. For example, this `glob` field is used in the [memo](https://github.com/true-grue/peco/blob/main/peco.py#L82) combinator.
5. `stack` is a list representing the stack-based memory of the constructed parser, this type of memory allows to implement [pushdown automata](https://en.m.wikipedia.org/wiki/Pushdown_automaton).

A **combinator** in peco allows to construct a parser which somehow process the accepted `State` instance and returns the new, possibly modified, `State` instance. The currently supported combinators include:
1. `def eat(f, size=1)` — eats `size` tokens from the `state.data` token sequence starting from the `state.pos` offset and returns a new `State` instance with `ok=True`, but only if `f(state)` returns `True`. Otherwise, `eat` returns a new `State` instance with `ok=False`.
2. `def alt(*funcs)` — applies parsers from the `funcs` list sequentially, until one of the parsers returns a `State` with `ok=True`:
```python
# The 'digit' and 'letter' combinators are defined in peco.py.
# However, it is easy to redefine them manually:
digit = eat(str.isdigit)
letter = eat(str.isalpha)
digit_or_letter = alt(digit, letter)
parse("1", digit_or_letter).ok  # True
parse("A", digit_or_letter).ok  # True
parse("$", digit_or_letter).ok  # False
```
3. `def seq(*funcs)` — similarly to `alt`, this combinator sequentially applies all parsers from the `funcs` list. However, `seq` requires all parsers from `funcs` to return `State` with `ok=True`, otherwise it stops parsing:
```python
digit_and_letter = seq(digit, letter)
parse("1d", digit_and_letter).ok  # True
parse("1", digit_and_letter).ok  # False
```
4. `def many(f)` — applies the `f` parser zero or unlimited times, until `f(state)` returns `ok=False`.
```python
# Given that the 'many' combinator matches tokens 0 or unlimited times,
# integer parsing could be implemented like this:
num = seq(digit, many(digit))
parse("1337", num).ok  # True
parse("", num).ok  # False
```
5. `def cite(f)` — adds a new group of tokens parsed by `f` to the end of `state.stack`, the stack is represented by a tuple.
```python
num = cite(seq(digit, many(digit)))
parse("1234", num).stack  # ("1234", )
```
6. `def to(f)` — pops `n` elements from `state.stack`, then passes the `n` elements to the lambda function `f` as arguments, and then pushes the result of the `f` function execution back to the stack. Here, `n` is equal to the count of arguments of the lambda function `f`.
```python
num = cite(seq(digit, many(digit)))
number = seq(num, to(lambda val: int(val)))
# First, the parser constructed by the 'cite'
# combinator pushes the 1234 number to the stack
# as a string. Then, the parser constructed by
# the 'to' combinator removes one element from
# the stack, applies 'lambda val: int(val)' to it,
# and pushes the obtained integer to the stack.
parse("1234", number).stack  # (1234,)
```
See [peco.py](https://github.com/true-grue/peco/blob/main/peco.py) for more combinators.

### Parsers Built with peco

- [Arithmetic Expressions parser](https://github.com/true-grue/peco/blob/main/test_expr.py)
- [JSON parser](https://github.com/true-grue/peco/blob/main/test_json.py)
- [Lambda Calculus parser](https://github.com/true-grue/peco/blob/main/test_lambda.py)
- [Aozaki Programming Language Parser](https://github.com/neroresearches/aozaki)

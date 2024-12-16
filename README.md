# peco

This is a tiny parser combinator library written in Python.

Main features:

* Implementation in 100 lines of code.
* No installation need, just add peco.py to your project.
* Combined lexical and syntactic parsing using the PEG formalism.
* Lexical rules use regular expressions (see `eat`).
* Stack-based implementation of semantic actions without the scary "monadic parsing" (see `push` and `to`).
* Selective memoization to speed up parsing (see `memo`).
* Left recursion is supported (see `left`).

Combinator functions generate parsers that take and return parsing state. The `state: namedtuple` has the following fields:

* `text: str`. Source text.
* `pos: int`. Position in the `text`.
* `ok: bool`. Parsing result.
* `stack: tuple`. Result of semantic actions.
* `glob: dict`. Contains the error position field (`err`).

Most combinators follow PEG constructions:

* `empty`. Empty string.
* `seq`. Sequence.
* `alt`. Ordered choice.
* `many`. Zero-or-more.
* `some`. One-or-more.
* `opt`. Optional.
* `peek`. And-predicate.
* `npeek`. Not-predicate.

Support for semantic actions:

* `push(f)`. Loads a text fragment parsed by the `f` combinator into `stack`.
* `to(f)`. Takes `n` elements from `stack` and passes them as arguments to the `f` function with arity `n`. The result of `f` is pushed into `stack`.
* `group(f)`. Combines all elements placed on `stack` by `f` into a single tuple.

For examples of using peco's combinators, see the tests.

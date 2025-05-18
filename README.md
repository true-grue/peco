# peco

This is a tiny (100 LOC) parser combinator library in Python.

No installation needed, just add peco.py to your project.

Main features:

* Combined lexical and syntactic parsing using the PEG formalism.
* Lexical rules with regular expressions (see `eat`).
* Stack-based implementation of semantic actions (see `push` and `to`).
* Selective memoization for performance (see `memo`).
* Support for left recursion (see `left`).

Parsers are built from combinators and operate on a `Peco` namedtuple:

* `text: str`. Source text.
* `pos: int`. Position in the `text`.
* `ok: bool`. Parsing result.
* `stack: tuple | None`. Semantic result stack.
* `glob: dict`. Global data, including the error position field (`err`).

Most combinators follow PEG constructs:

* `empty`. Empty string.
* `seq`. Sequence.
* `alt`. Ordered choice.
* `many`. Zero-or-more.
* `some`. One-or-more.
* `opt`. Optional.
* `peek`. And-predicate.
* `npeek`. Not-predicate.

Support for semantic actions:

* `push(f)`. Pushes a text fragment parsed by the `f` combinator onto the `stack`.
* `to(f)`.  Pops `n` elements from the `stack` and passes them as arguments to function `f` with arity `n`; the result is pushed back onto the `stack`.
* `group(f)`. Combines all elements pushed onto the `stack` by `f` into a single tuple.

For examples of using peco's combinators, see the tests.

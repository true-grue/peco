# peco

This is a tiny parser combinator library written in Python.

Main features:

* Implementation in less than 100 lines of code.
* No installation need, just add peco.py to your project.
* Combined lexical and syntactic parsing using the PEG formalism.
* Lexical rules use regular expressions (see `eat`).
* Stack-based implementation of semantic actions without the scary "monadic parsing" (see `push` and `to`).
* Selective memoization to speed up parsing (see `memo`).
* Left recursion is supported (see `left`).

For examples of using peco's parser combinators, see the tests.

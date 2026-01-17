QueryPredicateArg (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Interface QueryPredicateArg

All Known Implementing Classes:
:   `QueryPredicateArg.Capture, QueryPredicateArg.Literal`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public sealed interface QueryPredicateArg
permits [QueryPredicateArg.Capture](QueryPredicateArg.Capture.html "class in io.github.treesitter.jtreesitter"), [QueryPredicateArg.Literal](QueryPredicateArg.Literal.html "class in io.github.treesitter.jtreesitter")

An argument to a [`QueryPredicate`](QueryPredicate.html "class in io.github.treesitter.jtreesitter").

* ## Nested Class Summary

  Nested Classes

  Modifier and Type

  Interface

  Description

  `static final record`

  `QueryPredicateArg.Capture`

  A capture argument (`@value`).

  `static final record`

  `QueryPredicateArg.Literal`

  A literal string argument (`"value"`).
* ## Method Summary

  All MethodsInstance MethodsAbstract Methods

  Modifier and Type

  Method

  Description

  `String`

  `value()`

  The value of the argument.

* ## Method Details

  + ### value

    [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") value()

    The value of the argument.
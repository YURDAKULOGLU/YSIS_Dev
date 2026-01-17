QueryPredicate (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class QueryPredicate

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.QueryPredicate

Direct Known Subclasses:
:   `QueryPredicate.AnyOf, QueryPredicate.Eq, QueryPredicate.Match`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public sealed class QueryPredicate
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")
permits [QueryPredicate.AnyOf](QueryPredicate.AnyOf.html "class in io.github.treesitter.jtreesitter"), [QueryPredicate.Eq](QueryPredicate.Eq.html "class in io.github.treesitter.jtreesitter"), [QueryPredicate.Match](QueryPredicate.Match.html "class in io.github.treesitter.jtreesitter")

A query predicate that associates conditions (or arbitrary metadata) with a pattern.

See Also:
:   * [Predicates](https://tree-sitter.github.io/tree-sitter/using-parsers/queries/3-predicates-and-directives.html)

* ## Nested Class Summary

  Nested Classes

  Modifier and Type

  Class

  Description

  `static final class`

  `QueryPredicate.AnyOf`

  Handles the following predicates:  
  `#any-of?`, `#not-any-of?`

  `static final class`

  `QueryPredicate.Eq`

  Handles the following predicates:  
  `#eq?`, `#not-eq?`, `#any-eq?`, `#any-not-eq?`

  `static final class`

  `QueryPredicate.Match`

  Handles the following predicates:  
  `#match?`, `#not-match?`, `#any-match?`, `#any-not-match?`
* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `List<QueryPredicateArg>`

  `getArgs()`

  Get the arguments given to the predicate.

  `String`

  `getName()`

  Get the name of the predicate.

  `String`

  `toString()`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, wait, wait, wait`

* ## Method Details

  + ### getName

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getName()

    Get the name of the predicate.
  + ### getArgs

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[QueryPredicateArg](QueryPredicateArg.html "interface in io.github.treesitter.jtreesitter")> getArgs()

    Get the arguments given to the predicate.
  + ### toString

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") toString()

    Overrides:
    :   `toString` in class `Object`
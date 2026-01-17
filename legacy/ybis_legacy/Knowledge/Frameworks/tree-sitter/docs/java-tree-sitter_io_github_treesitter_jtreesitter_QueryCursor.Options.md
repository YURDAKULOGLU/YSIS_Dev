QueryCursor.Options (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class QueryCursor.Options

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.QueryCursor.Options

Enclosing class:
:   `QueryCursor`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public static class QueryCursor.Options
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

A class representing the query cursor options.

Since:
:   0.25.0

* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Options()`

  `Options(BiPredicate<QueryPredicate, QueryMatch> predicateCallback)`

  `Options(Predicate<QueryCursor.State> progressCallback)`

  `Options(Predicate<QueryCursor.State> progressCallback,
  BiPredicate<QueryPredicate, QueryMatch> predicateCallback)`
* ## Method Summary

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, toString, wait, wait, wait`

* ## Constructor Details

  + ### Options

    public Options()

    Since:
    :   0.26.0
  + ### Options

    public Options([Predicate](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/function/Predicate.html "class or interface in java.util.function")<[QueryCursor.State](QueryCursor.State.html "class in io.github.treesitter.jtreesitter")> progressCallback,
    [BiPredicate](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/function/BiPredicate.html "class or interface in java.util.function")<[QueryPredicate](QueryPredicate.html "class in io.github.treesitter.jtreesitter"), [QueryMatch](QueryMatch.html "class in io.github.treesitter.jtreesitter")> predicateCallback)

    Parameters:
    :   `progressCallback` - Progress handler. Return `true` to cancel query execution,
        `false` to continue query execution.
    :   `predicateCallback` - Custom predicate handler.

    Since:
    :   0.26.0
  + ### Options

    public Options([Predicate](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/function/Predicate.html "class or interface in java.util.function")<[QueryCursor.State](QueryCursor.State.html "class in io.github.treesitter.jtreesitter")> progressCallback)

    Parameters:
    :   `progressCallback` - Progress handler. Return `true` to cancel query execution,
        `false` to continue query execution.
  + ### Options

    public Options([BiPredicate](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/function/BiPredicate.html "class or interface in java.util.function")<[QueryPredicate](QueryPredicate.html "class in io.github.treesitter.jtreesitter"), [QueryMatch](QueryMatch.html "class in io.github.treesitter.jtreesitter")> predicateCallback)

    Parameters:
    :   `predicateCallback` - Custom predicate handler.
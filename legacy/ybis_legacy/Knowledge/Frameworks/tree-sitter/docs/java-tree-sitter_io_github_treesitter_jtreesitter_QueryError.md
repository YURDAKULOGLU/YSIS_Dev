QueryError (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class QueryError

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Throwable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Throwable.html "class or interface in java.lang")

[java.lang.Exception](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Exception.html "class or interface in java.lang")

[java.lang.RuntimeException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/RuntimeException.html "class or interface in java.lang")

[java.lang.IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.QueryError

All Implemented Interfaces:
:   `Serializable`

Direct Known Subclasses:
:   `QueryError.Capture, QueryError.Field, QueryError.NodeType, QueryError.Predicate, QueryError.Structure, QueryError.Syntax`

---

public abstract sealed class QueryError
extends [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")
permits [QueryError.Capture](QueryError.Capture.html "class in io.github.treesitter.jtreesitter"), [QueryError.Field](QueryError.Field.html "class in io.github.treesitter.jtreesitter"), [QueryError.NodeType](QueryError.NodeType.html "class in io.github.treesitter.jtreesitter"), [QueryError.Structure](QueryError.Structure.html "class in io.github.treesitter.jtreesitter"), [QueryError.Syntax](QueryError.Syntax.html "class in io.github.treesitter.jtreesitter"), [QueryError.Predicate](QueryError.Predicate.html "class in io.github.treesitter.jtreesitter")

Any error that occurred while instantiating a [`Query`](Query.html "class in io.github.treesitter.jtreesitter").

See Also:
:   * [Serialized Form](../../../../serialized-form.html#io.github.treesitter.jtreesitter.QueryError)

* ## Nested Class Summary

  Nested Classes

  Modifier and Type

  Class

  Description

  `static final class`

  `QueryError.Capture`

  A capture name error.

  `static final class`

  `QueryError.Field`

  A field name error.

  `static final class`

  `QueryError.NodeType`

  A node type error.

  `static final class`

  `QueryError.Predicate`

  A query predicate error.

  `static final class`

  `QueryError.Structure`

  A pattern structure error.

  `static final class`

  `QueryError.Syntax`

  A query syntax error.
* ## Method Summary

  ### Methods inherited from class [Throwable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Throwable.html#method-summary "class or interface in java.lang")

  `addSuppressed, fillInStackTrace, getCause, getLocalizedMessage, getMessage, getStackTrace, getSuppressed, initCause, printStackTrace, printStackTrace, printStackTrace, setStackTrace, toString`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, wait, wait, wait`
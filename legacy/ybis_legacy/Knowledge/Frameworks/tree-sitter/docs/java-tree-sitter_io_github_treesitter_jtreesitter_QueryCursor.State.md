QueryCursor.State (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class QueryCursor.State

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.QueryCursor.State

Enclosing class:
:   `QueryCursor`

---

public static final class QueryCursor.State
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

A class representing the current state of the query cursor.

Since:
:   0.25.0

* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `int`

  `getCurrentByteOffset()`

  Get the current byte offset of the cursor.

  `String`

  `toString()`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, wait, wait, wait`

* ## Method Details

  + ### getCurrentByteOffset

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getCurrentByteOffset()

    Get the current byte offset of the cursor.
  + ### toString

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") toString()

    Overrides:
    :   `toString` in class `Object`
Parser.State (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class Parser.State

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.Parser.State

Enclosing class:
:   `Parser`

---

public static final class Parser.State
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

A class representing the current state of the parser.

Since:
:   0.25.0

* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `int`

  `getCurrentByteOffset()`

  Get the current byte offset of the parser.

  `boolean`

  `hasError()`

  Check if the parser has encountered an error.

  `String`

  `toString()`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, wait, wait, wait`

* ## Method Details

  + ### getCurrentByteOffset

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getCurrentByteOffset()

    Get the current byte offset of the parser.
  + ### hasError

    public boolean hasError()

    Check if the parser has encountered an error.
  + ### toString

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") toString()

    Overrides:
    :   `toString` in class `Object`
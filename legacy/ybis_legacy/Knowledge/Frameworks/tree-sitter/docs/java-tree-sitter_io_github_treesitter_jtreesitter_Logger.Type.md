Logger.Type (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Enum Class Logger.Type

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Enum](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Enum.html "class or interface in java.lang")<[Logger.Type](Logger.Type.html "enum class in io.github.treesitter.jtreesitter")>

io.github.treesitter.jtreesitter.Logger.Type

All Implemented Interfaces:
:   `Serializable, Comparable<Logger.Type>, Constable`

Enclosing interface:
:   `Logger`

---

public static enum Logger.Type
extends [Enum](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Enum.html "class or interface in java.lang")<[Logger.Type](Logger.Type.html "enum class in io.github.treesitter.jtreesitter")>

The type of a log message.

* ## Nested Class Summary

  ### Nested classes/interfaces inherited from class [Enum](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Enum.html#nested-class-summary "class or interface in java.lang")

  `Enum.EnumDesc<E>`
* ## Enum Constant Summary

  Enum Constants

  Enum Constant

  Description

  `LEX`

  Lexer message.

  `PARSE`

  Parser message.
* ## Method Summary

  All MethodsStatic MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `static Logger.Type`

  `valueOf(String name)`

  Returns the enum constant of this class with the specified name.

  `static Logger.Type[]`

  `values()`

  Returns an array containing the constants of this enum class, in
  the order they are declared.

  ### Methods inherited from class [Enum](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Enum.html#method-summary "class or interface in java.lang")

  `compareTo, describeConstable, equals, getDeclaringClass, hashCode, name, ordinal, toString, valueOf`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Enum Constant Details

  + ### LEX

    public static final [Logger.Type](Logger.Type.html "enum class in io.github.treesitter.jtreesitter") LEX

    Lexer message.
  + ### PARSE

    public static final [Logger.Type](Logger.Type.html "enum class in io.github.treesitter.jtreesitter") PARSE

    Parser message.
* ## Method Details

  + ### values

    public static [Logger.Type](Logger.Type.html "enum class in io.github.treesitter.jtreesitter")[] values()

    Returns an array containing the constants of this enum class, in
    the order they are declared.

    Returns:
    :   an array containing the constants of this enum class, in the order they are declared
  + ### valueOf

    public static [Logger.Type](Logger.Type.html "enum class in io.github.treesitter.jtreesitter") valueOf([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name)

    Returns the enum constant of this class with the specified name.
    The string must match *exactly* an identifier used to declare an
    enum constant in this class. (Extraneous whitespace characters are
    not permitted.)

    Parameters:
    :   `name` - the name of the enum constant to be returned.

    Returns:
    :   the enum constant with the specified name

    Throws:
    :   `IllegalArgumentException` - if this enum class has no constant with the specified name
    :   `NullPointerException` - if the argument is null
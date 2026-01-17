InputEncoding (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Enum Class InputEncoding

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Enum](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Enum.html "class or interface in java.lang")<[InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter")>

io.github.treesitter.jtreesitter.InputEncoding

All Implemented Interfaces:
:   `Serializable, Comparable<InputEncoding>, Constable`

---

public enum InputEncoding
extends [Enum](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Enum.html "class or interface in java.lang")<[InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter")>

The encoding of source code.

* ## Nested Class Summary

  ### Nested classes/interfaces inherited from class [Enum](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Enum.html#nested-class-summary "class or interface in java.lang")

  `Enum.EnumDesc<E>`
* ## Enum Constant Summary

  Enum Constants

  Enum Constant

  Description

  `UTF_16BE`

  UTF-16 big endian encoding.

  `UTF_16LE`

  UTF-16 little endian encoding.

  `UTF_8`

  UTF-8 encoding.
* ## Method Summary

  All MethodsStatic MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `static InputEncoding`

  `valueOf(String name)`

  Returns the enum constant of this class with the specified name.

  `static @NonNull InputEncoding`

  `valueOf(@NonNull Charset charset)`

  Convert a standard [Charset](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/nio/charset/Charset.html "class or interface in java.nio.charset") to an [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter").

  `static InputEncoding[]`

  `values()`

  Returns an array containing the constants of this enum class, in
  the order they are declared.

  ### Methods inherited from class [Enum](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Enum.html#method-summary "class or interface in java.lang")

  `compareTo, describeConstable, equals, getDeclaringClass, hashCode, name, ordinal, toString, valueOf`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Enum Constant Details

  + ### UTF\_8

    public static final [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") UTF\_8

    UTF-8 encoding.
  + ### UTF\_16LE

    public static final [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") UTF\_16LE

    UTF-16 little endian encoding.

    Since:
    :   0.25.0
  + ### UTF\_16BE

    public static final [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") UTF\_16BE

    UTF-16 big endian encoding.

    Since:
    :   0.25.0
* ## Method Details

  + ### values

    public static [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter")[] values()

    Returns an array containing the constants of this enum class, in
    the order they are declared.

    Returns:
    :   an array containing the constants of this enum class, in the order they are declared
  + ### valueOf

    public static [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") valueOf([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name)

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
  + ### valueOf

    public static [@NonNull](https://jspecify.dev/docs/api/org/jspecify/annotations/NonNull.html "class or interface in org.jspecify.annotations") [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") valueOf([@NonNull](https://jspecify.dev/docs/api/org/jspecify/annotations/NonNull.html "class or interface in org.jspecify.annotations") [Charset](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/nio/charset/Charset.html "class or interface in java.nio.charset") charset)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Convert a standard [Charset](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/nio/charset/Charset.html "class or interface in java.nio.charset") to an [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter").

    Parameters:
    :   `charset` - one of [`StandardCharsets.UTF_8`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/nio/charset/StandardCharsets.html#UTF_8 "class or interface in java.nio.charset"), [`StandardCharsets.UTF_16BE`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/nio/charset/StandardCharsets.html#UTF_16BE "class or interface in java.nio.charset"),
        [`StandardCharsets.UTF_16LE`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/nio/charset/StandardCharsets.html#UTF_16LE "class or interface in java.nio.charset"), or [`StandardCharsets.UTF_16`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/nio/charset/StandardCharsets.html#UTF_16 "class or interface in java.nio.charset") (native byte order).

    Throws:
    :   `IllegalArgumentException` - If the character set is invalid.

    Since:
    :   0.25.1
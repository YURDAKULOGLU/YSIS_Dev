ParseCallback (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Interface ParseCallback

Functional Interface:
:   This is a functional interface and can therefore be used as the assignment target for a lambda expression or method reference.

---

[@FunctionalInterface](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/FunctionalInterface.html "class or interface in java.lang")
public interface ParseCallback

A function that retrieves a chunk of text at a given byte offset and point.

* ## Method Summary

  All MethodsInstance MethodsAbstract MethodsDefault MethodsDeprecated Methods

  Modifier and Type

  Method

  Description

  `default @Nullable String`

  `apply(Integer offset,
  @NonNull Point point)`

  Deprecated, for removal: This API element is subject to removal in a future version.

  Use [`read(int, Point)`](#read(int,io.github.treesitter.jtreesitter.Point)) instead

  `@Nullable String`

  `read(int offset,
  @NonNull Point point)`

  Applies this function to the given arguments.

* ## Method Details

  + ### read

    [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") read([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int offset,
    [@NonNull](https://jspecify.dev/docs/api/org/jspecify/annotations/NonNull.html "class or interface in org.jspecify.annotations") [Point](Point.html "class in io.github.treesitter.jtreesitter") point)

    Applies this function to the given arguments.

    Parameters:
    :   `offset` - the current byte offset
    :   `point` - the current point

    Returns:
    :   A chunk of text or `null` to indicate the end of the document.
  + ### apply

    [@Deprecated](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html "class or interface in java.lang")([since](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html#since() "class or interface in java.lang")="0.26.0",
    [forRemoval](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html#forRemoval() "class or interface in java.lang")=true)
    default [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") apply([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    [Integer](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Integer.html "class or interface in java.lang") offset,
    [@NonNull](https://jspecify.dev/docs/api/org/jspecify/annotations/NonNull.html "class or interface in org.jspecify.annotations") [Point](Point.html "class in io.github.treesitter.jtreesitter") point)

    Deprecated, for removal: This API element is subject to removal in a future version.

    Use [`read(int, Point)`](#read(int,io.github.treesitter.jtreesitter.Point)) instead

    Applies this function to the given arguments.

    Parameters:
    :   `offset` - the current byte offset
    :   `point` - the current point

    Returns:
    :   A chunk of text or `null` to indicate the end of the document.
Logger (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Interface Logger

Functional Interface:
:   This is a functional interface and can therefore be used as the assignment target for a lambda expression or method reference.

---

[@FunctionalInterface](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/FunctionalInterface.html "class or interface in java.lang")
public interface Logger

A function that logs parsing results.

* ## Nested Class Summary

  Nested Classes

  Modifier and Type

  Interface

  Description

  `static enum`

  `Logger.Type`

  The type of a log message.
* ## Method Summary

  All MethodsInstance MethodsAbstract MethodsDefault MethodsDeprecated Methods

  Modifier and Type

  Method

  Description

  `default void`

  `accept(@NonNull Logger.Type type,
  @NonNull String message)`

  Deprecated, for removal: This API element is subject to removal in a future version.

  Use [`log(Logger.Type, String)`](#log(io.github.treesitter.jtreesitter.Logger.Type,java.lang.String)) instead

  `void`

  `log(@NonNull Logger.Type type,
  @NonNull String message)`

  Performs this operation on the given arguments.

* ## Method Details

  + ### log

    void log([@NonNull](https://jspecify.dev/docs/api/org/jspecify/annotations/NonNull.html "class or interface in org.jspecify.annotations") [Logger.Type](Logger.Type.html "enum class in io.github.treesitter.jtreesitter") type,
    [@NonNull](https://jspecify.dev/docs/api/org/jspecify/annotations/NonNull.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") message)

    Performs this operation on the given arguments.

    Parameters:
    :   `type` - the log type
    :   `message` - the log message
  + ### accept

    [@Deprecated](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html "class or interface in java.lang")([since](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html#since() "class or interface in java.lang")="0.26.0",
    [forRemoval](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html#forRemoval() "class or interface in java.lang")=true)
    default void accept([@NonNull](https://jspecify.dev/docs/api/org/jspecify/annotations/NonNull.html "class or interface in org.jspecify.annotations") [Logger.Type](Logger.Type.html "enum class in io.github.treesitter.jtreesitter") type,
    [@NonNull](https://jspecify.dev/docs/api/org/jspecify/annotations/NonNull.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") message)

    Deprecated, for removal: This API element is subject to removal in a future version.

    Use [`log(Logger.Type, String)`](#log(io.github.treesitter.jtreesitter.Logger.Type,java.lang.String)) instead

    Performs this operation on the given arguments.

    Parameters:
    :   `type` - the log type
    :   `message` - the log message
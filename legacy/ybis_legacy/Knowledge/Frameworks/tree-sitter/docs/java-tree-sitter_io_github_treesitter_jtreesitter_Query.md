Query (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class Query

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.Query

All Implemented Interfaces:
:   `AutoCloseable`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public final class Query
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")
implements [AutoCloseable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/AutoCloseable.html "class or interface in java.lang")

A class that represents a set of patterns which match
[nodes](Node.html "class in io.github.treesitter.jtreesitter") in a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter").

See Also:
:   * [Query Syntax](https://tree-sitter.github.io/tree-sitter/using-parsers/queries/1-syntax.html)

* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Query(Language language,
  String source)`

  Create a new query from a string containing one or more S-expression patterns.
* ## Method Summary

  All MethodsInstance MethodsConcrete MethodsDeprecated Methods

  Modifier and Type

  Method

  Description

  `void`

  `close()`

  `void`

  `disableCapture(String name)`

  Disable a certain capture within a query.

  `void`

  `disablePattern(int index)`

  Disable a certain pattern within a query.

  `int`

  `endByteForPattern(int index)`

  Get the byte offset where the given pattern ends in the query's source.

  `int`

  `getCaptureCount()`

  Deprecated.

  Use `getCaptureNames().size()` instead.

  `List<String>`

  `getCaptureNames()`

  Get the names of the captures used in the query.

  `Map<String, Optional<String>>`

  `getPatternAssertions(int index,
  boolean positive)`

  Get the property assertions for the given pattern index.

  `int`

  `getPatternCount()`

  Get the number of patterns in the query.

  `Map<String, Optional<String>>`

  `getPatternSettings(int index)`

  Get the property settings for the given pattern index.

  `List<String>`

  `getStringValues()`

  Get the string literals used in the query.

  `boolean`

  `isPatternGuaranteedAtStep(int offset)`

  Check if a pattern is guaranteed to match once a given byte offset is reached.

  `boolean`

  `isPatternNonLocal(int index)`

  Check if the pattern with the given index is "non-local".

  `boolean`

  `isPatternRooted(int index)`

  Check if the pattern with the given index has a single root node.

  `int`

  `startByteForPattern(int index)`

  Get the byte offset where the given pattern starts in the query's source.

  `String`

  `toString()`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, wait, wait, wait`

* ## Constructor Details

  + ### Query

    public Query([Language](Language.html "class in io.github.treesitter.jtreesitter") language,
    [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") source)
    throws [QueryError](QueryError.html "class in io.github.treesitter.jtreesitter")

    Create a new query from a string containing one or more S-expression patterns.

    Throws:
    :   `QueryError` - If an error occurred while creating the query.
* ## Method Details

  + ### getPatternCount

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getPatternCount()

    Get the number of patterns in the query.
  + ### getCaptureCount

    [@Deprecated](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html "class or interface in java.lang")([since](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html#since() "class or interface in java.lang")="0.25.0")
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getCaptureCount()

    Deprecated.

    Use `getCaptureNames().size()` instead.

    Get the number of captures in the query.
  + ### getCaptureNames

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang")> getCaptureNames()

    Get the names of the captures used in the query.

    Since:
    :   0.25.0
  + ### getStringValues

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang")> getStringValues()

    Get the string literals used in the query.

    Since:
    :   0.25.0
  + ### disablePattern

    public void disablePattern([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Disable a certain pattern within a query.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [pattern count](#getPatternCount()).

    API Note:
    :   This prevents the pattern from matching and removes most of the overhead
        associated with the pattern. Currently, there is no way to undo this.
  + ### disableCapture

    public void disableCapture([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name)
    throws [NoSuchElementException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/NoSuchElementException.html "class or interface in java.util")

    Disable a certain capture within a query.

    Throws:
    :   `NoSuchElementException` - If the capture does not exist.

    API Note:
    :   This prevents the capture from being returned in matches,
        and also avoids most resource usage associated with recording
        the capture. Currently, there is no way to undo this.
  + ### startByteForPattern

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int startByteForPattern([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Get the byte offset where the given pattern starts in the query's source.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [pattern count](#getPatternCount()).
  + ### endByteForPattern

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int endByteForPattern([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Get the byte offset where the given pattern ends in the query's source.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [pattern count](#getPatternCount()).

    Since:
    :   0.23.0
  + ### isPatternRooted

    public boolean isPatternRooted([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Check if the pattern with the given index has a single root node.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [pattern count](#getPatternCount()).
  + ### isPatternNonLocal

    public boolean isPatternNonLocal([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Check if the pattern with the given index is "non-local".

    A non-local pattern has multiple root nodes and can match within
    a repeating sequence of nodes, as specified by the grammar. Non-local
    patterns disable certain optimizations that would otherwise be possible
    when executing a query on a specific range of a syntax tree.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [pattern count](#getPatternCount()).
  + ### isPatternGuaranteedAtStep

    public boolean isPatternGuaranteedAtStep([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int offset)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Check if a pattern is guaranteed to match once a given byte offset is reached.

    Throws:
    :   `IndexOutOfBoundsException` - If the offset exceeds the source length.
  + ### getPatternSettings

    public [Map](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Map.html "class or interface in java.util")<[String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang"), [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang")>> getPatternSettings([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Get the property settings for the given pattern index.

    Properties are set using the `#set!` directive.

    Parameters:
    :   `index` - The index of a pattern within the query.

    Returns:
    :   A map of property keys with optional values.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [pattern count](#getPatternCount()).
  + ### getPatternAssertions

    public [Map](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Map.html "class or interface in java.util")<[String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang"), [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang")>> getPatternAssertions([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index,
    boolean positive)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Get the property assertions for the given pattern index.

    Assertions are performed using the `#is?`
    (positive) and `#is-not?` (negative) predicates.

    Parameters:
    :   `index` - The index of a pattern within the query.
    :   `positive` - Indicates whether to include positive or negative assertions.

    Returns:
    :   A map of property keys with optional values.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [pattern count](#getPatternCount()).
  + ### close

    public void close()
    throws [RuntimeException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/RuntimeException.html "class or interface in java.lang")

    Specified by:
    :   `close` in interface `AutoCloseable`

    Throws:
    :   `RuntimeException`
  + ### toString

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") toString()

    Overrides:
    :   `toString` in class `Object`
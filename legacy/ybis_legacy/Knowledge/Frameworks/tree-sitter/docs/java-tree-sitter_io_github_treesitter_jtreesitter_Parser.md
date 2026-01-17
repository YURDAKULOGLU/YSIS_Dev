Parser (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class Parser

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.Parser

All Implemented Interfaces:
:   `AutoCloseable`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public final class Parser
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")
implements [AutoCloseable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/AutoCloseable.html "class or interface in java.lang")

A class that is used to produce a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter") from source code.

* ## Nested Class Summary

  Nested Classes

  Modifier and Type

  Class

  Description

  `static final class`

  `Parser.Options`

  A class representing the parser options.

  `static final class`

  `Parser.State`

  A class representing the current state of the parser.
* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Parser()`

  Creates a new instance with a `null` language.

  `Parser(Language language)`

  Creates a new instance with the given language.
* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `void`

  `close()`

  `List<Range>`

  `getIncludedRanges()`

  Get the ranges of text that the parser should include when parsing.

  `@Nullable Language`

  `getLanguage()`

  Get the language that the parser will use for parsing.

  `Optional<Tree>`

  `parse(ParseCallback parseCallback,
  InputEncoding encoding)`

  Parse source code from a callback and create a syntax tree.

  `Optional<Tree>`

  `parse(ParseCallback parseCallback,
  InputEncoding encoding,
  @Nullable Tree oldTree,
  @Nullable Parser.Options options)`

  Parse source code from a callback and create a syntax tree.

  `Optional<Tree>`

  `parse(ParseCallback parseCallback,
  InputEncoding encoding,
  Parser.Options options)`

  Parse source code from a callback and create a syntax tree.

  `Optional<Tree>`

  `parse(String source)`

  Parse source code from a string and create a syntax tree.

  `Optional<Tree>`

  `parse(String source,
  InputEncoding encoding)`

  Parse source code from a string and create a syntax tree.

  `Optional<Tree>`

  `parse(String source,
  InputEncoding encoding,
  @Nullable Tree oldTree)`

  Parse source code from a string and create a syntax tree.

  `Optional<Tree>`

  `parse(String source,
  Tree oldTree)`

  Parse source code from a string and create a syntax tree.

  `void`

  `reset()`

  Instruct the parser to start the next [parse](#parse(java.lang.String)) from the beginning.

  `Parser`

  `setIncludedRanges(List<Range> includedRanges)`

  Set the ranges of text that the parser should include when parsing.

  `Parser`

  `setLanguage(Language language)`

  Set the language that the parser will use for parsing.

  `Parser`

  `setLogger(@Nullable Logger logger)`

  Set the logger that the parser will use during parsing.

  `String`

  `toString()`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, wait, wait, wait`

* ## Constructor Details

  + ### Parser

    public Parser()

    Creates a new instance with a `null` language.

    See Also:
    :   - [`setLanguage(Language)`](#setLanguage(io.github.treesitter.jtreesitter.Language))

    API Note:
    :   Parsing cannot be performed while the language is `null`.
  + ### Parser

    public Parser([Language](Language.html "class in io.github.treesitter.jtreesitter") language)

    Creates a new instance with the given language.
* ## Method Details

  + ### getLanguage

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [Language](Language.html "class in io.github.treesitter.jtreesitter") getLanguage()

    Get the language that the parser will use for parsing.
  + ### setLanguage

    public [Parser](Parser.html "class in io.github.treesitter.jtreesitter") setLanguage([Language](Language.html "class in io.github.treesitter.jtreesitter") language)

    Set the language that the parser will use for parsing.
  + ### setLogger

    public [Parser](Parser.html "class in io.github.treesitter.jtreesitter") setLogger([@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [Logger](Logger.html "interface in io.github.treesitter.jtreesitter") logger)

    Set the logger that the parser will use during parsing.

    #### Example

    Copy![Copy snippet](../../../../resource-files/copy.svg)

    ```
    import java.util.logging.Logger;

    Logger logger = Logger.getLogger("tree-sitter");
    Parser parser = new Parser().setLogger(
       (type, message) -> logger.info("%s - %s".formatted(type.name(), message)));
    ```
  + ### getIncludedRanges

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[Range](Range.html "class in io.github.treesitter.jtreesitter")> getIncludedRanges()

    Get the ranges of text that the parser should include when parsing.

    API Note:
    :   By default, the parser will always include entire documents.
  + ### setIncludedRanges

    public [Parser](Parser.html "class in io.github.treesitter.jtreesitter") setIncludedRanges([List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[Range](Range.html "class in io.github.treesitter.jtreesitter")> includedRanges)

    Set the ranges of text that the parser should include when parsing.

    This allows you to parse only a *portion* of a document
    but still return a syntax tree whose ranges match up with the
    document as a whole. You can also pass multiple disjoint ranges.

    Throws:
    :   `IllegalArgumentException` - If the ranges overlap or are not in ascending order.
  + ### parse

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Tree](Tree.html "class in io.github.treesitter.jtreesitter")> parse([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") source)
    throws [IllegalStateException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalStateException.html "class or interface in java.lang")

    Parse source code from a string and create a syntax tree.

    Returns:
    :   An optional [Tree](Tree.html "class in io.github.treesitter.jtreesitter") which is empty if parsing was halted.

    Throws:
    :   `IllegalStateException` - If the parser does not have a language assigned.
  + ### parse

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Tree](Tree.html "class in io.github.treesitter.jtreesitter")> parse([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") source,
    [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") encoding)
    throws [IllegalStateException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalStateException.html "class or interface in java.lang")

    Parse source code from a string and create a syntax tree.

    Returns:
    :   An optional [Tree](Tree.html "class in io.github.treesitter.jtreesitter") which is empty if parsing was halted.

    Throws:
    :   `IllegalStateException` - If the parser does not have a language assigned.
  + ### parse

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Tree](Tree.html "class in io.github.treesitter.jtreesitter")> parse([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") source,
    [Tree](Tree.html "class in io.github.treesitter.jtreesitter") oldTree)
    throws [IllegalStateException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalStateException.html "class or interface in java.lang")

    Parse source code from a string and create a syntax tree.

    If you have already parsed an earlier version of this document and the
    document has since been edited, pass the previous syntax tree to `oldTree`
    so that the unchanged parts of it can be reused. This will save time and memory.
      
    For this to work correctly, you must have already edited the old syntax tree using
    the [`Tree.edit(InputEdit)`](Tree.html#edit(io.github.treesitter.jtreesitter.InputEdit)) method in a way that exactly matches the source code changes.

    Returns:
    :   An optional [Tree](Tree.html "class in io.github.treesitter.jtreesitter") which is empty if parsing was halted.

    Throws:
    :   `IllegalStateException` - If the parser does not have a language assigned.
  + ### parse

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Tree](Tree.html "class in io.github.treesitter.jtreesitter")> parse([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") source,
    [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") encoding,
    [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [Tree](Tree.html "class in io.github.treesitter.jtreesitter") oldTree)
    throws [IllegalStateException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalStateException.html "class or interface in java.lang")

    Parse source code from a string and create a syntax tree.

    If you have already parsed an earlier version of this document and the
    document has since been edited, pass the previous syntax tree to `oldTree`
    so that the unchanged parts of it can be reused. This will save time and memory.
      
    For this to work correctly, you must have already edited the old syntax tree using
    the [`Tree.edit(InputEdit)`](Tree.html#edit(io.github.treesitter.jtreesitter.InputEdit)) method in a way that exactly matches the source code changes.

    Returns:
    :   An optional [Tree](Tree.html "class in io.github.treesitter.jtreesitter") which is empty if parsing was halted.

    Throws:
    :   `IllegalStateException` - If the parser does not have a language assigned.
  + ### parse

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Tree](Tree.html "class in io.github.treesitter.jtreesitter")> parse([ParseCallback](ParseCallback.html "interface in io.github.treesitter.jtreesitter") parseCallback,
    [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") encoding)
    throws [IllegalStateException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalStateException.html "class or interface in java.lang")

    Parse source code from a callback and create a syntax tree.

    Returns:
    :   An optional [Tree](Tree.html "class in io.github.treesitter.jtreesitter") which is empty if parsing was halted.

    Throws:
    :   `IllegalStateException` - If the parser does not have a language assigned.
  + ### parse

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Tree](Tree.html "class in io.github.treesitter.jtreesitter")> parse([ParseCallback](ParseCallback.html "interface in io.github.treesitter.jtreesitter") parseCallback,
    [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") encoding,
    [Parser.Options](Parser.Options.html "class in io.github.treesitter.jtreesitter") options)
    throws [IllegalStateException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalStateException.html "class or interface in java.lang")

    Parse source code from a callback and create a syntax tree.

    Returns:
    :   An optional [Tree](Tree.html "class in io.github.treesitter.jtreesitter") which is empty if parsing was halted.

    Throws:
    :   `IllegalStateException` - If the parser does not have a language assigned.
  + ### parse

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Tree](Tree.html "class in io.github.treesitter.jtreesitter")> parse([ParseCallback](ParseCallback.html "interface in io.github.treesitter.jtreesitter") parseCallback,
    [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter") encoding,
    [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [Tree](Tree.html "class in io.github.treesitter.jtreesitter") oldTree,
    [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [Parser.Options](Parser.Options.html "class in io.github.treesitter.jtreesitter") options)
    throws [IllegalStateException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalStateException.html "class or interface in java.lang")

    Parse source code from a callback and create a syntax tree.

    If you have already parsed an earlier version of this document and the
    document has since been edited, pass the previous syntax tree to `oldTree`
    so that the unchanged parts of it can be reused. This will save time and memory.
      
    For this to work correctly, you must have already edited the old syntax tree using
    the [`Tree.edit(InputEdit)`](Tree.html#edit(io.github.treesitter.jtreesitter.InputEdit)) method in a way that exactly matches the source code changes.

    Returns:
    :   An optional [Tree](Tree.html "class in io.github.treesitter.jtreesitter") which is empty if parsing was halted.

    Throws:
    :   `IllegalStateException` - If the parser does not have a language assigned.
  + ### reset

    public void reset()

    Instruct the parser to start the next [parse](#parse(java.lang.String)) from the beginning.

    API Note:
    :   If parsing was previously halted, the parser will resume where it left off.
        If you intend to parse another document instead, you must call this method first.
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
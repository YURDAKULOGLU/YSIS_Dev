Language (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class Language

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.Language

All Implemented Interfaces:
:   `Cloneable`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public final class Language
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")
implements [Cloneable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Cloneable.html "class or interface in java.lang")

A class that defines how to parse a particular language.

* ## Field Summary

  Fields

  Modifier and Type

  Field

  Description

  `static final int`

  `LANGUAGE_VERSION`

  The latest ABI version that is supported by the current version of the library.

  `static final int`

  `MIN_COMPATIBLE_LANGUAGE_VERSION`

  The earliest ABI version that is supported by the current version of the library.
* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Language(MemorySegment self)`

  Creates a new instance from the given language pointer.
* ## Method Summary

  All MethodsStatic MethodsInstance MethodsConcrete MethodsDeprecated Methods

  Modifier and Type

  Method

  Description

  `Language`

  `clone()`

  Get another reference to the language.

  `boolean`

  `equals(Object o)`

  `int`

  `getAbiVersion()`

  Get the ABI version number for this language.

  `int`

  `getFieldCount()`

  Get the number of distinct field names in this language

  `short`

  `getFieldIdForName(String name)`

  Get the numerical ID for the given field name.

  `@Nullable String`

  `getFieldNameForId(short id)`

  Get the field name for the given numerical id.

  `@Nullable LanguageMetadata`

  `getMetadata()`

  Get the metadata for this language, if available.

  `@Nullable String`

  `getName()`

  Get the name of this language, if available.

  `int`

  `getStateCount()`

  Get the number of valid states in this language

  `short[]`

  `getSubtypes(short supertype)`

  Get all symbols for a given supertype symbol.

  `short[]`

  `getSupertypes()`

  Get all supertype symbols for the language.

  `int`

  `getSymbolCount()`

  Get the number of distinct node types in this language.

  `short`

  `getSymbolForName(String name,
  boolean isNamed)`

  Get the numerical ID for the given node type, or `0` if not found.

  `@Nullable String`

  `getSymbolName(short symbol)`

  Get the node type for the given numerical ID.

  `int`

  `getVersion()`

  Deprecated, for removal: This API element is subject to removal in a future version.

  Use [`getAbiVersion()`](#getAbiVersion()) instead.

  `int`

  `hashCode()`

  `boolean`

  `isNamed(short symbol)`

  Check if the node for the given numerical ID is named.

  `boolean`

  `isSupertype(short symbol)`

  Check if the node for the given numerical ID is a supertype.

  `boolean`

  `isVisible(short symbol)`

  Check if the node for the given numerical ID is visible.

  `static Language`

  `load(SymbolLookup symbols,
  String language)`

  Load a language by looking for its function in the given symbols.

  `LookaheadIterator`

  `lookaheadIterator(short state)`

  Create a new lookahead iterator for the given parse state.

  `short`

  `nextState(short state,
  short symbol)`

  Get the next parse state.

  `Query`

  `query(String source)`

  Deprecated.

  Use the [`Query`](Query.html#%3Cinit%3E(io.github.treesitter.jtreesitter.Language,java.lang.String)) constructor instead.

  `String`

  `toString()`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Field Details

  + ### LANGUAGE\_VERSION

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public static final int LANGUAGE\_VERSION

    The latest ABI version that is supported by the current version of the library.

    API Note:
    :   The Tree-sitter library is generally backwards-compatible with
        languages generated using older CLI versions, but is not forwards-compatible.
  + ### MIN\_COMPATIBLE\_LANGUAGE\_VERSION

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public static final int MIN\_COMPATIBLE\_LANGUAGE\_VERSION

    The earliest ABI version that is supported by the current version of the library.
* ## Constructor Details

  + ### Language

    public Language([MemorySegment](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/MemorySegment.html "class or interface in java.lang.foreign") self)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Creates a new instance from the given language pointer.

    Throws:
    :   `IllegalArgumentException` - If the language version is incompatible.

    Implementation Note:
    :   It is up to the caller to ensure that the pointer is valid.
* ## Method Details

  + ### load

    public static [Language](Language.html "class in io.github.treesitter.jtreesitter") load([SymbolLookup](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SymbolLookup.html "class or interface in java.lang.foreign") symbols,
    [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") language)
    throws [RuntimeException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/RuntimeException.html "class or interface in java.lang")

    Load a language by looking for its function in the given symbols.

    #### Example

    Copy![Copy snippet](../../../../resource-files/copy.svg)

    ```
    String library = System.mapLibraryName("tree-sitter-java");
    SymbolLookup symbols = SymbolLookup.libraryLookup(library, Arena.global());
    Language language = Language.load(symbols, "tree_sitter_java");
    ```

    **The [Arena](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/Arena.html "class or interface in java.lang.foreign") used to load the language
    must not be closed while the language is being used.**

    Throws:
    :   `UnsatisfiedLinkError` - If the language symbol could not be found.
    :   `RuntimeException` - If the language could not be loaded.

    Since:
    :   0.23.1
  + ### getAbiVersion

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getAbiVersion()

    Get the ABI version number for this language.

    This version number is used to ensure that languages
    were generated by a compatible version of Tree-sitter.

    Since:
    :   0.25.0
  + ### getVersion

    [@Deprecated](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html "class or interface in java.lang")([since](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html#since() "class or interface in java.lang")="0.25.0",
    [forRemoval](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html#forRemoval() "class or interface in java.lang")=true)
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getVersion()

    Deprecated, for removal: This API element is subject to removal in a future version.

    Use [`getAbiVersion()`](#getAbiVersion()) instead.

    Get the ABI version number for this language.
  + ### getName

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getName()

    Get the name of this language, if available.
  + ### getMetadata

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [LanguageMetadata](LanguageMetadata.html "class in io.github.treesitter.jtreesitter") getMetadata()

    Get the metadata for this language, if available.

    Since:
    :   0.25.0

    API Note:
    :   This information is generated by the Tree-sitter
        CLI and relies on the language author providing the correct
        metadata in the language's `tree-sitter.json` file.
  + ### getSymbolCount

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getSymbolCount()

    Get the number of distinct node types in this language.
  + ### getStateCount

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getStateCount()

    Get the number of valid states in this language
  + ### getFieldCount

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getFieldCount()

    Get the number of distinct field names in this language
  + ### getSupertypes

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short[] getSupertypes()

    Get all supertype symbols for the language.

    Since:
    :   0.25.0
  + ### getSubtypes

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short[] getSubtypes([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short supertype)

    Get all symbols for a given supertype symbol.

    Since:
    :   0.25.0

    See Also:
    :   - [`getSupertypes()`](#getSupertypes())
  + ### getSymbolName

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getSymbolName([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short symbol)

    Get the node type for the given numerical ID.
  + ### getSymbolForName

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short getSymbolForName([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name,
    boolean isNamed)

    Get the numerical ID for the given node type, or `0` if not found.
  + ### isNamed

    public boolean isNamed([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short symbol)

    Check if the node for the given numerical ID is named.

    See Also:
    :   - [`Node.isNamed()`](Node.html#isNamed())
  + ### isVisible

    public boolean isVisible([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short symbol)

    Check if the node for the given numerical ID is visible.
  + ### isSupertype

    public boolean isSupertype([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short symbol)

    Check if the node for the given numerical ID is a supertype.

    Since:
    :   0.24.0
  + ### getFieldNameForId

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getFieldNameForId([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short id)

    Get the field name for the given numerical id.
  + ### getFieldIdForName

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short getFieldIdForName([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name)

    Get the numerical ID for the given field name.
  + ### nextState

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short nextState([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short state,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short symbol)

    Get the next parse state.

    Copy![Copy snippet](../../../../resource-files/copy.svg)

    ```
    short state = language.nextState(node.getParseState(), node.getGrammarSymbol());
    ```

    Combine this with [`lookaheadIterator(state)`](#lookaheadIterator(short))
    to generate completion suggestions or valid symbols in ERROR nodes.
  + ### lookaheadIterator

    public [LookaheadIterator](LookaheadIterator.html "class in io.github.treesitter.jtreesitter") lookaheadIterator([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short state)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Create a new lookahead iterator for the given parse state.

    Throws:
    :   `IllegalArgumentException` - If the state is invalid for this language.
  + ### query

    [@Deprecated](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html "class or interface in java.lang")([since](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Deprecated.html#since() "class or interface in java.lang")="0.25.0")
    public [Query](Query.html "class in io.github.treesitter.jtreesitter") query([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") source)
    throws [QueryError](QueryError.html "class in io.github.treesitter.jtreesitter")

    Deprecated.

    Use the [`Query`](Query.html#%3Cinit%3E(io.github.treesitter.jtreesitter.Language,java.lang.String)) constructor instead.

    Create a new query from a string containing one or more S-expression patterns.

    Throws:
    :   `QueryError` - If an error occurred while creating the query.
  + ### clone

    public [Language](Language.html "class in io.github.treesitter.jtreesitter") clone()

    Get another reference to the language.

    Since:
    :   0.24.0
  + ### equals

    public boolean equals([Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang") o)

    Overrides:
    :   `equals` in class `Object`
  + ### hashCode

    public int hashCode()

    Overrides:
    :   `hashCode` in class `Object`
  + ### toString

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") toString()

    Overrides:
    :   `toString` in class `Object`
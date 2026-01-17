LookaheadIterator (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class LookaheadIterator

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.LookaheadIterator

All Implemented Interfaces:
:   `AutoCloseable, Iterator<LookaheadIterator.Symbol>`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public final class LookaheadIterator
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")
implements [AutoCloseable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/AutoCloseable.html "class or interface in java.lang"), [Iterator](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Iterator.html "class or interface in java.util")<[LookaheadIterator.Symbol](LookaheadIterator.Symbol.html "class in io.github.treesitter.jtreesitter")>

A class that is used to look up valid symbols in a specific parse state.

Lookahead iterators can be useful to generate suggestions and improve syntax error diagnostics.  
To get symbols valid in an ERROR node, use the lookahead iterator on its first leaf node state.  
For MISSING nodes, a lookahead iterator created on the previous non-extra leaf node may be appropriate.

See Also:
:   * [`Language.lookaheadIterator(short)`](Language.html#lookaheadIterator(short))

* ## Nested Class Summary

  Nested Classes

  Modifier and Type

  Class

  Description

  `static final record`

  `LookaheadIterator.Symbol`

  A class that pairs a symbol ID with its name.
* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `void`

  `close()`

  `short`

  `getCurrentSymbol()`

  Get the current symbol ID.

  `String`

  `getCurrentSymbolName()`

  The current symbol name.

  `Language`

  `getLanguage()`

  Get the current language of the lookahead iterator.

  `boolean`

  `hasNext()`

  Check if the lookahead iterator has more symbols.

  `Stream<String>`

  `names()`

  Iterate over the symbol names.

  `LookaheadIterator.Symbol`

  `next()`

  Advance the lookahead iterator to the next symbol.

  `boolean`

  `reset(short state)`

  Reset the lookahead iterator to the given state.

  `boolean`

  `reset(short state,
  Language language)`

  Reset the lookahead iterator to the given state and another language.

  `Stream<Short>`

  `symbols()`

  Iterate over the symbol IDs.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, toString, wait, wait, wait`

  ### Methods inherited from interface [Iterator](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Iterator.html#method-summary "class or interface in java.util")

  `forEachRemaining`

* ## Method Details

  + ### getLanguage

    public [Language](Language.html "class in io.github.treesitter.jtreesitter") getLanguage()

    Get the current language of the lookahead iterator.
  + ### getCurrentSymbol

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short getCurrentSymbol()

    Get the current symbol ID.

    API Note:
    :   The ID of the ERROR symbol is equal to `-1`.
  + ### getCurrentSymbolName

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getCurrentSymbolName()

    The current symbol name.

    API Note:
    :   Newly created lookahead iterators will contain the ERROR symbol.
  + ### reset

    public boolean reset([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short state)

    Reset the lookahead iterator to the given state.

    Returns:
    :   `true` if the iterator was reset
        successfully or `false` if it failed.
  + ### reset

    public boolean reset([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short state,
    [Language](Language.html "class in io.github.treesitter.jtreesitter") language)

    Reset the lookahead iterator to the given state and another language.

    Returns:
    :   `true` if the iterator was reset
        successfully or `false` if it failed.
  + ### hasNext

    public boolean hasNext()

    Check if the lookahead iterator has more symbols.

    Specified by:
    :   `hasNext` in interface `Iterator<LookaheadIterator.Symbol>`
  + ### next

    public [LookaheadIterator.Symbol](LookaheadIterator.Symbol.html "class in io.github.treesitter.jtreesitter") next()
    throws [NoSuchElementException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/NoSuchElementException.html "class or interface in java.util")

    Advance the lookahead iterator to the next symbol.

    Specified by:
    :   `next` in interface `Iterator<LookaheadIterator.Symbol>`

    Throws:
    :   `NoSuchElementException` - If there are no more symbols.
  + ### symbols

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public [Stream](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/stream/Stream.html "class or interface in java.util.stream")<[Short](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Short.html "class or interface in java.lang")> symbols()

    Iterate over the symbol IDs.

    Implementation Note:
    :   Calling this method will reset the iterator to its original state.
  + ### names

    public [Stream](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/stream/Stream.html "class or interface in java.util.stream")<[String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang")> names()

    Iterate over the symbol names.

    Implementation Note:
    :   Calling this method will reset the iterator to its original state.
  + ### close

    public void close()
    throws [RuntimeException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/RuntimeException.html "class or interface in java.lang")

    Specified by:
    :   `close` in interface `AutoCloseable`

    Throws:
    :   `RuntimeException`
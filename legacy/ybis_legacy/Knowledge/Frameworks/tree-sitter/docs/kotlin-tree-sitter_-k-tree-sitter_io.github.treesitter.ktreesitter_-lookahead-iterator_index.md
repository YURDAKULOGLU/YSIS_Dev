LookaheadIterator



[KTreeSitter](../../../index.html)/[io.github.treesitter.ktreesitter](../index.html)/LookaheadIterator

# LookaheadIterator

androidcommonjvmnative

actual class [LookaheadIterator](index.html) : [AbstractIterator](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-abstract-iterator/index.html)<[LookaheadIterator.Symbol](-symbol/index.html)> , [AutoCloseable](https://developer.android.com/reference/kotlin/java/lang/AutoCloseable.html)([source](https://github.com/tree-sitter/kotlin-tree-sitter/blob/a1a9e0e/ktreesitter/src/androidMain/kotlin/io/github/treesitter/ktreesitter/LookaheadIterator.kt#L17))

A class that is used to look up valid symbols in a specific parse state.

Lookahead iterators can be useful to generate suggestions and improve syntax error diagnostics. To get symbols valid in an `ERROR` node, use the lookahead iterator on its first leaf node state. For `MISSING` nodes, a lookahead iterator created on the previous non-extra leaf node may be appropriate.

**NOTE:** If you're targeting Android SDK level < 33, you must `use` or [close](close.html) the instance to free up resources.

expect class [LookaheadIterator](index.html) : [AbstractIterator](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-abstract-iterator/index.html)<[LookaheadIterator.Symbol](-symbol/index.html)> ([source](https://github.com/tree-sitter/kotlin-tree-sitter/blob/a1a9e0e/ktreesitter/src/commonMain/kotlin/io/github/treesitter/ktreesitter/LookaheadIterator.kt#L11))

A class that is used to look up valid symbols in a specific parse state.

Lookahead iterators can be useful to generate suggestions and improve syntax error diagnostics. To get symbols valid in an `ERROR` node, use the lookahead iterator on its first leaf node state. For `MISSING` nodes, a lookahead iterator created on the previous non-extra leaf node may be appropriate.

actual class [LookaheadIterator](index.html) : [AbstractIterator](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-abstract-iterator/index.html)<[LookaheadIterator.Symbol](-symbol/index.html)> ([source](https://github.com/tree-sitter/kotlin-tree-sitter/blob/a1a9e0e/ktreesitter/src/jvmMain/kotlin/io/github/treesitter/ktreesitter/LookaheadIterator.kt#L11))

A class that is used to look up valid symbols in a specific parse state.

Lookahead iterators can be useful to generate suggestions and improve syntax error diagnostics. To get symbols valid in an `ERROR` node, use the lookahead iterator on its first leaf node state. For `MISSING` nodes, a lookahead iterator created on the previous non-extra leaf node may be appropriate.

actual class [LookaheadIterator](index.html) : [AbstractIterator](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-abstract-iterator/index.html)<[LookaheadIterator.Symbol](-symbol/index.html)> ([source](https://github.com/tree-sitter/kotlin-tree-sitter/blob/a1a9e0e/ktreesitter/src/nativeMain/kotlin/io/github/treesitter/ktreesitter/LookaheadIterator.kt#L17))

A class that is used to look up valid symbols in a specific parse state.

Lookahead iterators can be useful to generate suggestions and improve syntax error diagnostics. To get symbols valid in an `ERROR` node, use the lookahead iterator on its first leaf node state. For `MISSING` nodes, a lookahead iterator created on the previous non-extra leaf node may be appropriate.

Members

## Types

[Symbol](-symbol/index.html)

Link copied to clipboard

androidcommonjvmnative

@[JvmRecord](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-record/index.html)

actual data class [Symbol](-symbol/index.html)(val id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html), val name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)) : [Record](https://developer.android.com/reference/kotlin/java/lang/Record.html)

A class that pairs a symbol ID with its name.

expect class [Symbol](-symbol/index.html)(id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html), name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html))

A class that pairs a symbol ID with its name.

@[JvmRecord](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-record/index.html)

actual data class [Symbol](-symbol/index.html)(val id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html), val name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)) : [Record](https://developer.android.com/reference/kotlin/java/lang/Record.html)

A class that pairs a symbol ID with its name.

actual data class [Symbol](-symbol/index.html)(val id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html), val name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html))

A class that pairs a symbol ID with its name.

## Properties

[currentSymbol](current-symbol.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getCurrentSymbol")

actual val [currentSymbol](current-symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The current symbol ID.

expect val [currentSymbol](current-symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The current symbol ID.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getCurrentSymbol")

actual val [currentSymbol](current-symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The current symbol ID.

actual val [currentSymbol](current-symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The current symbol ID.

[currentSymbolName](current-symbol-name.html)

Link copied to clipboard

androidcommonjvmnative

actual val [currentSymbolName](current-symbol-name.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The current symbol name.

expect val [currentSymbolName](current-symbol-name.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The current symbol name.

actual val [currentSymbolName](current-symbol-name.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The current symbol name.

actual val [currentSymbolName](current-symbol-name.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The current symbol name.

[language](language.html)

Link copied to clipboard

androidcommonjvmnative

actual val [language](language.html): [Language](../-language/index.html)

The current language of the lookahead iterator.

expect val [language](language.html): [Language](../-language/index.html)

The current language of the lookahead iterator.

actual val [language](language.html): [Language](../-language/index.html)

The current language of the lookahead iterator.

actual val [language](language.html): [Language](../-language/index.html)

The current language of the lookahead iterator.

## Functions

[close](close.html)

Link copied to clipboard

android

open override fun [close](close.html)()

forEachRemaining

Link copied to clipboard

androidjvm

open fun [forEachRemaining](index.html#-245129299%2FFunctions%2F-1811550354)(p0: [Consumer](https://developer.android.com/reference/kotlin/java/util/function/Consumer.html)<in [LookaheadIterator.Symbol](-symbol/index.html)>)

open fun [forEachRemaining](index.html#-245129299%2FFunctions%2F-922305398)(p0: [Consumer](https://developer.android.com/reference/kotlin/java/util/function/Consumer.html)<in [LookaheadIterator.Symbol](-symbol/index.html)>)

hasNext

Link copied to clipboard

androidcommonjvmnative

open operator override fun [hasNext](index.html#1451785448%2FFunctions%2F-1811550354)(): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

open operator override fun [hasNext](index.html#1451785448%2FFunctions%2F-665312020)(): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

open operator override fun [hasNext](index.html#1451785448%2FFunctions%2F-922305398)(): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

open operator override fun [hasNext](index.html#1451785448%2FFunctions%2F884350316)(): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

iterator

Link copied to clipboard

androidjvmnative

operator fun [iterator]([android]iterator.html)(): [LookaheadIterator](index.html)

operator fun [iterator]([jvm]iterator.html)(): [LookaheadIterator](index.html)

operator fun [iterator]([native]iterator.html)(): [LookaheadIterator](index.html)

[next](next.html)

Link copied to clipboard

androidcommonjvmnative

actual open operator override fun [next](next.html)(): [LookaheadIterator.Symbol](-symbol/index.html)

Advance the lookahead iterator to the next symbol.

expect open operator override fun [next](next.html)(): [LookaheadIterator.Symbol](-symbol/index.html)

Advance the lookahead iterator to the next symbol.

actual open operator override fun [next](next.html)(): [LookaheadIterator.Symbol](-symbol/index.html)

Advance the lookahead iterator to the next symbol.

actual open operator override fun [next](next.html)(): [LookaheadIterator.Symbol](-symbol/index.html)

Advance the lookahead iterator to the next symbol.

[reset](reset.html)

Link copied to clipboard

androidcommonjvmnative

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "reset")

actual external fun [reset](reset.html)(state: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html), language: [Language](../-language/index.html)?): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Reset the lookahead iterator the given [state](reset.html) and, optionally, another [language](reset.html).

expect fun [reset](reset.html)(state: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html), language: [Language](../-language/index.html)? = null): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Reset the lookahead iterator the given [state](reset.html) and, optionally, another [language](reset.html).

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "reset")

actual external fun [reset](reset.html)(state: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html), language: [Language](../-language/index.html)?): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Reset the lookahead iterator the given [state](reset.html) and, optionally, another [language](reset.html).

actual fun [reset](reset.html)(state: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html), language: [Language](../-language/index.html)?): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Reset the lookahead iterator the given [state](reset.html) and, optionally, another [language](reset.html).

[symbolNames](symbol-names.html)

Link copied to clipboard

androidcommonjvmnative

actual fun [symbolNames](symbol-names.html)(): [Sequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/index.html)<[String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)>

Iterate over the symbol names.

expect fun [symbolNames](symbol-names.html)(): [Sequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/index.html)<[String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)>

Iterate over the symbol names.

actual fun [symbolNames](symbol-names.html)(): [Sequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/index.html)<[String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)>

Iterate over the symbol names.

actual fun [symbolNames](symbol-names.html)(): [Sequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/index.html)<[String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)>

Iterate over the symbol names.

[symbols](symbols.html)

Link copied to clipboard

androidcommonjvmnative

actual fun [symbols](symbols.html)(): [Sequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/index.html)<[UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)>

Iterate over the symbol IDs.

expect fun [symbols](symbols.html)(): [Sequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/index.html)<[UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)>

Iterate over the symbol IDs.

actual fun [symbols](symbols.html)(): [Sequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/index.html)<[UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)>

Iterate over the symbol IDs.

actual fun [symbols](symbols.html)(): [Sequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/index.html)<[UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)>

Iterate over the symbol IDs.

© 2024 tree-sitterGenerated by [dokka](https://github.com/Kotlin/dokka)
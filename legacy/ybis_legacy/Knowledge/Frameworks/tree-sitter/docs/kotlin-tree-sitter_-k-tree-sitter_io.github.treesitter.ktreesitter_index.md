io.github.treesitter.ktreesitter



[KTreeSitter](../../index.html)/io.github.treesitter.ktreesitter

# Package-level declarations

TypesProperties

## Types

[InputEdit](-input-edit/index.html)

Link copied to clipboard

data class [InputEdit](-input-edit/index.html)(val startByte: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), val oldEndByte: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), val newEndByte: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), val startPoint: [Point](-point/index.html), val oldEndPoint: [Point](-point/index.html), val newEndPoint: [Point](-point/index.html))

An edit to a text document.

[Language](-language/index.html)

Link copied to clipboard

androidcommonjvmnative

actual class [Language](-language/index.html) constructor(language: [Any](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/index.html))

A class that defines how to parse a particular language.

expect class [Language](-language/index.html) constructor(language: [Any](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/index.html))

A class that defines how to parse a particular language.

actual class [Language](-language/index.html) constructor(language: [Any](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/index.html))

A class that defines how to parse a particular language.

actual class [Language](-language/index.html) constructor(language: [Any](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/index.html))

A class that defines how to parse a particular language.

[LogFunction](-log-function/index.html)

Link copied to clipboard

typealias [LogFunction](-log-function/index.html) = (type: [Parser.LogType](-parser/-log-type/index.html), message: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)) -> [Unit](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-unit/index.html)

A function that logs parsing results.

[LookaheadIterator](-lookahead-iterator/index.html)

Link copied to clipboard

androidcommonjvmnative

actual class [LookaheadIterator](-lookahead-iterator/index.html) : [AbstractIterator](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-abstract-iterator/index.html)<[LookaheadIterator.Symbol](-lookahead-iterator/-symbol/index.html)> , [AutoCloseable](https://developer.android.com/reference/kotlin/java/lang/AutoCloseable.html)

A class that is used to look up valid symbols in a specific parse state.

expect class [LookaheadIterator](-lookahead-iterator/index.html) : [AbstractIterator](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-abstract-iterator/index.html)<[LookaheadIterator.Symbol](-lookahead-iterator/-symbol/index.html)>

A class that is used to look up valid symbols in a specific parse state.

actual class [LookaheadIterator](-lookahead-iterator/index.html) : [AbstractIterator](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-abstract-iterator/index.html)<[LookaheadIterator.Symbol](-lookahead-iterator/-symbol/index.html)>

A class that is used to look up valid symbols in a specific parse state.

actual class [LookaheadIterator](-lookahead-iterator/index.html) : [AbstractIterator](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-abstract-iterator/index.html)<[LookaheadIterator.Symbol](-lookahead-iterator/-symbol/index.html)>

A class that is used to look up valid symbols in a specific parse state.

[Node](-node/index.html)

Link copied to clipboard

androidcommonjvmnative

actual class [Node](-node/index.html)

A single node within a [syntax tree](-tree/index.html).

expect class [Node](-node/index.html)

A single node within a [syntax tree](-tree/index.html).

actual class [Node](-node/index.html)

A single node within a [syntax tree](-tree/index.html).

actual class [Node](-node/index.html)

A single node within a [syntax tree](-tree/index.html).

[ParseCallback](-parse-callback/index.html)

Link copied to clipboard

typealias [ParseCallback](-parse-callback/index.html) = (byte: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), point: [Point](-point/index.html)) -> [CharSequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-char-sequence/index.html)?

A function to retrieve a chunk of text at a given byte offset and point.

[Parser](-parser/index.html)

Link copied to clipboard

androidcommonjvmnative

actual class [Parser](-parser/index.html) : [AutoCloseable](https://developer.android.com/reference/kotlin/java/lang/AutoCloseable.html)

A class that is used to produce a [syntax tree](-tree/index.html) from source code.

expect class [Parser](-parser/index.html)

A class that is used to produce a [syntax tree](-tree/index.html) from source code.

actual class [Parser](-parser/index.html)

A class that is used to produce a [syntax tree](-tree/index.html) from source code.

actual class [Parser](-parser/index.html)

A class that is used to produce a [syntax tree](-tree/index.html) from source code.

[Point](-point/index.html)

Link copied to clipboard

data class [Point](-point/index.html)(val row: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), val column: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)) : [Comparable](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-comparable/index.html)<[Point](-point/index.html)>

A position in a text document in terms of rows and columns.

[Query](-query/index.html)

Link copied to clipboard

androidcommonjvmnative

actual class [Query](-query/index.html) constructor(language: [Language](-language/index.html), source: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)) : [AutoCloseable](https://developer.android.com/reference/kotlin/java/lang/AutoCloseable.html)

A class that represents a set of patterns which match nodes in a syntax tree.

expect class [Query](-query/index.html) constructor(language: [Language](-language/index.html), source: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html))

A class that represents a set of patterns which match nodes in a syntax tree.

actual class [Query](-query/index.html) constructor(language: [Language](-language/index.html), source: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html))

A class that represents a set of patterns which match nodes in a syntax tree.

actual class [Query](-query/index.html) constructor(language: [Language](-language/index.html), source: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html))

A class that represents a set of patterns which match nodes in a syntax tree.

[QueryCapture](-query-capture/index.html)

Link copied to clipboard

data class [QueryCapture](-query-capture/index.html)

A [Node](-node/index.html) that was captured with a certain capture [name](-query-capture/name.html).

[QueryError](-query-error/index.html)

Link copied to clipboard

sealed class [QueryError](-query-error/index.html) : [IllegalArgumentException](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-illegal-argument-exception/index.html)

Any error that occurred while instantiating a [Query](-query/index.html).

[QueryMatch](-query-match/index.html)

Link copied to clipboard

class [QueryMatch](-query-match/index.html)

A match that corresponds to a certain pattern in the query.

[QueryPredicate](-query-predicate/index.html)

Link copied to clipboard

sealed class [QueryPredicate](-query-predicate/index.html)

A query [predicate](https://tree-sitter.github.io/tree-sitter/using-parsers#predicates) that associates conditions or arbitrary metadata with a pattern.

[QueryPredicateArg](-query-predicate-arg/index.html)

Link copied to clipboard

sealed interface [QueryPredicateArg](-query-predicate-arg/index.html)

An argument to a [QueryPredicate](-query-predicate/index.html).

[Range](-range/index.html)

Link copied to clipboard

data class [Range](-range/index.html) constructor(val startPoint: [Point](-point/index.html), val endPoint: [Point](-point/index.html), val startByte: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), val endByte: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html))

A range of positions in a text document, both in terms of bytes and of row-column points.

[Tree](-tree/index.html)

Link copied to clipboard

androidcommonjvmnative

actual class [Tree](-tree/index.html) : [AutoCloseable](https://developer.android.com/reference/kotlin/java/lang/AutoCloseable.html)

A class that represents a syntax tree.

expect class [Tree](-tree/index.html)

A class that represents a syntax tree.

actual class [Tree](-tree/index.html)

A class that represents a syntax tree.

actual class [Tree](-tree/index.html)

A class that represents a syntax tree.

[TreeCursor](-tree-cursor/index.html)

Link copied to clipboard

androidcommonjvmnative

actual class [TreeCursor](-tree-cursor/index.html) : [AutoCloseable](https://developer.android.com/reference/kotlin/java/lang/AutoCloseable.html)

A class that can be used to efficiently walk a [syntax tree](-tree/index.html).

expect class [TreeCursor](-tree-cursor/index.html)

A class that can be used to efficiently walk a [syntax tree](-tree/index.html).

actual class [TreeCursor](-tree-cursor/index.html)

A class that can be used to efficiently walk a [syntax tree](-tree/index.html).

actual class [TreeCursor](-tree-cursor/index.html)

A class that can be used to efficiently walk a [syntax tree](-tree/index.html).

## Properties

[LANGUAGE\_VERSION](-l-a-n-g-u-a-g-e_-v-e-r-s-i-o-n.html)

Link copied to clipboard

const val [LANGUAGE\_VERSION](-l-a-n-g-u-a-g-e_-v-e-r-s-i-o-n.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The latest ABI version that is supported by the current version of the library.

[MIN\_COMPATIBLE\_LANGUAGE\_VERSION](-m-i-n_-c-o-m-p-a-t-i-b-l-e_-l-a-n-g-u-a-g-e_-v-e-r-s-i-o-n.html)

Link copied to clipboard

const val [MIN\_COMPATIBLE\_LANGUAGE\_VERSION](-m-i-n_-c-o-m-p-a-t-i-b-l-e_-l-a-n-g-u-a-g-e_-v-e-r-s-i-o-n.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The earliest ABI version that is supported by the current version of the library.

© 2024 tree-sitterGenerated by [dokka](https://github.com/Kotlin/dokka)
Node



[KTreeSitter](../../../index.html)/[io.github.treesitter.ktreesitter](../index.html)/Node

# Node

androidcommonjvmnative

actual class [Node](index.html)([source](https://github.com/tree-sitter/kotlin-tree-sitter/blob/a1a9e0e/ktreesitter/src/androidMain/kotlin/io/github/treesitter/ktreesitter/Node.kt#L7))

A single node within a [syntax tree](../-tree/index.html).

expect class [Node](index.html)([source](https://github.com/tree-sitter/kotlin-tree-sitter/blob/a1a9e0e/ktreesitter/src/commonMain/kotlin/io/github/treesitter/ktreesitter/Node.kt#L4))

A single node within a [syntax tree](../-tree/index.html).

actual class [Node](index.html)([source](https://github.com/tree-sitter/kotlin-tree-sitter/blob/a1a9e0e/ktreesitter/src/jvmMain/kotlin/io/github/treesitter/ktreesitter/Node.kt#L5))

A single node within a [syntax tree](../-tree/index.html).

actual class [Node](index.html)([source](https://github.com/tree-sitter/kotlin-tree-sitter/blob/a1a9e0e/ktreesitter/src/nativeMain/kotlin/io/github/treesitter/ktreesitter/Node.kt#L8))

A single node within a [syntax tree](../-tree/index.html).

Members

## Properties

[byteRange](byte-range.html)

Link copied to clipboard

androidcommonjvmnative

actual val [byteRange](byte-range.html): [UIntRange](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.ranges/-u-int-range/index.html)

The range of the node in terms of bytes.

expect val [byteRange](byte-range.html): [UIntRange](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.ranges/-u-int-range/index.html)

The range of the node in terms of bytes.

actual val [byteRange](byte-range.html): [UIntRange](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.ranges/-u-int-range/index.html)

The range of the node in terms of bytes.

actual val [byteRange](byte-range.html): [UIntRange](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.ranges/-u-int-range/index.html)

The range of the node in terms of bytes.

[childCount](child-count.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getChildCount")

actual val [childCount](child-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's children.

expect val [childCount](child-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's children.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getChildCount")

actual val [childCount](child-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's children.

actual val [childCount](child-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's children.

[children](children.html)

Link copied to clipboard

androidcommonjvmnative

actual val [children](children.html): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

This node's children.

expect val [children](children.html): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

This node's children.

actual val [children](children.html): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

This node's children.

actual val [children](children.html): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

This node's children.

[descendantCount](descendant-count.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getDescendantCount")

actual val [descendantCount](descendant-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's descendants, including one for the node itself.

expect val [descendantCount](descendant-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's descendants, including one for the node itself.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getDescendantCount")

actual val [descendantCount](descendant-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's descendants, including one for the node itself.

actual val [descendantCount](descendant-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's descendants, including one for the node itself.

[endByte](end-byte.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getEndByte")

actual val [endByte](end-byte.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The end byte of the node.

expect val [endByte](end-byte.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The end byte of the node.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getEndByte")

actual val [endByte](end-byte.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The end byte of the node.

actual val [endByte](end-byte.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The end byte of the node.

[endPoint](end-point.html)

Link copied to clipboard

androidcommonjvmnative

actual val [endPoint](end-point.html): [Point](../-point/index.html)

The end point of the node.

expect val [endPoint](end-point.html): [Point](../-point/index.html)

The end point of the node.

actual val [endPoint](end-point.html): [Point](../-point/index.html)

The end point of the node.

actual val [endPoint](end-point.html): [Point](../-point/index.html)

The end point of the node.

[grammarSymbol](grammar-symbol.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getGrammarSymbol")

actual val [grammarSymbol](grammar-symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The numerical ID of the node's type, as it appears in the grammar ignoring aliases.

expect val [grammarSymbol](grammar-symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The numerical ID of the node's type, as it appears in the grammar ignoring aliases.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getGrammarSymbol")

actual val [grammarSymbol](grammar-symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The numerical ID of the node's type, as it appears in the grammar ignoring aliases.

actual val [grammarSymbol](grammar-symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The numerical ID of the node's type, as it appears in the grammar ignoring aliases.

[grammarType](grammar-type.html)

Link copied to clipboard

androidcommonjvmnative

actual val [grammarType](grammar-type.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The type of the node, as it appears in the grammar ignoring aliases.

expect val [grammarType](grammar-type.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The type of the node, as it appears in the grammar ignoring aliases.

actual val [grammarType](grammar-type.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The type of the node, as it appears in the grammar ignoring aliases.

actual val [grammarType](grammar-type.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The type of the node, as it appears in the grammar ignoring aliases.

[hasChanges](has-changes.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "hasChanges")

actual val [hasChanges](has-changes.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node has been edited.

expect val [hasChanges](has-changes.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node has been edited.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "hasChanges")

actual val [hasChanges](has-changes.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node has been edited.

actual val [hasChanges](has-changes.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node has been edited.

[hasError](has-error.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "hasError")

actual val [hasError](has-error.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is a syntax error, or contains any syntax errors.

expect val [hasError](has-error.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is a syntax error, or contains any syntax errors.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "hasError")

actual val [hasError](has-error.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is a syntax error, or contains any syntax errors.

actual val [hasError](has-error.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is a syntax error, or contains any syntax errors.

[id](id.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getId")

actual val [id](id.html): [ULong](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-long/index.html)

The numeric ID of the node.

expect val [id](id.html): [ULong](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-long/index.html)

The numeric ID of the node.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getId")

actual val [id](id.html): [ULong](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-long/index.html)

The numeric ID of the node.

actual val [id](id.html): [ULong](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-long/index.html)

The numeric ID of the node.

[isError](is-error.html)

Link copied to clipboard

androidcommonjvmnative

actual val [isError](is-error.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is a syntax error.

expect val [isError](is-error.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is a syntax error.

actual val [isError](is-error.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is a syntax error.

actual val [isError](is-error.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is a syntax error.

[isExtra](is-extra.html)

Link copied to clipboard

androidcommonjvmnative

actual val [isExtra](is-extra.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *extra*.

expect val [isExtra](is-extra.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *extra*.

actual val [isExtra](is-extra.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *extra*.

actual val [isExtra](is-extra.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *extra*.

[isMissing](is-missing.html)

Link copied to clipboard

androidcommonjvmnative

actual val [isMissing](is-missing.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *missing*.

expect val [isMissing](is-missing.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *missing*.

actual val [isMissing](is-missing.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *missing*.

actual val [isMissing](is-missing.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *missing*.

[isNamed](is-named.html)

Link copied to clipboard

androidcommonjvmnative

actual val [isNamed](is-named.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *named*.

expect val [isNamed](is-named.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *named*.

actual val [isNamed](is-named.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *named*.

actual val [isNamed](is-named.html): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

Check if the node is *named*.

[namedChildCount](named-child-count.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getNamedChildCount")

actual val [namedChildCount](named-child-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's *named* children.

expect val [namedChildCount](named-child-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's *named* children.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getNamedChildCount")

actual val [namedChildCount](named-child-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's *named* children.

actual val [namedChildCount](named-child-count.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The number of this node's *named* children.

[namedChildren](named-children.html)

Link copied to clipboard

androidcommonjvmnative

actual val [namedChildren](named-children.html): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

This node's *named* children.

expect val [namedChildren](named-children.html): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

This node's *named* children.

actual val [namedChildren](named-children.html): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

This node's *named* children.

actual val [namedChildren](named-children.html): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

This node's *named* children.

[nextNamedSibling](next-named-sibling.html)

Link copied to clipboard

androidcommonjvmnative

actual val [nextNamedSibling](next-named-sibling.html): [Node](index.html)?

The node's next *named* sibling, if any.

expect val [nextNamedSibling](next-named-sibling.html): [Node](index.html)?

The node's next *named* sibling, if any.

actual val [nextNamedSibling](next-named-sibling.html): [Node](index.html)?

The node's next *named* sibling, if any.

actual val [nextNamedSibling](next-named-sibling.html): [Node](index.html)?

The node's next *named* sibling, if any.

[nextParseState](next-parse-state.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getNextParseState")

actual val [nextParseState](next-parse-state.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The parse state after this node.

expect val [nextParseState](next-parse-state.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The parse state after this node.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getNextParseState")

actual val [nextParseState](next-parse-state.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The parse state after this node.

actual val [nextParseState](next-parse-state.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The parse state after this node.

[nextSibling](next-sibling.html)

Link copied to clipboard

androidcommonjvmnative

actual val [nextSibling](next-sibling.html): [Node](index.html)?

The node's next sibling, if any.

expect val [nextSibling](next-sibling.html): [Node](index.html)?

The node's next sibling, if any.

actual val [nextSibling](next-sibling.html): [Node](index.html)?

The node's next sibling, if any.

actual val [nextSibling](next-sibling.html): [Node](index.html)?

The node's next sibling, if any.

[parent](parent.html)

Link copied to clipboard

androidcommonjvmnative

actual val [parent](parent.html): [Node](index.html)?

The node's immediate parent, if any.

expect val [parent](parent.html): [Node](index.html)?

The node's immediate parent, if any.

actual val [parent](parent.html): [Node](index.html)?

The node's immediate parent, if any.

actual val [parent](parent.html): [Node](index.html)?

The node's immediate parent, if any.

[parseState](parse-state.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getParseState")

actual val [parseState](parse-state.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The parse state of this node.

expect val [parseState](parse-state.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The parse state of this node.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getParseState")

actual val [parseState](parse-state.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The parse state of this node.

actual val [parseState](parse-state.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The parse state of this node.

[prevNamedSibling](prev-named-sibling.html)

Link copied to clipboard

androidcommonjvmnative

actual val [prevNamedSibling](prev-named-sibling.html): [Node](index.html)?

The node's previous *named* sibling, if any.

expect val [prevNamedSibling](prev-named-sibling.html): [Node](index.html)?

The node's previous *named* sibling, if any.

actual val [prevNamedSibling](prev-named-sibling.html): [Node](index.html)?

The node's previous *named* sibling, if any.

actual val [prevNamedSibling](prev-named-sibling.html): [Node](index.html)?

The node's previous *named* sibling, if any.

[prevSibling](prev-sibling.html)

Link copied to clipboard

androidcommonjvmnative

actual val [prevSibling](prev-sibling.html): [Node](index.html)?

The node's previous sibling, if any.

expect val [prevSibling](prev-sibling.html): [Node](index.html)?

The node's previous sibling, if any.

actual val [prevSibling](prev-sibling.html): [Node](index.html)?

The node's previous sibling, if any.

actual val [prevSibling](prev-sibling.html): [Node](index.html)?

The node's previous sibling, if any.

[range](range.html)

Link copied to clipboard

androidcommonjvmnative

actual val [range](range.html): [Range](../-range/index.html)

The range of the node in terms of bytes and points.

expect val [range](range.html): [Range](../-range/index.html)

The range of the node in terms of bytes and points.

actual val [range](range.html): [Range](../-range/index.html)

The range of the node in terms of bytes and points.

actual val [range](range.html): [Range](../-range/index.html)

The range of the node in terms of bytes and points.

[startByte](start-byte.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getStartByte")

actual val [startByte](start-byte.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The start byte of the node.

expect val [startByte](start-byte.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The start byte of the node.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getStartByte")

actual val [startByte](start-byte.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The start byte of the node.

actual val [startByte](start-byte.html): [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)

The start byte of the node.

[startPoint](start-point.html)

Link copied to clipboard

androidcommonjvmnative

actual val [startPoint](start-point.html): [Point](../-point/index.html)

The start point of the node.

expect val [startPoint](start-point.html): [Point](../-point/index.html)

The start point of the node.

actual val [startPoint](start-point.html): [Point](../-point/index.html)

The start point of the node.

actual val [startPoint](start-point.html): [Point](../-point/index.html)

The start point of the node.

[symbol](symbol.html)

Link copied to clipboard

androidcommonjvmnative

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getSymbol")

actual val [symbol](symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The numerical ID of the node's type.

expect val [symbol](symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The numerical ID of the node's type.

@get:[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "getSymbol")

actual val [symbol](symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The numerical ID of the node's type.

actual val [symbol](symbol.html): [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)

The numerical ID of the node's type.

[type](type.html)

Link copied to clipboard

androidcommonjvmnative

actual val [type](type.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The type of the node.

expect val [type](type.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The type of the node.

actual val [type](type.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The type of the node.

actual val [type](type.html): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

The type of the node.

## Functions

[child](child.html)

Link copied to clipboard

androidcommonjvmnative

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "child")

actual external fun [child](child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

The node's child at the given index, if any.

expect fun [child](child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

The node's child at the given index, if any.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "child")

actual external fun [child](child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

The node's child at the given index, if any.

actual fun [child](child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

The node's child at the given index, if any.

[childByFieldId](child-by-field-id.html)

Link copied to clipboard

androidcommonjvmnative

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "childByFieldId")

actual external fun [childByFieldId](child-by-field-id.html)(id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)): [Node](index.html)?

Get the node's child with the given field ID, if any.

expect fun [childByFieldId](child-by-field-id.html)(id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)): [Node](index.html)?

Get the node's child with the given field ID, if any.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "childByFieldId")

actual external fun [childByFieldId](child-by-field-id.html)(id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)): [Node](index.html)?

Get the node's child with the given field ID, if any.

actual fun [childByFieldId](child-by-field-id.html)(id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)): [Node](index.html)?

Get the node's child with the given field ID, if any.

[childByFieldName](child-by-field-name.html)

Link copied to clipboard

androidcommonjvmnative

actual external fun [childByFieldName](child-by-field-name.html)(name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)): [Node](index.html)?

Get the node's child with the given field name, if any.

expect fun [childByFieldName](child-by-field-name.html)(name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)): [Node](index.html)?

Get the node's child with the given field name, if any.

actual external fun [childByFieldName](child-by-field-name.html)(name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)): [Node](index.html)?

Get the node's child with the given field name, if any.

actual fun [childByFieldName](child-by-field-name.html)(name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)): [Node](index.html)?

Get the node's child with the given field name, if any.

[childContainingDescendant](child-containing-descendant.html)

Link copied to clipboard

androidcommonjvmnative

actual external fun [childContainingDescendant](child-containing-descendant.html)(descendant: [Node](index.html)): [Node](index.html)?

Get the child of the node that contains the given descendant, if any.

expect fun [childContainingDescendant](child-containing-descendant.html)(descendant: [Node](index.html)): [Node](index.html)?

Get the child of the node that contains the given descendant, if any.

actual external fun [childContainingDescendant](child-containing-descendant.html)(descendant: [Node](index.html)): [Node](index.html)?

Get the child of the node that contains the given descendant, if any.

actual fun [childContainingDescendant](child-containing-descendant.html)(descendant: [Node](index.html)): [Node](index.html)?

Get the child of the node that contains the given descendant, if any.

[childrenByFieldId](children-by-field-id.html)

Link copied to clipboard

androidcommonjvmnative

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "childrenByFieldId")

actual external fun [childrenByFieldId](children-by-field-id.html)(id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

Get a list of children with the given field ID.

expect fun [childrenByFieldId](children-by-field-id.html)(id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

Get a list of children with the given field ID.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "childrenByFieldId")

actual external fun [childrenByFieldId](children-by-field-id.html)(id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

Get a list of children with the given field ID.

actual fun [childrenByFieldId](children-by-field-id.html)(id: [UShort](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-short/index.html)): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

Get a list of children with the given field ID.

[childrenByFieldName](children-by-field-name.html)

Link copied to clipboard

androidcommonjvmnative

actual fun [childrenByFieldName](children-by-field-name.html)(name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

Get a list of children with the given field name.

expect fun [childrenByFieldName](children-by-field-name.html)(name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

Get a list of children with the given field name.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "childrenByFieldName")

actual fun [childrenByFieldName](children-by-field-name.html)(name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

Get a list of children with the given field name.

actual fun [childrenByFieldName](children-by-field-name.html)(name: [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)): [List](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-list/index.html)<[Node](index.html)>

Get a list of children with the given field name.

[childWithDescendant](child-with-descendant.html)

Link copied to clipboard

androidcommonjvmnative

actual external fun [childWithDescendant](child-with-descendant.html)(descendant: [Node](index.html)): [Node](index.html)?

Get the node that contains the given descendant, if any.

expect fun [childWithDescendant](child-with-descendant.html)(descendant: [Node](index.html)): [Node](index.html)?

Get the node that contains the given descendant, if any.

actual external fun [childWithDescendant](child-with-descendant.html)(descendant: [Node](index.html)): [Node](index.html)?

Get the node that contains the given descendant, if any.

actual fun [childWithDescendant](child-with-descendant.html)(descendant: [Node](index.html)): [Node](index.html)?

Get the node that contains the given descendant, if any.

[descendant](descendant.html)

Link copied to clipboard

androidcommonjvmnative

actual external fun [descendant](descendant.html)(start: [Point](../-point/index.html), end: [Point](../-point/index.html)): [Node](index.html)?

Get the smallest node within this node that spans the given point range, if any.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "descendant")

actual external fun [descendant](descendant.html)(start: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), end: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the smallest node within this node that spans the given byte range, if any.

expect fun [descendant](descendant.html)(start: [Point](../-point/index.html), end: [Point](../-point/index.html)): [Node](index.html)?

Get the smallest node within this node that spans the given point range, if any.

expect fun [descendant](descendant.html)(start: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), end: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the smallest node within this node that spans the given byte range, if any.

actual external fun [descendant](descendant.html)(start: [Point](../-point/index.html), end: [Point](../-point/index.html)): [Node](index.html)?

Get the smallest node within this node that spans the given point range, if any.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "descendant")

actual external fun [descendant](descendant.html)(start: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), end: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the smallest node within this node that spans the given byte range, if any.

actual fun [descendant](descendant.html)(start: [Point](../-point/index.html), end: [Point](../-point/index.html)): [Node](index.html)?

Get the smallest node within this node that spans the given point range, if any.

actual fun [descendant](descendant.html)(start: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), end: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the smallest node within this node that spans the given byte range, if any.

[edit](edit.html)

Link copied to clipboard

androidcommonjvmnative

actual external fun [edit](edit.html)(edit: [InputEdit](../-input-edit/index.html))

Edit this node to keep it in-sync with source code that has been edited.

expect fun [edit](edit.html)(edit: [InputEdit](../-input-edit/index.html))

Edit this node to keep it in-sync with source code that has been edited.

actual external fun [edit](edit.html)(edit: [InputEdit](../-input-edit/index.html))

Edit this node to keep it in-sync with source code that has been edited.

@[ExperimentalMultiplatform](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-experimental-multiplatform/index.html)

actual fun [edit](edit.html)(edit: [InputEdit](../-input-edit/index.html))

Edit this node to keep it in-sync with source code that has been edited.

[equals](equals.html)

Link copied to clipboard

androidcommonjvmnative

actual open operator override fun [equals](equals.html)(other: [Any](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/index.html)?): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

expect open operator override fun [equals](equals.html)(other: [Any](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/index.html)?): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

actual open operator override fun [equals](equals.html)(other: [Any](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/index.html)?): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

actual open operator override fun [equals](equals.html)(other: [Any](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/index.html)?): [Boolean](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-boolean/index.html)

[fieldNameForChild](field-name-for-child.html)

Link copied to clipboard

androidcommonjvmnative

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "fieldNameForChild")

actual external fun [fieldNameForChild](field-name-for-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)?

Get the field name of this node’s child at the given index, if available.

expect fun [fieldNameForChild](field-name-for-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)?

Get the field name of this node’s child at the given index, if available.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "fieldNameForChild")

actual external fun [fieldNameForChild](field-name-for-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)?

Get the field name of this node’s child at the given index, if available.

actual fun [fieldNameForChild](field-name-for-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)?

Get the field name of this node’s child at the given index, if available.

[fieldNameForNamedChild](field-name-for-named-child.html)

Link copied to clipboard

androidcommonjvmnative

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "fieldNameForNamedChild")

actual external fun [fieldNameForNamedChild](field-name-for-named-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)?

Get the field name of this node’s *named* child at the given index, if available.

expect fun [fieldNameForNamedChild](field-name-for-named-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)?

Get the field name of this node’s *named* child at the given index, if available.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "fieldNameForNamedChild")

actual external fun [fieldNameForNamedChild](field-name-for-named-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)?

Get the field name of this node’s *named* child at the given index, if available.

actual fun [fieldNameForNamedChild](field-name-for-named-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)?

Get the field name of this node’s *named* child at the given index, if available.

[hashCode](hash-code.html)

Link copied to clipboard

androidcommonjvmnative

actual open external override fun [hashCode](hash-code.html)(): [Int](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-int/index.html)

expect open override fun [hashCode](hash-code.html)(): [Int](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-int/index.html)

actual open external override fun [hashCode](hash-code.html)(): [Int](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-int/index.html)

actual open override fun [hashCode](hash-code.html)(): [Int](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-int/index.html)

[namedChild](named-child.html)

Link copied to clipboard

androidcommonjvmnative

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "namedChild")

actual external fun [namedChild](named-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the node's *named* child at the given index, if any.

expect fun [namedChild](named-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the node's *named* child at the given index, if any.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "namedChild")

actual external fun [namedChild](named-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the node's *named* child at the given index, if any.

actual fun [namedChild](named-child.html)(index: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the node's *named* child at the given index, if any.

[namedDescendant](named-descendant.html)

Link copied to clipboard

androidcommonjvmnative

actual external fun [namedDescendant](named-descendant.html)(start: [Point](../-point/index.html), end: [Point](../-point/index.html)): [Node](index.html)?

Get the smallest *named* node within this node that spans the given point range, if any.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "namedDescendant")

actual external fun [namedDescendant](named-descendant.html)(start: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), end: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the smallest *named* node within this node that spans the given byte range, if any.

expect fun [namedDescendant](named-descendant.html)(start: [Point](../-point/index.html), end: [Point](../-point/index.html)): [Node](index.html)?

Get the smallest *named* node within this node that spans the given point range, if any.

expect fun [namedDescendant](named-descendant.html)(start: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), end: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the smallest *named* node within this node that spans the given byte range, if any.

actual external fun [namedDescendant](named-descendant.html)(start: [Point](../-point/index.html), end: [Point](../-point/index.html)): [Node](index.html)?

Get the smallest *named* node within this node that spans the given point range, if any.

@[JvmName](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-name/index.html)(name = "namedDescendant")

actual external fun [namedDescendant](named-descendant.html)(start: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), end: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the smallest *named* node within this node that spans the given byte range, if any.

actual fun [namedDescendant](named-descendant.html)(start: [Point](../-point/index.html), end: [Point](../-point/index.html)): [Node](index.html)?

Get the smallest *named* node within this node that spans the given point range, if any.

actual fun [namedDescendant](named-descendant.html)(start: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html), end: [UInt](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-u-int/index.html)): [Node](index.html)?

Get the smallest *named* node within this node that spans the given byte range, if any.

[sexp](sexp.html)

Link copied to clipboard

androidcommonjvmnative

actual external fun [sexp](sexp.html)(): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

Get the S-expression of the node.

expect fun [sexp](sexp.html)(): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

Get the S-expression of the node.

actual external fun [sexp](sexp.html)(): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

Get the S-expression of the node.

actual fun [sexp](sexp.html)(): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

Get the S-expression of the node.

[text](text.html)

Link copied to clipboard

androidcommonjvmnative

actual fun [text](text.html)(): [CharSequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-char-sequence/index.html)?

Get the source code of the node, if available.

expect fun [text](text.html)(): [CharSequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-char-sequence/index.html)?

Get the source code of the node, if available.

actual fun [text](text.html)(): [CharSequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-char-sequence/index.html)?

Get the source code of the node, if available.

actual fun [text](text.html)(): [CharSequence](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-char-sequence/index.html)?

Get the source code of the node, if available.

toString

Link copied to clipboard

androidjvmnative

open override fun [toString]([android]to-string.html)(): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

open override fun [toString]([jvm]to-string.html)(): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

open override fun [toString]([native]to-string.html)(): [String](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-string/index.html)

[walk](walk.html)

Link copied to clipboard

androidcommonjvmnative

actual fun [walk](walk.html)(): [TreeCursor](../-tree-cursor/index.html)

Create a new tree cursor starting from this node.

expect fun [walk](walk.html)(): [TreeCursor](../-tree-cursor/index.html)

Create a new tree cursor starting from this node.

actual fun [walk](walk.html)(): [TreeCursor](../-tree-cursor/index.html)

Create a new tree cursor starting from this node.

actual fun [walk](walk.html)(): [TreeCursor](../-tree-cursor/index.html)

Create a new tree cursor starting from this node.

© 2024 tree-sitterGenerated by [dokka](https://github.com/Kotlin/dokka)
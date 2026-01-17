Node (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class Node

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.Node

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public final class Node
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

A single node within a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter").

Implementation Note:
:   Node lifetimes are tied to the [`Tree`](Tree.html "class in io.github.treesitter.jtreesitter"),
    [`TreeCursor`](TreeCursor.html "class in io.github.treesitter.jtreesitter"), or [`Query`](Query.html "class in io.github.treesitter.jtreesitter") that they belong to.

* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `void`

  `edit(InputEdit edit)`

  Edit this node to keep it in-sync with source code that has been edited.

  `boolean`

  `equals(Object o)`

  Check if two nodes are identical.

  `Optional<Node>`

  `getChild(int index)`

  Get the node's child at the given index, if any.

  `Optional<Node>`

  `getChildByFieldId(short id)`

  Get the node's first child with the given field ID, if any.

  `Optional<Node>`

  `getChildByFieldName(String name)`

  Get the node's first child with the given field name, if any.

  `int`

  `getChildCount()`

  Get the number of this node's children.

  `List<Node>`

  `getChildren()`

  Get this node's children.

  `List<Node>`

  `getChildrenByFieldId(short id)`

  Get a list of the node's children with the given field ID.

  `List<Node>`

  `getChildrenByFieldName(String name)`

  Get a list of the node's child with the given field name.

  `Optional<Node>`

  `getChildWithDescendant(Node descendant)`

  Get the node that contains the given descendant, if any.

  `Optional<Node>`

  `getDescendant(int start,
  int end)`

  Get the smallest node within this node that spans the given byte range, if any.

  `Optional<Node>`

  `getDescendant(Point start,
  Point end)`

  Get the smallest node within this node that spans the given point range, if any.

  `int`

  `getDescendantCount()`

  Get the number of this node's descendants, including the node itself.

  `int`

  `getEndByte()`

  Get the end byte of the node.

  `Point`

  `getEndPoint()`

  Get the end point of the node.

  `@Nullable String`

  `getFieldNameForChild(int index)`

  Get the field name of this node’s child at the given index, if available.

  `@Nullable String`

  `getFieldNameForNamedChild(int index)`

  Get the field name of this node's *named* child at the given index, if available.

  `Optional<Node>`

  `getFirstChildForByte(int byte_offset)`

  Get the node's first child that contains or starts after the given byte offset.

  `Optional<Node>`

  `getFirstNamedChildForByte(int byte_offset)`

  Get the node's first *named* child that contains or starts after the given byte offset.

  `short`

  `getGrammarSymbol()`

  Get the numerical ID of the node's type, as it appears in the grammar ignoring aliases.

  `String`

  `getGrammarType()`

  Get the type of the node, as it appears in the grammar ignoring aliases.

  `long`

  `getId()`

  Get the numerical ID of the node.

  `Optional<Node>`

  `getNamedChild(int index)`

  Get the node's *named* child at the given index, if any.

  `int`

  `getNamedChildCount()`

  Get the number of this node's *named* children.

  `List<Node>`

  `getNamedChildren()`

  Get this node's *named* children.

  `Optional<Node>`

  `getNamedDescendant(int start,
  int end)`

  Get the smallest *named* node within this node that spans the given byte range, if any.

  `Optional<Node>`

  `getNamedDescendant(Point start,
  Point end)`

  Get the smallest *named* node within this node that spans the given point range, if any.

  `Optional<Node>`

  `getNextNamedSibling()`

  The node's next *named* sibling, if any.

  `short`

  `getNextParseState()`

  Get the parse state after this node.

  `Optional<Node>`

  `getNextSibling()`

  The node's next sibling, if any.

  `Optional<Node>`

  `getParent()`

  The node's immediate parent, if any.

  `short`

  `getParseState()`

  Get the parse state of this node.

  `Optional<Node>`

  `getPrevNamedSibling()`

  The node's previous *named* sibling, if any.

  `Optional<Node>`

  `getPrevSibling()`

  The node's previous sibling, if any.

  `Range`

  `getRange()`

  Get the range of the node.

  `int`

  `getStartByte()`

  Get the start byte of the node.

  `Point`

  `getStartPoint()`

  Get the start point of the node.

  `short`

  `getSymbol()`

  Get the numerical ID of the node's type.

  `@Nullable String`

  `getText()`

  Get the source code of the node, if available.

  `Tree`

  `getTree()`

  Get the tree that contains this node.

  `String`

  `getType()`

  Get the type of the node.

  `boolean`

  `hasChanges()`

  Check if the node has been edited.

  `boolean`

  `hasError()`

  Check if the node is an ERROR,
  or contains any ERROR nodes.

  `int`

  `hashCode()`

  `boolean`

  `isError()`

  Check if the node is an ERROR node.

  `boolean`

  `isExtra()`

  Check if the node is *extra*.

  `boolean`

  `isMissing()`

  Check if the node is MISSING.

  `boolean`

  `isNamed()`

  Check if the node is *named*.

  `String`

  `toSexp()`

  Get the S-expression representing the node.

  `String`

  `toString()`

  `TreeCursor`

  `walk()`

  Create a new [tree cursor](TreeCursor.html "class in io.github.treesitter.jtreesitter") starting from this node.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Method Details

  + ### getTree

    public [Tree](Tree.html "class in io.github.treesitter.jtreesitter") getTree()

    Get the tree that contains this node.
  + ### getId

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public long getId()

    Get the numerical ID of the node.

    API Note:
    :   Within any given syntax tree, no two nodes have the same ID. However,
        if a new tree is created based on an older tree, and a node from the old tree
        is reused in the process, then that node will have the same ID in both trees.
  + ### getSymbol

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short getSymbol()

    Get the numerical ID of the node's type.
  + ### getGrammarSymbol

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short getGrammarSymbol()

    Get the numerical ID of the node's type, as it appears in the grammar ignoring aliases.
  + ### getType

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getType()

    Get the type of the node.
  + ### getGrammarType

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getGrammarType()

    Get the type of the node, as it appears in the grammar ignoring aliases.
  + ### isNamed

    public boolean isNamed()

    Check if the node is *named*.

    Named nodes correspond to named rules in the grammar,
    whereas *anonymous* nodes correspond to string literals.
  + ### isExtra

    public boolean isExtra()

    Check if the node is *extra*.

    Extra nodes represent things which are not required
    by the grammar but can appear anywhere (e.g. whitespace).
  + ### isError

    public boolean isError()

    Check if the node is an ERROR node.
  + ### isMissing

    public boolean isMissing()

    Check if the node is MISSING.

    MISSING nodes are inserted by the parser in order
    to recover from certain kinds of syntax errors.
  + ### hasChanges

    public boolean hasChanges()

    Check if the node has been edited.
  + ### hasError

    public boolean hasError()

    Check if the node is an ERROR,
    or contains any ERROR nodes.
  + ### getParseState

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short getParseState()

    Get the parse state of this node.
  + ### getNextParseState

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short getNextParseState()

    Get the parse state after this node.
  + ### getStartByte

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getStartByte()

    Get the start byte of the node.
  + ### getEndByte

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getEndByte()

    Get the end byte of the node.
  + ### getRange

    public [Range](Range.html "class in io.github.treesitter.jtreesitter") getRange()

    Get the range of the node.
  + ### getStartPoint

    public [Point](Point.html "class in io.github.treesitter.jtreesitter") getStartPoint()

    Get the start point of the node.
  + ### getEndPoint

    public [Point](Point.html "class in io.github.treesitter.jtreesitter") getEndPoint()

    Get the end point of the node.
  + ### getChildCount

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getChildCount()

    Get the number of this node's children.
  + ### getNamedChildCount

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getNamedChildCount()

    Get the number of this node's *named* children.
  + ### getDescendantCount

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getDescendantCount()

    Get the number of this node's descendants, including the node itself.
  + ### getParent

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getParent()

    The node's immediate parent, if any.
  + ### getNextSibling

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getNextSibling()

    The node's next sibling, if any.
  + ### getPrevSibling

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getPrevSibling()

    The node's previous sibling, if any.
  + ### getNextNamedSibling

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getNextNamedSibling()

    The node's next *named* sibling, if any.
  + ### getPrevNamedSibling

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getPrevNamedSibling()

    The node's previous *named* sibling, if any.
  + ### getChild

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getChild([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Get the node's child at the given index, if any.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [child count](#getChildCount()).

    API Note:
    :   This method is fairly fast, but its cost is technically
        `log(i)`, so if you might be iterating over a long list of children,
        you should use [`getChildren()`](#getChildren()) or [`walk()`](#walk()) instead.
  + ### getNamedChild

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getNamedChild([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Get the node's *named* child at the given index, if any.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [child count](#getNamedChildCount()).

    API Note:
    :   This method is fairly fast, but its cost is technically
        `log(i)`, so if you might be iterating over a long list of children,
        you should use [`getNamedChildren()`](#getNamedChildren()) or [`walk()`](#walk()) instead.
  + ### getFirstChildForByte

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getFirstChildForByte([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int byte\_offset)

    Get the node's first child that contains or starts after the given byte offset.

    Since:
    :   0.25.0
  + ### getFirstNamedChildForByte

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getFirstNamedChildForByte([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int byte\_offset)

    Get the node's first *named* child that contains or starts after the given byte offset.

    Since:
    :   0.25.0
  + ### getChildByFieldId

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getChildByFieldId([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short id)

    Get the node's first child with the given field ID, if any.

    See Also:
    :   - [`Language.getFieldIdForName(String)`](Language.html#getFieldIdForName(java.lang.String))
  + ### getChildByFieldName

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getChildByFieldName([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name)

    Get the node's first child with the given field name, if any.
  + ### getChildren

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getChildren()

    Get this node's children.

    API Note:
    :   If you're walking the tree recursively, you may want to use [`walk()`](#walk()) instead.
  + ### getNamedChildren

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getNamedChildren()

    Get this node's *named* children.
  + ### getChildrenByFieldId

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getChildrenByFieldId([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short id)

    Get a list of the node's children with the given field ID.

    See Also:
    :   - [`Language.getFieldIdForName(String)`](Language.html#getFieldIdForName(java.lang.String))
  + ### getChildrenByFieldName

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getChildrenByFieldName([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name)

    Get a list of the node's child with the given field name.
  + ### getFieldNameForChild

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getFieldNameForChild([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Get the field name of this node’s child at the given index, if available.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [child count](#getNamedChildCount()).
  + ### getFieldNameForNamedChild

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getFieldNameForNamedChild([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)
    throws [IndexOutOfBoundsException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IndexOutOfBoundsException.html "class or interface in java.lang")

    Get the field name of this node's *named* child at the given index, if available.

    Throws:
    :   `IndexOutOfBoundsException` - If the index exceeds the
        [child count](#getNamedChildCount()).

    Since:
    :   0.24.0
  + ### getDescendant

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getDescendant([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int start,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int end)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Get the smallest node within this node that spans the given byte range, if any.

    Throws:
    :   `IllegalArgumentException` - If `start > end`.
  + ### getDescendant

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getDescendant([Point](Point.html "class in io.github.treesitter.jtreesitter") start,
    [Point](Point.html "class in io.github.treesitter.jtreesitter") end)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Get the smallest node within this node that spans the given point range, if any.

    Throws:
    :   `IllegalArgumentException` - If `start > end`.
  + ### getNamedDescendant

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getNamedDescendant([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int start,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int end)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Get the smallest *named* node within this node that spans the given byte range, if any.

    Throws:
    :   `IllegalArgumentException` - If `start > end`.
  + ### getNamedDescendant

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getNamedDescendant([Point](Point.html "class in io.github.treesitter.jtreesitter") start,
    [Point](Point.html "class in io.github.treesitter.jtreesitter") end)

    Get the smallest *named* node within this node that spans the given point range, if any.

    Throws:
    :   `IllegalArgumentException` - If `start > end`.
  + ### getChildWithDescendant

    public [Optional](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Optional.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> getChildWithDescendant([Node](Node.html "class in io.github.treesitter.jtreesitter") descendant)

    Get the node that contains the given descendant, if any.

    Since:
    :   0.24.0
  + ### getText

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getText()

    Get the source code of the node, if available.
  + ### edit

    public void edit([InputEdit](InputEdit.html "class in io.github.treesitter.jtreesitter") edit)

    Edit this node to keep it in-sync with source code that has been edited.

    API Note:
    :   This method is only rarely needed. When you edit a syntax
        tree via [`Tree.edit(InputEdit)`](Tree.html#edit(io.github.treesitter.jtreesitter.InputEdit)), all of the nodes that you retrieve from
        the tree afterward will already reflect the edit. You only need
        to use this when you have a specific [Node](Node.html "class in io.github.treesitter.jtreesitter") instance
        that you want to keep and continue to use after an edit.
  + ### walk

    public [TreeCursor](TreeCursor.html "class in io.github.treesitter.jtreesitter") walk()

    Create a new [tree cursor](TreeCursor.html "class in io.github.treesitter.jtreesitter") starting from this node.
  + ### toSexp

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") toSexp()

    Get the S-expression representing the node.
  + ### equals

    public boolean equals([Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang") o)

    Check if two nodes are identical.

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
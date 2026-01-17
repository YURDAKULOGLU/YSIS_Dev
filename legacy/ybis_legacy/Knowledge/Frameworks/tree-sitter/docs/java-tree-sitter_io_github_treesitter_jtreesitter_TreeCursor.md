TreeCursor (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class TreeCursor

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.TreeCursor

All Implemented Interfaces:
:   `AutoCloseable, Cloneable`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public final class TreeCursor
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")
implements [AutoCloseable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/AutoCloseable.html "class or interface in java.lang"), [Cloneable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Cloneable.html "class or interface in java.lang")

A class that can be used to efficiently walk a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter").

See Also:
:   * [`Tree.walk()`](Tree.html#walk())
    * [`Node.walk()`](Node.html#walk())

API Note:
:   The node the cursor was constructed with is considered the
    root of the cursor, and the cursor cannot walk outside this node.

* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `TreeCursor`

  `clone()`

  Create a shallow copy of the tree cursor.

  `void`

  `close()`

  `int`

  `getCurrentDepth()`

  Get the depth of the cursor's current node relative to
  the original node that the cursor was constructed with.

  `int`

  `getCurrentDescendantIndex()`

  Get the index of the cursor's current node out of the descendants
  of the original node that the cursor was constructed with.

  `short`

  `getCurrentFieldId()`

  Get the field ID of the tree cursor's current node, or `0`.

  `@Nullable String`

  `getCurrentFieldName()`

  Get the field name of the tree cursor's current node, or `null`.

  `Node`

  `getCurrentNode()`

  Get the current node of the cursor.

  `Node`

  `getCurrentNode(SegmentAllocator allocator)`

  Get the current node of the cursor using the given allocator.

  `void`

  `gotoDescendant(int index)`

  Move the cursor to the node that is the nth descendant of
  the original node that the cursor was constructed with.

  `boolean`

  `gotoFirstChild()`

  Move the cursor to the first child of its current node.

  `OptionalInt`

  `gotoFirstChildForByte(int offset)`

  Move the cursor to the first child of its current node
  that contains or starts after the given byte offset.

  `OptionalInt`

  `gotoFirstChildForPoint(Point point)`

  Move the cursor to the first child of its current node
  that contains or starts after the given point.

  `boolean`

  `gotoLastChild()`

  Move the cursor to the last child of its current node.

  `boolean`

  `gotoNextSibling()`

  Move the cursor to the next sibling of its current node.

  `boolean`

  `gotoParent()`

  Move the cursor to the parent of its current node.

  `boolean`

  `gotoPreviousSibling()`

  Move the cursor to the previous sibling of its current node.

  `void`

  `reset(Node node)`

  Reset the cursor to start at a different node.

  `void`

  `reset(TreeCursor cursor)`

  Reset the cursor to start at the same position as another cursor.

  `String`

  `toString()`

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, wait, wait, wait`

* ## Method Details

  + ### getCurrentNode

    public [Node](Node.html "class in io.github.treesitter.jtreesitter") getCurrentNode()

    Get the current node of the cursor.

    Implementation Note:
    :   The node will become invalid once the cursor is closed.
  + ### getCurrentNode

    public [Node](Node.html "class in io.github.treesitter.jtreesitter") getCurrentNode([SegmentAllocator](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SegmentAllocator.html "class or interface in java.lang.foreign") allocator)

    Get the current node of the cursor using the given allocator.

    Since:
    :   0.25.0
  + ### getCurrentDepth

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getCurrentDepth()

    Get the depth of the cursor's current node relative to
    the original node that the cursor was constructed with.
  + ### getCurrentFieldId

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short getCurrentFieldId()

    Get the field ID of the tree cursor's current node, or `0`.

    See Also:
    :   - [`Node.getChildByFieldId(short)`](Node.html#getChildByFieldId(short))
        - [`Language.getFieldIdForName(String)`](Language.html#getFieldIdForName(java.lang.String))
  + ### getCurrentFieldName

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getCurrentFieldName()

    Get the field name of the tree cursor's current node, or `null`.

    See Also:
    :   - [`Node.getChildByFieldName(String)`](Node.html#getChildByFieldName(java.lang.String))
  + ### getCurrentDescendantIndex

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getCurrentDescendantIndex()

    Get the index of the cursor's current node out of the descendants
    of the original node that the cursor was constructed with.
  + ### gotoFirstChild

    public boolean gotoFirstChild()

    Move the cursor to the first child of its current node.

    Returns:
    :   `true` if the cursor successfully moved, or
        `false` if there were no children.
  + ### gotoLastChild

    public boolean gotoLastChild()

    Move the cursor to the last child of its current node.

    Returns:
    :   `true` if the cursor successfully moved, or
        `false` if there were no children.
  + ### gotoParent

    public boolean gotoParent()

    Move the cursor to the parent of its current node.

    Returns:
    :   `true` if the cursor successfully moved, or
        `false` if there was no parent node.
  + ### gotoNextSibling

    public boolean gotoNextSibling()

    Move the cursor to the next sibling of its current node.

    Returns:
    :   `true` if the cursor successfully moved, or
        `false` if there was no next sibling node.
  + ### gotoPreviousSibling

    public boolean gotoPreviousSibling()

    Move the cursor to the previous sibling of its current node.

    Returns:
    :   `true` if the cursor successfully moved, or
        `false` if there was no previous sibling node.
  + ### gotoDescendant

    public void gotoDescendant([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int index)

    Move the cursor to the node that is the nth descendant of
    the original node that the cursor was constructed with.

    API Note:
    :   The index `0` represents the original node itself.
  + ### gotoFirstChildForByte

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public [OptionalInt](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/OptionalInt.html "class or interface in java.util") gotoFirstChildForByte([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int offset)

    Move the cursor to the first child of its current node
    that contains or starts after the given byte offset.

    Returns:
    :   The index of the child node, if found.
  + ### gotoFirstChildForPoint

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public [OptionalInt](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/OptionalInt.html "class or interface in java.util") gotoFirstChildForPoint([Point](Point.html "class in io.github.treesitter.jtreesitter") point)

    Move the cursor to the first child of its current node
    that contains or starts after the given point.

    Returns:
    :   The index of the child node, if found.
  + ### reset

    public void reset([Node](Node.html "class in io.github.treesitter.jtreesitter") node)

    Reset the cursor to start at a different node.
  + ### reset

    public void reset([TreeCursor](TreeCursor.html "class in io.github.treesitter.jtreesitter") cursor)

    Reset the cursor to start at the same position as another cursor.
  + ### clone

    public [TreeCursor](TreeCursor.html "class in io.github.treesitter.jtreesitter") clone()

    Create a shallow copy of the tree cursor.
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
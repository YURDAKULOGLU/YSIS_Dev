Tree (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class Tree

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.Tree

All Implemented Interfaces:
:   `AutoCloseable, Cloneable`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public final class Tree
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")
implements [AutoCloseable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/AutoCloseable.html "class or interface in java.lang"), [Cloneable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Cloneable.html "class or interface in java.lang")

A class that represents a syntax tree.

* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `Tree`

  `clone()`

  Create a shallow copy of the syntax tree.

  `void`

  `close()`

  `void`

  `edit(InputEdit edit)`

  Edit the syntax tree to keep it in sync
  with source code that has been modified.

  `List<Range>`

  `getChangedRanges(Tree newTree)`

  Compare an old edited syntax tree to a new
  syntax tree representing the same document.

  `List<Range>`

  `getIncludedRanges()`

  Get the included ranges of the syntax tree.

  `Language`

  `getLanguage()`

  Get the language that was used to parse the syntax tree.

  `Node`

  `getRootNode()`

  Get the root node of the syntax tree.

  `@Nullable Node`

  `getRootNodeWithOffset(int bytes,
  Point extent)`

  Get the root node of the syntax tree, but with
  its position shifted forward by the given offset.

  `@Nullable String`

  `getText()`

  Get the source code of the syntax tree, if available.

  `String`

  `toString()`

  `TreeCursor`

  `walk()`

  Create a new tree cursor starting from the root node of the tree.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, wait, wait, wait`

* ## Method Details

  + ### getLanguage

    public [Language](Language.html "class in io.github.treesitter.jtreesitter") getLanguage()

    Get the language that was used to parse the syntax tree.
  + ### getText

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") getText()

    Get the source code of the syntax tree, if available.
  + ### getRootNode

    public [Node](Node.html "class in io.github.treesitter.jtreesitter") getRootNode()

    Get the root node of the syntax tree.
  + ### getRootNodeWithOffset

    public [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [Node](Node.html "class in io.github.treesitter.jtreesitter") getRootNodeWithOffset([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int bytes,
    [Point](Point.html "class in io.github.treesitter.jtreesitter") extent)

    Get the root node of the syntax tree, but with
    its position shifted forward by the given offset.
  + ### getIncludedRanges

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[Range](Range.html "class in io.github.treesitter.jtreesitter")> getIncludedRanges()

    Get the included ranges of the syntax tree.
  + ### getChangedRanges

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[Range](Range.html "class in io.github.treesitter.jtreesitter")> getChangedRanges([Tree](Tree.html "class in io.github.treesitter.jtreesitter") newTree)

    Compare an old edited syntax tree to a new
    syntax tree representing the same document.

    For this to work correctly, this tree must have been
    edited such that its ranges match up to the new tree.

    Returns:
    :   A list of ranges whose syntactic structure has changed.
  + ### edit

    public void edit([InputEdit](InputEdit.html "class in io.github.treesitter.jtreesitter") edit)

    Edit the syntax tree to keep it in sync
    with source code that has been modified.
  + ### walk

    public [TreeCursor](TreeCursor.html "class in io.github.treesitter.jtreesitter") walk()

    Create a new tree cursor starting from the root node of the tree.
  + ### clone

    public [Tree](Tree.html "class in io.github.treesitter.jtreesitter") clone()

    Create a shallow copy of the syntax tree.

    Implementation Note:
    :   You need to clone a tree in order to use it on more than
        one thread at a time, as [Tree](Tree.html "class in io.github.treesitter.jtreesitter") objects are not thread safe.
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
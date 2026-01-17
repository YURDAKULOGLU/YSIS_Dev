QueryMatch (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Record Class QueryMatch

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.QueryMatch

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public record QueryMatch(int patternIndex, [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[QueryCapture](QueryCapture.html "class in io.github.treesitter.jtreesitter")> captures)
extends [Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

A match that corresponds to a certain pattern in a [`Query`](Query.html "class in io.github.treesitter.jtreesitter").

* ## Constructor Summary

  Constructors

  Constructor

  Description

  `QueryMatch(int patternIndex,
  List<QueryCapture> captures)`

  Creates an instance of a QueryMatch record class.
* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `List<QueryCapture>`

  `captures()`

  Returns the value of the `captures` record component.

  `final boolean`

  `equals(Object o)`

  Indicates whether some other object is "equal to" this one.

  `List<Node>`

  `findNodes(String capture)`

  Find the nodes that are captured by the given capture name.

  `final int`

  `hashCode()`

  Returns a hash code value for this object.

  `int`

  `patternIndex()`

  Returns the value of the `patternIndex` record component.

  `String`

  `toString()`

  Returns a string representation of this record class.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Constructor Details

  + ### QueryMatch

    public QueryMatch([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int patternIndex,
    [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[QueryCapture](QueryCapture.html "class in io.github.treesitter.jtreesitter")> captures)

    Creates an instance of a QueryMatch record class.
* ## Method Details

  + ### findNodes

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[Node](Node.html "class in io.github.treesitter.jtreesitter")> findNodes([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") capture)

    Find the nodes that are captured by the given capture name.
  + ### toString

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") toString()

    Returns a string representation of this record class. The representation contains the name of the class, followed by the name and value of each of the record components.

    Specified by:
    :   `toString` in class `Record`

    Returns:
    :   a string representation of this object
  + ### hashCode

    public final int hashCode()

    Returns a hash code value for this object. The value is derived from the hash code of each of the record components.

    Specified by:
    :   `hashCode` in class `Record`

    Returns:
    :   a hash code value for this object
  + ### equals

    public final boolean equals([Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang") o)

    Indicates whether some other object is "equal to" this one. The objects are equal if the other object is of the same class and if all the record components are equal. Reference components are compared with [`Objects::equals(Object,Object)`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Objects.html#equals(java.lang.Object,java.lang.Object) "class or interface in java.util"); primitive components are compared with the `compare` method from their corresponding wrapper classes.

    Specified by:
    :   `equals` in class `Record`

    Parameters:
    :   `o` - the object with which to compare

    Returns:
    :   `true` if this object is the same as the `o` argument; `false` otherwise.
  + ### patternIndex

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int patternIndex()

    Returns the value of the `patternIndex` record component.

    Returns:
    :   the value of the `patternIndex` record component
  + ### captures

    public [List](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/List.html "class or interface in java.util")<[QueryCapture](QueryCapture.html "class in io.github.treesitter.jtreesitter")> captures()

    Returns the value of the `captures` record component.

    Returns:
    :   the value of the `captures` record component
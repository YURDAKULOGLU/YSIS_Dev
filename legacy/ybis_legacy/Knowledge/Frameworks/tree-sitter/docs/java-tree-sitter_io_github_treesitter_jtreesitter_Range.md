Range (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Record Class Range

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.Range

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public record Range([Point](Point.html "class in io.github.treesitter.jtreesitter") startPoint, [Point](Point.html "class in io.github.treesitter.jtreesitter") endPoint, int startByte, int endByte)
extends [Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

A range of positions in a text document,
both in terms of bytes and of row-column points.

* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Range(Point startPoint,
  Point endPoint,
  int startByte,
  int endByte)`

  Creates an instance of a Range record class.
* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `void`

  `edit(InputEdit edit)`

  Edit the range to keep it in-sync with source code that has been edited.

  `int`

  `endByte()`

  Returns the value of the `endByte` record component.

  `Point`

  `endPoint()`

  Returns the value of the `endPoint` record component.

  `final boolean`

  `equals(Object o)`

  Indicates whether some other object is "equal to" this one.

  `final int`

  `hashCode()`

  Returns a hash code value for this object.

  `int`

  `startByte()`

  Returns the value of the `startByte` record component.

  `Point`

  `startPoint()`

  Returns the value of the `startPoint` record component.

  `String`

  `toString()`

  Returns a string representation of this record class.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Constructor Details

  + ### Range

    public Range([Point](Point.html "class in io.github.treesitter.jtreesitter") startPoint,
    [Point](Point.html "class in io.github.treesitter.jtreesitter") endPoint,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int startByte,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int endByte)

    Creates an instance of a Range record class.

    Throws:
    :   `IllegalArgumentException` - If `startPoint > endPoint` or `startByte > endByte`.
* ## Method Details

  + ### edit

    public void edit([InputEdit](InputEdit.html "class in io.github.treesitter.jtreesitter") edit)

    Edit the range to keep it in-sync with source code that has been edited.

    This function updates the range's byte offset and row/column position based on an edit
    operation. This is useful for editing ranges without requiring a tree or node instance.

    Since:
    :   0.26.0
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
  + ### startPoint

    public [Point](Point.html "class in io.github.treesitter.jtreesitter") startPoint()

    Returns the value of the `startPoint` record component.

    Returns:
    :   the value of the `startPoint` record component
  + ### endPoint

    public [Point](Point.html "class in io.github.treesitter.jtreesitter") endPoint()

    Returns the value of the `endPoint` record component.

    Returns:
    :   the value of the `endPoint` record component
  + ### startByte

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int startByte()

    Returns the value of the `startByte` record component.

    Returns:
    :   the value of the `startByte` record component
  + ### endByte

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int endByte()

    Returns the value of the `endByte` record component.

    Returns:
    :   the value of the `endByte` record component
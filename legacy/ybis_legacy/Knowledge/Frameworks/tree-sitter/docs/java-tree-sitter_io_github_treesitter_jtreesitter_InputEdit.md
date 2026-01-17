InputEdit (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Record Class InputEdit

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.InputEdit

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public record InputEdit(int startByte, int oldEndByte, int newEndByte, [Point](Point.html "class in io.github.treesitter.jtreesitter") startPoint, [Point](Point.html "class in io.github.treesitter.jtreesitter") oldEndPoint, [Point](Point.html "class in io.github.treesitter.jtreesitter") newEndPoint)
extends [Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

An edit to a text document.

* ## Constructor Summary

  Constructors

  Constructor

  Description

  `InputEdit(int startByte,
  int oldEndByte,
  int newEndByte,
  Point startPoint,
  Point oldEndPoint,
  Point newEndPoint)`

  Creates an instance of a `InputEdit` record class.
* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `final boolean`

  `equals(Object o)`

  Indicates whether some other object is "equal to" this one.

  `final int`

  `hashCode()`

  Returns a hash code value for this object.

  `int`

  `newEndByte()`

  Returns the value of the `newEndByte` record component.

  `Point`

  `newEndPoint()`

  Returns the value of the `newEndPoint` record component.

  `int`

  `oldEndByte()`

  Returns the value of the `oldEndByte` record component.

  `Point`

  `oldEndPoint()`

  Returns the value of the `oldEndPoint` record component.

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

  + ### InputEdit

    public InputEdit([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int startByte,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int oldEndByte,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int newEndByte,
    [Point](Point.html "class in io.github.treesitter.jtreesitter") startPoint,
    [Point](Point.html "class in io.github.treesitter.jtreesitter") oldEndPoint,
    [Point](Point.html "class in io.github.treesitter.jtreesitter") newEndPoint)

    Creates an instance of a `InputEdit` record class.

    Parameters:
    :   `startByte` - the value for the `startByte` record component
    :   `oldEndByte` - the value for the `oldEndByte` record component
    :   `newEndByte` - the value for the `newEndByte` record component
    :   `startPoint` - the value for the `startPoint` record component
    :   `oldEndPoint` - the value for the `oldEndPoint` record component
    :   `newEndPoint` - the value for the `newEndPoint` record component
* ## Method Details

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
  + ### startByte

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int startByte()

    Returns the value of the `startByte` record component.

    Returns:
    :   the value of the `startByte` record component
  + ### oldEndByte

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int oldEndByte()

    Returns the value of the `oldEndByte` record component.

    Returns:
    :   the value of the `oldEndByte` record component
  + ### newEndByte

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int newEndByte()

    Returns the value of the `newEndByte` record component.

    Returns:
    :   the value of the `newEndByte` record component
  + ### startPoint

    public [Point](Point.html "class in io.github.treesitter.jtreesitter") startPoint()

    Returns the value of the `startPoint` record component.

    Returns:
    :   the value of the `startPoint` record component
  + ### oldEndPoint

    public [Point](Point.html "class in io.github.treesitter.jtreesitter") oldEndPoint()

    Returns the value of the `oldEndPoint` record component.

    Returns:
    :   the value of the `oldEndPoint` record component
  + ### newEndPoint

    public [Point](Point.html "class in io.github.treesitter.jtreesitter") newEndPoint()

    Returns the value of the `newEndPoint` record component.

    Returns:
    :   the value of the `newEndPoint` record component
Point (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Record Class Point

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.Point

Record Components:
:   `row` - The zero-based row of the document.
:   `column` - The zero-based column of the document.

All Implemented Interfaces:
:   `Comparable<Point>`

---

public record Point(int row, int column)
extends [Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")
implements [Comparable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Comparable.html "class or interface in java.lang")<[Point](Point.html "class in io.github.treesitter.jtreesitter")>

A position in a text document in terms of rows and columns.

* ## Field Summary

  Fields

  Modifier and Type

  Field

  Description

  `static final Point`

  `MAX`

  The maximum value a [Point](Point.html "class in io.github.treesitter.jtreesitter") can have.

  `static final Point`

  `MIN`

  The minimum value a [Point](Point.html "class in io.github.treesitter.jtreesitter") can have.
* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Point(int row,
  int column)`

  Creates an instance of a `Point` record class.
* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `int`

  `column()`

  Returns the value of the [`column`](#param-column) record component.

  `int`

  `compareTo(Point other)`

  `int`

  `edit(InputEdit edit)`

  Edit the point to keep it in-sync with source code that has been edited.

  `final boolean`

  `equals(Object o)`

  Indicates whether some other object is "equal to" this one.

  `final int`

  `hashCode()`

  Returns a hash code value for this object.

  `int`

  `row()`

  Returns the value of the [`row`](#param-row) record component.

  `String`

  `toString()`

  Returns a string representation of this record class.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Field Details

  + ### MIN

    public static final [Point](Point.html "class in io.github.treesitter.jtreesitter") MIN

    The minimum value a [Point](Point.html "class in io.github.treesitter.jtreesitter") can have.
  + ### MAX

    public static final [Point](Point.html "class in io.github.treesitter.jtreesitter") MAX

    The maximum value a [Point](Point.html "class in io.github.treesitter.jtreesitter") can have.
* ## Constructor Details

  + ### Point

    public Point([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int row,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int column)

    Creates an instance of a `Point` record class.

    Parameters:
    :   `row` - the value for the [`row`](#param-row) record component
    :   `column` - the value for the [`column`](#param-column) record component
* ## Method Details

  + ### compareTo

    public int compareTo([Point](Point.html "class in io.github.treesitter.jtreesitter") other)

    Specified by:
    :   `compareTo` in interface `Comparable<Point>`
  + ### edit

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int edit([InputEdit](InputEdit.html "class in io.github.treesitter.jtreesitter") edit)

    Edit the point to keep it in-sync with source code that has been edited.

    This function updates the point's byte offset and row/column position based on an edit
    operation. This is useful for editing points without requiring a tree or node instance.

    Returns:
    :   The new start byte of the point.

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

    Indicates whether some other object is "equal to" this one. The objects are equal if the other object is of the same class and if all the record components are equal. All components in this record class are compared with the `compare` method from their corresponding wrapper classes.

    Specified by:
    :   `equals` in class `Record`

    Parameters:
    :   `o` - the object with which to compare

    Returns:
    :   `true` if this object is the same as the `o` argument; `false` otherwise.
  + ### row

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int row()

    Returns the value of the [`row`](#param-row) record component.

    Returns:
    :   the value of the [`row`](#param-row) record component
  + ### column

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int column()

    Returns the value of the [`column`](#param-column) record component.

    Returns:
    :   the value of the [`column`](#param-column) record component
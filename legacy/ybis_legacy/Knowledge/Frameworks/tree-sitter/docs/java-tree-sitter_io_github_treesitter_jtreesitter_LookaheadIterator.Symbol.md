LookaheadIterator.Symbol (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Record Class LookaheadIterator.Symbol

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.LookaheadIterator.Symbol

Enclosing class:
:   `LookaheadIterator`

---

public static record LookaheadIterator.Symbol(short id, [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name)
extends [Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

A class that pairs a symbol ID with its name.

* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Symbol(short id,
  String name)`

  Creates an instance of a `Symbol` record class.
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

  `short`

  `id()`

  Returns the value of the `id` record component.

  `String`

  `name()`

  Returns the value of the `name` record component.

  `final String`

  `toString()`

  Returns a string representation of this record class.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Constructor Details

  + ### Symbol

    public Symbol([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short id,
    [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name)

    Creates an instance of a `Symbol` record class.

    Parameters:
    :   `id` - the value for the `id` record component
    :   `name` - the value for the `name` record component
* ## Method Details

  + ### toString

    public final [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") toString()

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
  + ### id

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short id()

    Returns the value of the `id` record component.

    Returns:
    :   the value of the `id` record component
  + ### name

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name()

    Returns the value of the `name` record component.

    Returns:
    :   the value of the `name` record component
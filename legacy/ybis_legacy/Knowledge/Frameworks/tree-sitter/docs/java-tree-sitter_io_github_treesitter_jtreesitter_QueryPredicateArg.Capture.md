QueryPredicateArg.Capture (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Record Class QueryPredicateArg.Capture

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.QueryPredicateArg.Capture

All Implemented Interfaces:
:   `QueryPredicateArg`

Enclosing interface:
:   `QueryPredicateArg`

---

public static record QueryPredicateArg.Capture([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") value)
extends [Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")
implements [QueryPredicateArg](QueryPredicateArg.html "interface in io.github.treesitter.jtreesitter")

A capture argument (`@value`).

* ## Nested Class Summary

  ### Nested classes/interfaces inherited from interface [QueryPredicateArg](QueryPredicateArg.html#nested-class-summary "interface in io.github.treesitter.jtreesitter")

  `QueryPredicateArg.Capture, QueryPredicateArg.Literal`
* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Capture(String value)`

  Creates an instance of a `Capture` record class.
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

  `String`

  `toString()`

  Returns a string representation of this record class.

  `String`

  `value()`

  Returns the value of the `value` record component.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Constructor Details

  + ### Capture

    public Capture([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") value)

    Creates an instance of a `Capture` record class.

    Parameters:
    :   `value` - the value for the `value` record component
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

    Indicates whether some other object is "equal to" this one. The objects are equal if the other object is of the same class and if all the record components are equal. All components in this record class are compared with [`Objects::equals(Object,Object)`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Objects.html#equals(java.lang.Object,java.lang.Object) "class or interface in java.util").

    Specified by:
    :   `equals` in class `Record`

    Parameters:
    :   `o` - the object with which to compare

    Returns:
    :   `true` if this object is the same as the `o` argument; `false` otherwise.
  + ### value

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") value()

    Returns the value of the `value` record component.

    Specified by:
    :   `value` in interface `QueryPredicateArg`

    Returns:
    :   the value of the `value` record component
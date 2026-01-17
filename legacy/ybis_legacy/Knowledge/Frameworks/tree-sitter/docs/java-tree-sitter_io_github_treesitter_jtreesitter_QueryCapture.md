QueryCapture (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Record Class QueryCapture

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.QueryCapture

Record Components:
:   `name` - The name of the capture.
:   `node` - The captured node.

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public record QueryCapture([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name, [Node](Node.html "class in io.github.treesitter.jtreesitter") node)
extends [Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

A [`Node`](Node.html "class in io.github.treesitter.jtreesitter") that was captured with a certain capture name.

* ## Constructor Summary

  Constructors

  Constructor

  Description

  `QueryCapture(String name,
  Node node)`

  Creates an instance of a `QueryCapture` record class.
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

  `name()`

  Returns the value of the [`name`](#param-name) record component.

  `Node`

  `node()`

  Returns the value of the [`node`](#param-node) record component.

  `final String`

  `toString()`

  Returns a string representation of this record class.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Constructor Details

  + ### QueryCapture

    public QueryCapture([String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name,
    [Node](Node.html "class in io.github.treesitter.jtreesitter") node)

    Creates an instance of a `QueryCapture` record class.

    Parameters:
    :   `name` - the value for the [`name`](#param-name) record component
    :   `node` - the value for the [`node`](#param-node) record component
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

    Indicates whether some other object is "equal to" this one. The objects are equal if the other object is of the same class and if all the record components are equal. All components in this record class are compared with [`Objects::equals(Object,Object)`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/Objects.html#equals(java.lang.Object,java.lang.Object) "class or interface in java.util").

    Specified by:
    :   `equals` in class `Record`

    Parameters:
    :   `o` - the object with which to compare

    Returns:
    :   `true` if this object is the same as the `o` argument; `false` otherwise.
  + ### name

    public [String](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/String.html "class or interface in java.lang") name()

    Returns the value of the [`name`](#param-name) record component.

    Returns:
    :   the value of the [`name`](#param-name) record component
  + ### node

    public [Node](Node.html "class in io.github.treesitter.jtreesitter") node()

    Returns the value of the [`node`](#param-node) record component.

    Returns:
    :   the value of the [`node`](#param-node) record component
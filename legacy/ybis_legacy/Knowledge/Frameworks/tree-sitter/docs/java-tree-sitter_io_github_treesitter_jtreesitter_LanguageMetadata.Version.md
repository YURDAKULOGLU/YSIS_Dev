LanguageMetadata.Version (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Record Class LanguageMetadata.Version

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.LanguageMetadata.Version

Enclosing class:
:   `LanguageMetadata`

---

public static record LanguageMetadata.Version(short major, short minor, short patch)
extends [Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

The [Semantic Version](https://semver.org/) of the [Language](Language.html "class in io.github.treesitter.jtreesitter").

This version information may be used to signal if a given parser
is incompatible with existing queries when upgrading between versions.

Since:
:   0.25.0

* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Version(short major,
  short minor,
  short patch)`

  Creates an instance of a `Version` record class.
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

  `major()`

  Returns the value of the `major` record component.

  `short`

  `minor()`

  Returns the value of the `minor` record component.

  `short`

  `patch()`

  Returns the value of the `patch` record component.

  `String`

  `toString()`

  Returns a string representation of this record class.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Constructor Details

  + ### Version

    public Version([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short major,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short minor,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    short patch)

    Creates an instance of a `Version` record class.

    Parameters:
    :   `major` - the value for the `major` record component
    :   `minor` - the value for the `minor` record component
    :   `patch` - the value for the `patch` record component
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

    Indicates whether some other object is "equal to" this one. The objects are equal if the other object is of the same class and if all the record components are equal. All components in this record class are compared with the `compare` method from their corresponding wrapper classes.

    Specified by:
    :   `equals` in class `Record`

    Parameters:
    :   `o` - the object with which to compare

    Returns:
    :   `true` if this object is the same as the `o` argument; `false` otherwise.
  + ### major

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short major()

    Returns the value of the `major` record component.

    Returns:
    :   the value of the `major` record component
  + ### minor

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short minor()

    Returns the value of the `minor` record component.

    Returns:
    :   the value of the `minor` record component
  + ### patch

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public short patch()

    Returns the value of the `patch` record component.

    Returns:
    :   the value of the `patch` record component
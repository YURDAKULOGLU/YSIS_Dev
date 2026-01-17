LanguageMetadata (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Record Class LanguageMetadata

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

[java.lang.Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.LanguageMetadata

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public record LanguageMetadata([LanguageMetadata.Version](LanguageMetadata.Version.html "class in io.github.treesitter.jtreesitter") version)
extends [Record](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Record.html "class or interface in java.lang")

The metadata associated with a [Language](Language.html "class in io.github.treesitter.jtreesitter").

Since:
:   0.25.0

* ## Nested Class Summary

  Nested Classes

  Modifier and Type

  Class

  Description

  `static final record`

  `LanguageMetadata.Version`

  The [Semantic Version](https://semver.org/) of the [Language](Language.html "class in io.github.treesitter.jtreesitter").
* ## Constructor Summary

  Constructors

  Constructor

  Description

  `LanguageMetadata(LanguageMetadata.Version version)`

  Creates an instance of a `LanguageMetadata` record class.
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

  `final String`

  `toString()`

  Returns a string representation of this record class.

  `LanguageMetadata.Version`

  `version()`

  Returns the value of the `version` record component.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `getClass, notify, notifyAll, wait, wait, wait`

* ## Constructor Details

  + ### LanguageMetadata

    public LanguageMetadata([LanguageMetadata.Version](LanguageMetadata.Version.html "class in io.github.treesitter.jtreesitter") version)

    Creates an instance of a `LanguageMetadata` record class.

    Parameters:
    :   `version` - the value for the `version` record component
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
  + ### version

    public [LanguageMetadata.Version](LanguageMetadata.Version.html "class in io.github.treesitter.jtreesitter") version()

    Returns the value of the `version` record component.

    Returns:
    :   the value of the `version` record component
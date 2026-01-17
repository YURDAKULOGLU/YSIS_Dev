Parser.Options (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class Parser.Options

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.Parser.Options

Enclosing class:
:   `Parser`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public static final class Parser.Options
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

A class representing the parser options.

Since:
:   0.25.0

* ## Constructor Summary

  Constructors

  Constructor

  Description

  `Options(Predicate<Parser.State> progressCallback)`
* ## Method Summary

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, toString, wait, wait, wait`

* ## Constructor Details

  + ### Options

    public Options([Predicate](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/function/Predicate.html "class or interface in java.util.function")<[Parser.State](Parser.State.html "class in io.github.treesitter.jtreesitter")> progressCallback)

    Parameters:
    :   `progressCallback` - Called when parsing progress was made. Return `true` to cancel parsing,
        `false` to continue parsing.
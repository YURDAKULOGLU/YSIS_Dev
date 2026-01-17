NativeLibraryLookup (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Interface NativeLibraryLookup

Functional Interface:
:   This is a functional interface and can therefore be used as the assignment target for a lambda expression or method reference.

---

[@FunctionalInterface](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/FunctionalInterface.html "class or interface in java.lang")
public interface NativeLibraryLookup

An interface implemented by clients that wish to customize the [`SymbolLookup`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SymbolLookup.html "class or interface in java.lang.foreign")
used for the tree-sitter native library. Implementations must be registered
by listing their fully qualified class name in a resource file named
`META-INF/services/io.github.treesitter.jtreesitter.NativeLibraryLookup`.

Since:
:   0.25.0

See Also:
:   * [`ServiceLoader`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/ServiceLoader.html "class or interface in java.util")

* ## Method Summary

  All MethodsInstance MethodsAbstract Methods

  Modifier and Type

  Method

  Description

  `SymbolLookup`

  `get(Arena arena)`

  Get the [`SymbolLookup`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SymbolLookup.html "class or interface in java.lang.foreign") to be used for the tree-sitter native library.

* ## Method Details

  + ### get

    [SymbolLookup](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SymbolLookup.html "class or interface in java.lang.foreign") get([Arena](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/Arena.html "class or interface in java.lang.foreign") arena)

    Get the [`SymbolLookup`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SymbolLookup.html "class or interface in java.lang.foreign") to be used for the tree-sitter native library.

    Parameters:
    :   `arena` - The arena that will manage the native memory.

    Since:
    :   0.25.0
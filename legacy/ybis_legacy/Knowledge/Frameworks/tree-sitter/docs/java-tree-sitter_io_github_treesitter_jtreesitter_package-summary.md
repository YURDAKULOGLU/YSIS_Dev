io.github.treesitter.jtreesitter (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Package io.github.treesitter.jtreesitter

---

package io.github.treesitter.jtreesitter

Java bindings to the [tree-sitter](https://tree-sitter.github.io/tree-sitter/) parsing library.

## Requirements

* JDK 22 (for the
  [Foreign Function and Memory API](https://docs.oracle.com/en/java/javase/22/core/foreign-function-and-memory-api.html))
* Tree-sitter shared library
* Generated bindings for languages
* Shared libraries for languages

## Basic Usage

Copy![Copy snippet](../../../../resource-files/copy.svg)

```
 Language language = new Language(TreeSitterJava.language());
 try (Parser parser = new Parser(language)) {
     try (Tree tree = parser.parse("void main() {}", InputEncoding.UTF_8).orElseThrow()) {
         Node rootNode = tree.getRootNode();
         assert rootNode.getType().equals("program");
         assert rootNode.getStartPoint().column() == 0;
         assert rootNode.getEndPoint().column() == 14;
     }
 }
```

## Library Loading

There are three ways to load the shared libraries:

1. The libraries can be installed in the OS-specific library search path or in
   `java.library.path`. The search path can be amended using the
   `LD_LIBRARY_PATH` environment variable on Linux, `DYLD_LIBRARY_PATH`
   on macOS, or `PATH` on Windows. The libraries will be loaded automatically by
   [`SymbolLookup.libraryLookup(String, Arena)`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SymbolLookup.html#libraryLookup(java.lang.String,java.lang.foreign.Arena) "class or interface in java.lang.foreign")[RESTRICTED](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SymbolLookup.html#restricted-libraryLookup(java.lang.String,java.lang.foreign.Arena) "class or interface in java.lang.foreign").
2. If the libraries are installed in `java.library.path` instead,
   they will be loaded automatically by [`SymbolLookup.loaderLookup()`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SymbolLookup.html#loaderLookup() "class or interface in java.lang.foreign").
3. The libraries can be loaded manually by registering a custom implementation of
   [`NativeLibraryLookup`](NativeLibraryLookup.html "interface in io.github.treesitter.jtreesitter").
   This can be used, for example, to load libraries from inside a JAR file.

* All Classes and InterfacesInterfacesClassesEnum ClassesRecord ClassesException ClassesAnnotation Interfaces

  Class

  Description

  [InputEdit](InputEdit.html "class in io.github.treesitter.jtreesitter")

  An edit to a text document.

  [InputEncoding](InputEncoding.html "enum class in io.github.treesitter.jtreesitter")

  The encoding of source code.

  [Language](Language.html "class in io.github.treesitter.jtreesitter")

  A class that defines how to parse a particular language.

  [LanguageMetadata](LanguageMetadata.html "class in io.github.treesitter.jtreesitter")

  The metadata associated with a [Language](Language.html "class in io.github.treesitter.jtreesitter").

  [LanguageMetadata.Version](LanguageMetadata.Version.html "class in io.github.treesitter.jtreesitter")

  The [Semantic Version](https://semver.org/) of the [Language](Language.html "class in io.github.treesitter.jtreesitter").

  [Logger](Logger.html "interface in io.github.treesitter.jtreesitter")

  A function that logs parsing results.

  [Logger.Type](Logger.Type.html "enum class in io.github.treesitter.jtreesitter")

  The type of a log message.

  [LookaheadIterator](LookaheadIterator.html "class in io.github.treesitter.jtreesitter")

  A class that is used to look up valid symbols in a specific parse state.

  [LookaheadIterator.Symbol](LookaheadIterator.Symbol.html "class in io.github.treesitter.jtreesitter")

  A class that pairs a symbol ID with its name.

  [NativeLibraryLookup](NativeLibraryLookup.html "interface in io.github.treesitter.jtreesitter")

  An interface implemented by clients that wish to customize the [`SymbolLookup`](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SymbolLookup.html "class or interface in java.lang.foreign")
  used for the tree-sitter native library.

  [Node](Node.html "class in io.github.treesitter.jtreesitter")

  A single node within a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter").

  [ParseCallback](ParseCallback.html "interface in io.github.treesitter.jtreesitter")

  A function that retrieves a chunk of text at a given byte offset and point.

  [Parser](Parser.html "class in io.github.treesitter.jtreesitter")

  A class that is used to produce a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter") from source code.

  [Parser.Options](Parser.Options.html "class in io.github.treesitter.jtreesitter")

  A class representing the parser options.

  [Parser.State](Parser.State.html "class in io.github.treesitter.jtreesitter")

  A class representing the current state of the parser.

  [Point](Point.html "class in io.github.treesitter.jtreesitter")

  A position in a text document in terms of rows and columns.

  [Query](Query.html "class in io.github.treesitter.jtreesitter")

  A class that represents a set of patterns which match
  [nodes](Node.html "class in io.github.treesitter.jtreesitter") in a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter").

  [QueryCapture](QueryCapture.html "class in io.github.treesitter.jtreesitter")

  A [`Node`](Node.html "class in io.github.treesitter.jtreesitter") that was captured with a certain capture name.

  [QueryCursor](QueryCursor.html "class in io.github.treesitter.jtreesitter")

  A class that can be used to execute a [query](Query.html "class in io.github.treesitter.jtreesitter")
  on a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter").

  [QueryCursor.Options](QueryCursor.Options.html "class in io.github.treesitter.jtreesitter")

  A class representing the query cursor options.

  [QueryCursor.State](QueryCursor.State.html "class in io.github.treesitter.jtreesitter")

  A class representing the current state of the query cursor.

  [QueryError](QueryError.html "class in io.github.treesitter.jtreesitter")

  Any error that occurred while instantiating a [`Query`](Query.html "class in io.github.treesitter.jtreesitter").

  [QueryError.Capture](QueryError.Capture.html "class in io.github.treesitter.jtreesitter")

  A capture name error.

  [QueryError.Field](QueryError.Field.html "class in io.github.treesitter.jtreesitter")

  A field name error.

  [QueryError.NodeType](QueryError.NodeType.html "class in io.github.treesitter.jtreesitter")

  A node type error.

  [QueryError.Predicate](QueryError.Predicate.html "class in io.github.treesitter.jtreesitter")

  A query predicate error.

  [QueryError.Structure](QueryError.Structure.html "class in io.github.treesitter.jtreesitter")

  A pattern structure error.

  [QueryError.Syntax](QueryError.Syntax.html "class in io.github.treesitter.jtreesitter")

  A query syntax error.

  [QueryMatch](QueryMatch.html "class in io.github.treesitter.jtreesitter")

  A match that corresponds to a certain pattern in a [`Query`](Query.html "class in io.github.treesitter.jtreesitter").

  [QueryPredicate](QueryPredicate.html "class in io.github.treesitter.jtreesitter")

  A query predicate that associates conditions (or arbitrary metadata) with a pattern.

  [QueryPredicate.AnyOf](QueryPredicate.AnyOf.html "class in io.github.treesitter.jtreesitter")

  Handles the following predicates:  
  `#any-of?`, `#not-any-of?`

  [QueryPredicate.Eq](QueryPredicate.Eq.html "class in io.github.treesitter.jtreesitter")

  Handles the following predicates:  
  `#eq?`, `#not-eq?`, `#any-eq?`, `#any-not-eq?`

  [QueryPredicate.Match](QueryPredicate.Match.html "class in io.github.treesitter.jtreesitter")

  Handles the following predicates:  
  `#match?`, `#not-match?`, `#any-match?`, `#any-not-match?`

  [QueryPredicateArg](QueryPredicateArg.html "interface in io.github.treesitter.jtreesitter")

  An argument to a [`QueryPredicate`](QueryPredicate.html "class in io.github.treesitter.jtreesitter").

  [QueryPredicateArg.Capture](QueryPredicateArg.Capture.html "class in io.github.treesitter.jtreesitter")

  A capture argument (`@value`).

  [QueryPredicateArg.Literal](QueryPredicateArg.Literal.html "class in io.github.treesitter.jtreesitter")

  A literal string argument (`"value"`).

  [Range](Range.html "class in io.github.treesitter.jtreesitter")

  A range of positions in a text document,
  both in terms of bytes and of row-column points.

  [Tree](Tree.html "class in io.github.treesitter.jtreesitter")

  A class that represents a syntax tree.

  [TreeCursor](TreeCursor.html "class in io.github.treesitter.jtreesitter")

  A class that can be used to efficiently walk a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter").

  [Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")

  Specifies that the value is of an unsigned data type.
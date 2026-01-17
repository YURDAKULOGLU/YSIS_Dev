QueryCursor (JTreeSitter 0.26.0 API)




JavaScript is disabled on your browser.

# Class QueryCursor

[java.lang.Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")

io.github.treesitter.jtreesitter.QueryCursor

All Implemented Interfaces:
:   `AutoCloseable`

---

[@NullMarked](https://jspecify.dev/docs/api/org/jspecify/annotations/NullMarked.html "class or interface in org.jspecify.annotations")
public class QueryCursor
extends [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html "class or interface in java.lang")
implements [AutoCloseable](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/AutoCloseable.html "class or interface in java.lang")

A class that can be used to execute a [query](Query.html "class in io.github.treesitter.jtreesitter")
on a [syntax tree](Tree.html "class in io.github.treesitter.jtreesitter").

Since:
:   0.25.0

* ## Nested Class Summary

  Nested Classes

  Modifier and Type

  Class

  Description

  `static class`

  `QueryCursor.Options`

  A class representing the query cursor options.

  `static final class`

  `QueryCursor.State`

  A class representing the current state of the query cursor.
* ## Constructor Summary

  Constructors

  Constructor

  Description

  `QueryCursor(Query query)`

  Create a new cursor for the given query.
* ## Method Summary

  All MethodsInstance MethodsConcrete Methods

  Modifier and Type

  Method

  Description

  `void`

  `close()`

  `boolean`

  `didExceedMatchLimit()`

  Check if the query exceeded its maximum number of
  in-progress matches during its last execution.

  `Stream<AbstractMap.SimpleImmutableEntry<Integer, QueryMatch>>`

  `findCaptures(Node node)`

  Iterate over all the captures in the order that they were found.

  `Stream<AbstractMap.SimpleImmutableEntry<Integer, QueryMatch>>`

  `findCaptures(Node node,
  QueryCursor.Options options)`

  Iterate over all the captures in the order that they were found.

  `Stream<AbstractMap.SimpleImmutableEntry<Integer, QueryMatch>>`

  `findCaptures(Node node,
  SegmentAllocator allocator,
  @Nullable QueryCursor.Options options)`

  Iterate over all the captures in the order that they were found.

  `Stream<QueryMatch>`

  `findMatches(Node node)`

  Iterate over all the matches in the order that they were found.

  `Stream<QueryMatch>`

  `findMatches(Node node,
  QueryCursor.Options options)`

  Iterate over all the matches in the order that they were found.

  `Stream<QueryMatch>`

  `findMatches(Node node,
  SegmentAllocator allocator,
  @Nullable QueryCursor.Options options)`

  Iterate over all the matches in the order that they were found, using the given allocator.

  `int`

  `getMatchLimit()`

  Get the maximum number of in-progress matches.

  `QueryCursor`

  `setByteRange(int startByte,
  int endByte)`

  Set the range of bytes in which the query will be executed.

  `QueryCursor`

  `setContainingByteRange(int startByte,
  int endByte)`

  Set the byte range within which all matches must be fully contained.

  `QueryCursor`

  `setContainingPointRange(Point startPoint,
  Point endPoint)`

  Set the point range within which all matches must be fully contained.

  `QueryCursor`

  `setMatchLimit(int matchLimit)`

  Get the maximum number of in-progress matches.

  `QueryCursor`

  `setMaxStartDepth(int maxStartDepth)`

  Set the maximum start depth for the query.

  `QueryCursor`

  `setPointRange(Point startPoint,
  Point endPoint)`

  Set the range of points in which the query will be executed.

  ### Methods inherited from class [Object](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Object.html#method-summary "class or interface in java.lang")

  `equals, getClass, hashCode, notify, notifyAll, toString, wait, wait, wait`

* ## Constructor Details

  + ### QueryCursor

    public QueryCursor([Query](Query.html "class in io.github.treesitter.jtreesitter") query)

    Create a new cursor for the given query.
* ## Method Details

  + ### getMatchLimit

    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    public int getMatchLimit()

    Get the maximum number of in-progress matches.

    API Note:
    :   Defaults to `-1` (unlimited).
  + ### setMatchLimit

    public [QueryCursor](QueryCursor.html "class in io.github.treesitter.jtreesitter") setMatchLimit([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int matchLimit)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Get the maximum number of in-progress matches.

    Throws:
    :   `IllegalArgumentException` - If `matchLimit == 0`.
  + ### setMaxStartDepth

    public [QueryCursor](QueryCursor.html "class in io.github.treesitter.jtreesitter") setMaxStartDepth([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int maxStartDepth)

    Set the maximum start depth for the query.

    This prevents cursors from exploring children nodes at a certain depth.
      
    Note that if a pattern includes many children, then they will still be checked.
  + ### setByteRange

    public [QueryCursor](QueryCursor.html "class in io.github.treesitter.jtreesitter") setByteRange([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int startByte,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int endByte)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Set the range of bytes in which the query will be executed.

    The query cursor will return matches that intersect with the given range.
    This means that a match may be returned even if some of its captures fall
    outside the specified range, as long as at least part of the match
    overlaps with the range.

    For example, if a query pattern matches a node that spans a larger area
    than the specified range, but part of that node intersects with the range,
    the entire match will be returned.

    Throws:
    :   `IllegalArgumentException` - If `endByte > startByte`.
  + ### setContainingByteRange

    public [QueryCursor](QueryCursor.html "class in io.github.treesitter.jtreesitter") setContainingByteRange([@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int startByte,
    [@Unsigned](Unsigned.html "annotation interface in io.github.treesitter.jtreesitter")
    int endByte)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Set the byte range within which all matches must be fully contained.

    In contrast to [`setByteRange(int, int)`](#setByteRange(int,int)), this will restrict the query cursor
    to only return matches where *all* nodes are *fully* contained within
    the given range. Both functions can be used together, e.g. to search for any matches
    that intersect line 5000, as long as they are fully contained within lines 4500-5500.

    Throws:
    :   `IllegalArgumentException` - If `endByte > startByte`.

    Since:
    :   0.26.0
  + ### setPointRange

    public [QueryCursor](QueryCursor.html "class in io.github.treesitter.jtreesitter") setPointRange([Point](Point.html "class in io.github.treesitter.jtreesitter") startPoint,
    [Point](Point.html "class in io.github.treesitter.jtreesitter") endPoint)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Set the range of points in which the query will be executed.

    The query cursor will return matches that intersect with the given range.
    This means that a match may be returned even if some of its captures fall
    outside the specified range, as long as at least part of the match
    overlaps with the range.

    For example, if a query pattern matches a node that spans a larger area
    than the specified range, but part of that node intersects with the range,
    the entire match will be returned.

    Throws:
    :   `IllegalArgumentException` - If `endPoint > startPoint`.
  + ### setContainingPointRange

    public [QueryCursor](QueryCursor.html "class in io.github.treesitter.jtreesitter") setContainingPointRange([Point](Point.html "class in io.github.treesitter.jtreesitter") startPoint,
    [Point](Point.html "class in io.github.treesitter.jtreesitter") endPoint)
    throws [IllegalArgumentException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/IllegalArgumentException.html "class or interface in java.lang")

    Set the point range within which all matches must be fully contained.

    In contrast to [`setPointRange(Point, Point)`](#setPointRange(io.github.treesitter.jtreesitter.Point,io.github.treesitter.jtreesitter.Point)), this will restrict the query cursor
    to only return matches where *all* nodes are *fully* contained within
    the given range. Both functions can be used together, e.g. to search for any matches
    that intersect line 5000, as long as they are fully contained within lines 4500-5500.

    Throws:
    :   `IllegalArgumentException` - If `endPoint > startPoint`.

    Since:
    :   0.26.0
  + ### didExceedMatchLimit

    public boolean didExceedMatchLimit()

    Check if the query exceeded its maximum number of
    in-progress matches during its last execution.
  + ### findCaptures

    public [Stream](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/stream/Stream.html "class or interface in java.util.stream")<[AbstractMap.SimpleImmutableEntry](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/AbstractMap.SimpleImmutableEntry.html "class or interface in java.util")<[Integer](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Integer.html "class or interface in java.lang"), [QueryMatch](QueryMatch.html "class in io.github.treesitter.jtreesitter")>> findCaptures([Node](Node.html "class in io.github.treesitter.jtreesitter") node)

    Iterate over all the captures in the order that they were found.

    This is useful if you don't care about which pattern matched,
    and just want a single, ordered sequence of captures.

    Parameters:
    :   `node` - The node that the query will run on.

    Implementation Note:
    :   The lifetime of the matches is bound to that of the cursor.
  + ### findCaptures

    public [Stream](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/stream/Stream.html "class or interface in java.util.stream")<[AbstractMap.SimpleImmutableEntry](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/AbstractMap.SimpleImmutableEntry.html "class or interface in java.util")<[Integer](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Integer.html "class or interface in java.lang"), [QueryMatch](QueryMatch.html "class in io.github.treesitter.jtreesitter")>> findCaptures([Node](Node.html "class in io.github.treesitter.jtreesitter") node,
    [QueryCursor.Options](QueryCursor.Options.html "class in io.github.treesitter.jtreesitter") options)

    Iterate over all the captures in the order that they were found.

    This is useful if you don't care about which pattern matched,
    and just want a single, ordered sequence of captures.

    Parameters:
    :   `node` - The node that the query will run on.
    :   `options` - The options of the query cursor.

    Implementation Note:
    :   The lifetime of the matches is bound to that of the cursor.
  + ### findCaptures

    public [Stream](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/stream/Stream.html "class or interface in java.util.stream")<[AbstractMap.SimpleImmutableEntry](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/AbstractMap.SimpleImmutableEntry.html "class or interface in java.util")<[Integer](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/Integer.html "class or interface in java.lang"), [QueryMatch](QueryMatch.html "class in io.github.treesitter.jtreesitter")>> findCaptures([Node](Node.html "class in io.github.treesitter.jtreesitter") node,
    [SegmentAllocator](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SegmentAllocator.html "class or interface in java.lang.foreign") allocator,
    [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [QueryCursor.Options](QueryCursor.Options.html "class in io.github.treesitter.jtreesitter") options)

    Iterate over all the captures in the order that they were found.

    This is useful if you don't care about which pattern matched,
    and just want a single, ordered sequence of captures.

    Parameters:
    :   `node` - The node that the query will run on.
    :   `options` - The options of the query cursor.
  + ### findMatches

    public [Stream](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/stream/Stream.html "class or interface in java.util.stream")<[QueryMatch](QueryMatch.html "class in io.github.treesitter.jtreesitter")> findMatches([Node](Node.html "class in io.github.treesitter.jtreesitter") node)

    Iterate over all the matches in the order that they were found.

    Because multiple patterns can match the same set of nodes, one match may contain
    captures that appear *before* some of the captures from a previous match.

    Parameters:
    :   `node` - The node that the query will run on.

    Implementation Note:
    :   The lifetime of the matches is bound to that of the cursor.
  + ### findMatches

    public [Stream](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/stream/Stream.html "class or interface in java.util.stream")<[QueryMatch](QueryMatch.html "class in io.github.treesitter.jtreesitter")> findMatches([Node](Node.html "class in io.github.treesitter.jtreesitter") node,
    [QueryCursor.Options](QueryCursor.Options.html "class in io.github.treesitter.jtreesitter") options)

    Iterate over all the matches in the order that they were found.

    Because multiple patterns can match the same set of nodes, one match may contain
    captures that appear *before* some of the captures from a previous match.

    #### Predicate Example

    Copy![Copy snippet](../../../../resource-files/copy.svg)

    ```
     QueryCursor.Options options = new QueryCursor.Options((predicate, match) -> {
         if (!predicate.getName().equals("ieq?")) return true;
         List<QueryPredicateArg> args = predicate.getArgs();
         Node node = match.findNodes(args.getFirst().value()).getFirst();
         return args.getLast().value().equalsIgnoreCase(node.getText());
     });
     Stream<QueryMatch> matches = self.findMatches(tree.getRootNode(), options);
    ```

    Parameters:
    :   `node` - The node that the query will run on.
    :   `options` - The options of the query cursor.

    Implementation Note:
    :   The lifetime of the matches is bound to that of the cursor.
  + ### findMatches

    public [Stream](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/util/stream/Stream.html "class or interface in java.util.stream")<[QueryMatch](QueryMatch.html "class in io.github.treesitter.jtreesitter")> findMatches([Node](Node.html "class in io.github.treesitter.jtreesitter") node,
    [SegmentAllocator](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/foreign/SegmentAllocator.html "class or interface in java.lang.foreign") allocator,
    [@Nullable](https://jspecify.dev/docs/api/org/jspecify/annotations/Nullable.html "class or interface in org.jspecify.annotations") [QueryCursor.Options](QueryCursor.Options.html "class in io.github.treesitter.jtreesitter") options)

    Iterate over all the matches in the order that they were found, using the given allocator.

    Because multiple patterns can match the same set of nodes, one match may contain
    captures that appear *before* some of the captures from a previous match.

    Parameters:
    :   `node` - The node that the query will run on.
    :   `options` - The options of the query cursor.

    See Also:
    :   - [`findMatches(Node, Options)`](#findMatches(io.github.treesitter.jtreesitter.Node,io.github.treesitter.jtreesitter.QueryCursor.Options))
  + ### close

    public void close()
    throws [RuntimeException](https://docs.oracle.com/en/java/javase/23/docs/api/java.base/java/lang/RuntimeException.html "class or interface in java.lang")

    Specified by:
    :   `close` in interface `AutoCloseable`

    Throws:
    :   `RuntimeException`
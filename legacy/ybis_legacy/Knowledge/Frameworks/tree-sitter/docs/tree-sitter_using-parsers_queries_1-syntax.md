Basic Syntax - Tree-sitter



## Keyboard shortcuts

Press `←` or `→` to navigate between chapters

Press `S` or `/` to search in the book

Press `?` to show this help

Press `Esc` to hide this help

* Auto
* Light
* Rust
* Coal
* Navy
* Ayu

# Tree-sitter

# [Query Syntax](#query-syntax)

A *query* consists of one or more *patterns*, where each pattern is an [S-expression](https://en.wikipedia.org/wiki/S-expression) that matches a certain set of
nodes in a syntax tree. The expression to match a given node consists of a pair of parentheses containing two things: the
node's type, and optionally, a series of other S-expressions that match the node's children. For example, this pattern would
match any `binary_expression` node whose children are both `number_literal` nodes:

```
(binary_expression (number_literal) (number_literal))
```

Children can also be omitted. For example, this would match any `binary_expression` where at least *one* of child is a
`string_literal` node:

```
(binary_expression (string_literal))
```

## [Fields](#fields)

In general, it's a good idea to make patterns more specific by specifying [field names](../2-basic-parsing.html#node-field-names) associated with
child nodes. You do this by prefixing a child pattern with a field name followed by a colon. For example, this pattern would
match an `assignment_expression` node where the `left` child is a `member_expression` whose `object` is a `call_expression`.

```
(assignment_expression
  left: (member_expression
    object: (call_expression)))
```

## [Negated Fields](#negated-fields)

You can also constrain a pattern so that it only matches nodes that *lack* a certain field. To do this, add a field name
prefixed by a `!` within the parent pattern. For example, this pattern would match a class declaration with no type parameters:

```
(class_declaration
  name: (identifier) @class_name
  !type_parameters)
```

## [Anonymous Nodes](#anonymous-nodes)

The parenthesized syntax for writing nodes only applies to [named nodes](../2-basic-parsing.html#named-vs-anonymous-nodes). To match specific anonymous
nodes, you write their name between double quotes. For example, this pattern would match any `binary_expression` where the
operator is `!=` and the right side is `null`:

```
(binary_expression
  operator: "!="
  right: (null))
```

## [Special Nodes](#special-nodes)

### [The Wildcard Node](#the-wildcard-node)

A wildcard node is represented with an underscore (`_`), it matches any node.
This is similar to `.` in regular expressions.
There are two types, `(_)` will match any named node,
and `_` will match any named or anonymous node.

For example, this pattern would match any node inside a call:

```
(call (_) @call.inner)
```

### [The `ERROR` Node](#the-error-node)

When the parser encounters text it does not recognize, it represents this node
as `(ERROR)` in the syntax tree. These error nodes can be queried just like
normal nodes:

```
(ERROR) @error-node
```

### [The `MISSING` Node](#the-missing-node)

If the parser is able to recover from erroneous text by inserting a missing token and then reducing, it will insert that
missing node in the final tree so long as that tree has the lowest error cost. These missing nodes appear as seemingly normal
nodes in the tree, but they are zero tokens wide, and are internally represented as a property of the actual terminal node
that was inserted, instead of being its own kind of node, like the `ERROR` node. These special missing nodes can be queried
using `(MISSING)`:

```
(MISSING) @missing-node
```

This is useful when attempting to detect all syntax errors in a given parse tree, since these missing node are not captured
by `(ERROR)` queries. Specific missing node types can also be queried:

```
(MISSING identifier) @missing-identifier
(MISSING ";") @missing-semicolon
```

### [Supertype Nodes](#supertype-nodes)

Some node types are marked as *supertypes* in a grammar. A supertype is a node type that contains multiple
subtypes. For example, in the [JavaScript grammar example](../../creating-parsers/3-writing-the-grammar.html#structuring-rules-well), `expression` is a supertype that can represent any kind
of expression, such as a `binary_expression`, `call_expression`, or `identifier`. You can use supertypes in queries to match
any of their subtypes, rather than having to list out each subtype individually. For example, this pattern would match any
kind of expression, even though it's not a visible node in the syntax tree:

```
(expression) @any-expression
```

To query specific subtypes of a supertype, you can use the syntax `supertype/subtype`. For example, this pattern would
match a `binary_expression` only if it is a child of `expression`:

```
(expression/binary_expression) @binary-expression
```

This also applies to anonymous nodes. For example, this pattern would match `"()"` only if it is a child of `expression`:

```
(expression/"()") @empty-expression
```
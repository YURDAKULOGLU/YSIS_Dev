Static Node Types - Tree-sitter



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

# [Static Node Types](#static-node-types)

In languages with static typing, it can be helpful for syntax trees to provide specific type information about individual
syntax nodes. Tree-sitter makes this information available via a generated file called `node-types.json`. This *node types*
file provides structured data about every possible syntax node in a grammar.

You can use this data to generate type declarations in statically-typed programming languages.

The node types file contains an array of objects, each of which describes a particular type of syntax node using the
following entries:

## [Basic Info](#basic-info)

Every object in this array has these two entries:

* `"type"` — A string that indicates, which grammar rule the node represents. This corresponds to the `ts_node_type` function
  described [here](./2-basic-parsing.html#syntax-nodes).
* `"named"` — A boolean that indicates whether this kind of node corresponds to a rule name in the grammar or just a string
  literal. See [here](./2-basic-parsing.html#named-vs-anonymous-nodes) for more info.

Examples:

```
{
  "type": "string_literal",
  "named": true
}
{
  "type": "+",
  "named": false
}
```

Together, these two fields constitute a unique identifier for a node type; no two top-level objects in the `node-types.json`
should have the same values for both `"type"` and `"named"`.

## [Internal Nodes](#internal-nodes)

Many syntax nodes can have *children*. The node type object describes the possible children that a node can have using the
following entries:

* `"fields"` — An object that describes the possible [fields](./2-basic-parsing.html#node-field-names) that the node can have. The keys of this
  object are field names, and the values are *child type* objects, described below.
* `"children"` — Another *child type* object that describes all the node's possible *named* children *without* fields.

A *child type* object describes a set of child nodes using the following entries:

* `"required"` — A boolean indicating whether there is always *at least one* node in this set.
* `"multiple"` — A boolean indicating whether there can be *multiple* nodes in this set.
* `"types"`- An array of objects that represent the possible types of nodes in this set. Each object has two keys: `"type"`
  and `"named"`, whose meanings are described above.

Example with fields:

```
{
  "type": "method_definition",
  "named": true,
  "fields": {
    "body": {
      "multiple": false,
      "required": true,
      "types": [{ "type": "statement_block", "named": true }]
    },
    "decorator": {
      "multiple": true,
      "required": false,
      "types": [{ "type": "decorator", "named": true }]
    },
    "name": {
      "multiple": false,
      "required": true,
      "types": [
        { "type": "computed_property_name", "named": true },
        { "type": "property_identifier", "named": true }
      ]
    },
    "parameters": {
      "multiple": false,
      "required": true,
      "types": [{ "type": "formal_parameters", "named": true }]
    }
  }
}
```

Example with children:

```
{
  "type": "array",
  "named": true,
  "fields": {},
  "children": {
    "multiple": true,
    "required": false,
    "types": [
      { "type": "_expression", "named": true },
      { "type": "spread_element", "named": true }
    ]
  }
}
```

## [Supertype Nodes](#supertype-nodes)

In Tree-sitter grammars, there are usually certain rules that represent abstract *categories* of syntax nodes (e.g. "expression",
"type", "declaration"). In the `grammar.js` file, these are often written as [hidden rules](../creating-parsers/3-writing-the-grammar.html#hiding-rules)
whose definition is a simple [`choice`](../creating-parsers/2-the-grammar-dsl.html) where each member is just a single symbol.

Normally, hidden rules are not mentioned in the node types file, since they don't appear in the syntax tree. But if you add
a hidden rule to the grammar's [`supertypes` list](../creating-parsers/2-the-grammar-dsl.html), then it *will* show up in the node
types file, with the following special entry:

* `"subtypes"` — An array of objects that specify the *types* of nodes that this 'supertype' node can wrap.

Example:

```
{
  "type": "_declaration",
  "named": true,
  "subtypes": [
    { "type": "class_declaration", "named": true },
    { "type": "function_declaration", "named": true },
    { "type": "generator_function_declaration", "named": true },
    { "type": "lexical_declaration", "named": true },
    { "type": "variable_declaration", "named": true }
  ]
}
```

Supertype nodes will also appear elsewhere in the node types file, as children of other node types, in a way that corresponds
with how the supertype rule was used in the grammar. This can make the node types much shorter and easier to read, because
a single supertype will take the place of multiple subtypes.

Example:

```
{
  "type": "export_statement",
  "named": true,
  "fields": {
    "declaration": {
      "multiple": false,
      "required": false,
      "types": [{ "type": "_declaration", "named": true }]
    },
    "source": {
      "multiple": false,
      "required": false,
      "types": [{ "type": "string", "named": true }]
    }
  }
}
```
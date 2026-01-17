tree-sitter - v0.25.0

# tree-sitter - v0.25.0

# Node Tree-sitter

[![CI](https://img.shields.io/github/actions/workflow/status/tree-sitter/node-tree-sitter/ci.yml?logo=github&label=CI)](https://github.com/tree-sitter/node-tree-sitter/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/tree-sitter?logo=npm)](https://npmjs.com/package/tree-sitter)
[![docs](https://img.shields.io/badge/docs-website-blue)](https://tree-sitter.github.io/node-tree-sitter)

This module provides Node.js bindings to the [tree-sitter] parsing library.

## Installation

```
npm install tree-sitter
Copy
```

## Basic Usage

### Prerequisites

First, you'll need a Tree-sitter grammar for the language you want to parse. There are many [existing grammars](https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers),
such as [tree-sitter-javascript](http://github.com/tree-sitter/tree-sitter-javascript). These grammars can typically be installed with a package manager like NPM,
so long as the author has published them.

```
npm install tree-sitter-javascript
Copy
```

You can also develop a new grammar by using the [Tree-sitter CLI](https://github.com/tree-sitter/tree-sitter/tree/master/cli) and following the [docs](https://tree-sitter.github.io/tree-sitter/creating-parsers).

### Parsing Source Code

Once you've got your grammar, create a parser with that grammar.

```
const Parser = require('tree-sitter');  
const JavaScript = require('tree-sitter-javascript');  
  
const parser = new Parser();  
parser.setLanguage(JavaScript);
Copy
```

Then you can parse some source code,

```
const sourceCode = 'let x = 1; console.log(x);';  
const tree = parser.parse(sourceCode);
Copy
```

and inspect the syntax tree.

```
console.log(tree.rootNode.toString());  
  
// (program  
//   (lexical_declaration  
//     (variable_declarator (identifier) (number)))  
//   (expression_statement  
//     (call_expression  
//       (member_expression (identifier) (property_identifier))  
//       (arguments (identifier)))))  
  
const callExpression = tree.rootNode.child(1).firstChild;  
console.log(callExpression);  
  
// {  
//   type: 'call_expression',  
//   startPosition: {row: 0, column: 16},  
//   endPosition: {row: 0, column: 30},  
//   startIndex: 0,  
//   endIndex: 30  
// }
Copy
```

If your source code *changes*, you can update the syntax tree. This is much faster than the first parse.

```
// In the code, we replaced 'let' with 'const'.  
// So, we set our old end index to 3, and our new end index to 5.  
// Note that the end index is exclusive.  
const newSourceCode = 'const x = 1; console.log(x);';  
//                        ^ ^  
// indices:               3 5  
// points:            (0,3) (0,5)  
  
tree.edit({  
  startIndex: 0,  
  oldEndIndex: 3,  
  newEndIndex: 5,  
  startPosition: {row: 0, column: 0},  
  oldEndPosition: {row: 0, column: 3},  
  newEndPosition: {row: 0, column: 5},  
});  
  
const newTree = parser.parse(newSourceCode, tree);
Copy
```

### Parsing Text From a Custom Data Structure

If your text is stored in a data structure other than a single string, such as a rope or array, you can parse it by supplying
a callback to `parse` instead of a string:

```
const sourceLines = [  
  'let x = 1;',  
  'console.log(x);'  
];  
  
const tree = parser.parse((index, position) => {  
  let line = sourceLines[position.row];  
  if (line) {  
    return line.slice(position.column);  
  }  
});
Copy
```

### Further Reading

It's recommended that you read the [Tree-sitter documentation](https://tree-sitter.github.io/tree-sitter/using-parsers) on using parsers to get a higher-level overview
of the API. Once you're comfortable with the basics, you can explore the [full API documentation](https://tree-sitter.github.io/node-tree-sitter),
which should map closely to the C API, though there are some differences.

### Settings

Member Visibility

* Protected
* Inherited
* External

ThemeOSLightDark

### On This Page

[Node Tree-sitter](#node-tree-sitter)

* [Installation](#installation)
* [Basic Usage](#basic-usage)
* + [Prerequisites](#prerequisites)
  + [Parsing Source Code](#parsing-source-code)
  + [Parsing Text From a Custom Data Structure](#parsing-text-from-a-custom-data-structure)
  + [Further Reading](#further-reading)
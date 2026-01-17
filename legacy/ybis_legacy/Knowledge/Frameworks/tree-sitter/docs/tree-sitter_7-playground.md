Playground - Tree-sitter



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

# [Syntax Tree Playground](#syntax-tree-playground)

## [Code](#code)

JavaScript

Bash

C

C++

C#

Go

HTML

Java

JavaScript

PHP

Python

Ruby

Rust

TOML

TypeScript

YAML

Bash
C
C++
C#
Go
HTML
Java
JavaScript
PHP
Python
Ruby
Rust
TOML
TypeScript
YAML

Log

Show anonymous nodes

Query

Accessibility



## [Query](#query)

## Tree

## [About](#about)

You can try out tree-sitter with a few pre-selected grammars on this page.
You can also run playground locally (with your own grammar) using the
[CLI](/tree-sitter/cli/playground.html)'s `tree-sitter playground` subcommand.

Info

Logging (if enabled) can be viewed in the browser's console.

The syntax tree should update as you type in the code. As you move around the
code, the current node should be highlighted in the tree; you can also click any
node in the tree to select the corresponding part of the code.

You can enter one or more [patterns](/tree-sitter/using-parsers/queries/index.html)
into the Query panel. If the query is valid, its captures will be
highlighted both in the Code and in the Query panels. Otherwise
the problematic parts of the query will be underlined, and detailed
diagnostics will be available on hover. Note that to see any results
you must use at least one capture, like `(node_name) @capture-name`
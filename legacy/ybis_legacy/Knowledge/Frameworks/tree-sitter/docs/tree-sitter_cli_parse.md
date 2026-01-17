Parse - Tree-sitter



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

# [`tree-sitter parse`](#tree-sitter-parse)

The `parse` command parses source files using a Tree-sitter parser. You can pass any number of file paths and glob patterns
to `tree-sitter parse`, and it will parse all the given files. If no paths are provided, input will be parsed from stdin.
The command will exit with a non-zero status code if any parse errors occurred.

```
tree-sitter parse [OPTIONS] [PATHS]... # Aliases: p
```

## [Options](#options)

### [`--paths <PATHS_FILE>`](#--paths-paths_file)

The path to a file that contains paths to source files to parse.

### [`-p/--grammar-path <PATH>`](#-p--grammar-path-path)

The path to the directory containing the grammar.

### [`-l/--lib-path`](#-l--lib-path)

The path to the parser's dynamic library. This is used instead of the cached or automatically generated dynamic library.

### [`--lang-name`](#--lang-name)

If `--lib-path` is used, the name of the language used to extract the library's language function

### [`--scope <SCOPE>`](#--scope-scope)

The language scope to use for parsing. This is useful when the language is ambiguous.

### [`-d/--debug`](#-d--debug)

Outputs parsing and lexing logs. This logs to stderr.

### [`-0/--debug-build`](#-0--debug-build)

Compile the parser with debug flags enabled. This is useful when debugging issues that require a debugger like `gdb` or `lldb`.

### [`-D/--debug-graph`](#-d--debug-graph)

Outputs logs of the graphs of the stack and parse trees during parsing, as well as the actual parsing and lexing message.
The graphs are constructed with [graphviz dot](https://graphviz.org/doc/info/lang.html), and the output is written to `log.html`.

### [`--wasm`](#--wasm)

Compile and run the parser as a Wasm module (only if the tree-sitter CLI was built with `--features=wasm`).

### [`--dot`](#--dot)

Output the parse tree with [graphviz dot](https://graphviz.org/doc/info/lang.html).

### [`-x/--xml`](#-x--xml)

Output the parse tree in XML format.

### [`-c/--cst`](#-c--cst)

Output the parse tree in a pretty-printed CST format.

### [`-s/--stat`](#-s--stat)

Show parsing statistics.

### [`--timeout <TIMEOUT>`](#--timeout-timeout)

Set the timeout for parsing a single file, in microseconds.

### [`-t/--time`](#-t--time)

Print the time taken to parse the file. If edits are provided, this will also print the time taken to parse the file after
each edit.

### [`-q/--quiet`](#-q--quiet)

Suppress main output.

### [`--edits <EDITS>...`](#--edits-edits)

Apply edits after parsing the file. Edits are in the form of `row,col|position delcount insert_text` where row and col, or position are 0-indexed.

### [`--encoding <ENCODING>`](#--encoding-encoding)

Set the encoding of the input file. By default, the CLI will look for the [`BOM`](https://en.wikipedia.org/wiki/Byte_order_mark) to determine if the file is encoded
in `UTF-16BE` or `UTF-16LE`. If no `BOM` is present, `UTF-8` is the default. One of `utf8`, `utf16-le`, `utf16-be`.

### [`--open-log`](#--open-log)

When using the `--debug-graph` option, open the log file in the default browser.

### [`-j/--json-summary`](#-j--json-summary)

Output parsing results in a JSON format.

### [`--config-path <CONFIG_PATH>`](#--config-path-config_path)

The path to an alternative configuration (`config.json`) file. See [the init-config command](./init-config.html) for more information.

### [`-n/--test-number <TEST_NUMBER>`](#-n--test-number-test_number)

Parse a specific test in the corpus. The test number is the same number that appears in the output of `tree-sitter test`.

### [`-r/--rebuild`](#-r--rebuild)

Force a rebuild of the parser before running tests.

### [`--no-ranges`](#--no-ranges)

Omit the node's ranges from the default parse output. This is useful when copying S-Expressions to a test file.
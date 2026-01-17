Highlight - Tree-sitter



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

# [`tree-sitter highlight`](#tree-sitter-highlight)

You can run syntax highlighting on an arbitrary file using `tree-sitter highlight`. This can either output colors directly
to your terminal using ANSI escape codes, or produce HTML (if the `--html` flag is passed). For more information, see
[the syntax highlighting page](../3-syntax-highlighting.html).

```
tree-sitter highlight [OPTIONS] [PATHS]... # Aliases: hi
```

## [Options](#options)

### [`-H/--html`](#-h--html)

Output an HTML document with syntax highlighting.

### [`--css-classes`](#--css-classes)

Output HTML with CSS classes instead of inline styles.

### [`--check`](#--check)

Check that the highlighting captures conform strictly to the standards.

### [`--captures-path <CAPTURES_PATH>`](#--captures-path-captures_path)

The path to a file with captures. These captures would be considered the "standard" captures to compare against.

### [`--query-paths <QUERY_PATHS>`](#--query-paths-query_paths)

The paths to query files to use for syntax highlighting. These should end in `highlights.scm`.

### [`--scope <SCOPE>`](#--scope-scope)

The language scope to use for syntax highlighting. This is useful when the language is ambiguous.

### [`-t/--time`](#-t--time)

Print the time taken to highlight the file.

### [`-q/--quiet`](#-q--quiet)

Suppress main output.

### [`--paths <PATHS_FILE>`](#--paths-paths_file)

The path to a file that contains paths to source files to highlight

### [`-p/--grammar-path <PATH>`](#-p--grammar-path-path)

The path to the directory containing the grammar.

### [`--config-path <CONFIG_PATH>`](#--config-path-config_path)

The path to an alternative configuration (`config.json`) file. See [the init-config command](./init-config.html) for more information.

### [`-n/--test-number <TEST_NUMBER>`](#-n--test-number-test_number)

Highlight the contents of a specific test.

### [`-r/--rebuild`](#-r--rebuild)

Force a rebuild of the parser before running the fuzzer.
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

# [`tree-sitter playground`](#tree-sitter-playground)

The `playground` command allows you to start a local playground to test your parser interactively.

```
tree-sitter playground [OPTIONS] # Aliases: play, pg, web-ui
```

Note

For this to work, you must have already built the parser as a Wasm module. This can be done with the [`build`](./build.html) subcommand
(`tree-sitter build --wasm`).

## [Options](#options)

### [`-q/--quiet`](#-q--quiet)

Don't automatically open the playground in the default browser.

### [`--grammar-path <GRAMMAR_PATH>`](#--grammar-path-grammar_path)

The path to the directory containing the grammar and wasm files.

### [`-e/--export <EXPORT_PATH>`](#-e--export-export_path)

Export static playground files to the specified directory instead of serving them.
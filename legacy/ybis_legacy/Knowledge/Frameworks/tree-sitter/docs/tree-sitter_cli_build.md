Build - Tree-sitter



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

# [`tree-sitter build`](#tree-sitter-build)

The `build` command compiles your parser into a dynamically-loadable library,
either as a shared object (`.so`, `.dylib`, or `.dll`) or as a Wasm module.

```
tree-sitter build [OPTIONS] [PATH] # Aliases: b
```

You can change the compiler executable via the `CC` environment variable and add extra flags via `CFLAGS`.
For macOS or iOS, you can set `MACOSX_DEPLOYMENT_TARGET` or `IPHONEOS_DEPLOYMENT_TARGET` respectively to define the
minimum supported version.

The path argument allows you to specify the directory of the parser to build. If you don't supply this argument, the CLI
will attempt to build the parser in the current working directory.

## [Options](#options)

### [`-w/--wasm`](#-w--wasm)

Compile the parser as a Wasm module. This command looks for the [Wasi SDK](https://github.com/WebAssembly/wasi-sdk) indicated by the `TREE_SITTER_WASI_SDK_PATH`
environment variable. If you don't have the binary, the CLI will attempt to download it for you to `<CACHE_DIR>/tree-sitter/wasi-sdk/`, where
`<CACHE_DIR>` is resolved according to the [XDG base directory](https://specifications.freedesktop.org/basedir/latest/) or Window's [Known\_Folder\_Locations](https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid).

### [`-o/--output`](#-o--output)

Specify where to output the shared object file (native or Wasm). This flag accepts either an absolute path or a relative
path. If you don't supply this flag, the CLI will attempt to figure out what the language name is based on the parent
directory name to use for the output file. If the CLI can't figure it out, it will default to `parser`, thus generating
`parser.so` or `parser.wasm` in the current working directory.

### [`--reuse-allocator`](#--reuse-allocator)

Reuse the allocator that's set in the core library for the parser's external scanner. This is useful in applications
where the author overrides the default allocator with their own, and wants to ensure every parser that allocates memory
in the external scanner does so using their allocator.

### [`-0/--debug`](#-0--debug)

Compile the parser with debug flags enabled. This is useful when debugging issues that require a debugger like `gdb` or `lldb`.
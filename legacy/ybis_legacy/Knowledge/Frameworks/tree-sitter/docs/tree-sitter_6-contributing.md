Contributing - Tree-sitter



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

# [Contributing](#contributing)

## [Code of Conduct](#code-of-conduct)

Contributors to Tree-sitter should abide by the [Contributor Covenant](https://www.contributor-covenant.org/version/1/4/code-of-conduct).

## [Developing Tree-sitter](#developing-tree-sitter)

### [Prerequisites](#prerequisites)

To make changes to Tree-sitter, you should have:

1. A C compiler, for compiling the core library and the generated parsers.
2. A [Rust toolchain](https://rustup.rs), for compiling the Rust bindings, the highlighting library, and the CLI.
3. Node.js and NPM, for generating parsers from `grammar.js` files.
4. Either [Emscripten](https://emscripten.org), [Docker](https://www.docker.com), or [podman](https://podman.io) for
   compiling the library to Wasm.

### [Building](#building)

Clone the repository:

```
git clone https://github.com/tree-sitter/tree-sitter
cd tree-sitter
```

Optionally, build the Wasm library. If you skip this step, then the `tree-sitter playground` command will require an internet
connection. If you have Emscripten installed, this will use your `emcc` compiler. Otherwise, it will use Docker or Podman:

```
cd lib/binding_web
npm install # or your JS package manager of choice
npm run build
```

Build the Rust libraries and the CLI:

```
cargo build --release
```

This will create the `tree-sitter` CLI executable in the `target/release` folder.

If you want to automatically install the `tree-sitter` CLI in your system, you can run:

```
cargo install --path crates/cli
```

If you're going to be in a fast iteration cycle and would like the CLI to build faster, you can use the `release-dev` profile:

```
cargo build --profile release-dev
# or
cargo install --path crates/cli --profile release-dev
```

### [Testing](#testing)

Before you can run the tests, you need to fetch some upstream grammars that are used for testing:

```
cargo xtask fetch-fixtures
```

To test any changes you've made to the CLI, you can regenerate these parsers using your current CLI code:

```
cargo xtask generate-fixtures
```

Then you can run the tests:

```
cargo xtask test
```

Similarly, to test the Wasm binding, you need to compile these parsers to Wasm:

```
cargo xtask generate-fixtures --wasm
cargo xtask test-wasm
```

#### [Wasm Stdlib](#wasm-stdlib)

The tree-sitter Wasm stdlib can be built via xtask:

```
cargo xtask build-wasm-stdlib
```

This command looks for the [Wasi SDK](https://github.com/WebAssembly/wasi-sdk) indicated by the `TREE_SITTER_WASI_SDK_PATH`
environment variable. If you don't have the binary, it can be downloaded from wasi-sdk's [releases](https://github.com/WebAssembly/wasi-sdk/releases)
page.

### [Debugging](#debugging)

The test script has a number of useful flags. You can list them all by running `cargo xtask test -h`.
Here are some of the main flags:

If you want to run a specific unit test, pass its name (or part of its name) as an argument:

```
cargo xtask test test_does_something
```

You can run the tests under the debugger (either `lldb` or `gdb`) using the `-g` flag:

```
cargo xtask test -g test_does_something
```

Part of the Tree-sitter test suite involves parsing the *corpus* tests for several languages and performing randomized edits
to each example in the corpus. If you just want to run the tests for a particular *language*, you can pass the `-l` flag.
Additionally, if you want to run a particular *example* from the corpus, you can pass the `-e` flag:

```
cargo xtask test -l javascript -e Arrays
```

If you are using `lldb` to debug the C library, tree-sitter provides custom pretty printers for several of its types.
You can enable these helpers by importing them:

```
(lldb) command script import /path/to/tree-sitter/lib/lldb_pretty_printers/tree_sitter_types.py
```

## [Published Packages](#published-packages)

The main [`tree-sitter/tree-sitter`](https://github.com/tree-sitter/tree-sitter) repository contains the source code for
several packages that are published to package registries for different languages:

* Rust crates on [crates.io](https://crates.io):

  + [`tree-sitter`](https://crates.io/crates/tree-sitter) — A Rust binding to the core library
  + [`tree-sitter-highlight`](https://crates.io/crates/tree-sitter-highlight) — The syntax-highlighting library
  + [`tree-sitter-cli`](https://crates.io/crates/tree-sitter-cli) — The command-line tool
* JavaScript modules on [npmjs.com](https://npmjs.com):

  + [`web-tree-sitter`](https://www.npmjs.com/package/web-tree-sitter) — A Wasm-based JavaScript binding to the core library
  + [`tree-sitter-cli`](https://www.npmjs.com/package/tree-sitter-cli) — The command-line tool

There are also several other dependent repositories that contain other published packages:

* [`tree-sitter/node-tree-sitter`](https://github.com/tree-sitter/node-tree-sitter) — Node.js bindings to the core library,
  published as [`tree-sitter`](https://www.npmjs.com/package/tree-sitter) on npmjs.com
* [`tree-sitter/py-tree-sitter`](https://github.com/tree-sitter/py-tree-sitter) — Python bindings to the core library,
  published as [`tree-sitter`](https://pypi.org/project/tree-sitter) on [PyPI.org](https://pypi.org).
* [`tree-sitter/go-tree-sitter`](https://github.com/tree-sitter/go-tree-sitter) — Go bindings to the core library,
  published as [`tree_sitter`](https://pkg.go.dev/github.com/tree-sitter/go-tree-sitter) on [pkg.go.dev](https://pkg.go.dev).

## [Developing Documentation](#developing-documentation)

Our current static site generator for documentation is [`mdBook`](https://rust-lang.github.io/mdBook), with a little bit of custom JavaScript to handle
the playground page. Most of the documentation is written in Markdown, including this file! You can find these files
at [`docs/src`](https://github.com/tree-sitter/tree-sitter/tree/master/docs/src). If you'd like to submit a PR to improve the documentation, navigate to the page you'd like to
edit and hit the edit icon at the top right of the page.

### [Prerequisites for Local Development](#prerequisites-for-local-development)

Note

We're assuming you have `cargo` installed, the Rust package manager.

To run and iterate on the docs locally, the
[`mdbook`](https://rust-lang.github.io/mdBook/guide/installation.html) CLI tool is required, which can be installed with

```
cargo install mdbook
```

You might have noticed we have some fancy admonitions sprinkled throughout the documentation, like the note above.
These are created using [`mdbook-admonish`](https://github.com/tommilligan/mdbook-admonish), a [preprocessor](https://rust-lang.github.io/mdBook/for_developers/preprocessors.html) for `mdBook`. As such, this is also
a requirement for developing the documentation locally. To install it, run:

```
cargo install mdbook-admonish
```

Once you've installed it, you can begin using admonitions in your markdown files. See the [reference](https://tommilligan.github.io/mdbook-admonish/reference.html)
for more information.

### [Spinning it up](#spinning-it-up)

Now that you've installed the prerequisites, you can run the following command to start a local server:

```
cd docs
mdbook serve --open
```

`mdbook` has a live-reload feature, so any changes you make to the markdown files will be reflected in the browser after
a short delay. Once you've made a change that you're happy with, you can submit a PR with your changes.

### [Improving the Playground](#improving-the-playground)

The playground page is a little more complicated, but if you know some basic JavaScript and CSS you should be able to make
changes. The playground code can be found in [`docs/src/assets/js/playground.js`](https://github.com/tree-sitter/tree-sitter/blob/master/docs/src/assets/js/playground.js), and its corresponding css
at [`docs/src/assets/css/playground.css`](https://github.com/tree-sitter/tree-sitter/blob/master/docs/src/assets/css/playground.css). The editor of choice we use for the playground is [CodeMirror](https://codemirror.net),
and the tree-sitter module is fetched from [here](https://tree-sitter.github.io/web-tree-sitter.js). This, along with the Wasm module and Wasm parsers, live in the
[.github.io repo](https://github.com/tree-sitter/tree-sitter.github.io).
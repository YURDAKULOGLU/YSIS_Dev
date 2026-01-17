markdown-it-py — markdown-it-py



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![markdown-it-py - Home](_static/markdown-it-py.svg)](#)

* [Repository](https://github.com/executablebooks/markdown-it-py "Source repository")
* [Suggest edit](https://github.com/executablebooks/markdown-it-py/edit/master/docs/index.md "Suggest edit")

* [.md](_sources/index.md "Download source file")
* .pdf

# markdown-it-py

## Contents

# markdown-it-py[#](#markdown-it-py "Link to this heading")

> Markdown parser done right.

* Follows the **[CommonMark spec](http://spec.commonmark.org/)** for baseline parsing
* Configurable syntax: you can add new rules and even replace existing ones.
* Pluggable: Adds syntax extensions to extend the parser (see the [plugin list](plugins.html#md-plugins))
* High speed (see our [benchmarking tests](performance.html#md-performance))
* Easy to configure for [security](security.html#md-security)
* Member of [Google’s Assured Open Source Software](https://cloud.google.com/assured-open-source-software/docs/supported-packages)

For a good introduction to [markdown-it](https://github.com/markdown-it/markdown-it) see the **[Live demo](https://markdown-it.github.io)**.
This is a Python port of the well used [markdown-it](https://github.com/markdown-it/markdown-it), and some of its associated plugins.
The driving design philosophy of the port has been to change as little of the fundamental code structure (file names, function name, etc) as possible, just sprinkling in a little Python syntactical sugar ✨.
It is very simple to write complementary extensions for both language implementations!

## References & Thanks[#](#references-thanks "Link to this heading")

Big thanks to the authors of [markdown-it](https://github.com/markdown-it/markdown-it)

* Alex Kocharin [github/rlidwka](https://github.com/rlidwka)
* Vitaly Puzrin [github/puzrin](https://github.com/puzrin)

Also [John MacFarlane](https://github.com/jgm) for his work on the CommonMark spec and reference implementations.

## Related Links[#](#related-links "Link to this heading")

* [jgm/CommonMark](https://github.com/jgm/CommonMark) - reference CommonMark implementations in C & JS, also contains latest spec & online demo.
* <http://talk.commonmark.org> - CommonMark forum, good place to collaborate developers’ efforts.

* [Using `markdown_it`](using.html)
  + [Quick-Start](using.html#quick-start)
  + [The Parser](using.html#the-parser)
  + [The Token Stream](using.html#the-token-stream)
  + [Renderers](using.html#renderers)
* [Design principles](architecture.html)
  + [Data flow](architecture.html#data-flow)
  + [Token stream](architecture.html#token-stream)
  + [Rules](architecture.html#rules)
  + [Renderer](architecture.html#renderer)
  + [Summary](architecture.html#summary)
* [Security](security.html)
  + [Plugins](security.html#plugins)
* [Performance](performance.html)
* [Plugin extensions](plugins.html)
* [Contribute](contributing.html)
  + [Development guidance](contributing.html#development-guidance)
  + [Code Style](contributing.html#code-style)
  + [Testing](contributing.html#testing)
  + [Contributing a plugin](contributing.html#contributing-a-plugin)
  + [FAQ](contributing.html#faq)
* [markdown\_it package](api/markdown_it.html)
  + [Subpackages](api/markdown_it.html#subpackages)
  + [Submodules](api/markdown_it.html#submodules)

Contents
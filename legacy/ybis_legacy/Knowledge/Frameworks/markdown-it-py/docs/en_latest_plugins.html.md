Plugin extensions — markdown-it-py



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![markdown-it-py - Home](_static/markdown-it-py.svg)](index.html)

* [Repository](https://github.com/executablebooks/markdown-it-py "Source repository")
* [Suggest edit](https://github.com/executablebooks/markdown-it-py/edit/master/docs/plugins.md "Suggest edit")

* [.md](_sources/plugins.md "Download source file")
* .pdf

# Plugin extensions

# Plugin extensions[#](#plugin-extensions "Link to this heading")

The following plugins are embedded within the core package:

* [tables](https://help.github.com/articles/organizing-information-with-tables/) (GFM)
* [strikethrough](https://help.github.com/articles/basic-writing-and-formatting-syntax/#styling-text) (GFM)

These can be enabled individually:

```
from markdown_it import MarkdownIt
md = MarkdownIt("commonmark").enable('table')
```

or as part of a configuration:

```
from markdown_it import MarkdownIt
md = MarkdownIt("gfm-like")
```

See also

See [Using markdown\_it](using.html)

Many other plugins are then available *via* the `mdit-py-plugins` package, including:

* Front-matter
* Footnotes
* Definition lists
* Task lists
* Heading anchors
* LaTeX math
* Containers
* Word count

For full information see: <https://mdit-py-plugins.readthedocs.io>

Or you can write them yourself!

They can be chained and loaded *via*:

```
from markdown_it import MarkdownIt
from mdit_py_plugins import plugin1, plugin2
md = MarkdownIt().use(plugin1, keyword=value).use(plugin2, keyword=value)
html_string = md.render("some *Markdown*")
```
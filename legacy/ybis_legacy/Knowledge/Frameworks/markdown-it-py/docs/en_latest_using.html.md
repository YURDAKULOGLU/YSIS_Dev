Using markdown\_it — markdown-it-py



[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

[![markdown-it-py - Home](_static/markdown-it-py.svg)](index.html)

* [Repository](https://github.com/executablebooks/markdown-it-py "Source repository")
* [Suggest edit](https://github.com/executablebooks/markdown-it-py/edit/master/docs/using.md "Suggest edit")

* [.md](_sources/using.md "Download source file")
* .pdf

# Using markdown\_it

## Contents

# Using `markdown_it`[#](#using-markdown-it "Link to this heading")

> This document can be opened to execute with [Jupytext](https://jupytext.readthedocs.io)!

markdown-it-py may be used as an API *via* the [`markdown-it-py`](https://pypi.org/project/markdown-it-py/) package.

The raw text is first parsed to syntax ‘tokens’,
then these are converted to other formats using ‘renderers’.

## Quick-Start[#](#quick-start "Link to this heading")

The simplest way to understand how text will be parsed is using:

```
from pprint import pprint
from markdown_it import MarkdownIt
```

```
md = MarkdownIt()
md.render("some *text*")
```

```
'<p>some <em>text</em></p>\n'
```

```
for token in md.parse("some *text*"):
    print(token)
    print()
```

```
Token(type='paragraph_open', tag='p', nesting=1, attrs={}, map=[0, 1], level=0, children=None, content='', markup='', info='', meta={}, block=True, hidden=False)

Token(type='inline', tag='', nesting=0, attrs={}, map=[0, 1], level=1, children=[Token(type='text', tag='', nesting=0, attrs={}, map=None, level=0, children=None, content='some ', markup='', info='', meta={}, block=False, hidden=False), Token(type='em_open', tag='em', nesting=1, attrs={}, map=None, level=0, children=None, content='', markup='*', info='', meta={}, block=False, hidden=False), Token(type='text', tag='', nesting=0, attrs={}, map=None, level=1, children=None, content='text', markup='', info='', meta={}, block=False, hidden=False), Token(type='em_close', tag='em', nesting=-1, attrs={}, map=None, level=0, children=None, content='', markup='*', info='', meta={}, block=False, hidden=False)], content='some *text*', markup='', info='', meta={}, block=True, hidden=False)

Token(type='paragraph_close', tag='p', nesting=-1, attrs={}, map=None, level=0, children=None, content='', markup='', info='', meta={}, block=True, hidden=False)
```

## The Parser[#](#the-parser "Link to this heading")

The `MarkdownIt` class is instantiated with parsing configuration options,
dictating the syntax rules and additional options for the parser and renderer.
You can define this configuration *via* directly supplying a dictionary or a preset name:

* `zero`: This configures the minimum components to parse text (i.e. just paragraphs and text)
* `commonmark` (default): This configures the parser to strictly comply with the [CommonMark specification](http://spec.commonmark.org/).
* `js-default`: This is the default in the JavaScript version.
  Compared to `commonmark`, it disables HTML parsing and enables the table and strikethrough components.
* `gfm-like`: This configures the parser to approximately comply with the [GitHub Flavored Markdown specification](https://github.github.com/gfm/).
  Compared to `commonmark`, it enables the table, strikethrough and linkify components.
  **Important**, to use this configuration you must have `linkify-it-py` installed.

```
from markdown_it.presets import zero
zero.make()
```

```
{'options': {'maxNesting': 20,
  'html': False,
  'linkify': False,
  'typographer': False,
  'quotes': '“”‘’',
  'xhtmlOut': False,
  'breaks': False,
  'langPrefix': 'language-',
  'highlight': None},
 'components': {'core': {'rules': ['normalize',
    'block',
    'inline',
    'text_join']},
  'block': {'rules': ['paragraph']},
  'inline': {'rules': ['text'],
   'rules2': ['balance_pairs', 'fragments_join']}}}
```

```
md = MarkdownIt("zero")
md.options
```

```
{'maxNesting': 20, 'html': False, 'linkify': False, 'typographer': False, 'quotes': '“”‘’', 'xhtmlOut': False, 'breaks': False, 'langPrefix': 'language-', 'highlight': None}
```

You can also override specific options:

```
md = MarkdownIt("zero", {"maxNesting": 99})
md.options
```

```
{'maxNesting': 99, 'html': False, 'linkify': False, 'typographer': False, 'quotes': '“”‘’', 'xhtmlOut': False, 'breaks': False, 'langPrefix': 'language-', 'highlight': None}
```

```
pprint(md.get_active_rules())
```

```
{'block': ['paragraph'],
 'core': ['normalize', 'block', 'inline', 'text_join'],
 'inline': ['text'],
 'inline2': ['balance_pairs', 'fragments_join']}
```

You can find all the parsing rules in the source code:
`parser_core.py`, `parser_block.py`,
`parser_inline.py`.

```
pprint(md.get_all_rules())
```

```
{'block': ['table',
           'code',
           'fence',
           'blockquote',
           'hr',
           'list',
           'reference',
           'html_block',
           'heading',
           'lheading',
           'paragraph'],
 'core': ['normalize',
          'block',
          'inline',
          'linkify',
          'replacements',
          'smartquotes',
          'text_join'],
 'inline': ['text',
            'linkify',
            'newline',
            'escape',
            'backticks',
            'strikethrough',
            'emphasis',
            'link',
            'image',
            'autolink',
            'html_inline',
            'entity'],
 'inline2': ['balance_pairs', 'strikethrough', 'emphasis', 'fragments_join']}
```

Any of the parsing rules can be enabled/disabled, and these methods are “chainable”:

```
md.render("- __*emphasise this*__")
```

```
'<p>- __*emphasise this*__</p>\n'
```

```
md.enable(["list", "emphasis"]).render("- __*emphasise this*__")
```

```
'<ul>\n<li><strong><em>emphasise this</em></strong></li>\n</ul>\n'
```

You can temporarily modify rules with the `reset_rules` context manager.

```
with md.reset_rules():
    md.disable("emphasis")
    print(md.render("__*emphasise this*__"))
md.render("__*emphasise this*__")
```

```
<p>__*emphasise this*__</p>
```

```
'<p><strong><em>emphasise this</em></strong></p>\n'
```

Additionally `renderInline` runs the parser with all block syntax rules disabled.

```
md.renderInline("__*emphasise this*__")
```

```
'<strong><em>emphasise this</em></strong>'
```

### Typographic components[#](#typographic-components "Link to this heading")

The `smartquotes` and `replacements` components are intended to improve typography:

`smartquotes` will convert basic quote marks to their opening and closing variants:

* ‘single quotes’ -> ‘single quotes’
* “double quotes” -> “double quotes”

`replacements` will replace particular text constructs:

* `(c)`, `(C)` → ©
* `(tm)`, `(TM)` → ™
* `(r)`, `(R)` → ®
* `(p)`, `(P)` → §
* `+-` → ±
* `...` → …
* `?....` → ?..
* `!....` → !..
* `????????` → ???
* `!!!!!` → !!!
* `,,,` → ,
* `--` → &ndash
* `---` → &mdash

Both of these components require typography to be turned on, as well as the components enabled:

```
md = MarkdownIt("commonmark", {"typographer": True})
md.enable(["replacements", "smartquotes"])
md.render("'single quotes' (c)")
```

```
'<p>‘single quotes’ ©</p>\n'
```

### Linkify[#](#linkify "Link to this heading")

The `linkify` component requires that [linkify-it-py](https://github.com/tsutsu3/linkify-it-py) be installed (e.g. *via* `pip install markdown-it-py[linkify]`).
This allows URI autolinks to be identified, without the need for enclosing in `<>` brackets:

```
md = MarkdownIt("commonmark", {"linkify": True})
md.enable(["linkify"])
md.render("github.com")
```

```
'<p><a href="http://github.com">github.com</a></p>\n'
```

### Plugins load[#](#plugins-load "Link to this heading")

Plugins load collections of additional syntax rules and render methods into the parser.
A number of useful plugins are available in [`mdit_py_plugins`](https://github.com/executablebooks/mdit-py-plugins) (see [the plugin list](plugins.html)),
or you can create your own (following the [markdown-it design principles](architecture.html)).

```
from markdown_it import MarkdownIt
import mdit_py_plugins
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin

md = (
    MarkdownIt()
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .enable('table')
)
text = ("""\
---
a: 1
---

a | b
- | -
1 | 2

A footnote [^1]

[^1]: some details
""")
print(md.render(text))
```

```
<p>a | b</p>
<ul>
<li>| -
1 | 2</li>
</ul>
<p>A footnote <sup class="footnote-ref"><a href="#fn1" id="fnref1">[1]</a></sup></p>
<hr class="footnotes-sep" />
<section class="footnotes">
<ol class="footnotes-list">
<li id="fn1" class="footnote-item"><p>some details <a href="#fnref1" class="footnote-backref">↩︎</a></p>
</li>
</ol>
</section>
```

## The Token Stream[#](#the-token-stream "Link to this heading")

Before rendering, the text is parsed to a flat token stream of block level syntax elements, with nesting defined by opening (1) and closing (-1) attributes:

```
md = MarkdownIt("commonmark")
tokens = md.parse("""
Here's some *text*

1. a list

> a *quote*""")
[(t.type, t.nesting) for t in tokens]
```

```
[('paragraph_open', 1),
 ('inline', 0),
 ('paragraph_close', -1),
 ('ordered_list_open', 1),
 ('list_item_open', 1),
 ('paragraph_open', 1),
 ('inline', 0),
 ('paragraph_close', -1),
 ('list_item_close', -1),
 ('ordered_list_close', -1),
 ('blockquote_open', 1),
 ('paragraph_open', 1),
 ('inline', 0),
 ('paragraph_close', -1),
 ('blockquote_close', -1)]
```

Naturally all openings should eventually be closed,
such that:

```
sum([t.nesting for t in tokens]) == 0
```

```
True
```

All tokens are the same class, which can also be created outside the parser:

```
tokens[0]
```

```
Token(type='paragraph_open', tag='p', nesting=1, attrs={}, map=[1, 2], level=0, children=None, content='', markup='', info='', meta={}, block=True, hidden=False)
```

```
from markdown_it.token import Token
token = Token("paragraph_open", "p", 1, block=True, map=[1, 2])
token == tokens[0]
```

```
True
```

The `'inline'` type token contain the inline tokens as children:

```
tokens[1]
```

```
Token(type='inline', tag='', nesting=0, attrs={}, map=[1, 2], level=1, children=[Token(type='text', tag='', nesting=0, attrs={}, map=None, level=0, children=None, content="Here's some ", markup='', info='', meta={}, block=False, hidden=False), Token(type='em_open', tag='em', nesting=1, attrs={}, map=None, level=0, children=None, content='', markup='*', info='', meta={}, block=False, hidden=False), Token(type='text', tag='', nesting=0, attrs={}, map=None, level=1, children=None, content='text', markup='', info='', meta={}, block=False, hidden=False), Token(type='em_close', tag='em', nesting=-1, attrs={}, map=None, level=0, children=None, content='', markup='*', info='', meta={}, block=False, hidden=False)], content="Here's some *text*", markup='', info='', meta={}, block=True, hidden=False)
```

You can serialize a token (and its children) to a JSONable dictionary using:

```
print(tokens[1].as_dict())
```

```
{'type': 'inline', 'tag': '', 'nesting': 0, 'attrs': None, 'map': [1, 2], 'level': 1, 'children': [{'type': 'text', 'tag': '', 'nesting': 0, 'attrs': None, 'map': None, 'level': 0, 'children': None, 'content': "Here's some ", 'markup': '', 'info': '', 'meta': {}, 'block': False, 'hidden': False}, {'type': 'em_open', 'tag': 'em', 'nesting': 1, 'attrs': None, 'map': None, 'level': 0, 'children': None, 'content': '', 'markup': '*', 'info': '', 'meta': {}, 'block': False, 'hidden': False}, {'type': 'text', 'tag': '', 'nesting': 0, 'attrs': None, 'map': None, 'level': 1, 'children': None, 'content': 'text', 'markup': '', 'info': '', 'meta': {}, 'block': False, 'hidden': False}, {'type': 'em_close', 'tag': 'em', 'nesting': -1, 'attrs': None, 'map': None, 'level': 0, 'children': None, 'content': '', 'markup': '*', 'info': '', 'meta': {}, 'block': False, 'hidden': False}], 'content': "Here's some *text*", 'markup': '', 'info': '', 'meta': {}, 'block': True, 'hidden': False}
```

This dictionary can also be deserialized:

```
Token.from_dict(tokens[1].as_dict())
```

```
Token(type='inline', tag='', nesting=0, attrs={}, map=[1, 2], level=1, children=[Token(type='text', tag='', nesting=0, attrs={}, map=None, level=0, children=None, content="Here's some ", markup='', info='', meta={}, block=False, hidden=False), Token(type='em_open', tag='em', nesting=1, attrs={}, map=None, level=0, children=None, content='', markup='*', info='', meta={}, block=False, hidden=False), Token(type='text', tag='', nesting=0, attrs={}, map=None, level=1, children=None, content='text', markup='', info='', meta={}, block=False, hidden=False), Token(type='em_close', tag='em', nesting=-1, attrs={}, map=None, level=0, children=None, content='', markup='*', info='', meta={}, block=False, hidden=False)], content="Here's some *text*", markup='', info='', meta={}, block=True, hidden=False)
```

### Creating a syntax tree[#](#creating-a-syntax-tree "Link to this heading")

Changed in version 0.7.0: `nest_tokens` and `NestedTokens` are deprecated and replaced by `SyntaxTreeNode`.

In some use cases it may be useful to convert the token stream into a syntax tree,
with opening/closing tokens collapsed into a single token that contains children.

```
from markdown_it.tree import SyntaxTreeNode

md = MarkdownIt("commonmark")
tokens = md.parse("""
# Header

Here's some text and an image ![title](image.png)

1. a **list**

> a *quote*
""")

node = SyntaxTreeNode(tokens)
print(node.pretty(indent=2, show_text=True))
```

```
<root>
  <heading>
    <inline>
      <text>
        Header
  <paragraph>
    <inline>
      <text>
        Here's some text and an image 
      <image src='image.png' alt=''>
        <text>
          title
  <ordered_list>
    <list_item>
      <paragraph>
        <inline>
          <text>
            a 
          <strong>
            <text>
              list
          <text>
  <blockquote>
    <paragraph>
      <inline>
        <text>
          a 
        <em>
          <text>
            quote
```

You can then use methods to traverse the tree

```
node.children
```

```
[SyntaxTreeNode(heading),
 SyntaxTreeNode(paragraph),
 SyntaxTreeNode(ordered_list),
 SyntaxTreeNode(blockquote)]
```

```
print(node[0])
node[0].next_sibling
```

```
SyntaxTreeNode(heading)
```

```
SyntaxTreeNode(paragraph)
```

## Renderers[#](#renderers "Link to this heading")

After the token stream is generated, it’s passed to a [renderer](https://github.com/executablebooks/markdown-it-py/tree/master/markdown_it/renderer.py).
It then plays all the tokens, passing each to a rule with the same name as token type.

Renderer rules are located in `md.renderer.rules` and are simple functions
with the same signature:

```
def function(renderer, tokens, idx, options, env):
  return htmlResult
```

You can inject render methods into the instantiated render class.

```
md = MarkdownIt("commonmark")

def render_em_open(self, tokens, idx, options, env):
    return '<em class="myclass">'

md.add_render_rule("em_open", render_em_open)
md.render("*a*")
```

```
'<p><em class="myclass">a</em></p>\n'
```

This is a slight change to the JS version, where the renderer argument is at the end.
Also `add_render_rule` method is specific to Python, rather than adding directly to the `md.renderer.rules`, this ensures the method is bound to the renderer.

You can also subclass a render and add the method there:

```
from markdown_it.renderer import RendererHTML

class MyRenderer(RendererHTML):
    def em_open(self, tokens, idx, options, env):
        return '<em class="myclass">'

md = MarkdownIt("commonmark", renderer_cls=MyRenderer)
md.render("*a*")
```

```
'<p><em class="myclass">a</em></p>\n'
```

Plugins can support multiple render types, using the `__output__` attribute (this is currently a Python only feature).

```
from markdown_it.renderer import RendererHTML

class MyRenderer1(RendererHTML):
    __output__ = "html1"

class MyRenderer2(RendererHTML):
    __output__ = "html2"

def plugin(md):
    def render_em_open1(self, tokens, idx, options, env):
        return '<em class="myclass1">'
    def render_em_open2(self, tokens, idx, options, env):
        return '<em class="myclass2">'
    md.add_render_rule("em_open", render_em_open1, fmt="html1")
    md.add_render_rule("em_open", render_em_open2, fmt="html2")

md = MarkdownIt("commonmark", renderer_cls=MyRenderer1).use(plugin)
print(md.render("*a*"))

md = MarkdownIt("commonmark", renderer_cls=MyRenderer2).use(plugin)
print(md.render("*a*"))
```

```
<p><em class="myclass1">a</em></p>

<p><em class="myclass2">a</em></p>
```

Here’s a more concrete example; let’s replace images with vimeo links to player’s iframe:

```
import re
from markdown_it import MarkdownIt

vimeoRE = re.compile(r'^https?:\/\/(www\.)?vimeo.com\/(\d+)($|\/)')

def render_vimeo(self, tokens, idx, options, env):
    token = tokens[idx]

    if vimeoRE.match(token.attrs["src"]):

        ident = vimeoRE.match(token.attrs["src"])[2]

        return ('<div class="embed-responsive embed-responsive-16by9">\n' +
               '  <iframe class="embed-responsive-item" src="//player.vimeo.com/video/' +
                ident + '"></iframe>\n' +
               '</div>\n')
    return self.image(tokens, idx, options, env)

md = MarkdownIt("commonmark")
md.add_render_rule("image", render_vimeo)
print(md.render("![](https://www.vimeo.com/123)"))
```

```
<p><div class="embed-responsive embed-responsive-16by9">
  <iframe class="embed-responsive-item" src="//player.vimeo.com/video/123"></iframe>
</div>
</p>
```

Here is another example, how to add `target="_blank"` to all links:

```
from markdown_it import MarkdownIt

def render_blank_link(self, tokens, idx, options, env):
    tokens[idx].attrSet("target", "_blank")

    # pass token to default renderer.
    return self.renderToken(tokens, idx, options, env)

md = MarkdownIt("commonmark")
md.add_render_rule("link_open", render_blank_link)
print(md.render("[a]\n\n[a]: b"))
```

```
<p><a href="b" target="_blank">a</a></p>
```

### Markdown renderer[#](#markdown-renderer "Link to this heading")

You can also render a token stream directly to markdown via the `MDRenderer` class from [`mdformat`](https://github.com/executablebooks/mdformat):

```
from markdown_it import MarkdownIt
from mdformat.renderer import MDRenderer

md = MarkdownIt("commonmark")

source_markdown = """
Here's some *text*

1. a list

> a *quote*"""

tokens = md.parse(source_markdown)

renderer = MDRenderer()
options = {}
env = {}

output_markdown = renderer.render(tokens, options, env)
```

Contents
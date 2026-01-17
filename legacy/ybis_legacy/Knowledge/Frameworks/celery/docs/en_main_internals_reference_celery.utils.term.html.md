celery.utils.term — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.time.html "celery.utils.time") |
* [previous](celery.utils.objects.html "celery.utils.objects") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.term`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.term.html).

# `celery.utils.term`[¶](#celery-utils-term "Link to this heading")

Terminals and colors.

*class* celery.utils.term.colored(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../../_modules/celery/utils/term.html#colored)[¶](#celery.utils.term.colored "Link to this definition")
:   Terminal colored text.

    Example

    ```
    >>> c = colored(enabled=True)
    >>> print(str(c.red('the quick '), c.blue('brown ', c.bold('fox ')),
    ...       c.magenta(c.underline('jumps over')),
    ...       c.yellow(' the lazy '),
    ...       c.green('dog ')))
    ```

    black(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.black)[¶](#celery.utils.term.colored.black "Link to this definition")

    blink(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.blink)[¶](#celery.utils.term.colored.blink "Link to this definition")

    blue(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.blue)[¶](#celery.utils.term.colored.blue "Link to this definition")

    bold(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.bold)[¶](#celery.utils.term.colored.bold "Link to this definition")

    bright(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.bright)[¶](#celery.utils.term.colored.bright "Link to this definition")

    cyan(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.cyan)[¶](#celery.utils.term.colored.cyan "Link to this definition")

    embed() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/term.html#colored.embed)[¶](#celery.utils.term.colored.embed "Link to this definition")

    green(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.green)[¶](#celery.utils.term.colored.green "Link to this definition")

    iblue(*\*s: [colored](#celery.utils.term.colored "celery.utils.term.colored")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.iblue)[¶](#celery.utils.term.colored.iblue "Link to this definition")

    icyan(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.icyan)[¶](#celery.utils.term.colored.icyan "Link to this definition")

    igreen(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.igreen)[¶](#celery.utils.term.colored.igreen "Link to this definition")

    imagenta(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.imagenta)[¶](#celery.utils.term.colored.imagenta "Link to this definition")

    ired(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.ired)[¶](#celery.utils.term.colored.ired "Link to this definition")

    iwhite(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.iwhite)[¶](#celery.utils.term.colored.iwhite "Link to this definition")

    iyellow(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.iyellow)[¶](#celery.utils.term.colored.iyellow "Link to this definition")

    magenta(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.magenta)[¶](#celery.utils.term.colored.magenta "Link to this definition")

    no\_color() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/term.html#colored.no_color)[¶](#celery.utils.term.colored.no_color "Link to this definition")

    node(*s: [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)"), ...]*, *op: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.node)[¶](#celery.utils.term.colored.node "Link to this definition")

    red(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.red)[¶](#celery.utils.term.colored.red "Link to this definition")

    reset(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.reset)[¶](#celery.utils.term.colored.reset "Link to this definition")

    reverse(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.reverse)[¶](#celery.utils.term.colored.reverse "Link to this definition")

    underline(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.underline)[¶](#celery.utils.term.colored.underline "Link to this definition")

    white(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.white)[¶](#celery.utils.term.colored.white "Link to this definition")

    yellow(*\*s: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*) → [colored](#celery.utils.term.colored "celery.utils.term.colored")[[source]](../../_modules/celery/utils/term.html#colored.yellow)[¶](#celery.utils.term.colored.yellow "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.utils.objects`](celery.utils.objects.html "previous chapter")

#### Next topic

[`celery.utils.time`](celery.utils.time.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.term.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.time.html "celery.utils.time") |
* [previous](celery.utils.objects.html "celery.utils.objects") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.term`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
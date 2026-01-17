celery.utils.debug — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.exceptions.html "celery.exceptions") |
* [previous](celery.security.html "celery.security") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.utils.debug`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.utils.debug.html).

# `celery.utils.debug`[¶](#celery-utils-debug "Link to this heading")

## [Sampling Memory Usage](#id1)[¶](#sampling-memory-usage "Link to this heading")

This module can be used to diagnose and sample the memory usage
used by parts of your application.

For example, to sample the memory usage of calling tasks you can do this:

```
from celery.utils.debug import sample_mem, memdump

from tasks import add


try:
    for i in range(100):
        for j in range(100):
            add.delay(i, j)
        sample_mem()
finally:
    memdump()
```

## [API Reference](#id2)[¶](#module-celery.utils.debug "Link to this heading")

Utilities for debugging memory usage, blocking calls, etc.

celery.utils.debug.sample\_mem()[[source]](../_modules/celery/utils/debug.html#sample_mem)[¶](#celery.utils.debug.sample_mem "Link to this definition")
:   Sample RSS memory usage.

    Statistics can then be output by calling [`memdump()`](#celery.utils.debug.memdump "celery.utils.debug.memdump").

celery.utils.debug.memdump(*samples=10*, *file=None*)[[source]](../_modules/celery/utils/debug.html#memdump)[¶](#celery.utils.debug.memdump "Link to this definition")
:   Dump memory statistics.

    Will print a sample of all RSS memory samples added by
    calling [`sample_mem()`](#celery.utils.debug.sample_mem "celery.utils.debug.sample_mem"), and in addition print
    used RSS memory after [`gc.collect()`](https://docs.python.org/dev/library/gc.html#gc.collect "(in Python v3.15)").

celery.utils.debug.sample(*x*, *n*, *k=0*)[[source]](../_modules/celery/utils/debug.html#sample)[¶](#celery.utils.debug.sample "Link to this definition")
:   Given a list x a sample of length `n` of that list is returned.

    For example, if n is 10, and x has 100 items, a list of every tenth.
    item is returned.

    `k` can be used as offset.

celery.utils.debug.mem\_rss()[[source]](../_modules/celery/utils/debug.html#mem_rss)[¶](#celery.utils.debug.mem_rss "Link to this definition")
:   Return RSS memory usage as a humanized string.

celery.utils.debug.ps()[[source]](../_modules/celery/utils/debug.html#ps)[¶](#celery.utils.debug.ps "Link to this definition")
:   Return the global `psutil.Process` instance.

    Note

    Returns `None` if <https://pypi.org/project/psutil/> is not installed.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.security`](celery.security.html "previous chapter")

#### Next topic

[`celery.exceptions`](celery.exceptions.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.utils.debug.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.exceptions.html "celery.exceptions") |
* [previous](celery.security.html "celery.security") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.utils.debug`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
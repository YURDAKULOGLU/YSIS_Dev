celery.utils.saferepr — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.serialization.html "celery.utils.serialization") |
* [previous](celery.utils.iso8601.html "celery.utils.iso8601") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.saferepr`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.saferepr.html).

# `celery.utils.saferepr`[¶](#celery-utils-saferepr "Link to this heading")

Streaming, truncating, non-recursive version of [`repr()`](https://docs.python.org/dev/library/functions.html#repr "(in Python v3.15)").

Differences from regular [`repr()`](https://docs.python.org/dev/library/functions.html#repr "(in Python v3.15)"):

* Sets are represented the Python 3 way: `{1, 2}` vs `set([1, 2])`.
* Unicode strings does not have the `u'` prefix, even on Python 2.
* Empty set formatted as `set()` (Python 3), not `set([])` (Python 2).
* Longs don’t have the `L` suffix.

Very slow with no limits, super quick with limits.

celery.utils.saferepr.reprstream(*stack: ~collections.deque*, *seen: ~typing.Set | None = None*, *maxlevels: int = 3*, *level: int = 0*, *isinstance: ~typing.Callable = <built-in function isinstance>*) → [Iterator](https://docs.python.org/dev/library/typing.html#typing.Iterator "(in Python v3.15)")[[Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")][[source]](../../_modules/celery/utils/saferepr.html#reprstream)[¶](#celery.utils.saferepr.reprstream "Link to this definition")
:   Streaming repr, yielding tokens.

celery.utils.saferepr.saferepr(*o: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *maxlen: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *maxlevels: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 3*, *seen: [Set](https://docs.python.org/dev/library/typing.html#typing.Set "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/saferepr.html#saferepr)[¶](#celery.utils.saferepr.saferepr "Link to this definition")
:   Safe version of [`repr()`](https://docs.python.org/dev/library/functions.html#repr "(in Python v3.15)").

    Warning

    Make sure you set the maxlen argument, or it will be very slow
    for recursive objects. With the maxlen set, it’s often faster
    than built-in repr.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.utils.iso8601`](celery.utils.iso8601.html "previous chapter")

#### Next topic

[`celery.utils.serialization`](celery.utils.serialization.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.saferepr.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.serialization.html "celery.utils.serialization") |
* [previous](celery.utils.iso8601.html "celery.utils.iso8601") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.saferepr`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
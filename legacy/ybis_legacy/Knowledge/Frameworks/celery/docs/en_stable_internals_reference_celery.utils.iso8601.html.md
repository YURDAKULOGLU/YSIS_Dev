celery.utils.iso8601 — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.saferepr.html "celery.utils.saferepr") |
* [previous](celery.utils.time.html "celery.utils.time") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.iso8601`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.iso8601.html).

# `celery.utils.iso8601`[¶](#celery-utils-iso8601 "Link to this heading")

Parse ISO8601 dates.

Originally taken from <https://pypi.org/project/pyiso8601/>
(<https://bitbucket.org/micktwomey/pyiso8601>)

Modified to match the behavior of `dateutil.parser`:

> * raise [`ValueError`](https://docs.python.org/dev/library/exceptions.html#ValueError "(in Python v3.15)") instead of `ParseError`
> * return naive [`datetime`](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)") by default

This is the original License:

Copyright (c) 2007 Michael Twomey

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sub-license, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

celery.utils.iso8601.parse\_iso8601(*datestring: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [datetime](https://docs.python.org/dev/library/datetime.html#datetime.datetime "(in Python v3.15)")[[source]](../../_modules/celery/utils/iso8601.html#parse_iso8601)[¶](#celery.utils.iso8601.parse_iso8601 "Link to this definition")
:   Parse and convert ISO-8601 string to datetime.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.utils.time`](celery.utils.time.html "previous chapter")

#### Next topic

[`celery.utils.saferepr`](celery.utils.saferepr.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.iso8601.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.saferepr.html "celery.utils.saferepr") |
* [previous](celery.utils.time.html "celery.utils.time") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.iso8601`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
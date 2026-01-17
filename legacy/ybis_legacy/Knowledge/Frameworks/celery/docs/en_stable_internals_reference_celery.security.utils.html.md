celery.security.utils — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.events.snapshot.html "celery.events.snapshot") |
* [previous](celery.security.serialization.html "celery.security.serialization") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.security.utils`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.security.utils.html).

# `celery.security.utils`[¶](#celery-security-utils "Link to this heading")

Utilities used by the message signing serializer.

celery.security.utils.get\_digest\_algorithm(*digest='sha256'*)[[source]](../../_modules/celery/security/utils.html#get_digest_algorithm)[¶](#celery.security.utils.get_digest_algorithm "Link to this definition")
:   Convert string to hash object of cryptography library.

celery.security.utils.reraise\_errors(*msg='{0!r}'*, *errors=None*)[[source]](../../_modules/celery/security/utils.html#reraise_errors)[¶](#celery.security.utils.reraise_errors "Link to this definition")
:   Context reraising crypto errors as `SecurityError`.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.security.serialization`](celery.security.serialization.html "previous chapter")

#### Next topic

[`celery.events.snapshot`](celery.events.snapshot.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.security.utils.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.events.snapshot.html "celery.events.snapshot") |
* [previous](celery.security.serialization.html "celery.security.serialization") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.security.utils`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
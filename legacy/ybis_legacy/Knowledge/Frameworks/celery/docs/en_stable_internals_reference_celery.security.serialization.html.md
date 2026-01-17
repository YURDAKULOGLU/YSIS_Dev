celery.security.serialization — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.security.utils.html "celery.security.utils") |
* [previous](celery.security.key.html "celery.security.key") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.security.serialization`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.security.serialization.html).

# `celery.security.serialization`[¶](#celery-security-serialization "Link to this heading")

Secure serializer.

*class* celery.security.serialization.SecureSerializer(*key=None*, *cert=None*, *cert\_store=None*, *digest='sha256'*, *serializer='json'*)[[source]](../../_modules/celery/security/serialization.html#SecureSerializer)[¶](#celery.security.serialization.SecureSerializer "Link to this definition")
:   Signed serializer.

    deserialize(*data*)[[source]](../../_modules/celery/security/serialization.html#SecureSerializer.deserialize)[¶](#celery.security.serialization.SecureSerializer.deserialize "Link to this definition")
    :   Deserialize data structure from string.

    serialize(*data*)[[source]](../../_modules/celery/security/serialization.html#SecureSerializer.serialize)[¶](#celery.security.serialization.SecureSerializer.serialize "Link to this definition")
    :   Serialize data structure into string.

celery.security.serialization.register\_auth(*key=None*, *key\_password=None*, *cert=None*, *store=None*, *digest='sha256'*, *serializer='json'*)[[source]](../../_modules/celery/security/serialization.html#register_auth)[¶](#celery.security.serialization.register_auth "Link to this definition")
:   Register security serializer.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.security.key`](celery.security.key.html "previous chapter")

#### Next topic

[`celery.security.utils`](celery.security.utils.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.security.serialization.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.security.utils.html "celery.security.utils") |
* [previous](celery.security.key.html "celery.security.key") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.security.serialization`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
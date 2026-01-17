celery.utils.deprecated — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.functional.html "celery.utils.functional") |
* [previous](celery.utils.nodenames.html "celery.utils.nodenames") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.deprecated`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.deprecated.html).

# `celery.utils.deprecated`[¶](#celery-utils-deprecated "Link to this heading")

Deprecation utilities.

celery.utils.deprecated.Callable(*deprecation=None*, *removal=None*, *alternative=None*, *description=None*)[[source]](../../_modules/celery/utils/deprecated.html#Callable)[¶](#celery.utils.deprecated.Callable "Link to this definition")
:   Decorator for deprecated functions.

    A deprecation warning will be emitted when the function is called.

    Parameters:
    :   * **deprecation** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Version that marks first deprecation, if this
          argument isn’t set a `PendingDeprecationWarning` will be
          emitted instead.
        * **removal** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Future version when this feature will be removed.
        * **alternative** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Instructions for an alternative solution (if any).
        * **description** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Description of what’s being deprecated.

celery.utils.deprecated.Property(*deprecation=None*, *removal=None*, *alternative=None*, *description=None*)[[source]](../../_modules/celery/utils/deprecated.html#Property)[¶](#celery.utils.deprecated.Property "Link to this definition")
:   Decorator for deprecated properties.

celery.utils.deprecated.warn(*description=None*, *deprecation=None*, *removal=None*, *alternative=None*, *stacklevel=2*)[[source]](../../_modules/celery/utils/deprecated.html#warn)[¶](#celery.utils.deprecated.warn "Link to this definition")
:   Warn of (pending) deprecation.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.utils.nodenames`](celery.utils.nodenames.html "previous chapter")

#### Next topic

[`celery.utils.functional`](celery.utils.functional.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.deprecated.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.functional.html "celery.utils.functional") |
* [previous](celery.utils.nodenames.html "celery.utils.nodenames") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.deprecated`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
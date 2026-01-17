celery.utils.serialization — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.sysinfo.html "celery.utils.sysinfo") |
* [previous](celery.utils.saferepr.html "celery.utils.saferepr") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.serialization`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.serialization.html).

# `celery.utils.serialization`[¶](#celery-utils-serialization "Link to this heading")

Utilities for safely pickling exceptions.

*exception* celery.utils.serialization.UnpickleableExceptionWrapper(*exc\_module*, *exc\_cls\_name*, *exc\_args*, *text=None*)[[source]](../../_modules/celery/utils/serialization.html#UnpickleableExceptionWrapper)[¶](#celery.utils.serialization.UnpickleableExceptionWrapper "Link to this definition")
:   Wraps unpickleable exceptions.

    Parameters:
    :   * **exc\_module** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – See [`exc_module`](#celery.utils.serialization.UnpickleableExceptionWrapper.exc_module "celery.utils.serialization.UnpickleableExceptionWrapper.exc_module").
        * **exc\_cls\_name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – See [`exc_cls_name`](#celery.utils.serialization.UnpickleableExceptionWrapper.exc_cls_name "celery.utils.serialization.UnpickleableExceptionWrapper.exc_cls_name").
        * **exc\_args** (*Tuple**[**Any**,* *...**]*) – See [`exc_args`](#celery.utils.serialization.UnpickleableExceptionWrapper.exc_args "celery.utils.serialization.UnpickleableExceptionWrapper.exc_args").

    Example

    ```
    >>> def pickle_it(raising_function):
    ...     try:
    ...         raising_function()
    ...     except Exception as e:
    ...         exc = UnpickleableExceptionWrapper(
    ...             e.__class__.__module__,
    ...             e.__class__.__name__,
    ...             e.args,
    ...         )
    ...         pickle.dumps(exc)  # Works fine.
    ```

    exc\_args *= None*[¶](#celery.utils.serialization.UnpickleableExceptionWrapper.exc_args "Link to this definition")
    :   The arguments for the original exception.

    exc\_cls\_name *= None*[¶](#celery.utils.serialization.UnpickleableExceptionWrapper.exc_cls_name "Link to this definition")
    :   The name of the original exception class.

    exc\_module *= None*[¶](#celery.utils.serialization.UnpickleableExceptionWrapper.exc_module "Link to this definition")
    :   The module of the original exception.

    *classmethod* from\_exception(*exc*)[[source]](../../_modules/celery/utils/serialization.html#UnpickleableExceptionWrapper.from_exception)[¶](#celery.utils.serialization.UnpickleableExceptionWrapper.from_exception "Link to this definition")

    restore()[[source]](../../_modules/celery/utils/serialization.html#UnpickleableExceptionWrapper.restore)[¶](#celery.utils.serialization.UnpickleableExceptionWrapper.restore "Link to this definition")

celery.utils.serialization.create\_exception\_cls(*name*, *module*, *parent=None*)[[source]](../../_modules/celery/utils/serialization.html#create_exception_cls)[¶](#celery.utils.serialization.create_exception_cls "Link to this definition")
:   Dynamically create an exception class.

celery.utils.serialization.find\_pickleable\_exception(*exc*, *loads=<built-in function loads>*, *dumps=<built-in function dumps>*)[[source]](../../_modules/celery/utils/serialization.html#find_pickleable_exception)[¶](#celery.utils.serialization.find_pickleable_exception "Link to this definition")
:   Find first pickleable exception base class.

    With an exception instance, iterate over its super classes (by MRO)
    and find the first super exception that’s pickleable. It does
    not go below [`Exception`](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)") (i.e., it skips [`Exception`](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)"),
    [`BaseException`](https://docs.python.org/dev/library/exceptions.html#BaseException "(in Python v3.15)") and [`object`](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")). If that happens
    you should use `UnpickleableException` instead.

    Parameters:
    :   * **exc** ([*BaseException*](https://docs.python.org/dev/library/exceptions.html#BaseException "(in Python v3.15)")) – An exception instance.
        * **loads** – decoder to use.
        * **dumps** – encoder to use

    Returns:
    :   Nearest pickleable parent exception class
        :   (except [`Exception`](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)") and parents), or if the exception is
            pickleable it will return `None`.

    Return type:
    :   [Exception](https://docs.python.org/dev/library/exceptions.html#Exception "(in Python v3.15)")

celery.utils.serialization.get\_pickleable\_etype(*cls*, *loads=<built-in function loads>*, *dumps=<built-in function dumps>*)[[source]](../../_modules/celery/utils/serialization.html#get_pickleable_etype)[¶](#celery.utils.serialization.get_pickleable_etype "Link to this definition")
:   Get pickleable exception type.

celery.utils.serialization.get\_pickleable\_exception(*exc*)[[source]](../../_modules/celery/utils/serialization.html#get_pickleable_exception)[¶](#celery.utils.serialization.get_pickleable_exception "Link to this definition")
:   Make sure exception is pickleable.

celery.utils.serialization.get\_pickled\_exception(*exc*)[[source]](../../_modules/celery/utils/serialization.html#get_pickled_exception)[¶](#celery.utils.serialization.get_pickled_exception "Link to this definition")
:   Reverse of [`get_pickleable_exception()`](#celery.utils.serialization.get_pickleable_exception "celery.utils.serialization.get_pickleable_exception").

celery.utils.serialization.strtobool(*term*, *table=None*)[[source]](../../_modules/celery/utils/serialization.html#strtobool)[¶](#celery.utils.serialization.strtobool "Link to this definition")
:   Convert common terms for true/false to bool.

    Examples (true/false/yes/no/on/off/1/0).

celery.utils.serialization.subclass\_exception(*name*, *parent*, *module*)[[source]](../../_modules/celery/utils/serialization.html#subclass_exception)[¶](#celery.utils.serialization.subclass_exception "Link to this definition")
:   Create new exception class.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.utils.saferepr`](celery.utils.saferepr.html "previous chapter")

#### Next topic

[`celery.utils.sysinfo`](celery.utils.sysinfo.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.serialization.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.sysinfo.html "celery.utils.sysinfo") |
* [previous](celery.utils.saferepr.html "celery.utils.saferepr") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.serialization`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
celery.contrib.testing.mocks — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.rdb.html "celery.contrib.rdb") |
* [previous](celery.contrib.testing.manager.html "celery.contrib.testing.manager") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.testing.mocks`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.mocks.html).

# `celery.contrib.testing.mocks`[¶](#celery-contrib-testing-mocks "Link to this heading")

## [API Reference](#id1)[¶](#module-celery.contrib.testing.mocks "Link to this heading")

Useful mocks for unit testing.

celery.contrib.testing.mocks.ContextMock(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/mocks.html#ContextMock)[¶](#celery.contrib.testing.mocks.ContextMock "Link to this definition")
:   Mock that mocks [`with`](https://docs.python.org/dev/reference/compound_stmts.html#with "(in Python v3.15)") statement contexts.

celery.contrib.testing.mocks.TaskMessage(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *id: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *args: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)") = ()*, *kwargs: [Mapping](https://docs.python.org/dev/library/typing.html#typing.Mapping "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *callbacks: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *errbacks: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *chain: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *shadow: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *utc: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *\*\*options: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/mocks.html#TaskMessage)[¶](#celery.contrib.testing.mocks.TaskMessage "Link to this definition")
:   Create task message in protocol 2 format.

celery.contrib.testing.mocks.TaskMessage1(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *id: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *args: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)") = ()*, *kwargs: [Mapping](https://docs.python.org/dev/library/typing.html#typing.Mapping "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *callbacks: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *errbacks: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *chain: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[Signature](celery.html#celery.Signature "celery.canvas.Signature")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *\*\*options: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/mocks.html#TaskMessage1)[¶](#celery.contrib.testing.mocks.TaskMessage1 "Link to this definition")
:   Create task message in protocol 1 format.

celery.contrib.testing.mocks.task\_message\_from\_sig(*app: ~celery.app.base.Celery*, *sig: ~celery.canvas.Signature*, *utc: bool = True*, *TaskMessage: ~typing.Any = <function TaskMessage>*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/mocks.html#task_message_from_sig)[¶](#celery.contrib.testing.mocks.task_message_from_sig "Link to this definition")
:   Create task message from [`celery.Signature`](celery.html#celery.Signature "celery.Signature").

    Example

    ```
    >>> m = task_message_from_sig(app, add.s(2, 2))
    >>> amqp_client.basic_publish(m, exchange='ex', routing_key='rkey')
    ```

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.contrib.testing.manager`](celery.contrib.testing.manager.html "previous chapter")

#### Next topic

[`celery.contrib.rdb`](celery.contrib.rdb.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.contrib.testing.mocks.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.rdb.html "celery.contrib.rdb") |
* [previous](celery.contrib.testing.manager.html "celery.contrib.testing.manager") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.testing.mocks`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
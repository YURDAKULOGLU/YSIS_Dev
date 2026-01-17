celery.contrib.testing.worker — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.testing.app.html "celery.contrib.testing.app") |
* [previous](celery.contrib.sphinx.html "celery.contrib.sphinx") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.testing.worker`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.worker.html).

# `celery.contrib.testing.worker`[¶](#celery-contrib-testing-worker "Link to this heading")

## [API Reference](#id1)[¶](#module-celery.contrib.testing.worker "Link to this heading")

Embedded workers for integration tests.

*class* celery.contrib.testing.worker.TestWorkController(*\*args: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*)[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController)[¶](#celery.contrib.testing.worker.TestWorkController "Link to this definition")
:   Worker that can synchronize on being fully started.

    *class* QueueHandler(*queue*)[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.QueueHandler)[¶](#celery.contrib.testing.worker.TestWorkController.QueueHandler "Link to this definition")
    :   handleError(*record*)[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.QueueHandler.handleError)[¶](#celery.contrib.testing.worker.TestWorkController.QueueHandler.handleError "Link to this definition")
        :   Handle errors which occur during an emit() call.

            This method should be called from handlers when an exception is
            encountered during an emit() call. If raiseExceptions is false,
            exceptions get silently ignored. This is what is mostly wanted
            for a logging system - most users will not care about errors in
            the logging system, they are more interested in application errors.
            You could, however, replace this with a custom handler if you wish.
            The record which was being processed is passed in to this method.

        prepare(*record*)[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.QueueHandler.prepare)[¶](#celery.contrib.testing.worker.TestWorkController.QueueHandler.prepare "Link to this definition")
        :   Prepares a record for queuing. The object returned by this method is
            enqueued.

            The base implementation formats the record to merge the message
            and arguments, and removes unpickleable items from the record
            in-place.

            You might want to override this method if you want to convert
            the record to a dict or JSON string, or send a modified copy
            of the record while leaving the original intact.

    ensure\_started() → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.ensure_started)[¶](#celery.contrib.testing.worker.TestWorkController.ensure_started "Link to this definition")
    :   Wait for worker to be fully up and running.

        Warning

        Worker must be started within a thread for this to work,
        or it will block forever.

    logger\_queue *= None*[¶](#celery.contrib.testing.worker.TestWorkController.logger_queue "Link to this definition")

    on\_consumer\_ready(*consumer: [Consumer](celery.worker.consumer.consumer.html#celery.worker.consumer.consumer.Consumer "celery.worker.consumer.consumer.Consumer")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.on_consumer_ready)[¶](#celery.contrib.testing.worker.TestWorkController.on_consumer_ready "Link to this definition")
    :   Callback called when the Consumer blueprint is fully started.

    start()[[source]](../_modules/celery/contrib/testing/worker.html#TestWorkController.start)[¶](#celery.contrib.testing.worker.TestWorkController.start "Link to this definition")

celery.contrib.testing.worker.setup\_app\_for\_worker(*app: [Celery](celery.html#celery.Celery "celery.app.base.Celery")*, *loglevel: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*, *logfile: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/worker.html#setup_app_for_worker)[¶](#celery.contrib.testing.worker.setup_app_for_worker "Link to this definition")
:   Setup the app to be used for starting an embedded worker.

celery.contrib.testing.worker.start\_worker(*app: [Celery](celery.html#celery.Celery "celery.app.base.Celery")*, *concurrency: [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 1*, *pool: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = 'solo'*, *loglevel: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)") = 'error'*, *logfile: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") = None*, *perform\_ping\_check: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*, *ping\_task\_timeout: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = 10.0*, *shutdown\_timeout: [float](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") = 10.0*, *\*\*kwargs: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Iterable](https://docs.python.org/dev/library/typing.html#typing.Iterable "(in Python v3.15)")[[source]](../_modules/celery/contrib/testing/worker.html#start_worker)[¶](#celery.contrib.testing.worker.start_worker "Link to this definition")
:   Start embedded worker.

    Yields:
    :   *celery.app.worker.Worker* – worker instance.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[celery.contrib.sphinx](celery.contrib.sphinx.html "previous chapter")

#### Next topic

[`celery.contrib.testing.app`](celery.contrib.testing.app.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.contrib.testing.worker.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.testing.app.html "celery.contrib.testing.app") |
* [previous](celery.contrib.sphinx.html "celery.contrib.sphinx") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.testing.worker`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
celery.app.trace — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.app.annotations.html "celery.app.annotations") |
* [previous](celery.backends.gcs.html "celery.backends.gcs") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.app.trace`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.app.trace.html).

# `celery.app.trace`[¶](#celery-app-trace "Link to this heading")

Trace task execution.

This module defines how the task execution is traced:
errors are recorded, handlers are applied and so on.

*class* celery.app.trace.TraceInfo(*state*, *retval=None*)[[source]](../../_modules/celery/app/trace.html#TraceInfo)[¶](#celery.app.trace.TraceInfo "Link to this definition")
:   Information about task execution.

    handle\_error\_state(*task*, *req*, *eager=False*, *call\_errbacks=True*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_error_state)[¶](#celery.app.trace.TraceInfo.handle_error_state "Link to this definition")

    handle\_failure(*task*, *req*, *store\_errors=True*, *call\_errbacks=True*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_failure)[¶](#celery.app.trace.TraceInfo.handle_failure "Link to this definition")
    :   Handle exception.

    handle\_ignore(*task*, *req*, *\*\*kwargs*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_ignore)[¶](#celery.app.trace.TraceInfo.handle_ignore "Link to this definition")

    handle\_reject(*task*, *req*, *\*\*kwargs*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_reject)[¶](#celery.app.trace.TraceInfo.handle_reject "Link to this definition")

    handle\_retry(*task*, *req*, *store\_errors=True*, *\*\*kwargs*)[[source]](../../_modules/celery/app/trace.html#TraceInfo.handle_retry)[¶](#celery.app.trace.TraceInfo.handle_retry "Link to this definition")
    :   Handle retry exception.

    retval[¶](#celery.app.trace.TraceInfo.retval "Link to this definition")

    state[¶](#celery.app.trace.TraceInfo.state "Link to this definition")

celery.app.trace.build\_tracer(*name*, *task*, *loader=None*, *hostname=None*, *store\_errors=True*, *Info=<class 'celery.app.trace.TraceInfo'>*, *eager=False*, *propagate=False*, *app=None*, *monotonic=<built-in function monotonic>*, *trace\_ok\_t=<class 'celery.app.trace.trace\_ok\_t'>*, *IGNORE\_STATES=frozenset({'IGNORED'*, *'REJECTED'*, *'RETRY'})*)[[source]](../../_modules/celery/app/trace.html#build_tracer)[¶](#celery.app.trace.build_tracer "Link to this definition")
:   Return a function that traces task execution.

    Catches all exceptions and updates result backend with the
    state and result.

    If the call was successful, it saves the result to the task result
    backend, and sets the task status to “SUCCESS”.

    If the call raises [`Retry`](../../reference/celery.exceptions.html#celery.exceptions.Retry "celery.exceptions.Retry"), it extracts
    the original exception, uses that as the result and sets the task state
    to “RETRY”.

    If the call results in an exception, it saves the exception as the task
    result, and sets the task state to “FAILURE”.

    Return a function that takes the following arguments:

    > param uuid:
    > :   The id of the task.
    >
    > param args:
    > :   List of positional args to pass on to the function.
    >
    > param kwargs:
    > :   Keyword arguments mapping to pass on to the function.
    >
    > keyword request:
    > :   Request dict.

celery.app.trace.reset\_worker\_optimizations(*app=<Celery default>*)[[source]](../../_modules/celery/app/trace.html#reset_worker_optimizations)[¶](#celery.app.trace.reset_worker_optimizations "Link to this definition")
:   Reset previously configured optimizations.

celery.app.trace.setup\_worker\_optimizations(*app*, *hostname=None*)[[source]](../../_modules/celery/app/trace.html#setup_worker_optimizations)[¶](#celery.app.trace.setup_worker_optimizations "Link to this definition")
:   Setup worker related optimizations.

celery.app.trace.trace\_task(*task*, *uuid*, *args*, *kwargs*, *request=None*, *\*\*opts*)[[source]](../../_modules/celery/app/trace.html#trace_task)[¶](#celery.app.trace.trace_task "Link to this definition")
:   Trace task execution.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.gcs`](celery.backends.gcs.html "previous chapter")

#### Next topic

[`celery.app.annotations`](celery.app.annotations.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.app.trace.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.app.annotations.html "celery.app.annotations") |
* [previous](celery.backends.gcs.html "celery.backends.gcs") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.app.trace`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
celery.\_state — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](../../history/index.html "History") |
* [previous](celery.platforms.html "celery.platforms") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery._state`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery._state.html).

# `celery._state`[¶](#celery-state "Link to this heading")

Internal state.

This is an internal module containing thread state
like the `current_app`, and `current_task`.

This module shouldn’t be used directly.

celery.\_state.connect\_on\_app\_finalize(*callback*)[[source]](../../_modules/celery/_state.html#connect_on_app_finalize)[¶](#celery._state.connect_on_app_finalize "Link to this definition")
:   Connect callback to be called when any app is finalized.

celery.\_state.current\_app *= <Celery default>*[¶](#celery._state.current_app "Link to this definition")
:   Proxy to current app.

celery.\_state.current\_task *= None*[¶](#celery._state.current_task "Link to this definition")
:   Proxy to current task.

celery.\_state.get\_current\_app()[[source]](../../_modules/celery/_state.html#get_current_app)[¶](#celery._state.get_current_app "Link to this definition")

celery.\_state.get\_current\_task()[[source]](../../_modules/celery/_state.html#get_current_task)[¶](#celery._state.get_current_task "Link to this definition")
:   Currently executing task.

celery.\_state.get\_current\_worker\_task()[[source]](../../_modules/celery/_state.html#get_current_worker_task)[¶](#celery._state.get_current_worker_task "Link to this definition")
:   Currently executing task, that was applied by the worker.

    This is used to differentiate between the actual task
    executed by the worker and any task that was called within
    a task (using `task.__call__` or `task.apply`)

celery.\_state.set\_default\_app(*app*)[[source]](../../_modules/celery/_state.html#set_default_app)[¶](#celery._state.set_default_app "Link to this definition")
:   Set default app.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.platforms`](celery.platforms.html "previous chapter")

#### Next topic

[History](../../history/index.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery._state.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](../../history/index.html "History") |
* [previous](celery.platforms.html "celery.platforms") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery._state`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
celery.backends.database — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.cache.html "celery.backends.cache") |
* [previous](celery.backends.rpc.html "celery.backends.rpc") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.database`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.database.html).

# `celery.backends.database`[¶](#celery-backends-database "Link to this heading")

SQLAlchemy result store backend.

*class* celery.backends.database.DatabaseBackend(*dburi=None*, *engine\_options=None*, *url=None*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/database.html#DatabaseBackend)[¶](#celery.backends.database.DatabaseBackend "Link to this definition")
:   The database result backend.

    ResultSession(*session\_manager=None*)[[source]](../../_modules/celery/backends/database.html#DatabaseBackend.ResultSession)[¶](#celery.backends.database.DatabaseBackend.ResultSession "Link to this definition")

    cleanup()[[source]](../../_modules/celery/backends/database.html#DatabaseBackend.cleanup)[¶](#celery.backends.database.DatabaseBackend.cleanup "Link to this definition")
    :   Delete expired meta-data.

    *property* extended\_result[¶](#celery.backends.database.DatabaseBackend.extended_result "Link to this definition")

    subpolling\_interval *= 0.5*[¶](#celery.backends.database.DatabaseBackend.subpolling_interval "Link to this definition")
    :   Time to sleep between polling each individual item
        in ResultSet.iterate. as opposed to the interval
        argument which is for each pass.

    task\_cls[¶](#celery.backends.database.DatabaseBackend.task_cls "Link to this definition")
    :   alias of [`Task`](celery.backends.database.models.html#celery.backends.database.models.Task "celery.backends.database.models.Task")

    taskset\_cls[¶](#celery.backends.database.DatabaseBackend.taskset_cls "Link to this definition")
    :   alias of [`TaskSet`](celery.backends.database.models.html#celery.backends.database.models.TaskSet "celery.backends.database.models.TaskSet")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.rpc`](celery.backends.rpc.html "previous chapter")

#### Next topic

[`celery.backends.cache`](celery.backends.cache.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.database.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.cache.html "celery.backends.cache") |
* [previous](celery.backends.rpc.html "celery.backends.rpc") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.database`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
celery.contrib.rdb — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.events.html "celery.events") |
* [previous](celery.contrib.testing.mocks.html "celery.contrib.testing.mocks") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.rdb`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.rdb.html).

# `celery.contrib.rdb`[¶](#module-celery.contrib.rdb "Link to this heading")

Remote Debugger.

## Introduction[¶](#introduction "Link to this heading")

This is a remote debugger for Celery tasks running in multiprocessing
pool workers. Inspired by a lost post on dzone.com.

### Usage[¶](#usage "Link to this heading")

```
from celery.contrib import rdb
from celery import task

@task()
def add(x, y):
    result = x + y
    rdb.set_trace()
    return result
```

## Environment Variables[¶](#environment-variables "Link to this heading")

CELERY\_RDB\_HOST[¶](#envvar-CELERY_RDB_HOST "Link to this definition")

### `CELERY_RDB_HOST`[¶](#celery-rdb-host "Link to this heading")

> Hostname to bind to. Default is ‘127.0.0.1’ (only accessible from
> localhost).

CELERY\_RDB\_PORT[¶](#envvar-CELERY_RDB_PORT "Link to this definition")

### `CELERY_RDB_PORT`[¶](#celery-rdb-port "Link to this heading")

> Base port to bind to. Default is 6899.
> The debugger will try to find an available port starting from the
> base port. The selected port will be logged by the worker.

celery.contrib.rdb.set\_trace(*frame=None*)[[source]](../_modules/celery/contrib/rdb.html#set_trace)[¶](#celery.contrib.rdb.set_trace "Link to this definition")
:   Set break-point at current location, or a specified frame.

celery.contrib.rdb.debugger()[[source]](../_modules/celery/contrib/rdb.html#debugger)[¶](#celery.contrib.rdb.debugger "Link to this definition")
:   Return the current debugger instance, or create if none.

*class* celery.contrib.rdb.Rdb(*host='127.0.0.1'*, *port=6899*, *port\_search\_limit=100*, *port\_skew=0*, *out=<\_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>*)[[source]](../_modules/celery/contrib/rdb.html#Rdb)[¶](#celery.contrib.rdb.Rdb "Link to this definition")
:   Remote debugger.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.contrib.testing.mocks`](celery.contrib.testing.mocks.html "previous chapter")

#### Next topic

[`celery.events`](celery.events.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.contrib.rdb.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.events.html "celery.events") |
* [previous](celery.contrib.testing.mocks.html "celery.contrib.testing.mocks") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.rdb`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
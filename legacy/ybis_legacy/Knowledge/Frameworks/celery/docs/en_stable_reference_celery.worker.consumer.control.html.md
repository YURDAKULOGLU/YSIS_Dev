celery.worker.consumer.control — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.events.html "celery.worker.consumer.events") |
* [previous](celery.worker.consumer.consumer.html "celery.worker.consumer.consumer") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.control`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.control.html).

# `celery.worker.consumer.control`[¶](#celery-worker-consumer-control "Link to this heading")

Worker Remote Control Bootstep.

`Control` -> [`celery.worker.pidbox`](../internals/reference/celery.worker.pidbox.html#module-celery.worker.pidbox "celery.worker.pidbox") -> [`kombu.pidbox`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.pidbox.html#module-kombu.pidbox "(in Kombu v5.6)").

The actual commands are implemented in [`celery.worker.control`](../internals/reference/celery.worker.control.html#module-celery.worker.control "celery.worker.control").

*class* celery.worker.consumer.control.Control(*c*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/control.html#Control)[¶](#celery.worker.consumer.control.Control "Link to this definition")
:   Remote control command service.

    include\_if(*c*)[[source]](../_modules/celery/worker/consumer/control.html#Control.include_if)[¶](#celery.worker.consumer.control.Control.include_if "Link to this definition")
    :   Return true if bootstep should be included.

        You can define this as an optional predicate that decides whether
        this step should be created.

    name *= 'celery.worker.consumer.control.Control'*[¶](#celery.worker.consumer.control.Control.name "Link to this definition")

    requires *= (step:celery.worker.consumer.tasks.Tasks{(step:celery.worker.consumer.mingle.Mingle{(step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)},)},)*[¶](#celery.worker.consumer.control.Control.requires "Link to this definition")

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.consumer.consumer`](celery.worker.consumer.consumer.html "previous chapter")

#### Next topic

[`celery.worker.consumer.events`](celery.worker.consumer.events.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.worker.consumer.control.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.events.html "celery.worker.consumer.events") |
* [previous](celery.worker.consumer.consumer.html "celery.worker.consumer.consumer") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.control`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
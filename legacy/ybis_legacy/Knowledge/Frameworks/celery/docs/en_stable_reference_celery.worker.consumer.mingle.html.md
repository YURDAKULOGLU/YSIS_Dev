celery.worker.consumer.mingle — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.tasks.html "celery.worker.consumer.tasks") |
* [previous](celery.worker.consumer.heart.html "celery.worker.consumer.heart") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.mingle`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.mingle.html).

# `celery.worker.consumer.mingle`[¶](#celery-worker-consumer-mingle "Link to this heading")

Worker <-> Worker Sync at startup (Bootstep).

*class* celery.worker.consumer.mingle.Mingle(*c*, *without\_mingle=False*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle)[¶](#celery.worker.consumer.mingle.Mingle "Link to this definition")
:   Bootstep syncing state with neighbor workers.

    At startup, or upon consumer restart, this will:

    * Sync logical clocks.
    * Sync revoked tasks.

    compatible\_transport(*app*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.compatible_transport)[¶](#celery.worker.consumer.mingle.Mingle.compatible_transport "Link to this definition")

    compatible\_transports *= {'amqp', 'gcpubsub', 'redis'}*[¶](#celery.worker.consumer.mingle.Mingle.compatible_transports "Link to this definition")

    label *= 'Mingle'*[¶](#celery.worker.consumer.mingle.Mingle.label "Link to this definition")

    name *= 'celery.worker.consumer.mingle.Mingle'*[¶](#celery.worker.consumer.mingle.Mingle.name "Link to this definition")

    on\_clock\_event(*c*, *clock*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.on_clock_event)[¶](#celery.worker.consumer.mingle.Mingle.on_clock_event "Link to this definition")

    on\_node\_reply(*c*, *nodename*, *reply*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.on_node_reply)[¶](#celery.worker.consumer.mingle.Mingle.on_node_reply "Link to this definition")

    on\_revoked\_received(*c*, *revoked*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.on_revoked_received)[¶](#celery.worker.consumer.mingle.Mingle.on_revoked_received "Link to this definition")

    requires *= (step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)*[¶](#celery.worker.consumer.mingle.Mingle.requires "Link to this definition")

    send\_hello(*c*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.send_hello)[¶](#celery.worker.consumer.mingle.Mingle.send_hello "Link to this definition")

    start(*c*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.start)[¶](#celery.worker.consumer.mingle.Mingle.start "Link to this definition")

    sync(*c*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.sync)[¶](#celery.worker.consumer.mingle.Mingle.sync "Link to this definition")

    sync\_with\_node(*c*, *clock=None*, *revoked=None*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/mingle.html#Mingle.sync_with_node)[¶](#celery.worker.consumer.mingle.Mingle.sync_with_node "Link to this definition")

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.consumer.heart`](celery.worker.consumer.heart.html "previous chapter")

#### Next topic

[`celery.worker.consumer.tasks`](celery.worker.consumer.tasks.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.worker.consumer.mingle.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.tasks.html "celery.worker.consumer.tasks") |
* [previous](celery.worker.consumer.heart.html "celery.worker.consumer.heart") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.mingle`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
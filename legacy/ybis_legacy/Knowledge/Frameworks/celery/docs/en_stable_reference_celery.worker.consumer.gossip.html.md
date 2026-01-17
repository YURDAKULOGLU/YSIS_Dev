celery.worker.consumer.gossip — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.heart.html "celery.worker.consumer.heart") |
* [previous](celery.worker.consumer.events.html "celery.worker.consumer.events") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.gossip`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.consumer.gossip.html).

# `celery.worker.consumer.gossip`[¶](#celery-worker-consumer-gossip "Link to this heading")

Worker <-> Worker communication Bootstep.

*class* celery.worker.consumer.gossip.Gossip(*c*, *without\_gossip=False*, *interval=5.0*, *heartbeat\_interval=2.0*, *\*\*kwargs*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip)[¶](#celery.worker.consumer.gossip.Gossip "Link to this definition")
:   Bootstep consuming events from other workers.

    This keeps the logical clock value up to date.

    call\_task(*task*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.call_task)[¶](#celery.worker.consumer.gossip.Gossip.call_task "Link to this definition")

    compatible\_transport(*app*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.compatible_transport)[¶](#celery.worker.consumer.gossip.Gossip.compatible_transport "Link to this definition")

    compatible\_transports *= {'amqp', 'redis'}*[¶](#celery.worker.consumer.gossip.Gossip.compatible_transports "Link to this definition")

    election(*id*, *topic*, *action=None*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.election)[¶](#celery.worker.consumer.gossip.Gossip.election "Link to this definition")

    get\_consumers(*channel*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.get_consumers)[¶](#celery.worker.consumer.gossip.Gossip.get_consumers "Link to this definition")

    label *= 'Gossip'*[¶](#celery.worker.consumer.gossip.Gossip.label "Link to this definition")

    name *= 'celery.worker.consumer.gossip.Gossip'*[¶](#celery.worker.consumer.gossip.Gossip.name "Link to this definition")

    on\_elect(*event*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_elect)[¶](#celery.worker.consumer.gossip.Gossip.on_elect "Link to this definition")

    on\_elect\_ack(*event*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_elect_ack)[¶](#celery.worker.consumer.gossip.Gossip.on_elect_ack "Link to this definition")

    on\_message(*prepare*, *message*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_message)[¶](#celery.worker.consumer.gossip.Gossip.on_message "Link to this definition")

    on\_node\_join(*worker*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_node_join)[¶](#celery.worker.consumer.gossip.Gossip.on_node_join "Link to this definition")

    on\_node\_leave(*worker*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_node_leave)[¶](#celery.worker.consumer.gossip.Gossip.on_node_leave "Link to this definition")

    on\_node\_lost(*worker*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.on_node_lost)[¶](#celery.worker.consumer.gossip.Gossip.on_node_lost "Link to this definition")

    periodic()[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.periodic)[¶](#celery.worker.consumer.gossip.Gossip.periodic "Link to this definition")

    register\_timer()[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.register_timer)[¶](#celery.worker.consumer.gossip.Gossip.register_timer "Link to this definition")

    requires *= (step:celery.worker.consumer.mingle.Mingle{(step:celery.worker.consumer.events.Events{(step:celery.worker.consumer.connection.Connection{()},)},)},)*[¶](#celery.worker.consumer.gossip.Gossip.requires "Link to this definition")

    start(*c*)[[source]](../_modules/celery/worker/consumer/gossip.html#Gossip.start)[¶](#celery.worker.consumer.gossip.Gossip.start "Link to this definition")

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.consumer.events`](celery.worker.consumer.events.html "previous chapter")

#### Next topic

[`celery.worker.consumer.heart`](celery.worker.consumer.heart.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.worker.consumer.gossip.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.heart.html "celery.worker.consumer.heart") |
* [previous](celery.worker.consumer.events.html "celery.worker.consumer.events") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.consumer.gossip`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
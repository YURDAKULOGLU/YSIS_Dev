celery.worker.strategy — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.html "celery.worker.consumer") |
* [previous](celery.worker.state.html "celery.worker.state") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.strategy`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.worker.strategy.html).

# `celery.worker.strategy`[¶](#celery-worker-strategy "Link to this heading")

Task execution strategy (optimization).

celery.worker.strategy.default(*task*, *app*, *consumer*, *info=<bound method Logger.info of <Logger celery.worker.strategy (WARNING)>>*, *error=<bound method Logger.error of <Logger celery.worker.strategy (WARNING)>>*, *task\_reserved=<function task\_reserved>*, *to\_system\_tz=<bound method \_Zone.to\_system of <celery.utils.time.\_Zone object>>*, *bytes=<class 'bytes'>*, *proto1\_to\_proto2=<function proto1\_to\_proto2>*)[[source]](../_modules/celery/worker/strategy.html#default)[¶](#celery.worker.strategy.default "Link to this definition")
:   Default task execution strategy.

    Note

    Strategies are here as an optimization, so sadly
    it’s not very easy to override.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.state`](celery.worker.state.html "previous chapter")

#### Next topic

[`celery.worker.consumer`](celery.worker.consumer.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.worker.strategy.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.worker.consumer.html "celery.worker.consumer") |
* [previous](celery.worker.state.html "celery.worker.state") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.worker.strategy`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
celery.worker.pidbox — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.worker.autoscale.html "celery.worker.autoscale") |
* [previous](celery.worker.control.html "celery.worker.control") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.worker.pidbox`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.worker.pidbox.html).

# `celery.worker.pidbox`[¶](#celery-worker-pidbox "Link to this heading")

Worker Pidbox (remote control).

*class* celery.worker.pidbox.Pidbox(*c*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox)[¶](#celery.worker.pidbox.Pidbox "Link to this definition")
:   Worker mailbox.

    consumer *= None*[¶](#celery.worker.pidbox.Pidbox.consumer "Link to this definition")

    on\_message(*body*, *message*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.on_message)[¶](#celery.worker.pidbox.Pidbox.on_message "Link to this definition")

    on\_stop()[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.on_stop)[¶](#celery.worker.pidbox.Pidbox.on_stop "Link to this definition")

    reset()[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.reset)[¶](#celery.worker.pidbox.Pidbox.reset "Link to this definition")

    shutdown(*c*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.shutdown)[¶](#celery.worker.pidbox.Pidbox.shutdown "Link to this definition")

    start(*c*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.start)[¶](#celery.worker.pidbox.Pidbox.start "Link to this definition")

    stop(*c*)[[source]](../../_modules/celery/worker/pidbox.html#Pidbox.stop)[¶](#celery.worker.pidbox.Pidbox.stop "Link to this definition")

*class* celery.worker.pidbox.gPidbox(*c*)[[source]](../../_modules/celery/worker/pidbox.html#gPidbox)[¶](#celery.worker.pidbox.gPidbox "Link to this definition")
:   Worker pidbox (greenlet).

    loop(*c*)[[source]](../../_modules/celery/worker/pidbox.html#gPidbox.loop)[¶](#celery.worker.pidbox.gPidbox.loop "Link to this definition")

    on\_stop()[[source]](../../_modules/celery/worker/pidbox.html#gPidbox.on_stop)[¶](#celery.worker.pidbox.gPidbox.on_stop "Link to this definition")

    reset()[[source]](../../_modules/celery/worker/pidbox.html#gPidbox.reset)[¶](#celery.worker.pidbox.gPidbox.reset "Link to this definition")

    start(*c*)[[source]](../../_modules/celery/worker/pidbox.html#gPidbox.start)[¶](#celery.worker.pidbox.gPidbox.start "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.control`](celery.worker.control.html "previous chapter")

#### Next topic

[`celery.worker.autoscale`](celery.worker.autoscale.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.worker.pidbox.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.worker.autoscale.html "celery.worker.autoscale") |
* [previous](celery.worker.control.html "celery.worker.control") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.worker.pidbox`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
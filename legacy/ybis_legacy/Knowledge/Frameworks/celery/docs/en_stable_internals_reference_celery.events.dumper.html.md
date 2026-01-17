celery.events.dumper — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.database.models.html "celery.backends.database.models") |
* [previous](celery.events.cursesmon.html "celery.events.cursesmon") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.events.dumper`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.events.dumper.html).

# `celery.events.dumper`[¶](#celery-events-dumper "Link to this heading")

Utility to dump events to screen.

This is a simple program that dumps events to the console
as they happen. Think of it like a tcpdump for Celery events.

*class* celery.events.dumper.Dumper(*out=<\_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>*)[[source]](../../_modules/celery/events/dumper.html#Dumper)[¶](#celery.events.dumper.Dumper "Link to this definition")
:   Monitor events.

    format\_task\_event(*hostname*, *timestamp*, *type*, *task*, *event*)[[source]](../../_modules/celery/events/dumper.html#Dumper.format_task_event)[¶](#celery.events.dumper.Dumper.format_task_event "Link to this definition")

    on\_event(*ev*)[[source]](../../_modules/celery/events/dumper.html#Dumper.on_event)[¶](#celery.events.dumper.Dumper.on_event "Link to this definition")

    say(*msg*)[[source]](../../_modules/celery/events/dumper.html#Dumper.say)[¶](#celery.events.dumper.Dumper.say "Link to this definition")

celery.events.dumper.evdump(*app=None*, *out=<\_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>*)[[source]](../../_modules/celery/events/dumper.html#evdump)[¶](#celery.events.dumper.evdump "Link to this definition")
:   Start event dump.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.events.cursesmon`](celery.events.cursesmon.html "previous chapter")

#### Next topic

[`celery.backends.database.models`](celery.backends.database.models.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.events.dumper.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.database.models.html "celery.backends.database.models") |
* [previous](celery.events.cursesmon.html "celery.events.cursesmon") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.events.dumper`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
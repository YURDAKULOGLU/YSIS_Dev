celery.events.snapshot — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.events.cursesmon.html "celery.events.cursesmon") |
* [previous](celery.security.utils.html "celery.security.utils") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.events.snapshot`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.events.snapshot.html).

# `celery.events.snapshot`[¶](#celery-events-snapshot "Link to this heading")

Periodically store events in a database.

Consuming the events as a stream isn’t always suitable
so this module implements a system to take snapshots of the
state of a cluster at regular intervals. There’s a full
implementation of this writing the snapshots to a database
in `djcelery.snapshots` in the django-celery distribution.

*class* celery.events.snapshot.Polaroid(*state*, *freq=1.0*, *maxrate=None*, *cleanup\_freq=3600.0*, *timer=None*, *app=None*)[[source]](../../_modules/celery/events/snapshot.html#Polaroid)[¶](#celery.events.snapshot.Polaroid "Link to this definition")
:   Record event snapshots.

    cancel()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.cancel)[¶](#celery.events.snapshot.Polaroid.cancel "Link to this definition")

    capture()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.capture)[¶](#celery.events.snapshot.Polaroid.capture "Link to this definition")

    cleanup()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.cleanup)[¶](#celery.events.snapshot.Polaroid.cleanup "Link to this definition")

    cleanup\_signal *= <Signal: cleanup\_signal providing\_args=set()>*[¶](#celery.events.snapshot.Polaroid.cleanup_signal "Link to this definition")

    clear\_after *= False*[¶](#celery.events.snapshot.Polaroid.clear_after "Link to this definition")

    install()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.install)[¶](#celery.events.snapshot.Polaroid.install "Link to this definition")

    on\_cleanup()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.on_cleanup)[¶](#celery.events.snapshot.Polaroid.on_cleanup "Link to this definition")

    on\_shutter(*state*)[[source]](../../_modules/celery/events/snapshot.html#Polaroid.on_shutter)[¶](#celery.events.snapshot.Polaroid.on_shutter "Link to this definition")

    shutter()[[source]](../../_modules/celery/events/snapshot.html#Polaroid.shutter)[¶](#celery.events.snapshot.Polaroid.shutter "Link to this definition")

    shutter\_signal *= <Signal: shutter\_signal providing\_args={'state'}>*[¶](#celery.events.snapshot.Polaroid.shutter_signal "Link to this definition")

    timer *= None*[¶](#celery.events.snapshot.Polaroid.timer "Link to this definition")

celery.events.snapshot.evcam(*camera*, *freq=1.0*, *maxrate=None*, *loglevel=0*, *logfile=None*, *pidfile=None*, *timer=None*, *app=None*, *\*\*kwargs*)[[source]](../../_modules/celery/events/snapshot.html#evcam)[¶](#celery.events.snapshot.evcam "Link to this definition")
:   Start snapshot recorder.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.security.utils`](celery.security.utils.html "previous chapter")

#### Next topic

[`celery.events.cursesmon`](celery.events.cursesmon.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.events.snapshot.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.events.cursesmon.html "celery.events.cursesmon") |
* [previous](celery.security.utils.html "celery.security.utils") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.events.snapshot`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
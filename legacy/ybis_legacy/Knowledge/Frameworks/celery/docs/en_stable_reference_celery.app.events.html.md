celery.app.events — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.app.log.html "celery.app.log") |
* [previous](celery.app.builtins.html "celery.app.builtins") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.app.events`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.events.html).

# `celery.app.events`[¶](#celery-app-events "Link to this heading")

Implementation for the app.events shortcuts.

*class* celery.app.events.Events(*app=None*)[[source]](../_modules/celery/app/events.html#Events)[¶](#celery.app.events.Events "Link to this definition")
:   Implements app.events.

    *property* Dispatcher[¶](#celery.app.events.Events.Dispatcher "Link to this definition")

    *property* Receiver[¶](#celery.app.events.Events.Receiver "Link to this definition")

    *property* State[¶](#celery.app.events.Events.State "Link to this definition")

    default\_dispatcher(*hostname=None*, *enabled=True*, *buffer\_while\_offline=False*)[[source]](../_modules/celery/app/events.html#Events.default_dispatcher)[¶](#celery.app.events.Events.default_dispatcher "Link to this definition")

    dispatcher\_cls *= 'celery.events.dispatcher:EventDispatcher'*[¶](#celery.app.events.Events.dispatcher_cls "Link to this definition")

    receiver\_cls *= 'celery.events.receiver:EventReceiver'*[¶](#celery.app.events.Events.receiver_cls "Link to this definition")

    state\_cls *= 'celery.events.state:State'*[¶](#celery.app.events.Events.state_cls "Link to this definition")

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.app.builtins`](celery.app.builtins.html "previous chapter")

#### Next topic

[`celery.app.log`](celery.app.log.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.app.events.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.app.log.html "celery.app.log") |
* [previous](celery.app.builtins.html "celery.app.builtins") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.app.events`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
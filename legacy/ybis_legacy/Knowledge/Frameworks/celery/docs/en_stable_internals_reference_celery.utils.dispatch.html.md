celery.utils.dispatch — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.dispatch.signal.html "celery.utils.dispatch.signal") |
* [previous](celery.utils.text.html "celery.utils.text") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.dispatch`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.dispatch.html).

# `celery.utils.dispatch`[¶](#celery-utils-dispatch "Link to this heading")

Observer pattern.

*class* celery.utils.dispatch.Signal(*providing\_args=None*, *use\_caching=False*, *name=None*)[[source]](../../_modules/celery/utils/dispatch/signal.html#Signal)[¶](#celery.utils.dispatch.Signal "Link to this definition")
:   Create new signal.

    Keyword Arguments:
    :   * **providing\_args** (*List*) – A list of the arguments this signal can pass
          along in a [`send()`](#celery.utils.dispatch.Signal.send "celery.utils.dispatch.Signal.send") call.
        * **use\_caching** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Enable receiver cache.
        * **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Name of signal, used for debugging purposes.

    connect(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/dispatch/signal.html#Signal.connect)[¶](#celery.utils.dispatch.Signal.connect "Link to this definition")
    :   Connect receiver to sender for signal.

        Parameters:
        :   * **receiver** (*Callable*) –

              A function or an instance method which is to
              receive signals. Receivers must be hashable objects.

              if weak is `True`, then receiver must be
              weak-referenceable.

              Receivers must be able to accept keyword arguments.

              If receivers have a dispatch\_uid attribute, the receiver will
              not be added if another receiver already exists with that
              dispatch\_uid.
            * **sender** (*Any*) – The sender to which the receiver should respond.
              Must either be a Python object, or `None` to
              receive events from any sender.
            * **weak** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – Whether to use weak references to the receiver.
              By default, the module will attempt to use weak references to
              the receiver objects. If this parameter is false, then strong
              references will be used.
            * **dispatch\_uid** (*Hashable*) – An identifier used to uniquely identify a
              particular instance of a receiver. This will usually be a
              string, though it may be anything hashable.
            * **retry** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – If the signal receiver raises an exception
              (e.g. ConnectionError), the receiver will be retried until it
              runs successfully. A strong ref to the receiver will be stored
              and the weak option will be ignored.

    disconnect(*receiver=None*, *sender=None*, *weak=None*, *dispatch\_uid=None*)[[source]](../../_modules/celery/utils/dispatch/signal.html#Signal.disconnect)[¶](#celery.utils.dispatch.Signal.disconnect "Link to this definition")
    :   Disconnect receiver from sender for signal.

        If weak references are used, disconnect needn’t be called.
        The receiver will be removed from dispatch automatically.

        Parameters:
        :   * **receiver** (*Callable*) – The registered receiver to disconnect.
              May be none if dispatch\_uid is specified.
            * **sender** (*Any*) – The registered sender to disconnect.
            * **weak** ([*bool*](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")) – The weakref state to disconnect.
            * **dispatch\_uid** (*Hashable*) – The unique identifier of the receiver
              to disconnect.

    has\_listeners(*sender=None*)[[source]](../../_modules/celery/utils/dispatch/signal.html#Signal.has_listeners)[¶](#celery.utils.dispatch.Signal.has_listeners "Link to this definition")

    receivers *= None*[¶](#celery.utils.dispatch.Signal.receivers "Link to this definition")
    :   Holds a dictionary of
        `{receiverkey (id): weakref(receiver)}` mappings.

    send(*sender*, *\*\*named*)[[source]](../../_modules/celery/utils/dispatch/signal.html#Signal.send)[¶](#celery.utils.dispatch.Signal.send "Link to this definition")
    :   Send signal from sender to all connected receivers.

        If any receiver raises an error, the exception is returned as the
        corresponding response. (This is different from the “send” in
        Django signals. In Celery “send” and “send\_robust” do the same thing.)

        Parameters:
        :   * **sender** (*Any*) – The sender of the signal.
              Either a specific object or `None`.
            * **\*\*named** (*Any*) – Named arguments which will be passed to receivers.

        Returns:
        :   of tuple pairs: [(receiver, response), … ].

        Return type:
        :   List

    send\_robust(*sender*, *\*\*named*)[¶](#celery.utils.dispatch.Signal.send_robust "Link to this definition")
    :   Send signal from sender to all connected receivers.

        If any receiver raises an error, the exception is returned as the
        corresponding response. (This is different from the “send” in
        Django signals. In Celery “send” and “send\_robust” do the same thing.)

        Parameters:
        :   * **sender** (*Any*) – The sender of the signal.
              Either a specific object or `None`.
            * **\*\*named** (*Any*) – Named arguments which will be passed to receivers.

        Returns:
        :   of tuple pairs: [(receiver, response), … ].

        Return type:
        :   List

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.utils.text`](celery.utils.text.html "previous chapter")

#### Next topic

[`celery.utils.dispatch.signal`](celery.utils.dispatch.signal.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.dispatch.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.dispatch.signal.html "celery.utils.dispatch.signal") |
* [previous](celery.utils.text.html "celery.utils.text") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.dispatch`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
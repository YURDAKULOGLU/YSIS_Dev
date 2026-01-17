celery.app.registry — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.app.backends.html "celery.app.backends") |
* [previous](celery.app.control.html "celery.app.control") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.app.registry`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.app.registry.html).

# `celery.app.registry`[¶](#celery-app-registry "Link to this heading")

Registry of available tasks.

*class* celery.app.registry.TaskRegistry[[source]](../_modules/celery/app/registry.html#TaskRegistry)[¶](#celery.app.registry.TaskRegistry "Link to this definition")
:   Map of registered tasks.

    *exception* NotRegistered[¶](#celery.app.registry.TaskRegistry.NotRegistered "Link to this definition")
    :   The task is not registered.

    filter\_types(*type*)[[source]](../_modules/celery/app/registry.html#TaskRegistry.filter_types)[¶](#celery.app.registry.TaskRegistry.filter_types "Link to this definition")

    periodic()[[source]](../_modules/celery/app/registry.html#TaskRegistry.periodic)[¶](#celery.app.registry.TaskRegistry.periodic "Link to this definition")

    register(*task*)[[source]](../_modules/celery/app/registry.html#TaskRegistry.register)[¶](#celery.app.registry.TaskRegistry.register "Link to this definition")
    :   Register a task in the task registry.

        The task will be automatically instantiated if not already an
        instance. Name must be configured prior to registration.

    regular()[[source]](../_modules/celery/app/registry.html#TaskRegistry.regular)[¶](#celery.app.registry.TaskRegistry.regular "Link to this definition")

    unregister(*name*)[[source]](../_modules/celery/app/registry.html#TaskRegistry.unregister)[¶](#celery.app.registry.TaskRegistry.unregister "Link to this definition")
    :   Unregister task by name.

        Parameters:
        :   **name** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – name of the task to unregister, or a
            [`celery.app.task.Task`](celery.app.task.html#celery.app.task.Task "celery.app.task.Task") with a valid name attribute.

        Raises:
        :   [**celery.exceptions.NotRegistered**](celery.exceptions.html#celery.exceptions.NotRegistered "celery.exceptions.NotRegistered") – if the task is not registered.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.app.control`](celery.app.control.html "previous chapter")

#### Next topic

[`celery.app.backends`](celery.app.backends.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.app.registry.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.app.backends.html "celery.app.backends") |
* [previous](celery.app.control.html "celery.app.control") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.app.registry`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
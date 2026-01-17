celery.contrib.migrate — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.pytest.html "celery.contrib.pytest") |
* [previous](celery.contrib.django.task.html "celery.contrib.django.task") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.migrate`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.migrate.html).

# `celery.contrib.migrate`[¶](#celery-contrib-migrate "Link to this heading")

Message migration tools (Broker <-> Broker).

*class* celery.contrib.migrate.State[[source]](../_modules/celery/contrib/migrate.html#State)[¶](#celery.contrib.migrate.State "Link to this definition")
:   Migration progress state.

    count *= 0*[¶](#celery.contrib.migrate.State.count "Link to this definition")

    filtered *= 0*[¶](#celery.contrib.migrate.State.filtered "Link to this definition")

    *property* strtotal[¶](#celery.contrib.migrate.State.strtotal "Link to this definition")

    total\_apx *= 0*[¶](#celery.contrib.migrate.State.total_apx "Link to this definition")

*exception* celery.contrib.migrate.StopFiltering[[source]](../_modules/celery/contrib/migrate.html#StopFiltering)[¶](#celery.contrib.migrate.StopFiltering "Link to this definition")
:   Semi-predicate used to signal filter stop.

celery.contrib.migrate.migrate\_task(*producer*, *body\_*, *message*, *queues=None*)[[source]](../_modules/celery/contrib/migrate.html#migrate_task)[¶](#celery.contrib.migrate.migrate_task "Link to this definition")
:   Migrate single task message.

celery.contrib.migrate.migrate\_tasks(*source*, *dest*, *migrate=<function migrate\_task>*, *app=None*, *queues=None*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/migrate.html#migrate_tasks)[¶](#celery.contrib.migrate.migrate_tasks "Link to this definition")
:   Migrate tasks from one broker to another.

celery.contrib.migrate.move(*predicate*, *connection=None*, *exchange=None*, *routing\_key=None*, *source=None*, *app=None*, *callback=None*, *limit=None*, *transform=None*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/migrate.html#move)[¶](#celery.contrib.migrate.move "Link to this definition")
:   Find tasks by filtering them and move the tasks to a new queue.

    Parameters:
    :   * **predicate** (*Callable*) –

          Filter function used to decide the messages
          to move. Must accept the standard signature of `(body, message)`
          used by Kombu consumer callbacks. If the predicate wants the
          message to be moved it must return either:

          > 1. a tuple of `(exchange, routing_key)`, or
          > 2. a [`Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instance, or
          > 3. any other true value means the specified
          >    :   `exchange` and `routing_key` arguments will be used.
        * **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Custom connection to use.
        * **source** – List[Union[str, kombu.Queue]]: Optional list of source
          queues to use instead of the default (queues
          in [`task_queues`](../userguide/configuration.html#std-setting-task_queues)). This list can also contain
          [`Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instances.
        * **exchange** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*kombu.Exchange*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Exchange "(in Kombu v5.6)")) – Default destination exchange.
        * **routing\_key** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Default destination routing key.
        * **limit** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Limit number of messages to filter.
        * **callback** (*Callable*) – Callback called after message moved,
          with signature `(state, body, message)`.
        * **transform** (*Callable*) – Optional function to transform the return
          value (destination) of the filter function.

    Also supports the same keyword arguments as [`start_filter()`](#celery.contrib.migrate.start_filter "celery.contrib.migrate.start_filter").

    To demonstrate, the [`move_task_by_id()`](#celery.contrib.migrate.move_task_by_id "celery.contrib.migrate.move_task_by_id") operation can be implemented
    like this:

    ```
    def is_wanted_task(body, message):
        if body['id'] == wanted_id:
            return Queue('foo', exchange=Exchange('foo'),
                         routing_key='foo')

    move(is_wanted_task)
    ```

    or with a transform:

    ```
    def transform(value):
        if isinstance(value, str):
            return Queue(value, Exchange(value), value)
        return value

    move(is_wanted_task, transform=transform)
    ```

    Note

    The predicate may also return a tuple of `(exchange, routing_key)`
    to specify the destination to where the task should be moved,
    or a [`Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instance.
    Any other true value means that the task will be moved to the
    default exchange/routing\_key.

celery.contrib.migrate.move\_by\_idmap(*map*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/migrate.html#move_by_idmap)[¶](#celery.contrib.migrate.move_by_idmap "Link to this definition")
:   Move tasks by matching from a `task_id: queue` mapping.

    Where `queue` is a queue to move the task to.

    Example

    ```
    >>> move_by_idmap({
    ...     '5bee6e82-f4ac-468e-bd3d-13e8600250bc': Queue('name'),
    ...     'ada8652d-aef3-466b-abd2-becdaf1b82b3': Queue('name'),
    ...     '3a2b140d-7db1-41ba-ac90-c36a0ef4ab1f': Queue('name')},
    ...   queues=['hipri'])
    ```

celery.contrib.migrate.move\_by\_taskmap(*map*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/migrate.html#move_by_taskmap)[¶](#celery.contrib.migrate.move_by_taskmap "Link to this definition")
:   Move tasks by matching from a `task_name: queue` mapping.

    `queue` is the queue to move the task to.

    Example

    ```
    >>> move_by_taskmap({
    ...     'tasks.add': Queue('name'),
    ...     'tasks.mul': Queue('name'),
    ... })
    ```

celery.contrib.migrate.move\_direct(*predicate*, *connection=None*, *exchange=None*, *routing\_key=None*, *source=None*, *app=None*, *callback=None*, *limit=None*, *\**, *transform=<function worker\_direct>*, *\*\*kwargs*)[¶](#celery.contrib.migrate.move_direct "Link to this definition")
:   Find tasks by filtering them and move the tasks to a new queue.

    Parameters:
    :   * **predicate** (*Callable*) –

          Filter function used to decide the messages
          to move. Must accept the standard signature of `(body, message)`
          used by Kombu consumer callbacks. If the predicate wants the
          message to be moved it must return either:

          > 1. a tuple of `(exchange, routing_key)`, or
          > 2. a [`Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instance, or
          > 3. any other true value means the specified
          >    :   `exchange` and `routing_key` arguments will be used.
        * **connection** ([*kombu.Connection*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Connection "(in Kombu v5.6)")) – Custom connection to use.
        * **source** – List[Union[str, kombu.Queue]]: Optional list of source
          queues to use instead of the default (queues
          in [`task_queues`](../userguide/configuration.html#std-setting-task_queues)). This list can also contain
          [`Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instances.
        * **exchange** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*kombu.Exchange*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Exchange "(in Kombu v5.6)")) – Default destination exchange.
        * **routing\_key** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Default destination routing key.
        * **limit** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")) – Limit number of messages to filter.
        * **callback** (*Callable*) – Callback called after message moved,
          with signature `(state, body, message)`.
        * **transform** (*Callable*) – Optional function to transform the return
          value (destination) of the filter function.

    Also supports the same keyword arguments as [`start_filter()`](#celery.contrib.migrate.start_filter "celery.contrib.migrate.start_filter").

    To demonstrate, the [`move_task_by_id()`](#celery.contrib.migrate.move_task_by_id "celery.contrib.migrate.move_task_by_id") operation can be implemented
    like this:

    ```
    def is_wanted_task(body, message):
        if body['id'] == wanted_id:
            return Queue('foo', exchange=Exchange('foo'),
                         routing_key='foo')

    move(is_wanted_task)
    ```

    or with a transform:

    ```
    def transform(value):
        if isinstance(value, str):
            return Queue(value, Exchange(value), value)
        return value

    move(is_wanted_task, transform=transform)
    ```

    Note

    The predicate may also return a tuple of `(exchange, routing_key)`
    to specify the destination to where the task should be moved,
    or a [`Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instance.
    Any other true value means that the task will be moved to the
    default exchange/routing\_key.

celery.contrib.migrate.move\_direct\_by\_id(*task\_id*, *dest*, *\*\*kwargs*)[¶](#celery.contrib.migrate.move_direct_by_id "Link to this definition")
:   Find a task by id and move it to another queue.

    Parameters:
    :   * **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Id of task to find and move.
        * **dest** – (str, kombu.Queue): Destination queue.
        * **transform** (*Callable*) – Optional function to transform the return
          value (destination) of the filter function.
        * **\*\*kwargs** (*Any*) – Also supports the same keyword
          arguments as [`move()`](#celery.contrib.migrate.move "celery.contrib.migrate.move").

celery.contrib.migrate.move\_task\_by\_id(*task\_id*, *dest*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/migrate.html#move_task_by_id)[¶](#celery.contrib.migrate.move_task_by_id "Link to this definition")
:   Find a task by id and move it to another queue.

    Parameters:
    :   * **task\_id** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Id of task to find and move.
        * **dest** – (str, kombu.Queue): Destination queue.
        * **transform** (*Callable*) – Optional function to transform the return
          value (destination) of the filter function.
        * **\*\*kwargs** (*Any*) – Also supports the same keyword
          arguments as [`move()`](#celery.contrib.migrate.move "celery.contrib.migrate.move").

celery.contrib.migrate.republish(*producer*, *message*, *exchange=None*, *routing\_key=None*, *remove\_props=None*)[[source]](../_modules/celery/contrib/migrate.html#republish)[¶](#celery.contrib.migrate.republish "Link to this definition")
:   Republish message.

celery.contrib.migrate.start\_filter(*app*, *conn*, *filter*, *limit=None*, *timeout=1.0*, *ack\_messages=False*, *tasks=None*, *queues=None*, *callback=None*, *forever=False*, *on\_declare\_queue=None*, *consume\_from=None*, *state=None*, *accept=None*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/migrate.html#start_filter)[¶](#celery.contrib.migrate.start_filter "Link to this definition")
:   Filter tasks.

celery.contrib.migrate.task\_id\_eq(*task\_id*, *body*, *message*)[[source]](../_modules/celery/contrib/migrate.html#task_id_eq)[¶](#celery.contrib.migrate.task_id_eq "Link to this definition")
:   Return true if task id equals task\_id’.

celery.contrib.migrate.task\_id\_in(*ids*, *body*, *message*)[[source]](../_modules/celery/contrib/migrate.html#task_id_in)[¶](#celery.contrib.migrate.task_id_in "Link to this definition")
:   Return true if task id is member of set ids’.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.contrib.django.task`](celery.contrib.django.task.html "previous chapter")

#### Next topic

[`celery.contrib.pytest`](celery.contrib.pytest.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.contrib.migrate.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.pytest.html "celery.contrib.pytest") |
* [previous](celery.contrib.django.task.html "celery.contrib.django.task") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.migrate`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
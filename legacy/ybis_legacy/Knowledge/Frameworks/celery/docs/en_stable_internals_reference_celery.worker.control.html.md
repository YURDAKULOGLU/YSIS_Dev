celery.worker.control — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.worker.pidbox.html "celery.worker.pidbox") |
* [previous](celery.worker.heartbeat.html "celery.worker.heartbeat") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.worker.control`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.worker.control.html).

# `celery.worker.control`[¶](#celery-worker-control "Link to this heading")

Worker remote control command implementations.

*class* celery.worker.control.Panel(*dict=None*, */*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/control.html#Panel)[¶](#celery.worker.control.Panel "Link to this definition")
:   Global registry of remote control commands.

    data *= {'active': <function active>, 'active\_queues': <function active\_queues>, 'add\_consumer': <function add\_consumer>, 'autoscale': <function autoscale>, 'cancel\_consumer': <function cancel\_consumer>, 'clock': <function clock>, 'conf': <function conf>, 'disable\_events': <function disable\_events>, 'dump\_active': <function active>, 'dump\_conf': <function conf>, 'dump\_reserved': <function reserved>, 'dump\_revoked': <function revoked>, 'dump\_schedule': <function scheduled>, 'dump\_tasks': <function registered>, 'election': <function election>, 'enable\_events': <function enable\_events>, 'heartbeat': <function heartbeat>, 'hello': <function hello>, 'memdump': <function memdump>, 'memsample': <function memsample>, 'objgraph': <function objgraph>, 'ping': <function ping>, 'pool\_grow': <function pool\_grow>, 'pool\_restart': <function pool\_restart>, 'pool\_shrink': <function pool\_shrink>, 'query\_task': <function query\_task>, 'rate\_limit': <function rate\_limit>, 'registered': <function registered>, 'report': <function report>, 'reserved': <function reserved>, 'revoke': <function revoke>, 'revoke\_by\_stamped\_headers': <function revoke\_by\_stamped\_headers>, 'revoked': <function revoked>, 'scheduled': <function scheduled>, 'shutdown': <function shutdown>, 'stats': <function stats>, 'terminate': <function terminate>, 'time\_limit': <function time\_limit>}*[¶](#celery.worker.control.Panel.data "Link to this definition")

    meta *= {'active': ('dump\_active', 'inspect', True, 1.0, 'List of tasks currently being executed.', None, None, None), 'active\_queues': (None, 'inspect', True, 1.0, 'List the task queues a worker is currently consuming from.', None, None, None), 'add\_consumer': (None, 'control', True, 1.0, 'Tell worker(s) to consume from task queue by name.', '<queue> [exchange [type [routing\_key]]]', [('queue', <class 'str'>), ('exchange', <class 'str'>), ('exchange\_type', <class 'str'>), ('routing\_key', <class 'str'>)], None), 'autoscale': (None, 'control', True, 1.0, 'Modify autoscale settings.', '[max [min]]', [('max', <class 'int'>), ('min', <class 'int'>)], None), 'cancel\_consumer': (None, 'control', True, 1.0, 'Tell worker(s) to stop consuming from task queue by name.', '<queue>', [('queue', <class 'str'>)], None), 'clock': (None, 'inspect', True, 1.0, 'Get current logical clock value.', None, None, None), 'conf': ('dump\_conf', 'inspect', True, 1.0, 'List configuration.', '[include\_defaults=False]', [('with\_defaults', <function strtobool>)], None), 'disable\_events': (None, 'control', True, 1.0, 'Tell worker(s) to stop sending task-related events.', None, None, None), 'election': (None, 'control', True, 1.0, 'Hold election.', None, None, None), 'enable\_events': (None, 'control', True, 1.0, 'Tell worker(s) to send task-related events.', None, None, None), 'heartbeat': (None, 'control', True, 1.0, 'Tell worker(s) to send event heartbeat immediately.', None, None, None), 'hello': (None, 'inspect', False, 1.0, 'Request mingle sync-data.', None, None, None), 'memdump': (None, 'inspect', True, 1.0, 'Dump statistics of previous memsample requests.', '[n\_samples=10]', [('samples', <class 'int'>)], None), 'memsample': (None, 'inspect', True, 1.0, 'Sample current RSS memory usage.', None, None, None), 'objgraph': (None, 'inspect', True, 60.0, 'Create graph of uncollected objects (memory-leak debugging).', '[object\_type=Request] [num=200 [max\_depth=10]]', [('type', <class 'str'>), ('num', <class 'int'>), ('max\_depth', <class 'int'>)], None), 'ping': (None, 'inspect', True, 0.2, 'Ping worker(s).', None, None, None), 'pool\_grow': (None, 'control', True, 1.0, 'Grow pool by n processes/threads.', '[N=1]', [('n', <class 'int'>)], None), 'pool\_restart': (None, 'control', True, 1.0, 'Restart execution pool.', None, None, None), 'pool\_shrink': (None, 'control', True, 1.0, 'Shrink pool by n processes/threads.', '[N=1]', [('n', <class 'int'>)], None), 'query\_task': (None, 'inspect', True, 1.0, 'Query for task information by id.', '[id1 [id2 [... [idN]]]]', None, 'ids'), 'rate\_limit': (None, 'control', True, 1.0, 'Tell worker(s) to modify the rate limit for a task by type.', '<task\_name> <rate\_limit (e.g., 5/s | 5/m | 5/h)>', [('task\_name', <class 'str'>), ('rate\_limit', <class 'str'>)], None), 'registered': ('dump\_tasks', 'inspect', True, 1.0, 'List of registered tasks.', '[attr1 [attr2 [... [attrN]]]]', None, 'taskinfoitems'), 'report': (None, 'inspect', True, 1.0, 'Information about Celery installation for bug reports.', None, None, None), 'reserved': ('dump\_reserved', 'inspect', True, 1.0, 'List of currently reserved tasks, not including scheduled/active.', None, None, None), 'revoke': (None, 'control', True, 1.0, 'Revoke task by task id (or list of ids).', '[id1 [id2 [... [idN]]]]', None, 'task\_id'), 'revoke\_by\_stamped\_headers': (None, 'control', True, 1.0, 'Revoke task by header (or list of headers).', '[key1=value1 [key2=value2 [... [keyN=valueN]]]]', None, 'headers'), 'revoked': ('dump\_revoked', 'inspect', True, 1.0, 'List of revoked task-ids.', None, None, None), 'scheduled': ('dump\_schedule', 'inspect', True, 1.0, 'List of currently scheduled ETA/countdown tasks.', None, None, None), 'shutdown': (None, 'control', True, 1.0, 'Shutdown worker(s).', None, None, None), 'stats': (None, 'inspect', True, 1.0, 'Request worker statistics/information.', None, None, None), 'terminate': (None, 'control', True, 1.0, 'Terminate task by task id (or list of ids).', '<signal> [id1 [id2 [... [idN]]]]', [('signal', <class 'str'>)], 'task\_id'), 'time\_limit': (None, 'control', True, 1.0, 'Tell worker(s) to modify the time limit for task by type.', '<task\_name> <soft\_secs> [hard\_secs]', [('task\_name', <class 'str'>), ('soft', <class 'float'>), ('hard', <class 'float'>)], None)}*[¶](#celery.worker.control.Panel.meta "Link to this definition")

    *classmethod* register(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/worker/control.html#Panel.register)[¶](#celery.worker.control.Panel.register "Link to this definition")
    :   Register a virtual subclass of an ABC.

        Returns the subclass, to allow usage as a class decorator.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.heartbeat`](celery.worker.heartbeat.html "previous chapter")

#### Next topic

[`celery.worker.pidbox`](celery.worker.pidbox.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.worker.control.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.worker.pidbox.html "celery.worker.pidbox") |
* [previous](celery.worker.heartbeat.html "celery.worker.heartbeat") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.worker.control`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
Contributors Guide to the Code — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](deprecation.html "Celery Deprecation Time-line") |
* [previous](index.html "Internals") |
* [Celery 5.6.2 documentation](../index.html) »
* [Internals](index.html) »
* Contributors Guide to the Code

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/guide.html).

# Contributors Guide to the Code[¶](#contributors-guide-to-the-code "Link to this heading")

## [Philosophy](#id1)[¶](#philosophy "Link to this heading")

### [The API>RCP Precedence Rule](#id2)[¶](#the-api-rcp-precedence-rule "Link to this heading")

* The API is more important than Readability
* Readability is more important than Convention
* Convention is more important than Performance
  :   + …unless the code is a proven hot-spot.

More important than anything else is the end-user API.
Conventions must step aside, and any suffering is always alleviated
if the end result is a better API.

## [Conventions and Idioms Used](#id3)[¶](#conventions-and-idioms-used "Link to this heading")

### [Classes](#id4)[¶](#classes "Link to this heading")

#### [Naming](#id5)[¶](#naming "Link to this heading")

* Follows [**PEP 8**](https://peps.python.org/pep-0008/).
* Class names must be CamelCase.
* but not if they’re verbs, verbs shall be lower\_case:

  > ```
  > # - test case for a class
  > class TestMyClass(Case):                # BAD
  >     pass
  >
  > class test_MyClass(Case):               # GOOD
  >     pass
  >
  > # - test case for a function
  > class TestMyFunction(Case):             # BAD
  >     pass
  >
  > class test_my_function(Case):           # GOOD
  >     pass
  >
  > # - "action" class (verb)
  > class UpdateTwitterStatus:    # BAD
  >     pass
  >
  > class update_twitter_status:    # GOOD
  >     pass
  > ```
  >
  > Note
  >
  > Sometimes it makes sense to have a class mask as a function,
  > and there’s precedence for this in the Python standard library (e.g.,
  > `contextmanager`). Celery examples include
  > [`signature`](../reference/celery.html#celery.signature "celery.signature"), [`chord`](../reference/celery.html#celery.chord "celery.chord"),
  > `inspect`, `promise` and more..
* Factory functions and methods must be CamelCase (excluding verbs):

  > ```
  > class Celery:
  >
  >     def consumer_factory(self):     # BAD
  >         ...
  >
  >     def Consumer(self):             # GOOD
  >         ...
  > ```

#### [Default values](#id6)[¶](#default-values "Link to this heading")

Class attributes serve as default values for the instance,
as this means that they can be set by either instantiation or inheritance.

**Example:**

```
class Producer:
    active = True
    serializer = 'json'

    def __init__(self, serializer=None, active=None):
        self.serializer = serializer or self.serializer

        # must check for None when value can be false-y
        self.active = active if active is not None else self.active
```

A subclass can change the default value:

```
TaskProducer(Producer):
    serializer = 'pickle'
```

and the value can be set at instantiation:

```
>>> producer = TaskProducer(serializer='msgpack')
```

#### [Exceptions](#id7)[¶](#exceptions "Link to this heading")

Custom exceptions raised by an objects methods and properties
should be available as an attribute and documented in the
method/property that throw.

This way a user doesn’t have to find out where to import the
exception from, but rather use `help(obj)` and access
the exception class from the instance directly.

**Example**:

```
class Empty(Exception):
    pass

class Queue:
    Empty = Empty

    def get(self):
        """Get the next item from the queue.

        :raises Queue.Empty: if there are no more items left.

        """
        try:
            return self.queue.popleft()
        except IndexError:
            raise self.Empty()
```

#### [Composites](#id8)[¶](#composites "Link to this heading")

Similarly to exceptions, composite classes should be override-able by
inheritance and/or instantiation. Common sense can be used when
selecting what classes to include, but often it’s better to add one
too many: predicting what users need to override is hard (this has
saved us from many a monkey patch).

**Example**:

```
class Worker:
    Consumer = Consumer

    def __init__(self, connection, consumer_cls=None):
        self.Consumer = consumer_cls or self.Consumer

    def do_work(self):
        with self.Consumer(self.connection) as consumer:
            self.connection.drain_events()
```

## [Applications vs. “single mode”](#id9)[¶](#applications-vs-single-mode "Link to this heading")

In the beginning Celery was developed for Django, simply because
this enabled us get the project started quickly, while also having
a large potential user base.

In Django there’s a global settings object, so multiple Django projects
can’t co-exist in the same process space, this later posed a problem
for using Celery with frameworks that don’t have this limitation.

Therefore the app concept was introduced. When using apps you use ‘celery’
objects instead of importing things from Celery sub-modules, this
(unfortunately) also means that Celery essentially has two API’s.

Here’s an example using Celery in single-mode:

```
from celery import task
from celery.task.control import inspect

from .models import CeleryStats

@task
def write_stats_to_db():
    stats = inspect().stats(timeout=1)
    for node_name, reply in stats:
        CeleryStats.objects.update_stat(node_name, stats)
```

and here’s the same using Celery app objects:

```
from .celery import celery
from .models import CeleryStats

@app.task
def write_stats_to_db():
    stats = celery.control.inspect().stats(timeout=1)
    for node_name, reply in stats:
        CeleryStats.objects.update_stat(node_name, stats)
```

In the example above the actual application instance is imported
from a module in the project, this module could look something like this:

```
from celery import Celery

app = Celery(broker='amqp://')
```

## [Module Overview](#id10)[¶](#module-overview "Link to this heading")

* celery.app

  > This is the core of Celery: the entry-point for all functionality.
* celery.loaders

  > Every app must have a loader. The loader decides how configuration
  > is read; what happens when the worker starts; when a task starts and ends;
  > and so on.
  >
  > The loaders included are:
  >
  > > + app
  > >
  > >   > Custom Celery app instances uses this loader by default.
  > > + default
  > >
  > >   > “single-mode” uses this loader by default.
  >
  > Extension loaders also exist, for example <https://pypi.org/project/celery-pylons/>.
* celery.worker

  > This is the worker implementation.
* celery.backends

  > Task result backends live here.
* celery.apps

  > Major user applications: worker and beat.
  > The command-line wrappers for these are in celery.bin (see below)
* celery.bin

  > Command-line applications.
  > `setup.py` creates setuptools entry-points for these.
* celery.concurrency

  > Execution pool implementations (prefork, eventlet, gevent, solo, thread).
* celery.db

  > Database models for the SQLAlchemy database result backend.
  > (should be moved into [`celery.backends.database`](reference/celery.backends.database.html#module-celery.backends.database "celery.backends.database"))
* celery.events

  > Sending and consuming monitoring events, also includes curses monitor,
  > event dumper and utilities to work with in-memory cluster state.
* celery.execute.trace

  > How tasks are executed and traced by the worker, and in eager mode.
* celery.security

  > Security related functionality, currently a serializer using
  > cryptographic digests.
* celery.task

  > single-mode interface to creating tasks, and controlling workers.
* t.unit (int distribution)

  > The unit test suite.
* celery.utils

  > Utility functions used by the Celery code base.
  > Much of it is there to be compatible across Python versions.
* celery.contrib

  > Additional public code that doesn’t fit into any other name-space.

## [Worker overview](#id11)[¶](#worker-overview "Link to this heading")

* celery.bin.worker:Worker

  > This is the command-line interface to the worker.
  >
  > Responsibilities:
  > :   + Daemonization when [`--detach`](../reference/cli.html#cmdoption-celery-worker-D) set,
  >     + dropping privileges when using [`--uid`](../reference/cli.html#cmdoption-celery-worker-uid)/
  >       [`--gid`](../reference/cli.html#cmdoption-celery-worker-gid) arguments
  >     + Installs “concurrency patches” (eventlet/gevent monkey patches).

  `app.worker_main(argv)` calls
  `instantiate('celery.bin.worker:Worker')(app).execute_from_commandline(argv)`
* app.Worker -> celery.apps.worker:Worker

  > Responsibilities:
  > \* sets up logging and redirects standard outs
  > \* installs signal handlers (TERM/HUP/STOP/USR1 (cry)/USR2 (rdb))
  > \* prints banner and warnings (e.g., pickle warning)
  > \* handles the [`celery worker --purge`](../reference/cli.html#cmdoption-celery-worker-purge) argument
* app.WorkController -> celery.worker.WorkController

  > This is the real worker, built up around bootsteps.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[Internals](index.html "previous chapter")

#### Next topic

[Celery Deprecation Time-line](deprecation.html "next chapter")

### This Page

* [Show Source](../_sources/internals/guide.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](deprecation.html "Celery Deprecation Time-line") |
* [previous](index.html "Internals") |
* [Celery 5.6.2 documentation](../index.html) »
* [Internals](index.html) »
* Contributors Guide to the Code

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
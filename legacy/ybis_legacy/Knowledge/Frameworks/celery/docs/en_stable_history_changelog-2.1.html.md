Change history for Celery 2.1 — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](changelog-2.0.html "Change history for Celery 2.0") |
* [previous](changelog-2.2.html "Change history for Celery 2.2") |
* [Celery 5.6.2 documentation](../index.html) »
* [History](index.html) »
* Change history for Celery 2.1

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/history/changelog-2.1.html).

# Change history for Celery 2.1[¶](#change-history-for-celery-2-1 "Link to this heading")

## [2.1.4](#id11)[¶](#version-2-1-4 "Link to this heading")

release-date:
:   2010-12-03 12:00 p.m. CEST

release-by:
:   Ask Solem

### [Fixes](#id12)[¶](#fixes "Link to this heading")

* Execution options to apply\_async now takes precedence over options
  returned by active routers. This was a regression introduced recently
  (Issue #244).
* curses monitor: Long arguments are now truncated so curses
  doesn’t crash with out of bounds errors (Issue #235).
* multi: Channel errors occurring while handling control commands no
  longer crash the worker but are instead logged with severity error.
* SQLAlchemy database backend: Fixed a race condition occurring when
  the client wrote the pending state. Just like the Django database backend,
  it does no longer save the pending state (Issue #261 + Issue #262).
* Error email body now uses repr(exception) instead of str(exception),
  as the latter could result in Unicode decode errors (Issue #245).
* Error email timeout value is now configurable by using the
  [`EMAIL_TIMEOUT`](http://docs.djangoproject.com/en/dev/ref/settings/#std-setting-EMAIL_TIMEOUT "(in Django v6.1)") setting.
* celeryev: Now works on Windows (but the curses monitor won’t work without
  having curses).
* Unit test output no longer emits non-standard characters.
* worker: The broadcast consumer is now closed if the connection is reset.
* worker: Now properly handles errors occurring while trying to acknowledge
  the message.
* TaskRequest.on\_failure now encodes traceback using the current file-system
  :   encoding (Issue #286).
* EagerResult can now be pickled (Issue #288).

### [Documentation](#id13)[¶](#documentation "Link to this heading")

* Adding [Contributing](../contributing.html#contributing).
* Added [Optimizing](../userguide/optimizing.html#guide-optimizing).
* Added [Security](../faq.html#faq-security) section to the FAQ.

## [2.1.3](#id14)[¶](#version-2-1-3 "Link to this heading")

release-date:
:   2010-11-09 05:00 p.m. CEST

release-by:
:   Ask Solem

* Fixed deadlocks in timer2 which could lead to djcelerymon/celeryev -c
  hanging.
* EventReceiver: now sends heartbeat request to find workers.

  > This means **celeryev** and friends finds workers immediately
  > at start-up.
* `celeryev` curses monitor: Set screen\_delay to 10ms, so the screen
  refreshes more often.
* Fixed pickling errors when pickling `AsyncResult` on older Python
  versions.
* worker: prefetch count was decremented by ETA tasks even if there
  were no active prefetch limits.

## [2.1.2](#id15)[¶](#version-2-1-2 "Link to this heading")

release-data:
:   TBA

### [Fixes](#id16)[¶](#v212-fixes "Link to this heading")

* worker: Now sends the [`task-retried`](../userguide/monitoring.html#std-event-task-retried) event for retried tasks.
* worker: Now honors ignore result for
  [`WorkerLostError`](../reference/celery.exceptions.html#celery.exceptions.WorkerLostError "celery.exceptions.WorkerLostError") and timeout errors.
* `celerybeat`: Fixed [`UnboundLocalError`](https://docs.python.org/dev/library/exceptions.html#UnboundLocalError "(in Python v3.15)") in `celerybeat` logging
  when using logging setup signals.
* worker: All log messages now includes exc\_info.

## [2.1.1](#id17)[¶](#version-2-1-1 "Link to this heading")

release-date:
:   2010-10-14 02:00 p.m. CEST

release-by:
:   Ask Solem

### [Fixes](#id18)[¶](#v211-fixes "Link to this heading")

* Now working on Windows again.

  > Removed dependency on the [`pwd`](https://docs.python.org/dev/library/pwd.html#module-pwd "(in Python v3.15)")/[`grp`](https://docs.python.org/dev/library/grp.html#module-grp "(in Python v3.15)") modules.
* snapshots: Fixed race condition leading to loss of events.
* worker: Reject tasks with an ETA that cannot be converted to a time stamp.

  > See issue #209
* concurrency.processes.pool: The semaphore was released twice for each task
  (both at ACK and result ready).

  > This has been fixed, and it is now released only once per task.
* docs/configuration: Fixed typo CELERYD\_TASK\_SOFT\_TIME\_LIMIT ->
  `CELERYD_TASK_SOFT_TIME_LIMIT`.

  > See issue #214
* control command dump\_scheduled: was using old .info attribute
* multi: Fixed set changed size during iteration bug
  :   occurring in the restart command.
* worker: Accidentally tried to use additional command-line arguments.

  > This would lead to an error like:
  >
  > > got multiple values for keyword argument ‘concurrency’.
  > >
  > > Additional command-line arguments are now ignored, and doesn’t
  > > produce this error. However – we do reserve the right to use
  > > positional arguments in the future, so please don’t depend on this
  > > behavior.
* `celerybeat`: Now respects routers and task execution options again.
* `celerybeat`: Now reuses the publisher instead of the connection.
* Cache result backend: Using [`float`](https://docs.python.org/dev/library/functions.html#float "(in Python v3.15)") as the expires argument
  to cache.set is deprecated by the Memcached libraries,
  so we now automatically cast to [`int`](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)").
* unit tests: No longer emits logging and warnings in test output.

### [News](#id19)[¶](#news "Link to this heading")

* Now depends on carrot version 0.10.7.
* Added `CELERY_REDIRECT_STDOUTS`, and
  `CELERYD_REDIRECT_STDOUTS_LEVEL` settings.

  > `CELERY_REDIRECT_STDOUTS` is used by the worker and
  > beat. All output to stdout and stderr will be
  > redirected to the current logger if enabled.
  >
  > `CELERY_REDIRECT_STDOUTS_LEVEL` decides the log level used and is
  > `WARNING` by default.
* Added `CELERYBEAT_SCHEDULER` setting.

  > This setting is used to define the default for the -S option to
  > **celerybeat**.
  >
  > Example:
  >
  > ```
  > CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
  > ```
* Added Task.expires: Used to set default expiry time for tasks.
* New remote control commands: add\_consumer and cancel\_consumer.

  > add\_consumer(queue, exchange, exchange\_type, routing\_key,
  >
  > \\*\\*options)
  > :   Tells the worker to declare and consume from the specified
  >     declaration.
  >
  > cancel\_consumer(*queue\_name*)[¶](#cancel_consumer "Link to this definition")
  > :   Tells the worker to stop consuming from queue (by queue name).
  >
  > Commands also added to **celeryctl** and
  > `inspect`.
  >
  > Example using `celeryctl` to start consuming from queue “queue”, in
  > exchange “exchange”, of type “direct” using binding key “key”:
  >
  > ```
  > $ celeryctl inspect add_consumer queue exchange direct key
  > $ celeryctl inspect cancel_consumer queue
  > ```
  >
  > See [Management Command-line Utilities (inspect/control)](../userguide/monitoring.html#monitoring-control) for more information about the
  > **celeryctl** program.
  >
  > Another example using `inspect`:
  >
  > ```
  > >>> from celery.task.control import inspect
  > >>> inspect.add_consumer(queue='queue', exchange='exchange',
  > ...                      exchange_type='direct',
  > ...                      routing_key='key',
  > ...                      durable=False,
  > ...                      auto_delete=True)
  >
  > >>> inspect.cancel_consumer('queue')
  > ```
* `celerybeat`: Now logs the traceback if a message can’t be sent.
* `celerybeat`: Now enables a default socket timeout of 30 seconds.
* `README`/introduction/homepage: Added link to [Flask-Celery](https://github.com/ask/flask-celery).

## [2.1.0](#id20)[¶](#version-2-1-0 "Link to this heading")

release-date:
:   2010-10-08 12:00 p.m. CEST

release-by:
:   Ask Solem

### [Important Notes](#id21)[¶](#important-notes "Link to this heading")

* Celery is now following the versioning semantics defined by [semver](http://semver.org).

  > This means we’re no longer allowed to use odd/even versioning semantics
  > By our previous versioning scheme this stable release should’ve
  > been version 2.2.

* Now depends on Carrot 0.10.7.
* No longer depends on SQLAlchemy, this needs to be installed separately
  if the database result backend is used.
* <https://pypi.org/project/django-celery/> now comes with a monitor for the Django Admin
  interface. This can also be used if you’re not a Django user.
  (Update: Django-Admin monitor has been replaced with Flower, see the
  Monitoring guide).
* If you get an error after upgrading saying:
  AttributeError: ‘module’ object has no attribute ‘system’,

  > Then this is because the celery.platform module has been
  > renamed to celery.platforms to not collide with the built-in
  > [`platform`](https://docs.python.org/dev/library/platform.html#module-platform "(in Python v3.15)") module.
  >
  > You have to remove the old `platform.py` (and maybe
  > `platform.pyc`) file from your previous Celery installation.
  >
  > To do this use **python** to find the location
  > of this module:
  >
  > ```
  > $ python
  > >>> import celery.platform
  > >>> celery.platform
  > <module 'celery.platform' from '/opt/devel/celery/celery/platform.pyc'>
  > ```
  >
  > Here the compiled module is in `/opt/devel/celery/celery/`,
  > to remove the offending files do:
  >
  > ```
  > $ rm -f /opt/devel/celery/celery/platform.py*
  > ```

### [News](#id22)[¶](#v210-news "Link to this heading")

* Added support for expiration of AMQP results (requires RabbitMQ 2.1.0)

  > The new configuration option `CELERY_AMQP_TASK_RESULT_EXPIRES`
  > sets the expiry time in seconds (can be int or float):
  >
  > ```
  > CELERY_AMQP_TASK_RESULT_EXPIRES = 30 * 60  # 30 minutes.
  > CELERY_AMQP_TASK_RESULT_EXPIRES = 0.80     # 800 ms.
  > ```
* `celeryev`: Event Snapshots

  > If enabled, the worker sends messages about what the worker is doing.
  > These messages are called “events”.
  > The events are used by real-time monitors to show what the
  > cluster is doing, but they’re not very useful for monitoring
  > over a longer period of time. Snapshots
  > lets you take “pictures” of the clusters state at regular intervals.
  > This can then be stored in a database to generate statistics
  > with, or even monitoring over longer time periods.
  >
  > <https://pypi.org/project/django-celery/> now comes with a Celery monitor for the Django
  > Admin interface. To use this you need to run the <https://pypi.org/project/django-celery/>
  > snapshot camera, which stores snapshots to the database at configurable
  > intervals.
  >
  > To use the Django admin monitor you need to do the following:
  >
  > 1. Create the new database tables:
  >
  >    > ```
  >    > $ python manage.py syncdb
  >    > ```
  > 2. Start the <https://pypi.org/project/django-celery/> snapshot camera:
  >
  >    > ```
  >    > $ python manage.py celerycam
  >    > ```
  > 3. Open up the django admin to monitor your cluster.
  >
  > The admin interface shows tasks, worker nodes, and even
  > lets you perform some actions, like revoking and rate limiting tasks,
  > and shutting down worker nodes.
  >
  > There’s also a Debian init.d script for [`events`](../reference/celery.bin.events.html#module-celery.bin.events "celery.bin.events") available,
  > see [Daemonization](../userguide/daemonizing.html#daemonizing) for more information.
  >
  > New command-line arguments to `celeryev`:
  >
  > > + [`celery events --camera`](../reference/cli.html#cmdoption-celery-events-c): Snapshot camera class to use.
  > > + [`celery events --logfile`](../reference/cli.html#cmdoption-celery-events-f): Log file
  > > + [`celery events --loglevel`](../reference/cli.html#cmdoption-celery-events-l): Log level
  > > + [`celery events --maxrate`](../reference/cli.html#cmdoption-celery-events-r): Shutter rate limit.
  > > + [`celery events --freq`](../reference/cli.html#cmdoption-celery-events-F): Shutter frequency
  >
  > The [`--camera`](../reference/cli.html#cmdoption-celery-events-c) argument is the name
  > of a class used to take snapshots with. It must support the interface
  > defined by [`celery.events.snapshot.Polaroid`](../internals/reference/celery.events.snapshot.html#celery.events.snapshot.Polaroid "celery.events.snapshot.Polaroid").
  >
  > Shutter frequency controls how often the camera thread wakes up,
  > while the rate limit controls how often it will actually take
  > a snapshot.
  > The rate limit can be an integer (snapshots/s), or a rate limit string
  > which has the same syntax as the task rate limit strings (“200/m”,
  > “10/s”, “1/h”, etc).
  >
  > For the Django camera case, this rate limit can be used to control
  > how often the snapshots are written to the database, and the frequency
  > used to control how often the thread wakes up to check if there’s
  > anything new.
  >
  > The rate limit is off by default, which means it will take a snapshot
  > for every [`--frequency`](../reference/cli.html#cmdoption-celery-events-F) seconds.
* `broadcast()`: Added callback argument, this can be
  used to process replies immediately as they arrive.
* `celeryctl`: New command line utility to manage and inspect worker nodes,
  apply tasks and inspect the results of tasks.

  > See also
  >
  > The [Management Command-line Utilities (inspect/control)](../userguide/monitoring.html#monitoring-control) section in the [User Guide](../userguide/index.html#guide).
  >
  > Some examples:
  >
  > ```
  > $ celeryctl apply tasks.add -a '[2, 2]' --countdown=10
  >
  > $ celeryctl inspect active
  > $ celeryctl inspect registered_tasks
  > $ celeryctl inspect scheduled
  > $ celeryctl inspect --help
  > $ celeryctl apply --help
  > ```
* Added the ability to set an expiry date and time for tasks.

  > Example:
  >
  > ```
  > >>> # Task expires after one minute from now.
  > >>> task.apply_async(args, kwargs, expires=60)
  > >>> # Also supports datetime
  > >>> task.apply_async(args, kwargs,
  > ...                  expires=datetime.now() + timedelta(days=1)
  > ```
  >
  > When a worker receives a task that’s been expired it will be
  > marked as revoked ([`TaskRevokedError`](../reference/celery.exceptions.html#celery.exceptions.TaskRevokedError "celery.exceptions.TaskRevokedError")).
* Changed the way logging is configured.

  > We now configure the root logger instead of only configuring
  > our custom logger. In addition we don’t hijack
  > the multiprocessing logger anymore, but instead use a custom logger name
  > for different applications:
  >
  > | **Application** | **Logger Name** |
  > | --- | --- |
  > | `celeryd` | `"celery"` |
  > | `celerybeat` | `"celery.beat"` |
  > | `celeryev` | `"celery.ev"` |
  >
  > This means that the loglevel and logfile arguments will
  > affect all registered loggers (even those from third-party libraries).
  > Unless you configure the loggers manually as shown below, that is.
  >
  > *Users can choose to configure logging by subscribing to the
  > :signal:`~celery.signals.setup\_logging` signal:*
  >
  > ```
  > from logging.config import fileConfig
  > from celery import signals
  >
  > @signals.setup_logging.connect
  > def setup_logging(**kwargs):
  >     fileConfig('logging.conf')
  > ```
  >
  > If there are no receivers for this signal, the logging subsystem
  > will be configured using the
  > [`--loglevel`](../reference/cli.html#cmdoption-celery-worker-l)/
  > [`--logfile`](../reference/cli.html#cmdoption-celery-worker-f)
  > arguments, this will be used for *all defined loggers*.
  >
  > Remember that the worker also redirects stdout and stderr
  > to the Celery logger, if manually configure logging
  > you also need to redirect the standard outs manually:
  >
  > ```
  >  from logging.config import fileConfig
  >  from celery import log
  >
  > def setup_logging(**kwargs):
  >      import logging
  >      fileConfig('logging.conf')
  >      stdouts = logging.getLogger('mystdoutslogger')
  >      log.redirect_stdouts_to_logger(stdouts, loglevel=logging.WARNING)
  > ```
* worker Added command line option
  [`--include`](../reference/cli.html#cmdoption-celery-worker-I):

  > A comma separated list of (task) modules to be imported.
  >
  > Example:
  >
  > ```
  > $ celeryd -I app1.tasks,app2.tasks
  > ```
* worker: now emits a warning if running as the root user (euid is 0).
* `celery.messaging.establish_connection()`: Ability to override defaults
  used using keyword argument “defaults”.
* worker: Now uses multiprocessing.freeze\_support() so that it should work
  with **py2exe**, **PyInstaller**, **cx\_Freeze**, etc.
* worker: Now includes more meta-data for the [`STARTED`](../userguide/tasks.html#std-state-STARTED) state: PID and
  host name of the worker that started the task.

  > See issue #181
* subtask: Merge additional keyword arguments to subtask() into task keyword
  arguments.

  > For example:
  >
  > ```
  > >>> s = subtask((1, 2), {'foo': 'bar'}, baz=1)
  > >>> s.args
  > (1, 2)
  > >>> s.kwargs
  > {'foo': 'bar', 'baz': 1}
  > ```
  >
  > See issue #182.
* worker: Now emits a warning if there’s already a worker node using the same
  name running on the same virtual host.
* AMQP result backend: Sending of results are now retried if the connection
  is down.
* AMQP result backend: result.get(): Wait for next state if state isn’t
  :   in `READY_STATES`.
* TaskSetResult now supports subscription.

  > ```
  > >>> res = TaskSet(tasks).apply_async()
  > >>> res[0].get()
  > ```
* Added Task.send\_error\_emails + Task.error\_whitelist, so these can
  be configured per task instead of just by the global setting.
* Added Task.store\_errors\_even\_if\_ignored, so it can be changed per Task,
  not just by the global setting.
* The Crontab scheduler no longer wakes up every second, but implements
  remaining\_estimate (*Optimization*).
* worker: Store [`FAILURE`](../userguide/tasks.html#std-state-FAILURE) result if the
  :   [`WorkerLostError`](../reference/celery.exceptions.html#celery.exceptions.WorkerLostError "celery.exceptions.WorkerLostError") exception occurs (worker process
      disappeared).
* worker: Store [`FAILURE`](../userguide/tasks.html#std-state-FAILURE) result if one of the \*TimeLimitExceeded
  exceptions occurs.
* Refactored the periodic task responsible for cleaning up results.

  > + The backend cleanup task is now only added to the schedule if
  >   :   `CELERY_TASK_RESULT_EXPIRES` is set.
  > + If the schedule already contains a periodic task named
  >   “celery.backend\_cleanup” it won’t change it, so the behavior of the
  >   backend cleanup task can be easily changed.
  > + The task is now run every day at 4:00 AM, rather than every day since
  >   the first time it was run (using Crontab schedule instead of
  >   run\_every)
  > + Renamed celery.task.builtins.DeleteExpiredTaskMetaTask
  >   :   -> `celery.task.builtins.backend_cleanup`
  > + The task itself has been renamed from “celery.delete\_expired\_task\_meta”
  >   to “celery.backend\_cleanup”
  >
  > See issue #134.
* Implemented AsyncResult.forget for SQLAlchemy/Memcached/Redis/Tokyo Tyrant
  backends (forget and remove task result).

  > See issue #184.
* `TaskSetResult.join`:
  Added ‘propagate=True’ argument.

  When set to `False` exceptions occurring in subtasks will
  not be re-raised.
* Added Task.update\_state(task\_id, state, meta)
  as a shortcut to task.backend.store\_result(task\_id, meta, state).

  > The backend interface is “private” and the terminology outdated,
  > so better to move this to `Task` so it can be
  > used.
* timer2: Set self.running=False in
  [`stop()`](../internals/reference/celery.utils.timer2.html#celery.utils.timer2.Timer.stop "celery.utils.timer2.Timer.stop") so it won’t try to join again on
  subsequent calls to stop().
* Log colors are now disabled by default on Windows.
* celery.platform renamed to [`celery.platforms`](../internals/reference/celery.platforms.html#module-celery.platforms "celery.platforms"), so it doesn’t
  collide with the built-in [`platform`](https://docs.python.org/dev/library/platform.html#module-platform "(in Python v3.15)") module.
* Exceptions occurring in Mediator+Pool callbacks are now caught and logged
  instead of taking down the worker.
* Redis result backend: Now supports result expiration using the Redis
  EXPIRE command.
* unit tests: Don’t leave threads running at tear down.
* worker: Task results shown in logs are now truncated to 46 chars.
* Task.\_\_name\_\_ is now an alias to self.\_\_class\_\_.\_\_name\_\_.
  :   This way tasks introspects more like regular functions.
* Task.retry: Now raises [`TypeError`](https://docs.python.org/dev/library/exceptions.html#TypeError "(in Python v3.15)") if kwargs argument is empty.

  > See issue #164.
* `timedelta_seconds`: Use `timedelta.total_seconds` if running on Python 2.7
* [`TokenBucket`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.utils.limits.html#kombu.utils.limits.TokenBucket "(in Kombu v5.6)"): Generic Token Bucket algorithm
* [`celery.events.state`](../reference/celery.events.state.html#module-celery.events.state "celery.events.state"): Recording of cluster state can now
  be paused and resumed, including support for buffering.

  > State.freeze(*buffer=True*)[¶](#State.freeze "Link to this definition")
  > :   Pauses recording of the stream.
  >
  >     If buffer is true, events received while being frozen will be
  >     buffered, and may be replayed later.
  >
  > State.thaw(*replay=True*)[¶](#State.thaw "Link to this definition")
  > :   Resumes recording of the stream.
  >
  >     If replay is true, then the recorded buffer will be applied.
  >
  > State.freeze\_while(*fun*)[¶](#State.freeze_while "Link to this definition")
  > :   With a function to apply, freezes the stream before,
  >     and replays the buffer after the function returns.
* [`EventReceiver.capture`](../reference/celery.events.html#celery.events.EventReceiver.capture "celery.events.EventReceiver.capture")
  Now supports a timeout keyword argument.
* worker: The mediator thread is now disabled if
  `CELERY_RATE_LIMITS` is enabled, and tasks are directly sent to the
  pool without going through the ready queue (*Optimization*).

### [Fixes](#id23)[¶](#v210-fixes "Link to this heading")

* Pool: Process timed out by TimeoutHandler must be joined by the Supervisor,
  so don’t remove it from the internal process list.

  > See issue #192.
* TaskPublisher.delay\_task now supports exchange argument, so exchange can be
  overridden when sending tasks in bulk using the same publisher

  > See issue #187.
* the worker no longer marks tasks as revoked if `CELERY_IGNORE_RESULT`
  is enabled.

  > See issue #207.
* AMQP Result backend: Fixed bug with result.get() if
  `CELERY_TRACK_STARTED` enabled.

  > result.get() would stop consuming after receiving the
  > [`STARTED`](../userguide/tasks.html#std-state-STARTED) state.
* Fixed bug where new processes created by the pool supervisor becomes stuck
  while reading from the task Queue.

  > See <http://bugs.python.org/issue10037>
* Fixed timing issue when declaring the remote control command reply queue

  > This issue could result in replies being lost, but have now been fixed.
* Backward compatible LoggerAdapter implementation: Now works for Python 2.4.

  > Also added support for several new methods:
  > fatal, makeRecord, \_log, log, isEnabledFor,
  > addHandler, removeHandler.

### [Experimental](#id24)[¶](#experimental "Link to this heading")

* multi: Added daemonization support.

  > multi can now be used to start, stop and restart worker nodes:
  >
  > ```
  > $ celeryd-multi start jerry elaine george kramer
  > ```
  >
  > This also creates PID files and log files (`celeryd@jerry.pid`,
  > …, `celeryd@jerry.log`. To specify a location for these files
  > use the –pidfile and –logfile arguments with the %n
  > format:
  >
  > ```
  > $ celeryd-multi start jerry elaine george kramer \
  >                 --logfile=/var/log/celeryd@%n.log \
  >                 --pidfile=/var/run/celeryd@%n.pid
  > ```
  >
  > Stopping:
  >
  > ```
  > $ celeryd-multi stop jerry elaine george kramer
  > ```
  >
  > Restarting. The nodes will be restarted one by one as the old ones
  > are shutdown:
  >
  > ```
  > $ celeryd-multi restart jerry elaine george kramer
  > ```
  >
  > Killing the nodes (**WARNING**: Will discard currently executing tasks):
  >
  > ```
  > $ celeryd-multi kill jerry elaine george kramer
  > ```
  >
  > See celeryd-multi help for help.
* multi: start command renamed to show.

  > celeryd-multi start will now actually start and detach worker nodes.
  > To just generate the commands you have to use celeryd-multi show.
* worker: Added –pidfile argument.

  > The worker will write its pid when it starts. The worker will
  > not be started if this file exists and the pid contained is still alive.
* Added generic init.d script using celeryd-multi

  > <https://github.com/celery/celery/tree/master/extra/generic-init.d/celeryd>

### [Documentation](#id25)[¶](#v210-documentation "Link to this heading")

* Added User guide section: Monitoring
* Added user guide section: Periodic Tasks

  > Moved from getting-started/periodic-tasks and updated.
* tutorials/external moved to new section: “community”.
* References has been added to all sections in the documentation.

  > This makes it easier to link between documents.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[Change history for Celery 2.2](changelog-2.2.html "previous chapter")

#### Next topic

[Change history for Celery 2.0](changelog-2.0.html "next chapter")

### This Page

* [Show Source](../_sources/history/changelog-2.1.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](changelog-2.0.html "Change history for Celery 2.0") |
* [previous](changelog-2.2.html "Change history for Celery 2.2") |
* [Celery 5.6.2 documentation](../index.html) »
* [History](index.html) »
* Change history for Celery 2.1

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
Change history for Celery 2.4 — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](changelog-2.3.html "Change history for Celery 2.3") |
* [previous](changelog-2.5.html "Change history for Celery 2.5") |
* [Celery 5.6.2 documentation](../index.html) »
* [History](index.html) »
* Change history for Celery 2.4

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/history/changelog-2.4.html).

# Change history for Celery 2.4[¶](#change-history-for-celery-2-4 "Link to this heading")

## [2.4.5](#id7)[¶](#version-2-4-5 "Link to this heading")

release-date:
:   2011-12-02 05:00 p.m. GMT

release-by:
:   Ask Solem

* Periodic task interval schedules were accidentally rounded down,
  resulting in some periodic tasks being executed early.
* Logging of humanized times in the beat log is now more detailed.
* New [Backends and Brokers](../getting-started/backends-and-brokers/index.html#brokers) section in the Getting Started part of the Documentation

  > This replaces the old “Other queues” tutorial, and adds
  > documentation for MongoDB, Beanstalk and CouchDB.

## [2.4.4](#id8)[¶](#version-2-4-4 "Link to this heading")

release-date:
:   2011-11-25 04:00 p.m. GMT

release-by:
:   Ask Solem

### [Security Fixes](#id9)[¶](#security-fixes "Link to this heading")

* [Security: [CELERYSA-0001](https://github.com/celery/celery/tree/master/docs/sec/CELERYSA-0001.txt)] Daemons would set effective id’s rather than
  real id’s when the `--uid`/
  `--gid` arguments to
  **celery multi**, **celeryd\_detach**,
  **celery beat** and **celery events** were used.

  This means privileges weren’t properly dropped, and that it would
  be possible to regain supervisor privileges later.

### [Fixes](#id10)[¶](#fixes "Link to this heading")

* Processes pool: Fixed rare deadlock at shutdown (Issue #523).

  > Fix contributed by Ionel Maries Christian.
* Webhook tasks issued the wrong HTTP POST headers (Issue #515).

  > The *Content-Type* header has been changed from
  > `application/json` ⇒ `application/x-www-form-urlencoded`,
  > and adds a proper *Content-Length* header.
  >
  > Fix contributed by Mitar.
* Daemonization tutorial: Adds a configuration example using Django and
  virtualenv together (Issue #505).

  > Contributed by Juan Ignacio Catalano.
* generic init-scripts now automatically creates log and pid file
  directories (Issue #545).

  > Contributed by Chris Streeter.

## [2.4.3](#id11)[¶](#version-2-4-3 "Link to this heading")

release-date:
:   2011-11-22 06:00 p.m. GMT

release-by:
:   Ask Solem

* Fixes module import typo in celeryctl (Issue #538).

  > Fix contributed by Chris Streeter.

## [2.4.2](#id12)[¶](#version-2-4-2 "Link to this heading")

release-date:
:   2011-11-14 12:00 p.m. GMT

release-by:
:   Ask Solem

* Program module no longer uses relative imports so that it’s
  possible to do `python -m celery.bin.name`.

## [2.4.1](#id13)[¶](#version-2-4-1 "Link to this heading")

release-date:
:   2011-11-07 06:00 p.m. GMT

release-by:
:   Ask Solem

* `celeryctl inspect` commands was missing output.
* processes pool: Decrease polling interval for less idle CPU usage.
* processes pool: MaybeEncodingError wasn’t wrapped in ExceptionInfo
  (Issue #524).
* worker: would silence errors occurring after task consumer started.
* logging: Fixed a bug where unicode in stdout redirected log messages
  couldn’t be written (Issue #522).

## [2.4.0](#id14)[¶](#version-2-4-0 "Link to this heading")

release-date:
:   2011-11-04 04:00 p.m. GMT

release-by:
:   Ask Solem

### [Important Notes](#id15)[¶](#important-notes "Link to this heading")

* Now supports Python 3.
* Fixed deadlock in worker process handling (Issue #496).

  > A deadlock could occur after spawning new child processes because
  > the logging library’s mutex wasn’t properly reset after fork.
  >
  > The symptoms of this bug affecting would be that the worker simply
  > stops processing tasks, as none of the workers child processes
  > are functioning. There was a greater chance of this bug occurring
  > with `maxtasksperchild` or a time-limit enabled.
  >
  > This is a workaround for <http://bugs.python.org/issue6721#msg140215>.
  >
  > Be aware that while this fixes the logging library lock,
  > there could still be other locks initialized in the parent
  > process, introduced by custom code.
  >
  > Fix contributed by Harm Verhagen.
* AMQP Result backend: Now expires results by default.

  > The default expiration value is now taken from the
  > `CELERY_TASK_RESULT_EXPIRES` setting.
  >
  > The old `CELERY_AMQP_TASK_RESULT_EXPIRES` setting has been
  > deprecated and will be removed in version 4.0.
  >
  > Note that this means that the result backend requires RabbitMQ 2.1.0 or
  > higher, and that you have to disable expiration if you’re running
  > with an older version. You can do so by disabling the
  > `CELERY_TASK_RESULT_EXPIRES` setting:
  >
  > ```
  > CELERY_TASK_RESULT_EXPIRES = None
  > ```
* Eventlet: Fixed problem with shutdown (Issue #457).
* Broker transports can be now be specified using URLs

  > The broker can now be specified as a URL instead.
  > This URL must have the format:
  >
  > ```
  > transport://user:password@hostname:port/virtual_host
  > ```
  >
  > for example the default broker is written as:
  >
  > ```
  > amqp://guest:guest@localhost:5672//
  > ```
  >
  > The scheme is required, so that the host is identified
  > as a URL and not just a host name.
  > User, password, port and virtual\_host are optional and
  > defaults to the particular transports default value.
  >
  > Note
  >
  > Note that the path component (virtual\_host) always starts with a
  > forward-slash. This is necessary to distinguish between the virtual
  > host `''` (empty) and `'/'`, which are both acceptable virtual
  > host names.
  >
  > A virtual host of `'/'` becomes:
  >
  > ```
  > amqp://guest:guest@localhost:5672//
  > ```
  >
  > and a virtual host of `''` (empty) becomes:
  >
  > ```
  > amqp://guest:guest@localhost:5672/
  > ```
  >
  > So the leading slash in the path component is **always required**.
  >
  > In addition the `BROKER_URL` setting has been added as an alias
  > to `BROKER_HOST`. Any broker setting specified in both the URL and in
  > the configuration will be ignored, if a setting isn’t provided in the URL
  > then the value from the configuration will be used as default.
  >
  > Also, programs now support the [`--broker`](../reference/cli.html#cmdoption-celery-b)
  > option to specify a broker URL on the command-line:
  >
  > ```
  > $ celery worker -b redis://localhost
  >
  > $ celery inspect -b amqp://guest:guest@localhost//e
  > ```
  >
  > The environment variable `CELERY_BROKER_URL` can also be used to
  > easily override the default broker used.
* The deprecated `celery.loaders.setup_loader()` function has been removed.
* The `CELERY_TASK_ERROR_WHITELIST` setting has been replaced
  by a more flexible approach (Issue #447).

  > The error mail sending logic is now available as `Task.ErrorMail`,
  > with the implementation (for reference) in `celery.utils.mail`.
  >
  > The error mail class can be sub-classed to gain complete control
  > of when error messages are sent, thus removing the need for a separate
  > white-list setting.
  >
  > The `CELERY_TASK_ERROR_WHITELIST` setting has been deprecated,
  > and will be removed completely in version 4.0.
* Additional Deprecations

  > The following functions has been deprecated and is scheduled for removal in
  > version 4.0:
  >
  > | **Old function** | **Alternative** |
  > | --- | --- |
  > | celery.loaders.current\_loader | celery.current\_app.loader |
  > | celery.loaders.load\_settings | celery.current\_app.conf |
  > | celery.execute.apply | Task.apply |
  > | celery.execute.apply\_async | Task.apply\_async |
  > | celery.execute.delay\_task | celery.execute.send\_task |
  >
  > The following settings has been deprecated and is scheduled for removal
  > in version 4.0:
  >
  > | **Old setting** | **Alternative** |
  > | --- | --- |
  > | CELERYD\_LOG\_LEVEL | `celery worker --loglevel=` |
  > | CELERYD\_LOG\_FILE | `celery worker --logfile=` |
  > | CELERYBEAT\_LOG\_LEVEL | `celery beat --loglevel=` |
  > | CELERYBEAT\_LOG\_FILE | `celery beat --logfile=` |
  > | CELERYMON\_LOG\_LEVEL | `celerymon --loglevel=` |
  > | CELERYMON\_LOG\_FILE | `celerymon --logfile=` |

### [News](#id16)[¶](#news "Link to this heading")

* No longer depends on <https://pypi.org/project/pyparsing/>.
* Now depends on Kombu 1.4.3.
* CELERY\_IMPORTS can now be a scalar value (Issue #485).

  > It’s too easy to forget to add the comma after the sole element of a
  > tuple, and this is something that often affects newcomers.
  >
  > The docs should probably use a list in examples, as using a tuple
  > for this doesn’t even make sense. Nonetheless, there are many
  > tutorials out there using a tuple, and this change should be a help
  > to new users.
  >
  > Suggested by [@jsaxon-cars](https://github.com/jsaxon-cars/).
* Fixed a memory leak when using the thread pool (Issue #486).

  > Contributed by Kornelijus Survila.
* The `statedb` wasn’t saved at exit.

  > This has now been fixed and it should again remember previously
  > revoked tasks when a `--statedb` is enabled.
* Adds [`EMAIL_USE_TLS`](http://docs.djangoproject.com/en/dev/ref/settings/#std-setting-EMAIL_USE_TLS "(in Django v6.1)") to enable secure SMTP connections
  (Issue #418).

  > Contributed by Stefan Kjartansson.
* Now handles missing fields in task messages as documented in the message
  format documentation.

  > + Missing required field throws [`InvalidTaskError`](../reference/celery.exceptions.html#celery.exceptions.InvalidTaskError "celery.exceptions.InvalidTaskError")
  > + Missing args/kwargs is assumed empty.
  >
  > Contributed by Chris Chamberlin.
* Fixed race condition in [`celery.events.state`](../reference/celery.events.state.html#module-celery.events.state "celery.events.state") (`celerymon`/`celeryev`)
  where task info would be removed while iterating over it (Issue #501).
* The Cache, Cassandra, MongoDB, Redis and Tyrant backends now respects
  the `CELERY_RESULT_SERIALIZER` setting (Issue #435).

  > This means that only the database (Django/SQLAlchemy) backends
  > currently doesn’t support using custom serializers.
  >
  > Contributed by Steeve Morin
* Logging calls no longer manually formats messages, but delegates
  that to the logging system, so tools like Sentry can easier
  work with the messages (Issue #445).

  > Contributed by Chris Adams.
* `multi` now supports a `stop_verify` command to wait for
  processes to shutdown.
* Cache backend didn’t work if the cache key was unicode (Issue #504).

  > Fix contributed by Neil Chintomby.
* New setting `CELERY_RESULT_DB_SHORT_LIVED_SESSIONS` added,
  which if enabled will disable the caching of SQLAlchemy sessions
  (Issue #449).

  > Contributed by Leo Dirac.
* All result backends now implements `__reduce__` so that they can
  be pickled (Issue #441).

  > Fix contributed by Remy Noel
* multi didn’t work on Windows (Issue #472).
* New-style `CELERY_REDIS_*` settings now takes precedence over
  the old `REDIS_*` configuration keys (Issue #508).

  > Fix contributed by Joshua Ginsberg
* Generic beat init-script no longer sets bash -e (Issue #510).

  > Fix contributed by Roger Hu.
* Documented that Chords don’t work well with **redis-server** versions
  before 2.2.

  > Contributed by Dan McGee.
* The `CELERYBEAT_MAX_LOOP_INTERVAL` setting wasn’t respected.
* `inspect.registered_tasks` renamed to `inspect.registered` for naming
  consistency.

  > The previous name is still available as an alias.
  >
  > Contributed by Mher Movsisyan
* Worker logged the string representation of args and kwargs
  without safe guards (Issue #480).
* RHEL init-script: Changed worker start-up priority.

  > The default start / stop priorities for MySQL on RHEL are:
  >
  > ```
  > # chkconfig: - 64 36
  > ```
  >
  > Therefore, if Celery is using a database as a broker / message store, it
  > should be started after the database is up and running, otherwise errors
  > will ensue. This commit changes the priority in the init-script to:
  >
  > ```
  > # chkconfig: - 85 15
  > ```
  >
  > which are the default recommended settings for 3-rd party applications
  > and assure that Celery will be started after the database service & shut
  > down before it terminates.
  >
  > Contributed by Yury V. Zaytsev.
* KeyValueStoreBackend.get\_many didn’t respect the `timeout` argument
  (Issue #512).
* beat/events’s `--workdir` option didn’t *chdir(2)* before after
  configuration was attempted (Issue #506).
* After deprecating 2.4 support we can now name modules correctly, since we
  can take use of absolute imports.

  > Therefore the following internal modules have been renamed:
  >
  > > `celery.concurrency.evlet` -> `celery.concurrency.eventlet`
  > > `celery.concurrency.evg` -> `celery.concurrency.gevent`
* `AUTHORS` file is now sorted alphabetically.

  > Also, as you may have noticed the contributors of new features/fixes are
  > now mentioned in the Changelog.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[Change history for Celery 2.5](changelog-2.5.html "previous chapter")

#### Next topic

[Change history for Celery 2.3](changelog-2.3.html "next chapter")

### This Page

* [Show Source](../_sources/history/changelog-2.4.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](changelog-2.3.html "Change history for Celery 2.3") |
* [previous](changelog-2.5.html "Change history for Celery 2.5") |
* [Celery 5.6.2 documentation](../index.html) »
* [History](index.html) »
* Change history for Celery 2.4

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
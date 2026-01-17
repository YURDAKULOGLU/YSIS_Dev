celery.contrib.pytest — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.sphinx.html "celery.contrib.sphinx") |
* [previous](celery.contrib.migrate.html "celery.contrib.migrate") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.pytest`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.pytest.html).

# `celery.contrib.pytest`[¶](#celery-contrib-pytest "Link to this heading")

## [API Reference](#id1)[¶](#module-celery.contrib.pytest "Link to this heading")

Fixtures and testing utilities for [pytest](https://pypi.org/project/pytest/).

celery.contrib.pytest.celery\_app(*request*, *celery\_config*, *celery\_parameters*, *celery\_enable\_logging*, *use\_celery\_app\_trap*)[[source]](../_modules/celery/contrib/pytest.html#celery_app)[¶](#celery.contrib.pytest.celery_app "Link to this definition")
:   Fixture creating a Celery application instance.

celery.contrib.pytest.celery\_class\_tasks()[[source]](../_modules/celery/contrib/pytest.html#celery_class_tasks)[¶](#celery.contrib.pytest.celery_class_tasks "Link to this definition")
:   Redefine this fixture to register tasks with the test Celery app.

celery.contrib.pytest.celery\_config() → [Mapping](https://docs.python.org/dev/library/typing.html#typing.Mapping "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")][[source]](../_modules/celery/contrib/pytest.html#celery_config)[¶](#celery.contrib.pytest.celery_config "Link to this definition")
:   Redefine this fixture to configure the test Celery app.

    The config returned by your fixture will then be used
    to configure the [`celery_app()`](#celery.contrib.pytest.celery_app "celery.contrib.pytest.celery_app") fixture.

celery.contrib.pytest.celery\_enable\_logging() → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")[[source]](../_modules/celery/contrib/pytest.html#celery_enable_logging)[¶](#celery.contrib.pytest.celery_enable_logging "Link to this definition")
:   You can override this fixture to enable logging.

celery.contrib.pytest.celery\_includes() → [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../_modules/celery/contrib/pytest.html#celery_includes)[¶](#celery.contrib.pytest.celery_includes "Link to this definition")
:   You can override this include modules when a worker start.

    You can have this return a list of module names to import,
    these can be task modules, modules registering signals, and so on.

celery.contrib.pytest.celery\_parameters() → [Mapping](https://docs.python.org/dev/library/typing.html#typing.Mapping "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")][[source]](../_modules/celery/contrib/pytest.html#celery_parameters)[¶](#celery.contrib.pytest.celery_parameters "Link to this definition")
:   Redefine this fixture to change the init parameters of test Celery app.

    The dict returned by your fixture will then be used
    as parameters when instantiating [`Celery`](celery.html#celery.Celery "celery.Celery").

celery.contrib.pytest.celery\_session\_app(*request: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *celery\_config: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *celery\_parameters: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *celery\_enable\_logging: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *use\_celery\_app\_trap: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")[[source]](../_modules/celery/contrib/pytest.html#celery_session_app)[¶](#celery.contrib.pytest.celery_session_app "Link to this definition")
:   Session Fixture: Return app for session fixtures.

celery.contrib.pytest.celery\_session\_worker(*request: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *celery\_session\_app: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*, *celery\_includes: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]*, *celery\_class\_tasks: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *celery\_worker\_pool: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *celery\_worker\_parameters: [Mapping](https://docs.python.org/dev/library/typing.html#typing.Mapping "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")]*) → [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")[[source]](../_modules/celery/contrib/pytest.html#celery_session_worker)[¶](#celery.contrib.pytest.celery_session_worker "Link to this definition")
:   Session Fixture: Start worker that lives throughout test suite.

celery.contrib.pytest.celery\_worker(*request: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*, *celery\_app: [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")*, *celery\_includes: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]*, *celery\_worker\_pool: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *celery\_worker\_parameters: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [object](https://docs.python.org/dev/library/functions.html#object "(in Python v3.15)")[[source]](../_modules/celery/contrib/pytest.html#celery_worker)[¶](#celery.contrib.pytest.celery_worker "Link to this definition")
:   Fixture: Start worker in a thread, stop it when the test returns.

celery.contrib.pytest.celery\_worker\_parameters() → [Mapping](https://docs.python.org/dev/library/typing.html#typing.Mapping "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")][[source]](../_modules/celery/contrib/pytest.html#celery_worker_parameters)[¶](#celery.contrib.pytest.celery_worker_parameters "Link to this definition")
:   Redefine this fixture to change the init parameters of Celery workers.

    This can be used e. g. to define queues the worker will consume tasks from.

    The dict returned by your fixture will then be used
    as parameters when instantiating [`WorkController`](celery.worker.html#celery.worker.WorkController "celery.worker.WorkController").

celery.contrib.pytest.celery\_worker\_pool() → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/contrib/pytest.html#celery_worker_pool)[¶](#celery.contrib.pytest.celery_worker_pool "Link to this definition")
:   You can override this fixture to set the worker pool.

    The “solo” pool is used by default, but you can set this to
    return e.g. “prefork”.

celery.contrib.pytest.depends\_on\_current\_app(*celery\_app*)[[source]](../_modules/celery/contrib/pytest.html#depends_on_current_app)[¶](#celery.contrib.pytest.depends_on_current_app "Link to this definition")
:   Fixture that sets app as current.

celery.contrib.pytest.pytest\_configure(*config*)[[source]](../_modules/celery/contrib/pytest.html#pytest_configure)[¶](#celery.contrib.pytest.pytest_configure "Link to this definition")
:   Register additional pytest configuration.

celery.contrib.pytest.use\_celery\_app\_trap() → [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)")[[source]](../_modules/celery/contrib/pytest.html#use_celery_app_trap)[¶](#celery.contrib.pytest.use_celery_app_trap "Link to this definition")
:   You can override this fixture to enable the app trap.

    The app trap raises an exception whenever something attempts
    to use the current or default apps.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.contrib.migrate`](celery.contrib.migrate.html "previous chapter")

#### Next topic

[celery.contrib.sphinx](celery.contrib.sphinx.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.contrib.pytest.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.sphinx.html "celery.contrib.sphinx") |
* [previous](celery.contrib.migrate.html "celery.contrib.migrate") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.pytest`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
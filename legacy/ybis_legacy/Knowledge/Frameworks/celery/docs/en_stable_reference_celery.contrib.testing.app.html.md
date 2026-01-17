celery.contrib.testing.app — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.testing.manager.html "celery.contrib.testing.manager") |
* [previous](celery.contrib.testing.worker.html "celery.contrib.testing.worker") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.testing.app`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.contrib.testing.app.html).

# `celery.contrib.testing.app`[¶](#celery-contrib-testing-app "Link to this heading")

## [API Reference](#id1)[¶](#module-celery.contrib.testing.app "Link to this heading")

Create Celery app instances used for testing.

celery.contrib.testing.app.DEFAULT\_TEST\_CONFIG *= {'accept\_content': {'json'}, 'broker\_heartbeat': 0, 'broker\_url': 'memory://', 'enable\_utc': True, 'result\_backend': 'cache+memory://', 'timezone': 'UTC', 'worker\_hijack\_root\_logger': False, 'worker\_log\_color': False}*[¶](#celery.contrib.testing.app.DEFAULT_TEST_CONFIG "Link to this definition")
:   Contains the default configuration values for the test app.

celery.contrib.testing.app.TestApp(*name=None*, *config=None*, *enable\_logging=False*, *set\_as\_current=False*, *log=<class 'celery.contrib.testing.app.UnitLogging'>*, *backend=None*, *broker=None*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/app.html#TestApp)[¶](#celery.contrib.testing.app.TestApp "Link to this definition")
:   App used for testing.

*class* celery.contrib.testing.app.Trap[[source]](../_modules/celery/contrib/testing/app.html#Trap)[¶](#celery.contrib.testing.app.Trap "Link to this definition")
:   Trap that pretends to be an app but raises an exception instead.

    This to protect from code that does not properly pass app instances,
    then falls back to the current\_app.

*class* celery.contrib.testing.app.UnitLogging(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/contrib/testing/app.html#UnitLogging)[¶](#celery.contrib.testing.app.UnitLogging "Link to this definition")
:   Sets up logging for the test application.

celery.contrib.testing.app.set\_trap(*app*)[[source]](../_modules/celery/contrib/testing/app.html#set_trap)[¶](#celery.contrib.testing.app.set_trap "Link to this definition")
:   Contextmanager that installs the trap app.

    The trap means that anything trying to use the current or default app
    will raise an exception.

celery.contrib.testing.app.setup\_default\_app(*app*, *use\_trap=False*)[[source]](../_modules/celery/contrib/testing/app.html#setup_default_app)[¶](#celery.contrib.testing.app.setup_default_app "Link to this definition")
:   Setup default app for testing.

    Ensures state is clean after the test returns.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.contrib.testing.worker`](celery.contrib.testing.worker.html "previous chapter")

#### Next topic

[`celery.contrib.testing.manager`](celery.contrib.testing.manager.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.contrib.testing.app.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.contrib.testing.manager.html "celery.contrib.testing.manager") |
* [previous](celery.contrib.testing.worker.html "celery.contrib.testing.worker") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.contrib.testing.app`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
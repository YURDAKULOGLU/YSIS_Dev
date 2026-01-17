celery.backends.database.session — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.html "celery.utils") |
* [previous](celery.backends.database.models.html "celery.backends.database.models") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.database.session`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.database.session.html).

# `celery.backends.database.session`[¶](#celery-backends-database-session "Link to this heading")

SQLAlchemy session.

*class* celery.backends.database.session.SessionManager[[source]](../../_modules/celery/backends/database/session.html#SessionManager)[¶](#celery.backends.database.session.SessionManager "Link to this definition")
:   Manage SQLAlchemy sessions.

    create\_session(*dburi*, *short\_lived\_sessions=False*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/database/session.html#SessionManager.create_session)[¶](#celery.backends.database.session.SessionManager.create_session "Link to this definition")

    get\_engine(*dburi*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/database/session.html#SessionManager.get_engine)[¶](#celery.backends.database.session.SessionManager.get_engine "Link to this definition")

    prepare\_models(*engine*)[[source]](../../_modules/celery/backends/database/session.html#SessionManager.prepare_models)[¶](#celery.backends.database.session.SessionManager.prepare_models "Link to this definition")

    session\_factory(*dburi*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/database/session.html#SessionManager.session_factory)[¶](#celery.backends.database.session.SessionManager.session_factory "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.database.models`](celery.backends.database.models.html "previous chapter")

#### Next topic

[`celery.utils`](celery.utils.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.database.session.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.html "celery.utils") |
* [previous](celery.backends.database.models.html "celery.backends.database.models") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.database.session`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
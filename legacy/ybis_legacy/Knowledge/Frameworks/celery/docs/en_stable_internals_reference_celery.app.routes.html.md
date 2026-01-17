celery.app.routes — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.security.certificate.html "celery.security.certificate") |
* [previous](celery.app.annotations.html "celery.app.annotations") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.app.routes`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.app.routes.html).

# `celery.app.routes`[¶](#celery-app-routes "Link to this heading")

Task Routing.

Contains utilities for working with task routers, ([`task_routes`](../../userguide/configuration.html#std-setting-task_routes)).

*class* celery.app.routes.MapRoute(*map*)[[source]](../../_modules/celery/app/routes.html#MapRoute)[¶](#celery.app.routes.MapRoute "Link to this definition")
:   Creates a router out of a [`dict`](https://docs.python.org/dev/library/stdtypes.html#dict "(in Python v3.15)").

*class* celery.app.routes.Router(*routes=None*, *queues=None*, *create\_missing=False*, *app=None*)[[source]](../../_modules/celery/app/routes.html#Router)[¶](#celery.app.routes.Router "Link to this definition")
:   Route tasks based on the [`task_routes`](../../userguide/configuration.html#std-setting-task_routes) setting.

    expand\_destination(*route*)[[source]](../../_modules/celery/app/routes.html#Router.expand_destination)[¶](#celery.app.routes.Router.expand_destination "Link to this definition")

    lookup\_route(*name*, *args=None*, *kwargs=None*, *options=None*, *task\_type=None*)[[source]](../../_modules/celery/app/routes.html#Router.lookup_route)[¶](#celery.app.routes.Router.lookup_route "Link to this definition")

    query\_router(*router*, *task*, *args*, *kwargs*, *options*, *task\_type*)[[source]](../../_modules/celery/app/routes.html#Router.query_router)[¶](#celery.app.routes.Router.query_router "Link to this definition")

    route(*options*, *name*, *args=()*, *kwargs=None*, *task\_type=None*)[[source]](../../_modules/celery/app/routes.html#Router.route)[¶](#celery.app.routes.Router.route "Link to this definition")

celery.app.routes.expand\_router\_string(*router*)[[source]](../../_modules/celery/app/routes.html#expand_router_string)[¶](#celery.app.routes.expand_router_string "Link to this definition")

celery.app.routes.prepare(*routes*)[[source]](../../_modules/celery/app/routes.html#prepare)[¶](#celery.app.routes.prepare "Link to this definition")
:   Expand the [`task_routes`](../../userguide/configuration.html#std-setting-task_routes) setting.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.app.annotations`](celery.app.annotations.html "previous chapter")

#### Next topic

[`celery.security.certificate`](celery.security.certificate.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.app.routes.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.security.certificate.html "celery.security.certificate") |
* [previous](celery.app.annotations.html "celery.app.annotations") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.app.routes`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
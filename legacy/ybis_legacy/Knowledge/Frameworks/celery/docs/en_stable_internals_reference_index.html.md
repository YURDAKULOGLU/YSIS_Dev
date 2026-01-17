Internal Module Reference — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.worker.components.html "celery.worker.components") |
* [previous](../app-overview.html "“The Big Instance” Refactor") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* Internal Module Reference

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/index.html).

# Internal Module Reference[¶](#internal-module-reference "Link to this heading")

Release:
:   5.6

Date:
:   Jan 04, 2026

* [`celery.worker.components`](celery.worker.components.html)
* [`celery.worker.loops`](celery.worker.loops.html)
* [`celery.worker.heartbeat`](celery.worker.heartbeat.html)
* [`celery.worker.control`](celery.worker.control.html)
* [`celery.worker.pidbox`](celery.worker.pidbox.html)
* [`celery.worker.autoscale`](celery.worker.autoscale.html)
* [`celery.concurrency`](celery.concurrency.html)
* [`celery.concurrency.solo`](celery.concurrency.solo.html)
* [`celery.concurrency.prefork`](celery.concurrency.prefork.html)
* [`celery.concurrency.eventlet`](celery.concurrency.eventlet.html)
* [`celery.concurrency.gevent`](celery.concurrency.gevent.html)
* [`celery.concurrency.thread`](celery.concurrency.thread.html)
* [`celery.concurrency.base`](celery.concurrency.base.html)
* [`celery.backends`](celery.backends.html)
* [`celery.backends.base`](celery.backends.base.html)
* [`celery.backends.asynchronous`](celery.backends.asynchronous.html)
* [`celery.backends.azureblockblob`](celery.backends.azureblockblob.html)
* [`celery.backends.rpc`](celery.backends.rpc.html)
* [`celery.backends.database`](celery.backends.database.html)
* [`celery.backends.cache`](celery.backends.cache.html)
* [celery.backends.consul](celery.backends.consul.html)
* [`celery.backends.couchdb`](celery.backends.couchdb.html)
* [`celery.backends.mongodb`](celery.backends.mongodb.html)
* [`celery.backends.elasticsearch`](celery.backends.elasticsearch.html)
* [`celery.backends.redis`](celery.backends.redis.html)
* [`celery.backends.cassandra`](celery.backends.cassandra.html)
* [`celery.backends.couchbase`](celery.backends.couchbase.html)
* [`celery.backends.arangodb`](celery.backends.arangodb.html)
* [`celery.backends.dynamodb`](celery.backends.dynamodb.html)
* [`celery.backends.filesystem`](celery.backends.filesystem.html)
* [`celery.backends.cosmosdbsql`](celery.backends.cosmosdbsql.html)
* [`celery.backends.s3`](celery.backends.s3.html)
* [`celery.backends.gcs`](celery.backends.gcs.html)
* [`celery.app.trace`](celery.app.trace.html)
* [`celery.app.annotations`](celery.app.annotations.html)
* [`celery.app.routes`](celery.app.routes.html)
* [`celery.security.certificate`](celery.security.certificate.html)
* [`celery.security.key`](celery.security.key.html)
* [`celery.security.serialization`](celery.security.serialization.html)
* [`celery.security.utils`](celery.security.utils.html)
* [`celery.events.snapshot`](celery.events.snapshot.html)
* [`celery.events.cursesmon`](celery.events.cursesmon.html)
* [`celery.events.dumper`](celery.events.dumper.html)
* [`celery.backends.database.models`](celery.backends.database.models.html)
* [`celery.backends.database.session`](celery.backends.database.session.html)
* [`celery.utils`](celery.utils.html)
* [`celery.utils.abstract`](celery.utils.abstract.html)
* [`celery.utils.collections`](celery.utils.collections.html)
* [`celery.utils.nodenames`](celery.utils.nodenames.html)
* [`celery.utils.deprecated`](celery.utils.deprecated.html)
* [`celery.utils.functional`](celery.utils.functional.html)
* [`celery.utils.graph`](celery.utils.graph.html)
* [`celery.utils.objects`](celery.utils.objects.html)
* [`celery.utils.term`](celery.utils.term.html)
* [`celery.utils.time`](celery.utils.time.html)
* [`celery.utils.iso8601`](celery.utils.iso8601.html)
* [`celery.utils.saferepr`](celery.utils.saferepr.html)
* [`celery.utils.serialization`](celery.utils.serialization.html)
* [`celery.utils.sysinfo`](celery.utils.sysinfo.html)
* [`celery.utils.threads`](celery.utils.threads.html)
* [`celery.utils.timer2`](celery.utils.timer2.html)
* [`celery.utils.imports`](celery.utils.imports.html)
* [`celery.utils.log`](celery.utils.log.html)
* [`celery.utils.text`](celery.utils.text.html)
* [`celery.utils.dispatch`](celery.utils.dispatch.html)
* [`celery.utils.dispatch.signal`](celery.utils.dispatch.signal.html)
* [`celery.platforms`](celery.platforms.html)
* [`celery._state`](celery._state.html)

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[“The Big Instance” Refactor](../app-overview.html "previous chapter")

#### Next topic

[`celery.worker.components`](celery.worker.components.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/index.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.worker.components.html "celery.worker.components") |
* [previous](../app-overview.html "“The Big Instance” Refactor") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* Internal Module Reference

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
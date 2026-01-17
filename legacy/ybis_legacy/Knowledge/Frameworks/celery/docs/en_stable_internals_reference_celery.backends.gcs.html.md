celery.backends.gcs — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.app.trace.html "celery.app.trace") |
* [previous](celery.backends.s3.html "celery.backends.s3") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.gcs`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.gcs.html).

# `celery.backends.gcs`[¶](#celery-backends-gcs "Link to this heading")

Google Cloud Storage result store backend for Celery.

*class* celery.backends.gcs.GCSBackend(*\*\*kwargs*)[[source]](../../_modules/celery/backends/gcs.html#GCSBackend)[¶](#celery.backends.gcs.GCSBackend "Link to this definition")
:   Google Cloud Storage task result backend.

    Uses Firestore for chord ref count.

    *property* firestore\_client[¶](#celery.backends.gcs.GCSBackend.firestore_client "Link to this definition")
    :   Returns a firestore client.

    implements\_incr *= True*[¶](#celery.backends.gcs.GCSBackend.implements_incr "Link to this definition")

    incr(*key: [bytes](https://docs.python.org/dev/library/stdtypes.html#bytes "(in Python v3.15)")*) → [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")[[source]](../../_modules/celery/backends/gcs.html#GCSBackend.incr)[¶](#celery.backends.gcs.GCSBackend.incr "Link to this definition")

    on\_chord\_part\_return(*request*, *state*, *result*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/gcs.html#GCSBackend.on_chord_part_return)[¶](#celery.backends.gcs.GCSBackend.on_chord_part_return "Link to this definition")
    :   Chord part return callback.

        Called for each task in the chord.
        Increments the counter stored in Firestore.
        If the counter reaches the number of tasks in the chord, the callback
        is called.
        If the callback raises an exception, the chord is marked as errored.
        If the callback returns a value, the chord is marked as successful.

    supports\_native\_join *= True*[¶](#celery.backends.gcs.GCSBackend.supports_native_join "Link to this definition")
    :   If true the backend must implement `get_many()`.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.s3`](celery.backends.s3.html "previous chapter")

#### Next topic

[`celery.app.trace`](celery.app.trace.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.gcs.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.app.trace.html "celery.app.trace") |
* [previous](celery.backends.s3.html "celery.backends.s3") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.gcs`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
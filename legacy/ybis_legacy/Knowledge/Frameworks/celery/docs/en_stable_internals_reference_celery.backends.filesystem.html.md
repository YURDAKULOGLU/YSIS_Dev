celery.backends.filesystem — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.cosmosdbsql.html "celery.backends.cosmosdbsql") |
* [previous](celery.backends.dynamodb.html "celery.backends.dynamodb") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.filesystem`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.backends.filesystem.html).

# `celery.backends.filesystem`[¶](#celery-backends-filesystem "Link to this heading")

File-system result store backend.

*class* celery.backends.filesystem.FilesystemBackend(*url=None*, *open=<built-in function open>*, *unlink=<built-in function unlink>*, *sep='/'*, *encoding='UTF-8'*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend)[¶](#celery.backends.filesystem.FilesystemBackend "Link to this definition")
:   File-system result backend.

    Parameters:
    :   * **url** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – URL to the directory we should use
        * **open** (*Callable*) – open function to use when opening files
        * **unlink** (*Callable*) – unlink function to use when deleting files
        * **sep** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – directory separator (to join the directory with the key)
        * **encoding** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – encoding used on the file-system

    cleanup()[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.cleanup)[¶](#celery.backends.filesystem.FilesystemBackend.cleanup "Link to this definition")
    :   Delete expired meta-data.

    delete(*key*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.delete)[¶](#celery.backends.filesystem.FilesystemBackend.delete "Link to this definition")

    get(*key*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.get)[¶](#celery.backends.filesystem.FilesystemBackend.get "Link to this definition")

    mget(*keys*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.mget)[¶](#celery.backends.filesystem.FilesystemBackend.mget "Link to this definition")

    set(*key*, *value*)[[source]](../../_modules/celery/backends/filesystem.html#FilesystemBackend.set)[¶](#celery.backends.filesystem.FilesystemBackend.set "Link to this definition")

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.dynamodb`](celery.backends.dynamodb.html "previous chapter")

#### Next topic

[`celery.backends.cosmosdbsql`](celery.backends.cosmosdbsql.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.backends.filesystem.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.backends.cosmosdbsql.html "celery.backends.cosmosdbsql") |
* [previous](celery.backends.dynamodb.html "celery.backends.dynamodb") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.backends.filesystem`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
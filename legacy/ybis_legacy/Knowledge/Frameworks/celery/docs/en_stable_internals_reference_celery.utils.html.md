celery.utils — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.abstract.html "celery.utils.abstract") |
* [previous](celery.backends.database.session.html "celery.backends.database.session") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.html).

# `celery.utils`[¶](#celery-utils "Link to this heading")

Utility functions.

Don’t import from here directly anymore, as these are only
here for backwards compatibility.

*class* celery.utils.cached\_property(*fget=None*, *fset=None*, *fdel=None*)[[source]](../../_modules/kombu/utils/objects.html#cached_property)[¶](#celery.utils.cached_property "Link to this definition")
:   Implementation of Cached property.

    deleter(*fdel*)[[source]](../../_modules/kombu/utils/objects.html#cached_property.deleter)[¶](#celery.utils.cached_property.deleter "Link to this definition")

    setter(*fset*)[[source]](../../_modules/kombu/utils/objects.html#cached_property.setter)[¶](#celery.utils.cached_property.setter "Link to this definition")

celery.utils.chunks(*it*, *n*)[[source]](../../_modules/celery/utils/functional.html#chunks)[¶](#celery.utils.chunks "Link to this definition")
:   Split an iterator into chunks with n elements each.

    Warning

    `it` must be an actual iterator, if you pass this a
    concrete sequence will get you repeating elements.

    So `chunks(iter(range(1000)), 10)` is fine, but
    `chunks(range(1000), 10)` is not.

    Example

    # n == 2
    >>> x = chunks(iter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 2)
    >>> list(x)
    [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10]]

    # n == 3
    >>> x = chunks(iter([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 3)
    >>> list(x)
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10]]

celery.utils.gen\_task\_name(*app*, *name*, *module\_name*)[[source]](../../_modules/celery/utils/imports.html#gen_task_name)[¶](#celery.utils.gen_task_name "Link to this definition")
:   Generate task name from name/module pair.

celery.utils.gen\_unique\_id(*\_uuid: ~typing.Callable[[]*, *~uuid.UUID] = <function uuid4>*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[¶](#celery.utils.gen_unique_id "Link to this definition")
:   Generate unique id in UUID4 format.

celery.utils.get\_cls\_by\_name(*name*, *aliases=None*, *imp=None*, *package=None*, *sep='.'*, *default=None*, *\*\*kwargs*)[¶](#celery.utils.get_cls_by_name "Link to this definition")
:   Get symbol by qualified name.

    The name should be the full dot-separated path to the class:

    ```
    modulename.ClassName
    ```

    Example:

    ```
    celery.concurrency.processes.TaskPool
                                ^- class name
    ```

    or using ‘:’ to separate module and symbol:

    ```
    celery.concurrency.processes:TaskPool
    ```

    If aliases is provided, a dict containing short name/long name
    mappings, the name is looked up in the aliases first.

    Examples

    ```
    >>> symbol_by_name('celery.concurrency.processes.TaskPool')
    <class 'celery.concurrency.processes.TaskPool'>
    ```

    ```
    >>> symbol_by_name('default', {
    ...     'default': 'celery.concurrency.processes.TaskPool'})
    <class 'celery.concurrency.processes.TaskPool'>
    ```

    # Does not try to look up non-string names.
    >>> from celery.concurrency.processes import TaskPool
    >>> symbol\_by\_name(TaskPool) is TaskPool
    True

celery.utils.get\_full\_cls\_name(*obj*)[¶](#celery.utils.get_full_cls_name "Link to this definition")
:   Return object name.

celery.utils.import\_from\_cwd(*module*, *imp=None*, *package=None*)[[source]](../../_modules/celery/utils/imports.html#import_from_cwd)[¶](#celery.utils.import_from_cwd "Link to this definition")
:   Import module, temporarily including modules in the current directory.

    Modules located in the current directory has
    precedence over modules located in sys.path.

celery.utils.instantiate(*name*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/imports.html#instantiate)[¶](#celery.utils.instantiate "Link to this definition")
:   Instantiate class by name.

    See also

    `symbol_by_name()`.

celery.utils.memoize(*maxsize=None*, *keyfun=None*, *Cache=<class 'kombu.utils.functional.LRUCache'>*)[[source]](../../_modules/kombu/utils/functional.html#memoize)[¶](#celery.utils.memoize "Link to this definition")
:   Decorator to cache function return value.

celery.utils.nodename(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*, *hostname: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/nodenames.html#nodename)[¶](#celery.utils.nodename "Link to this definition")
:   Create node name from name/hostname pair.

celery.utils.nodesplit(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*) → [tuple](https://docs.python.org/dev/library/stdtypes.html#tuple "(in Python v3.15)")[[None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)"), [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")] | [list](https://docs.python.org/dev/library/stdtypes.html#list "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")][[source]](../../_modules/celery/utils/nodenames.html#nodesplit)[¶](#celery.utils.nodesplit "Link to this definition")
:   Split node name into tuple of name/hostname.

celery.utils.noop(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/functional.html#noop)[¶](#celery.utils.noop "Link to this definition")
:   No operation.

    Takes any arguments/keyword arguments and does nothing.

celery.utils.uuid(*\_uuid: ~typing.Callable[[]*, *~uuid.UUID] = <function uuid4>*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/kombu/utils/uuid.html#uuid)[¶](#celery.utils.uuid "Link to this definition")
:   Generate unique id in UUID4 format.

celery.utils.worker\_direct(*hostname: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [Queue](celery.backends.rpc.html#celery.backends.rpc.RPCBackend.Queue "celery.backends.rpc.RPCBackend.Queue")*) → [Queue](celery.backends.rpc.html#celery.backends.rpc.RPCBackend.Queue "celery.backends.rpc.RPCBackend.Queue")[[source]](../../_modules/celery/utils/nodenames.html#worker_direct)[¶](#celery.utils.worker_direct "Link to this definition")
:   Return the [`kombu.Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") being a direct route to a worker.

    Parameters:
    :   **hostname** ([*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")*,* [*Queue*](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)")) – The fully qualified node name of
        a worker (e.g., `w1@example.com`). If passed a
        [`kombu.Queue`](https://docs.celeryq.dev/projects/kombu/en/main/reference/kombu.html#kombu.Queue "(in Kombu v5.6)") instance it will simply return
        that instead.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.backends.database.session`](celery.backends.database.session.html "previous chapter")

#### Next topic

[`celery.utils.abstract`](celery.utils.abstract.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.abstract.html "celery.utils.abstract") |
* [previous](celery.backends.database.session.html "celery.backends.database.session") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
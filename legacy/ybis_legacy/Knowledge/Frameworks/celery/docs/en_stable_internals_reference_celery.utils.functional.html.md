celery.utils.functional — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.graph.html "celery.utils.graph") |
* [previous](celery.utils.deprecated.html "celery.utils.deprecated") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.functional`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.functional.html).

# `celery.utils.functional`[¶](#celery-utils-functional "Link to this heading")

Functional-style utilities.

*class* celery.utils.functional.LRUCache(*limit=None*)[[source]](../../_modules/kombu/utils/functional.html#LRUCache)[¶](#celery.utils.functional.LRUCache "Link to this definition")
:   LRU Cache implementation using a doubly linked list to track access.

    ## Arguments:[¶](#arguments "Link to this heading")

    > limit (int): The maximum number of keys to keep in the cache.
    > :   When a new key is inserted and the limit has been exceeded,
    >     the *Least Recently Used* key will be discarded from the
    >     cache.

    incr(*key*, *delta=1*)[[source]](../../_modules/kombu/utils/functional.html#LRUCache.incr)[¶](#celery.utils.functional.LRUCache.incr "Link to this definition")

    items() → a set-like object providing a view on D's items[¶](#celery.utils.functional.LRUCache.items "Link to this definition")

    iteritems()[¶](#celery.utils.functional.LRUCache.iteritems "Link to this definition")

    iterkeys()[¶](#celery.utils.functional.LRUCache.iterkeys "Link to this definition")

    itervalues()[¶](#celery.utils.functional.LRUCache.itervalues "Link to this definition")

    keys() → a set-like object providing a view on D's keys[¶](#celery.utils.functional.LRUCache.keys "Link to this definition")

    popitem() → (k, v), remove and return some (key, value) pair[[source]](../../_modules/kombu/utils/functional.html#LRUCache.popitem)[¶](#celery.utils.functional.LRUCache.popitem "Link to this definition")
    :   as a 2-tuple; but raise KeyError if D is empty.

    update([*E*, ]*\*\*F*) → None.  Update D from mapping/iterable E and F.[[source]](../../_modules/kombu/utils/functional.html#LRUCache.update)[¶](#celery.utils.functional.LRUCache.update "Link to this definition")
    :   If E present and has a .keys() method, does: for k in E: D[k] = E[k]
        If E present and lacks .keys() method, does: for (k, v) in E: D[k] = v
        In either case, this is followed by: for k, v in F.items(): D[k] = v

    values() → an object providing a view on D's values[¶](#celery.utils.functional.LRUCache.values "Link to this definition")

celery.utils.functional.chunks(*it*, *n*)[[source]](../../_modules/celery/utils/functional.html#chunks)[¶](#celery.utils.functional.chunks "Link to this definition")
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

celery.utils.functional.dictfilter(*d=None*, *\*\*kw*)[[source]](../../_modules/kombu/utils/functional.html#dictfilter)[¶](#celery.utils.functional.dictfilter "Link to this definition")
:   Remove all keys from dict `d` whose value is `None`.

celery.utils.functional.first(*predicate*, *it*)[[source]](../../_modules/celery/utils/functional.html#first)[¶](#celery.utils.functional.first "Link to this definition")
:   Return the first element in `it` that `predicate` accepts.

    If `predicate` is None it will return the first item that’s not
    `None`.

celery.utils.functional.firstmethod(*method*, *on\_call=None*)[[source]](../../_modules/celery/utils/functional.html#firstmethod)[¶](#celery.utils.functional.firstmethod "Link to this definition")
:   Multiple dispatch.

    Return a function that with a list of instances,
    finds the first instance that gives a value for the given method.

    The list can also contain lazy instances
    ([`lazy`](#celery.utils.functional.lazy "kombu.utils.functional.lazy").)

celery.utils.functional.fun\_accepts\_kwargs(*fun*)[[source]](../../_modules/celery/utils/functional.html#fun_accepts_kwargs)[¶](#celery.utils.functional.fun_accepts_kwargs "Link to this definition")
:   Return true if function accepts arbitrary keyword arguments.

celery.utils.functional.head\_from\_fun(*fun: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[...], [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")]*, *bound: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*) → [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")[[source]](../../_modules/celery/utils/functional.html#head_from_fun)[¶](#celery.utils.functional.head_from_fun "Link to this definition")
:   Generate signature function from actual function.

celery.utils.functional.is\_list(*obj*, *scalars=(<class 'collections.abc.Mapping'>*, *<class 'str'>)*, *iters=(<class 'collections.abc.Iterable'>*, *)*)[[source]](../../_modules/kombu/utils/functional.html#is_list)[¶](#celery.utils.functional.is_list "Link to this definition")
:   Return true if the object is iterable.

    ## Note:[¶](#note "Link to this heading")

    > Returns false if object is a mapping or string.

*class* celery.utils.functional.lazy(*fun*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/kombu/utils/functional.html#lazy)[¶](#celery.utils.functional.lazy "Link to this definition")
:   Holds lazy evaluation.

    Evaluated when called or if the [`evaluate()`](#celery.utils.functional.lazy.evaluate "celery.utils.functional.lazy.evaluate") method is called.
    The function is re-evaluated on every call.

    Overloaded operations that will evaluate the promise:
    :   `__str__()`, `__repr__()`, `__cmp__()`.

    evaluate()[[source]](../../_modules/kombu/utils/functional.html#lazy.evaluate)[¶](#celery.utils.functional.lazy.evaluate "Link to this definition")

celery.utils.functional.mattrgetter(*\*attrs*)[[source]](../../_modules/celery/utils/functional.html#mattrgetter)[¶](#celery.utils.functional.mattrgetter "Link to this definition")
:   Get attributes, ignoring attribute errors.

    Like [`operator.itemgetter()`](https://docs.python.org/dev/library/operator.html#operator.itemgetter "(in Python v3.15)") but return `None` on missing
    attributes instead of raising [`AttributeError`](https://docs.python.org/dev/library/exceptions.html#AttributeError "(in Python v3.15)").

celery.utils.functional.maybe(*typ*, *val*)[[source]](../../_modules/celery/utils/functional.html#maybe)[¶](#celery.utils.functional.maybe "Link to this definition")
:   Call typ on value if val is defined.

celery.utils.functional.maybe\_evaluate(*value*)[[source]](../../_modules/kombu/utils/functional.html#maybe_evaluate)[¶](#celery.utils.functional.maybe_evaluate "Link to this definition")
:   Evaluate value only if value is a [`lazy`](#celery.utils.functional.lazy "celery.utils.functional.lazy") instance.

celery.utils.functional.maybe\_list(*obj*, *scalars=(<class 'collections.abc.Mapping'>*, *<class 'str'>)*)[[source]](../../_modules/kombu/utils/functional.html#maybe_list)[¶](#celery.utils.functional.maybe_list "Link to this definition")
:   Return list of one element if `l` is a scalar.

celery.utils.functional.memoize(*maxsize=None*, *keyfun=None*, *Cache=<class 'kombu.utils.functional.LRUCache'>*)[[source]](../../_modules/kombu/utils/functional.html#memoize)[¶](#celery.utils.functional.memoize "Link to this definition")
:   Decorator to cache function return value.

*class* celery.utils.functional.mlazy(*fun*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/functional.html#mlazy)[¶](#celery.utils.functional.mlazy "Link to this definition")
:   Memoized lazy evaluation.

    The function is only evaluated once, every subsequent access
    will return the same value.

    evaluate()[[source]](../../_modules/celery/utils/functional.html#mlazy.evaluate)[¶](#celery.utils.functional.mlazy.evaluate "Link to this definition")

    evaluated *= False*[¶](#celery.utils.functional.mlazy.evaluated "Link to this definition")
    :   Set to `True` after the object has been evaluated.

celery.utils.functional.noop(*\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/functional.html#noop)[¶](#celery.utils.functional.noop "Link to this definition")
:   No operation.

    Takes any arguments/keyword arguments and does nothing.

celery.utils.functional.padlist(*container*, *size*, *default=None*)[[source]](../../_modules/celery/utils/functional.html#padlist)[¶](#celery.utils.functional.padlist "Link to this definition")
:   Pad list with default elements.

    Example

    ```
    >>> first, last, city = padlist(['George', 'Costanza', 'NYC'], 3)
    ('George', 'Costanza', 'NYC')
    >>> first, last, city = padlist(['George', 'Costanza'], 3)
    ('George', 'Costanza', None)
    >>> first, last, city, planet = padlist(
    ...     ['George', 'Costanza', 'NYC'], 4, default='Earth',
    ... )
    ('George', 'Costanza', 'NYC', 'Earth')
    ```

celery.utils.functional.regen(*it*)[[source]](../../_modules/celery/utils/functional.html#regen)[¶](#celery.utils.functional.regen "Link to this definition")
:   Convert iterator to an object that can be consumed multiple times.

    `Regen` takes any iterable, and if the object is an
    generator it will cache the evaluated list on first access,
    so that the generator can be “consumed” multiple times.

celery.utils.functional.uniq(*it*)[[source]](../../_modules/celery/utils/functional.html#uniq)[¶](#celery.utils.functional.uniq "Link to this definition")
:   Return all unique elements in `it`, preserving order.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.utils.deprecated`](celery.utils.deprecated.html "previous chapter")

#### Next topic

[`celery.utils.graph`](celery.utils.graph.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.functional.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.graph.html "celery.utils.graph") |
* [previous](celery.utils.deprecated.html "celery.utils.deprecated") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.functional`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
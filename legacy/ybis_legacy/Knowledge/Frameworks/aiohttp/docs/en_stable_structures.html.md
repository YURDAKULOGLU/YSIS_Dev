Common data structures — aiohttp 3.13.3 documentation

# Common data structures[¶](#module-aiohttp "Link to this heading")

Common data structures used by *aiohttp* internally.

## FrozenList[¶](#frozenlist "Link to this heading")

A list-like structure which implements
[`collections.abc.MutableSequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableSequence "(in Python v3.14)").

The list is *mutable* unless [`FrozenList.freeze()`](#aiohttp.FrozenList.freeze "aiohttp.FrozenList.freeze") is called,
after that the list modification raises [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)").

class aiohttp.FrozenList(*items*)[¶](#aiohttp.FrozenList "Link to this definition")
:   Construct a new *non-frozen* list from *items* iterable.

    The list implements all [`collections.abc.MutableSequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableSequence "(in Python v3.14)")
    methods plus two additional APIs.

    frozen[¶](#aiohttp.FrozenList.frozen "Link to this definition")
    :   A read-only property, `True` is the list is *frozen*
        (modifications are forbidden).

    freeze()[¶](#aiohttp.FrozenList.freeze "Link to this definition")
    :   Freeze the list. There is no way to *thaw* it back.

## ChainMapProxy[¶](#chainmapproxy "Link to this heading")

An *immutable* version of [`collections.ChainMap`](https://docs.python.org/3/library/collections.html#collections.ChainMap "(in Python v3.14)"). Internally
the proxy is a list of mappings (dictionaries), if the requested key
is not present in the first mapping the second is looked up and so on.

The class supports [`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") interface.

class aiohttp.ChainMapProxy(*maps*)[[source]](_modules/aiohttp/helpers.html#ChainMapProxy)[¶](#aiohttp.ChainMapProxy "Link to this definition")
:   Create a new chained mapping proxy from a list of mappings (*maps*).

    Added in version 3.2.

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
* [Utilities](utilities.html)
  + [Abstract Base Classes](abc.html)
  + [Working with Multipart](multipart.html)
  + [Multipart reference](multipart_reference.html)
  + [Streaming API](streams.html)
  + [Common data structures](#)
  + [WebSocket utilities](websocket_utilities.html)
* [FAQ](faq.html)
* [Miscellaneous](misc.html)
* [Who uses aiohttp?](external.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/structures.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
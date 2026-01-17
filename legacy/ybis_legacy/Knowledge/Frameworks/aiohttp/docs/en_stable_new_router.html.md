Router refactoring in 0.21 — aiohttp 3.13.3 documentation

# Router refactoring in 0.21[¶](#router-refactoring-in-0-21 "Link to this heading")

## Rationale[¶](#rationale "Link to this heading")

First generation (v1) of router has mapped `(method, path)` pair to
[web-handler](glossary.html#term-web-handler). Mapping is named **route**. Routes used to have
unique names if any.

The main mistake with the design is coupling the **route** to
`(method, path)` pair while really URL construction operates with
**resources** (**location** is a synonym). HTTP method is not part of URI
but applied on sending HTTP request only.

Having different **route names** for the same path is confusing. Moreover
**named routes** constructed for the same path should have unique
non overlapping names which is cumbersome is certain situations.

From other side sometimes it’s desirable to bind several HTTP methods
to the same web handler. For *v1* router it can be solved by passing ‘\*’
as HTTP method. Class based views require ‘\*’ method also usually.

## Implementation[¶](#implementation "Link to this heading")

The change introduces **resource** as first class citizen:

```
resource = router.add_resource('/path/{to}', name='name')
```

*Resource* has a **path** (dynamic or constant) and optional **name**.

The name is **unique** in router context.

*Resource* has **routes**.

*Route* corresponds to *HTTP method* and [web-handler](glossary.html#term-web-handler) for the method:

```
route = resource.add_route('GET', handler)
```

User still may use wildcard for accepting all HTTP methods (maybe we
will add something like `resource.add_wildcard(handler)` later).

Since **names** belongs to **resources** now `app.router['name']`
returns a **resource** instance instead of [`aiohttp.web.AbstractRoute`](web_reference.html#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute").

**resource** has `.url()` method, so
`app.router['name'].url(parts={'a': 'b'}, query={'arg': 'param'})`
still works as usual.

The change allows to rewrite static file handling and implement nested
applications as well.

Decoupling of *HTTP location* and *HTTP method* makes life easier.

## Backward compatibility[¶](#backward-compatibility "Link to this heading")

The refactoring is 99% compatible with previous implementation.

99% means all example and the most of current code works without
modifications but we have subtle API backward incompatibles.

`app.router['name']` returns a [`aiohttp.web.AbstractResource`](web_reference.html#aiohttp.web.AbstractResource "aiohttp.web.AbstractResource")
instance instead of [`aiohttp.web.AbstractRoute`](web_reference.html#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") but resource has the
same `resource.url(...)` most useful method, so end user should feel no
difference.

`route.match(...)` is **not** supported anymore, use
[`aiohttp.web.AbstractResource.resolve()`](web_reference.html#aiohttp.web.AbstractResource.resolve "aiohttp.web.AbstractResource.resolve") instead.

`app.router.add_route(method, path, handler, name='name')` now is just
shortcut for:

```
resource = app.router.add_resource(path, name=name)
route = resource.add_route(method, handler)
return route
```

`app.router.register_route(...)` is still supported, it creates
`aiohttp.web.ResourceAdapter` for every call (but it’s deprecated now).

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
* [Utilities](utilities.html)
* [FAQ](faq.html)
* [Miscellaneous](misc.html)
  + [Essays](essays.html)
  + [Glossary](glossary.html)
  + [Changelog](changes.html)
  + [Indices and tables](misc.html#indices-and-tables)
* [Who uses aiohttp?](external.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/new_router.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
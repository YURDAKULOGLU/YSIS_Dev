What’s new in aiohttp 1.1 — aiohttp 3.13.3 documentation

# What’s new in aiohttp 1.1[¶](#what-s-new-in-aiohttp-1-1 "Link to this heading")

## YARL and URL encoding[¶](#yarl-and-url-encoding "Link to this heading")

Since aiohttp 1.1 the library uses [yarl](glossary.html#term-yarl) for URL processing.

### New API[¶](#new-api "Link to this heading")

[`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") gives handy methods for URL operations etc.

Client API still accepts [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") everywhere *url* is used,
e.g. `session.get('http://example.com')` works as well as
`session.get(yarl.URL('http://example.com'))`.

Internal API has been switched to [`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)").
[`aiohttp.CookieJar`](client_reference.html#aiohttp.CookieJar "aiohttp.CookieJar") accepts [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") instances only.

On server side has added [`aiohttp.web.BaseRequest.url`](web_reference.html#aiohttp.web.BaseRequest.url "aiohttp.web.BaseRequest.url") and
[`aiohttp.web.BaseRequest.rel_url`](web_reference.html#aiohttp.web.BaseRequest.rel_url "aiohttp.web.BaseRequest.rel_url") properties for representing relative and
absolute request’s URL.

URL using is the recommended way, already existed properties for
retrieving URL parts are deprecated and will be eventually removed.

Redirection web exceptions accepts [`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") as *location*
parameter. [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") is still supported and will be supported forever.

Reverse URL processing for *router* has been changed.

The main API is `aiohttp.web.Request.url_for`
which returns a [`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") instance for named resource. It
does not support *query args* but adding *args* is trivial:
`request.url_for('named_resource', param='a').with_query(arg='val')`.

The method returns a *relative* URL, absolute URL may be constructed by
`request.url.join(request.url_for(...)` call.

### URL encoding[¶](#url-encoding "Link to this heading")

YARL encodes all non-ASCII symbols on [`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") creation.

Thus `URL('https://www.python.org/путь')` becomes
`'https://www.python.org/%D0%BF%D1%83%D1%82%D1%8C'`.

On filling route table it’s possible to use both non-ASCII and percent
encoded paths:

```
app.router.add_get('/путь', handler)
```

and:

```
app.router.add_get('/%D0%BF%D1%83%D1%82%D1%8C', handler)
```

are the same. Internally `'/путь'` is converted into
percent-encoding representation.

Route matching also accepts both URL forms: raw and encoded by
converting the route pattern to *canonical* (encoded) form on route
registration.

## Sub-Applications[¶](#sub-applications "Link to this heading")

Sub applications are designed for solving the problem of the big
monolithic code base.
Let’s assume we have a project with own business logic and tools like
administration panel and debug toolbar.

Administration panel is a separate application by its own nature but all
toolbar URLs are served by prefix like `/admin`.

Thus we’ll create a totally separate application named `admin` and
connect it to main app with prefix:

```
admin = web.Application()
# setup admin routes, signals and middlewares

app.add_subapp('/admin/', admin)
```

Middlewares and signals from `app` and `admin` are chained.

It means that if URL is `'/admin/something'` middlewares from
`app` are applied first and `admin.middlewares` are the next in
the call chain.

The same is going for
[`on_response_prepare`](web_reference.html#aiohttp.web.Application.on_response_prepare "aiohttp.web.Application.on_response_prepare") signal – the
signal is delivered to both top level `app` and `admin` if
processing URL is routed to `admin` sub-application.

Common signals like [`on_startup`](web_reference.html#aiohttp.web.Application.on_startup "aiohttp.web.Application.on_startup"),
[`on_shutdown`](web_reference.html#aiohttp.web.Application.on_shutdown "aiohttp.web.Application.on_shutdown") and
[`on_cleanup`](web_reference.html#aiohttp.web.Application.on_cleanup "aiohttp.web.Application.on_cleanup") are delivered to all
registered sub-applications. The passed parameter is sub-application
instance, not top-level application.

Third level sub-applications can be nested into second level ones –
there are no limitation for nesting level.

### Url reversing[¶](#url-reversing "Link to this heading")

Url reversing for sub-applications should generate urls with proper prefix.

But for getting URL sub-application’s router should be used:

```
admin = web.Application()
admin.add_get('/resource', handler, name='name')

app.add_subapp('/admin/', admin)

url = admin.router['name'].url_for()
```

The generated `url` from example will have a value
`URL('/admin/resource')`.

## Application freezing[¶](#application-freezing "Link to this heading")

Application can be used either as main app (`app.make_handler()`) or as
sub-application – not both cases at the same time.

After connecting application by `.add_subapp()` call or starting
serving web-server as toplevel application the application is
**frozen**.

It means that registering new routes, signals and middlewares is
forbidden. Changing state (`app['name'] = 'value'`) of frozen application is
deprecated and will be eventually removed.

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
[Page source](_sources/whats_new_1_1.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
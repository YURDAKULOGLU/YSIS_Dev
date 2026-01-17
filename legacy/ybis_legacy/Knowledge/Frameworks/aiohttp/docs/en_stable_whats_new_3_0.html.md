What’s new in aiohttp 3.0 — aiohttp 3.13.3 documentation

# What’s new in aiohttp 3.0[¶](#what-s-new-in-aiohttp-3-0 "Link to this heading")

## async/await everywhere[¶](#async-await-everywhere "Link to this heading")

The main change is dropping `yield from` support and using
`async`/`await` everywhere. Farewell, Python 3.4.

The minimal supported Python version is **3.5.3** now.

Why not *3.5.0*? Because *3.5.3* has a crucial change:
[`asyncio.get_event_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_event_loop "(in Python v3.14)") returns the running loop instead of
*default*, which may be different, e.g.:

```
loop = asyncio.new_event_loop()
loop.run_until_complete(f())
```

Note, [`asyncio.set_event_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.set_event_loop "(in Python v3.14)") was not called and default loop
is not equal to actually executed one.

## Application Runners[¶](#application-runners "Link to this heading")

People constantly asked about ability to run aiohttp servers together
with other asyncio code, but [`aiohttp.web.run_app()`](web_reference.html#aiohttp.web.run_app "aiohttp.web.run_app") is blocking
synchronous call.

aiohttp had support for starting the application without `run_app` but the API
was very low-level and cumbersome.

Now application runners solve the task in a few lines of code, see
[Application runners](web_advanced.html#aiohttp-web-app-runners) for details.

## Client Tracing[¶](#client-tracing "Link to this heading")

Other long awaited feature is tracing client request life cycle to
figure out when and why client request spends a time waiting for
connection establishment, getting server response headers etc.

Now it is possible by registering special signal handlers on every
request processing stage. [Client Tracing](client_advanced.html#aiohttp-client-tracing) provides more
info about the feature.

## HTTPS support[¶](#https-support "Link to this heading")

Unfortunately asyncio has a bug with checking SSL certificates for
non-ASCII site DNS names, e.g. <https://историк.рф> or
<https://雜草工作室.香港>.

The bug has been fixed in upcoming Python 3.7 only (the change
requires breaking backward compatibility in [`ssl`](https://docs.python.org/3/library/ssl.html#module-ssl "(in Python v3.14)") API).

aiohttp installs a fix for older Python versions (3.5 and 3.6).

## Dropped obsolete API[¶](#dropped-obsolete-api "Link to this heading")

A switch to new major version is a great chance for dropping already
deprecated features.

The release dropped a lot, see [Changelog](changes.html#aiohttp-changes) for details.

All removals was already marked as deprecated or related to very low
level implementation details.

If user code did not raise [`DeprecationWarning`](https://docs.python.org/3/library/exceptions.html#DeprecationWarning "(in Python v3.14)") it is compatible
with aiohttp 3.0 most likely.

## Summary[¶](#summary "Link to this heading")

Enjoy aiohttp 3.0 release!

The full change log is here: [Changelog](changes.html#aiohttp-changes).

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
[Page source](_sources/whats_new_3_0.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
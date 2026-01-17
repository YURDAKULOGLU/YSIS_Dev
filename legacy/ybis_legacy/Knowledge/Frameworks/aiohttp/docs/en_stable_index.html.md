Welcome to AIOHTTP — aiohttp 3.13.3 documentation

# Welcome to AIOHTTP[¶](#welcome-to-aiohttp "Link to this heading")

Asynchronous HTTP Client/Server for [asyncio](glossary.html#term-asyncio) and Python.

Current version is 3.13.3.

## Key Features[¶](#key-features "Link to this heading")

* Supports both [Client](client.html#aiohttp-client) and [HTTP Server](web.html#aiohttp-web).
* Supports both [Server WebSockets](web_quickstart.html#aiohttp-web-websockets) and
  [Client WebSockets](client_quickstart.html#aiohttp-client-websockets) out-of-the-box
  without the Callback Hell.
* Web-server has [Middlewares](web_advanced.html#aiohttp-web-middlewares),
  [Signals](web_advanced.html#aiohttp-web-signals) and pluggable routing.
* Client supports [middleware](client_advanced.html#aiohttp-client-middleware) for
  customizing request/response processing.

## Library Installation[¶](#library-installation "Link to this heading")

```
$ pip install aiohttp
```

For speeding up DNS resolving by client API you may install
[aiodns](glossary.html#term-aiodns) as well.
This option is highly recommended:

```
$ pip install aiodns
```

### Installing all speedups in one command[¶](#installing-all-speedups-in-one-command "Link to this heading")

The following will get you `aiohttp` along with [aiodns](glossary.html#term-aiodns) and `Brotli` in one
bundle.
No need to type separate commands anymore!

```
$ pip install aiohttp[speedups]
```

## Getting Started[¶](#getting-started "Link to this heading")

### Client example[¶](#client-example "Link to this heading")

```
import aiohttp
import asyncio

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")

asyncio.run(main())
```

This prints:

```
Status: 200
Content-type: text/html; charset=utf-8
Body: <!doctype html> ...
```

Coming from [requests](glossary.html#term-requests) ? Read [why we need so many lines](http_request_lifecycle.html#aiohttp-request-lifecycle).

### Server example:[¶](#server-example "Link to this heading")

```
from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app)
```

For more information please visit [Client](client.html#aiohttp-client) and
[Server](web.html#aiohttp-web) pages.

## Development mode[¶](#development-mode "Link to this heading")

When writing your code, we recommend enabling Python’s
[development mode](https://docs.python.org/3/library/devmode.html)
(`python -X dev`). In addition to the extra features enabled for asyncio, aiohttp
will:

* Use a strict parser in the client code (which can help detect malformed responses
  from a server).
* Enable some additional checks (resulting in warnings in certain situations).

## What’s new in aiohttp 3?[¶](#what-s-new-in-aiohttp-3 "Link to this heading")

Go to [What’s new in aiohttp 3.0](whats_new_3_0.html#aiohttp-whats-new-3-0) page for aiohttp 3.0 major release
changes.

## Tutorial[¶](#tutorial "Link to this heading")

[Polls tutorial](https://aiohttp-demos.readthedocs.io/en/latest/index.html#aiohttp-demos-polls-beginning "(in aiohttp-demos v0.2)")

## Source code[¶](#source-code "Link to this heading")

The project is hosted on [GitHub](https://github.com/aio-libs/aiohttp)

Please feel free to file an issue on the [bug tracker](https://github.com/aio-libs/aiohttp/issues) if you have found a bug
or have some suggestion in order to improve the library.

## Dependencies[¶](#dependencies "Link to this heading")

* *attrs*
* *multidict*
* *yarl*
* *Optional* [aiodns](glossary.html#term-aiodns) for fast DNS resolving. The
  library is highly recommended.

  ```
  $ pip install aiodns
  ```
* *Optional* [Brotli](glossary.html#term-Brotli) or [brotlicffi](glossary.html#term-brotlicffi) for brotli ([**RFC 7932**](https://datatracker.ietf.org/doc/html/rfc7932.html))
  client compression support.

  ```
  $ pip install Brotli
  ```

## Communication channels[¶](#communication-channels "Link to this heading")

*aio-libs Discussions*: <https://github.com/aio-libs/aiohttp/discussions>

Feel free to post your questions and ideas here.

*Matrix*: [#aio-libs:matrix.org](https://matrix.to/#/#aio-libs:matrix.org)

We support [Stack Overflow](https://stackoverflow.com/questions/tagged/aiohttp).
Please add *aiohttp* tag to your question there.

## Contributing[¶](#contributing "Link to this heading")

Please read the [instructions for contributors](contributing.html#aiohttp-contributing)
before making a Pull Request.

## Authors and License[¶](#authors-and-license "Link to this heading")

The `aiohttp` package is written mostly by Nikolay Kim and Andrew Svetlov.

It’s *Apache 2* licensed and freely available.

Feel free to improve this package and send a pull request to [GitHub](https://github.com/aio-libs/aiohttp).

## Policy for Backward Incompatible Changes[¶](#policy-for-backward-incompatible-changes "Link to this heading")

*aiohttp* keeps backward compatibility.

After deprecating some *Public API* (method, class, function argument,
etc.) the library guaranties the usage of *deprecated API* is still
allowed at least for a year and half after publishing new release with
deprecation.

All deprecations are reflected in documentation and raises
[`DeprecationWarning`](https://docs.python.org/3/library/exceptions.html#DeprecationWarning "(in Python v3.14)").

Sometimes we are forced to break the own rule for sake of very strong
reason. Most likely the reason is a critical bug which cannot be
solved without major API change, but we are working hard for keeping
these changes as rare as possible.

## Table Of Contents[¶](#table-of-contents "Link to this heading")

* [Client](client.html)
  + [Quickstart](client_quickstart.html)
  + [Advanced Usage](client_advanced.html)
  + [Client Middleware Cookbook](client_middleware_cookbook.html)
  + [Reference](client_reference.html)
  + [Tracing Reference](tracing_reference.html)
  + [The aiohttp Request Lifecycle](http_request_lifecycle.html)
* [Server](web.html)
  + [Tutorial](https://demos.aiohttp.org)
  + [Quickstart](web_quickstart.html)
  + [Advanced Usage](web_advanced.html)
  + [Low Level](web_lowlevel.html)
  + [Reference](web_reference.html)
  + [Logging](logging.html)
  + [Testing](testing.html)
  + [Deployment](deployment.html)
* [Utilities](utilities.html)
  + [Abstract Base Classes](abc.html)
  + [Working with Multipart](multipart.html)
  + [Multipart reference](multipart_reference.html)
  + [Streaming API](streams.html)
  + [Common data structures](structures.html)
  + [WebSocket utilities](websocket_utilities.html)
* [FAQ](faq.html)
  + [Are there plans for an @app.route decorator like in Flask?](faq.html#are-there-plans-for-an-app-route-decorator-like-in-flask)
  + [Does aiohttp have a concept like Flask’s “blueprint” or Django’s “app”?](faq.html#does-aiohttp-have-a-concept-like-flask-s-blueprint-or-django-s-app)
  + [How do I create a route that matches urls with a given prefix?](faq.html#how-do-i-create-a-route-that-matches-urls-with-a-given-prefix)
  + [Where do I put my database connection so handlers can access it?](faq.html#where-do-i-put-my-database-connection-so-handlers-can-access-it)
  + [How can middleware store data for web handlers to use?](faq.html#how-can-middleware-store-data-for-web-handlers-to-use)
  + [Can a handler receive incoming events from different sources in parallel?](faq.html#can-a-handler-receive-incoming-events-from-different-sources-in-parallel)
  + [How do I programmatically close a WebSocket server-side?](faq.html#how-do-i-programmatically-close-a-websocket-server-side)
  + [How do I make a request from a specific IP address?](faq.html#how-do-i-make-a-request-from-a-specific-ip-address)
  + [What is the API stability and deprecation policy?](faq.html#what-is-the-api-stability-and-deprecation-policy)
  + [How do I enable gzip compression globally for my entire application?](faq.html#how-do-i-enable-gzip-compression-globally-for-my-entire-application)
  + [How do I manage a ClientSession within a web server?](faq.html#how-do-i-manage-a-clientsession-within-a-web-server)
  + [How do I access database connections from a subapplication?](faq.html#how-do-i-access-database-connections-from-a-subapplication)
  + [How do I perform operations in a request handler after sending the response?](faq.html#how-do-i-perform-operations-in-a-request-handler-after-sending-the-response)
  + [How do I make sure my custom middleware response will behave correctly?](faq.html#how-do-i-make-sure-my-custom-middleware-response-will-behave-correctly)
  + [Why is creating a ClientSession outside of an event loop dangerous?](faq.html#why-is-creating-a-clientsession-outside-of-an-event-loop-dangerous)
* [Miscellaneous](misc.html)
  + [Essays](essays.html)
  + [Glossary](glossary.html)
  + [Changelog](changes.html)
  + [Indices and tables](misc.html#indices-and-tables)
* [Who uses aiohttp?](external.html)
  + [Third-Party libraries](third_party.html)
  + [Built with aiohttp](built_with.html)
  + [Powered by aiohttp](powered_by.html)
* [Contributing](contributing.html)
  + [Instructions for contributors](contributing.html#instructions-for-contributors)
  + [Preconditions for running aiohttp test suite](contributing.html#preconditions-for-running-aiohttp-test-suite)
  + [LLHTTP](contributing.html#llhttp)
  + [Run autoformatter](contributing.html#run-autoformatter)
  + [Run aiohttp test suite](contributing.html#run-aiohttp-test-suite)
  + [Code coverage](contributing.html#code-coverage)
  + [Other tools](contributing.html#other-tools)
  + [Documentation](contributing.html#documentation)
  + [Spell checking](contributing.html#spell-checking)
  + [Preparing a pull request](contributing.html#preparing-a-pull-request)
  + [Changelog update](contributing.html#changelog-update)
  + [Making a pull request](contributing.html#making-a-pull-request)
  + [Backporting](contributing.html#backporting)
  + [How to become an aiohttp committer](contributing.html#how-to-become-an-aiohttp-committer)

[![Logo of aiohttp](_static/aiohttp-plain.svg)](#)

# [aiohttp](#)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
* [Utilities](utilities.html)
* [FAQ](faq.html)
* [Miscellaneous](misc.html)
* [Who uses aiohttp?](external.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/index.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
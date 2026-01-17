Low Level Server — aiohttp 3.13.3 documentation

# Low Level Server[¶](#low-level-server "Link to this heading")

This topic describes [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") based *low level* API.

## Abstract[¶](#abstract "Link to this heading")

Sometimes user don’t need high-level concepts introduced in
[Server](web.html#aiohttp-web): applications, routers, middlewares and signals.

All what is needed is supporting asynchronous callable which accepts a
request and returns a response object.

This is done by introducing [`aiohttp.web.Server`](web_reference.html#aiohttp.web.Server "aiohttp.web.Server") class which
serves a *protocol factory* role for
[`asyncio.loop.create_server()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_server "(in Python v3.14)") and bridges data
stream to *web handler* and sends result back.

Low level *web handler* should accept the single [`BaseRequest`](web_reference.html#aiohttp.web.BaseRequest "aiohttp.web.BaseRequest")
parameter and performs one of the following actions:

> 1. Return a [`Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response") with the whole HTTP body stored in memory.
> 2. Create a [`StreamResponse`](web_reference.html#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse"), send headers by
>    [`StreamResponse.prepare()`](web_reference.html#aiohttp.web.StreamResponse.prepare "aiohttp.web.StreamResponse.prepare") call, send data chunks by
>    [`StreamResponse.write()`](web_reference.html#aiohttp.web.StreamResponse.write "aiohttp.web.StreamResponse.write") and return finished response.
> 3. Raise [`HTTPException`](web_reference.html#aiohttp.web.HTTPException "aiohttp.web.HTTPException") derived exception (see
>    [Exceptions](web_quickstart.html#aiohttp-web-exceptions) section).
>
>    All other exceptions not derived from [`HTTPException`](web_reference.html#aiohttp.web.HTTPException "aiohttp.web.HTTPException")
>    leads to *500 Internal Server Error* response.
> 4. Initiate and process Web-Socket connection by
>    [`WebSocketResponse`](web_reference.html#aiohttp.web.WebSocketResponse "aiohttp.web.WebSocketResponse") using (see [WebSockets](web_quickstart.html#aiohttp-web-websockets)).

## Run a Basic Low-Level Server[¶](#run-a-basic-low-level-server "Link to this heading")

The following code demonstrates very trivial usage example:

```
import asyncio
from aiohttp import web


async def handler(request):
    return web.Response(text="OK")


async def main():
    server = web.Server(handler)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    print("======= Serving on http://127.0.0.1:8080/ ======")

    # pause here for very long time by serving HTTP requests and
    # waiting for keyboard interruption
    await asyncio.sleep(100*3600)


asyncio.run(main())
```

In the snippet we have `handler` which returns a regular
[`Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response") with `"OK"` in BODY.

This *handler* is processed by `server` ([`Server`](web_reference.html#aiohttp.web.Server "aiohttp.web.Server") which acts
as *protocol factory*). Network communication is created by
[runners API](web_reference.html#aiohttp-web-app-runners-reference) to serve
`http://127.0.0.1:8080/`.

The handler should process every request for every *path*, e.g.
`GET`, `POST`, Web-Socket.

The example is very basic: it always return `200 OK` response, real
life code is much more complex usually.

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
  + [Tutorial](https://demos.aiohttp.org)
  + [Quickstart](web_quickstart.html)
  + [Advanced Usage](web_advanced.html)
  + [Low Level](#)
  + [Reference](web_reference.html)
  + [Logging](logging.html)
  + [Testing](testing.html)
  + [Deployment](deployment.html)
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
[Page source](_sources/web_lowlevel.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
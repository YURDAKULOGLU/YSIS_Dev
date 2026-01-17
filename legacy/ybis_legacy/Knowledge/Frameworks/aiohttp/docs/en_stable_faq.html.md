FAQ — aiohttp 3.13.3 documentation

# FAQ[¶](#faq "Link to this heading")

## [Are there plans for an @app.route decorator like in Flask?](#id1)[¶](#are-there-plans-for-an-app-route-decorator-like-in-flask "Link to this heading")

As of aiohttp 2.3, [`RouteTableDef`](web_reference.html#aiohttp.web.RouteTableDef "aiohttp.web.RouteTableDef") provides an API
similar to Flask’s `@app.route`. See
[Alternative ways for registering routes](web_quickstart.html#aiohttp-web-alternative-routes-definition).

Unlike Flask’s `@app.route`, [`RouteTableDef`](web_reference.html#aiohttp.web.RouteTableDef "aiohttp.web.RouteTableDef")
does not require an `app` in the module namespace (which often leads
to circular imports).

Instead, a [`RouteTableDef`](web_reference.html#aiohttp.web.RouteTableDef "aiohttp.web.RouteTableDef") is decoupled from an application instance:

```
routes = web.RouteTableDef()

@routes.get('/get')
async def handle_get(request):
    ...


@routes.post('/post')
async def handle_post(request):
    ...

app.router.add_routes(routes)
```

## [Does aiohttp have a concept like Flask’s “blueprint” or Django’s “app”?](#id2)[¶](#does-aiohttp-have-a-concept-like-flask-s-blueprint-or-django-s-app "Link to this heading")

If you’re writing a large application, you may want to consider
using [nested applications](web_advanced.html#aiohttp-web-nested-applications), which
are similar to Flask’s “blueprints” or Django’s “apps”.

See: [Nested applications](web_advanced.html#aiohttp-web-nested-applications).

## [How do I create a route that matches urls with a given prefix?](#id3)[¶](#how-do-i-create-a-route-that-matches-urls-with-a-given-prefix "Link to this heading")

You can do something like the following:

```
app.router.add_route('*', '/path/to/{tail:.+}', sink_handler)
```

The first argument, `*`, matches any HTTP method
(*GET, POST, OPTIONS*, etc). The second argument matches URLS with the desired prefix.
The third argument is the handler function.

## [Where do I put my database connection so handlers can access it?](#id4)[¶](#where-do-i-put-my-database-connection-so-handlers-can-access-it "Link to this heading")

[`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") object supports the [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")
interface and provides a place to store your database connections or any
other resource you want to share between handlers.

```
db_key = web.AppKey("db_key", DB)

async def go(request):
    db = request.app[db_key]
    cursor = await db.cursor()
    await cursor.execute('SELECT 42')
    # ...
    return web.Response(status=200, text='ok')


async def init_app(loop):
    app = Application(loop=loop)
    db = await create_connection(user='user', password='123')
    app[db_key] = db
    app.router.add_get('/', go)
    return app
```

## [How can middleware store data for web handlers to use?](#id5)[¶](#how-can-middleware-store-data-for-web-handlers-to-use "Link to this heading")

Both [`aiohttp.web.Request`](web_reference.html#aiohttp.web.Request "aiohttp.web.Request") and [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application")
support the [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") interface.

Therefore, data may be stored inside a request object.

```
async def handler(request):
    request['unique_key'] = data
```

See <https://github.com/aio-libs/aiohttp_session> code for an example.
The `aiohttp_session.get_session(request)` method uses `SESSION_KEY`
for saving request-specific session information.

As of aiohttp 3.0, all response objects are dict-like structures as
well.

## [Can a handler receive incoming events from different sources in parallel?](#id6)[¶](#can-a-handler-receive-incoming-events-from-different-sources-in-parallel "Link to this heading")

Yes.

As an example, we may have two event sources:

> 1. WebSocket for events from an end user
> 2. Redis PubSub for events from other parts of the application

The most native way to handle this is to create a separate task for
PubSub handling.

Parallel [`aiohttp.web.WebSocketResponse.receive()`](web_reference.html#aiohttp.web.WebSocketResponse.receive "aiohttp.web.WebSocketResponse.receive") calls are forbidden;
a single task should perform WebSocket reading.
However, other tasks may use the same WebSocket object for sending data to
peers.

```
async def handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    task = asyncio.create_task(
        read_subscription(ws, request.app[redis_key]))
    try:
        async for msg in ws:
            # handle incoming messages
            # use ws.send_str() to send data back
            ...

    finally:
        task.cancel()

async def read_subscription(ws, redis):
    channel, = await redis.subscribe('channel:1')

    try:
        async for msg in channel.iter():
            answer = process_the_message(msg)  # your function here
            await ws.send_str(answer)
    finally:
        await redis.unsubscribe('channel:1')
```

## [How do I programmatically close a WebSocket server-side?](#id7)[¶](#how-do-i-programmatically-close-a-websocket-server-side "Link to this heading")

Let’s say we have an application with two endpoints:

> 1. `/echo` a WebSocket echo server that authenticates the user
> 2. `/logout_user` that, when invoked, closes all open
>    WebSockets for that user.

One simple solution is to keep a shared registry of WebSocket
responses for a user in the [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") instance
and call [`aiohttp.web.WebSocketResponse.close()`](web_reference.html#aiohttp.web.WebSocketResponse.close "aiohttp.web.WebSocketResponse.close") on all of them in
`/logout_user` handler:

```
async def echo_handler(request):

    ws = web.WebSocketResponse()
    user_id = authenticate_user(request)
    await ws.prepare(request)
    request.app[websockets_key][user_id].add(ws)
    try:
        async for msg in ws:
            ws.send_str(msg.data)
    finally:
        request.app[websockets_key][user_id].remove(ws)

    return ws


async def logout_handler(request):

    user_id = authenticate_user(request)

    ws_closers = [ws.close()
                  for ws in request.app[websockets_key][user_id]
                  if not ws.closed]

    # Watch out, this will keep us from returning the response
    # until all are closed
    ws_closers and await asyncio.gather(*ws_closers)

    return web.Response(text='OK')


def main():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/echo', echo_handler)
    app.router.add_route('POST', '/logout', logout_handler)
    app[websockets_key] = defaultdict(set)
    web.run_app(app, host='localhost', port=8080)
```

## [How do I make a request from a specific IP address?](#id8)[¶](#how-do-i-make-a-request-from-a-specific-ip-address "Link to this heading")

If your system has several IP interfaces, you may choose one which will
be used used to bind a socket locally:

```
conn = aiohttp.TCPConnector(local_addr=('127.0.0.1', 0), loop=loop)
async with aiohttp.ClientSession(connector=conn) as session:
    ...
```

See also

[`aiohttp.TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") and `local_addr` parameter.

## [What is the API stability and deprecation policy?](#id9)[¶](#what-is-the-api-stability-and-deprecation-policy "Link to this heading")

*aiohttp* follows strong [Semantic Versioning](https://semver.org) (SemVer).

Obsolete attributes and methods are marked as *deprecated* in the
documentation and raise [`DeprecationWarning`](https://docs.python.org/3/library/exceptions.html#DeprecationWarning "(in Python v3.14)") upon usage.

Assume aiohttp `X.Y.Z` where `X` is major version,
`Y` is minor version and `Z` is bugfix number.

For example, if the latest released version is `aiohttp==3.0.6`:

`3.0.7` fixes some bugs but have no new features.

`3.1.0` introduces new features and can deprecate some API but never
remove it, also all bug fixes from previous release are merged.

`4.0.0` removes all deprecations collected from `3.Y` versions
**except** deprecations from the **last** `3.Y` release. These
deprecations will be removed by `5.0.0`.

Unfortunately we may have to break these rules when a **security
vulnerability** is found.
If a security problem cannot be fixed without breaking backward
compatibility, a bugfix release may break compatibility. This is unlikely, but
possible.

All backward incompatible changes are explicitly marked in
[the changelog](changes.html#aiohttp-changes).

## [How do I enable gzip compression globally for my entire application?](#id10)[¶](#how-do-i-enable-gzip-compression-globally-for-my-entire-application "Link to this heading")

It’s impossible. Choosing what to compress and what not to compress is
is a tricky matter.

If you need global compression, write a custom middleware. Or
enable compression in NGINX (you are deploying aiohttp behind reverse
proxy, right?).

## [How do I manage a ClientSession within a web server?](#id11)[¶](#how-do-i-manage-a-clientsession-within-a-web-server "Link to this heading")

[`aiohttp.ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") should be created once for the lifetime
of the server in order to benefit from connection pooling.

Sessions save cookies internally. If you don’t need cookie processing,
use [`aiohttp.DummyCookieJar`](client_reference.html#aiohttp.DummyCookieJar "aiohttp.DummyCookieJar"). If you need separate cookies
for different http calls but process them in logical chains, use a single
[`aiohttp.TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") with separate
client sessions and `connector_owner=False`.

## [How do I access database connections from a subapplication?](#id12)[¶](#how-do-i-access-database-connections-from-a-subapplication "Link to this heading")

Restricting access from subapplication to main (or outer) app is a
deliberate choice.

A subapplication is an isolated unit by design. If you need to share a
database object, do it explicitly:

```
subapp[db_key] = mainapp[db_key]
mainapp.add_subapp("/prefix", subapp)
```

This can also be done from a [cleanup context](web_advanced.html#aiohttp-web-cleanup-ctx):

```
async def db_context(app: web.Application) -> AsyncIterator[None]:
   async with create_db() as db:
      mainapp[db_key] = mainapp[subapp_key][db_key] = db
      yield

mainapp[subapp_key] = subapp
mainapp.add_subapp("/prefix", subapp)
mainapp.cleanup_ctx.append(db_context)
```

## [How do I perform operations in a request handler after sending the response?](#id13)[¶](#how-do-i-perform-operations-in-a-request-handler-after-sending-the-response "Link to this heading")

Middlewares can be written to handle post-response operations, but
they run after every request. You can explicitly send the response by
calling `aiohttp.web.Response.write_eof()`, which starts sending
before the handler returns, giving you a chance to execute follow-up
operations:

```
def ping_handler(request):
    """Send PONG and increase DB counter."""

    # explicitly send the response
    resp = web.json_response({'message': 'PONG'})
    await resp.prepare(request)
    await resp.write_eof()

    # increase the pong count
    request.app[db_key].inc_pong()

    return resp
```

A [`aiohttp.web.Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response") object must be returned. This is
required by aiohttp web contracts, even though the response has
already been sent.

## [How do I make sure my custom middleware response will behave correctly?](#id14)[¶](#how-do-i-make-sure-my-custom-middleware-response-will-behave-correctly "Link to this heading")

Sometimes your middleware handlers might need to send a custom response.
This is just fine as long as you always create a new
[`aiohttp.web.Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response") object when required.

The response object is a Finite State Machine. Once it has been dispatched
by the server, it will reach its final state and cannot be used again.

The following middleware will make the server hang, once it serves the second
response:

```
from aiohttp import web

def misbehaved_middleware():
    # don't do this!
    cached = web.Response(status=200, text='Hi, I am cached!')

    @web.middleware
    async def middleware(request, handler):
        # ignoring response for the sake of this example
        _res = handler(request)
        return cached

    return middleware
```

The rule of thumb is *one request, one response*.

## [Why is creating a ClientSession outside of an event loop dangerous?](#id15)[¶](#why-is-creating-a-clientsession-outside-of-an-event-loop-dangerous "Link to this heading")

Short answer is: life-cycle of all asyncio objects should be shorter
than life-cycle of event loop.

Full explanation is longer. All asyncio object should be correctly
finished/disconnected/closed before event loop shutdown. Otherwise
user can get unexpected behavior. In the best case it is a warning
about unclosed resource, in the worst case the program just hangs,
awaiting for coroutine is never resumed etc.

Consider the following code from `mod.py`:

```
import aiohttp

session = aiohttp.ClientSession()

async def fetch(url):
    async with session.get(url) as resp:
        return await resp.text()
```

The session grabs current event loop instance and stores it in a
private variable.

The main module imports the module and installs `uvloop` (an
alternative fast event loop implementation).

`main.py`:

```
import asyncio
import uvloop
import mod

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
```

The code is broken: `session` is bound to default `asyncio` loop
on import time but the loop is changed **after the import** by
`set_event_loop()`. As result `fetch()` call hangs.

To avoid import dependency hell *aiohttp* encourages creation of
`ClientSession` from async function. The same policy works for
`web.Application` too.

Another use case is unit test writing. Very many test libraries
(*aiohttp test tools* first) creates a new loop instance for every
test function execution. It’s done for sake of tests isolation.
Otherwise pending activity (timers, network packets etc.) from
previous test may interfere with current one producing very cryptic
and unstable test failure.

Note: *class variables* are hidden globals actually. The following
code has the same problem as `mod.py` example, `session` variable
is the hidden global object:

```
class A:
    session = aiohttp.ClientSession()

    async def fetch(self, url):
        async with session.get(url) as resp:
            return await resp.text()
```

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
* [Utilities](utilities.html)
* [FAQ](#)
  + [Are there plans for an @app.route decorator like in Flask?](#are-there-plans-for-an-app-route-decorator-like-in-flask)
  + [Does aiohttp have a concept like Flask’s “blueprint” or Django’s “app”?](#does-aiohttp-have-a-concept-like-flask-s-blueprint-or-django-s-app)
  + [How do I create a route that matches urls with a given prefix?](#how-do-i-create-a-route-that-matches-urls-with-a-given-prefix)
  + [Where do I put my database connection so handlers can access it?](#where-do-i-put-my-database-connection-so-handlers-can-access-it)
  + [How can middleware store data for web handlers to use?](#how-can-middleware-store-data-for-web-handlers-to-use)
  + [Can a handler receive incoming events from different sources in parallel?](#can-a-handler-receive-incoming-events-from-different-sources-in-parallel)
  + [How do I programmatically close a WebSocket server-side?](#how-do-i-programmatically-close-a-websocket-server-side)
  + [How do I make a request from a specific IP address?](#how-do-i-make-a-request-from-a-specific-ip-address)
  + [What is the API stability and deprecation policy?](#what-is-the-api-stability-and-deprecation-policy)
  + [How do I enable gzip compression globally for my entire application?](#how-do-i-enable-gzip-compression-globally-for-my-entire-application)
  + [How do I manage a ClientSession within a web server?](#how-do-i-manage-a-clientsession-within-a-web-server)
  + [How do I access database connections from a subapplication?](#how-do-i-access-database-connections-from-a-subapplication)
  + [How do I perform operations in a request handler after sending the response?](#how-do-i-perform-operations-in-a-request-handler-after-sending-the-response)
  + [How do I make sure my custom middleware response will behave correctly?](#how-do-i-make-sure-my-custom-middleware-response-will-behave-correctly)
  + [Why is creating a ClientSession outside of an event loop dangerous?](#why-is-creating-a-clientsession-outside-of-an-event-loop-dangerous)
* [Miscellaneous](misc.html)
* [Who uses aiohttp?](external.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/faq.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
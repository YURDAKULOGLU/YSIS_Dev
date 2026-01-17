FAQ
===
.. contents::
:local:
Are there plans for an @app.route decorator like in Flask?
----------------------------------------------------------
As of aiohttp 2.3, :class:`~aiohttp.web.RouteTableDef` provides an API
similar to Flask's ``@app.route``. See
:ref:`aiohttp-web-alternative-routes-definition`.
Unlike Flask's ``@app.route``, :class:`~aiohttp.web.RouteTableDef`
does not require an ``app`` in the module namespace (which often leads
to circular imports).
Instead, a :class:`~aiohttp.web.RouteTableDef` is decoupled from an application instance::
routes = web.RouteTableDef()
@routes.get('/get')
async def handle\_get(request):
...
@routes.post('/post')
async def handle\_post(request):
...
app.router.add\_routes(routes)
Does aiohttp have a concept like Flask's "blueprint" or Django's "app"?
-----------------------------------------------------------------------
If you're writing a large application, you may want to consider
using :ref:`nested applications `, which
are similar to Flask's "blueprints" or Django's "apps".
See: :ref:`aiohttp-web-nested-applications`.
How do I create a route that matches urls with a given prefix?
--------------------------------------------------------------
You can do something like the following: ::
app.router.add\_route('\*', '/path/to/{tail:.+}', sink\_handler)
The first argument, ``\*``, matches any HTTP method
(\*GET, POST, OPTIONS\*, etc). The second argument matches URLS with the desired prefix.
The third argument is the handler function.
Where do I put my database connection so handlers can access it?
----------------------------------------------------------------
:class:`aiohttp.web.Application` object supports the :class:`dict`
interface and provides a place to store your database connections or any
other resource you want to share between handlers.
::
db\_key = web.AppKey("db\_key", DB)
async def go(request):
db = request.app[db\_key]
cursor = await db.cursor()
await cursor.execute('SELECT 42')
# ...
return web.Response(status=200, text='ok')
async def init\_app(loop):
app = Application(loop=loop)
db = await create\_connection(user='user', password='123')
app[db\_key] = db
app.router.add\_get('/', go)
return app
How can middleware store data for web handlers to use?
------------------------------------------------------
Both :class:`aiohttp.web.Request` and :class:`aiohttp.web.Application`
support the :class:`dict` interface.
Therefore, data may be stored inside a request object. ::
async def handler(request):
request['unique\_key'] = data
See https://github.com/aio-libs/aiohttp\_session code for an example.
The ``aiohttp\_session.get\_session(request)`` method uses ``SESSION\_KEY``
for saving request-specific session information.
As of aiohttp 3.0, all response objects are dict-like structures as
well.
.. \_aiohttp\_faq\_parallel\_event\_sources:
Can a handler receive incoming events from different sources in parallel?
-------------------------------------------------------------------------
Yes.
As an example, we may have two event sources:
1. WebSocket for events from an end user
2. Redis PubSub for events from other parts of the application
The most native way to handle this is to create a separate task for
PubSub handling.
Parallel :meth:`aiohttp.web.WebSocketResponse.receive` calls are forbidden;
a single task should perform WebSocket reading.
However, other tasks may use the same WebSocket object for sending data to
peers. ::
async def handler(request):
ws = web.WebSocketResponse()
await ws.prepare(request)
task = asyncio.create\_task(
read\_subscription(ws, request.app[redis\_key]))
try:
async for msg in ws:
# handle incoming messages
# use ws.send\_str() to send data back
...
finally:
task.cancel()
async def read\_subscription(ws, redis):
channel, = await redis.subscribe('channel:1')
try:
async for msg in channel.iter():
answer = process\_the\_message(msg) # your function here
await ws.send\_str(answer)
finally:
await redis.unsubscribe('channel:1')
.. \_aiohttp\_faq\_terminating\_websockets:
How do I programmatically close a WebSocket server-side?
--------------------------------------------------------
Let's say we have an application with two endpoints:
1. ``/echo`` a WebSocket echo server that authenticates the user
2. ``/logout\_user`` that, when invoked, closes all open
WebSockets for that user.
One simple solution is to keep a shared registry of WebSocket
responses for a user in the :class:`aiohttp.web.Application` instance
and call :meth:`aiohttp.web.WebSocketResponse.close` on all of them in
``/logout\_user`` handler::
async def echo\_handler(request):
ws = web.WebSocketResponse()
user\_id = authenticate\_user(request)
await ws.prepare(request)
request.app[websockets\_key][user\_id].add(ws)
try:
async for msg in ws:
ws.send\_str(msg.data)
finally:
request.app[websockets\_key][user\_id].remove(ws)
return ws
async def logout\_handler(request):
user\_id = authenticate\_user(request)
ws\_closers = [ws.close()
for ws in request.app[websockets\_key][user\_id]
if not ws.closed]
# Watch out, this will keep us from returning the response
# until all are closed
ws\_closers and await asyncio.gather(\*ws\_closers)
return web.Response(text='OK')
def main():
loop = asyncio.get\_event\_loop()
app = web.Application(loop=loop)
app.router.add\_route('GET', '/echo', echo\_handler)
app.router.add\_route('POST', '/logout', logout\_handler)
app[websockets\_key] = defaultdict(set)
web.run\_app(app, host='localhost', port=8080)
How do I make a request from a specific IP address?
---------------------------------------------------
If your system has several IP interfaces, you may choose one which will
be used used to bind a socket locally::
conn = aiohttp.TCPConnector(local\_addr=('127.0.0.1', 0), loop=loop)
async with aiohttp.ClientSession(connector=conn) as session:
...
.. seealso:: :class:`aiohttp.TCPConnector` and ``local\_addr`` parameter.
What is the API stability and deprecation policy?
-------------------------------------------------
\*aiohttp\* follows strong `Semantic Versioning `\_ (SemVer).
Obsolete attributes and methods are marked as \*deprecated\* in the
documentation and raise :class:`DeprecationWarning` upon usage.
Assume aiohttp ``X.Y.Z`` where ``X`` is major version,
``Y`` is minor version and ``Z`` is bugfix number.
For example, if the latest released version is ``aiohttp==3.0.6``:
``3.0.7`` fixes some bugs but have no new features.
``3.1.0`` introduces new features and can deprecate some API but never
remove it, also all bug fixes from previous release are merged.
``4.0.0`` removes all deprecations collected from ``3.Y`` versions
\*\*except\*\* deprecations from the \*\*last\*\* ``3.Y`` release. These
deprecations will be removed by ``5.0.0``.
Unfortunately we may have to break these rules when a \*\*security
vulnerability\*\* is found.
If a security problem cannot be fixed without breaking backward
compatibility, a bugfix release may break compatibility. This is unlikely, but
possible.
All backward incompatible changes are explicitly marked in
:ref:`the changelog `.
How do I enable gzip compression globally for my entire application?
--------------------------------------------------------------------
It's impossible. Choosing what to compress and what not to compress is
is a tricky matter.
If you need global compression, write a custom middleware. Or
enable compression in NGINX (you are deploying aiohttp behind reverse
proxy, right?).
How do I manage a ClientSession within a web server?
----------------------------------------------------
:class:`aiohttp.ClientSession` should be created once for the lifetime
of the server in order to benefit from connection pooling.
Sessions save cookies internally. If you don't need cookie processing,
use :class:`aiohttp.DummyCookieJar`. If you need separate cookies
for different http calls but process them in logical chains, use a single
:class:`aiohttp.TCPConnector` with separate
client sessions and ``connector\_owner=False``.
How do I access database connections from a subapplication?
-----------------------------------------------------------
Restricting access from subapplication to main (or outer) app is a
deliberate choice.
A subapplication is an isolated unit by design. If you need to share a
database object, do it explicitly::
subapp[db\_key] = mainapp[db\_key]
mainapp.add\_subapp("/prefix", subapp)
This can also be done from a :ref:`cleanup context`::
async def db\_context(app: web.Application) -> AsyncIterator[None]:
async with create\_db() as db:
mainapp[db\_key] = mainapp[subapp\_key][db\_key] = db
yield
mainapp[subapp\_key] = subapp
mainapp.add\_subapp("/prefix", subapp)
mainapp.cleanup\_ctx.append(db\_context)
How do I perform operations in a request handler after sending the response?
----------------------------------------------------------------------------
Middlewares can be written to handle post-response operations, but
they run after every request. You can explicitly send the response by
calling :meth:`aiohttp.web.Response.write\_eof`, which starts sending
before the handler returns, giving you a chance to execute follow-up
operations::
def ping\_handler(request):
"""Send PONG and increase DB counter."""
# explicitly send the response
resp = web.json\_response({'message': 'PONG'})
await resp.prepare(request)
await resp.write\_eof()
# increase the pong count
request.app[db\_key].inc\_pong()
return resp
A :class:`aiohttp.web.Response` object must be returned. This is
required by aiohttp web contracts, even though the response has
already been sent.
How do I make sure my custom middleware response will behave correctly?
------------------------------------------------------------------------
Sometimes your middleware handlers might need to send a custom response.
This is just fine as long as you always create a new
:class:`aiohttp.web.Response` object when required.
The response object is a Finite State Machine. Once it has been dispatched
by the server, it will reach its final state and cannot be used again.
The following middleware will make the server hang, once it serves the second
response::
from aiohttp import web
def misbehaved\_middleware():
# don't do this!
cached = web.Response(status=200, text='Hi, I am cached!')
@web.middleware
async def middleware(request, handler):
# ignoring response for the sake of this example
\_res = handler(request)
return cached
return middleware
The rule of thumb is \*one request, one response\*.
Why is creating a ClientSession outside of an event loop dangerous?
-------------------------------------------------------------------
Short answer is: life-cycle of all asyncio objects should be shorter
than life-cycle of event loop.
Full explanation is longer. All asyncio object should be correctly
finished/disconnected/closed before event loop shutdown. Otherwise
user can get unexpected behavior. In the best case it is a warning
about unclosed resource, in the worst case the program just hangs,
awaiting for coroutine is never resumed etc.
Consider the following code from ``mod.py``::
import aiohttp
session = aiohttp.ClientSession()
async def fetch(url):
async with session.get(url) as resp:
return await resp.text()
The session grabs current event loop instance and stores it in a
private variable.
The main module imports the module and installs ``uvloop`` (an
alternative fast event loop implementation).
``main.py``::
import asyncio
import uvloop
import mod
asyncio.set\_event\_loop\_policy(uvloop.EventLoopPolicy())
asyncio.run(main())
The code is broken: ``session`` is bound to default ``asyncio`` loop
on import time but the loop is changed \*\*after the import\*\* by
``set\_event\_loop()``. As result ``fetch()`` call hangs.
To avoid import dependency hell \*aiohttp\* encourages creation of
``ClientSession`` from async function. The same policy works for
``web.Application`` too.
Another use case is unit test writing. Very many test libraries
(\*aiohttp test tools\* first) creates a new loop instance for every
test function execution. It's done for sake of tests isolation.
Otherwise pending activity (timers, network packets etc.) from
previous test may interfere with current one producing very cryptic
and unstable test failure.
Note: \*class variables\* are hidden globals actually. The following
code has the same problem as ``mod.py`` example, ``session`` variable
is the hidden global object::
class A:
session = aiohttp.ClientSession()
async def fetch(self, url):
async with session.get(url) as resp:
return await resp.text()
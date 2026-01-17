.. \_aiohttp-web-advanced:
Web Server Advanced
===================
.. currentmodule:: aiohttp.web
Unicode support
---------------
\*aiohttp\* does :term:`requoting` of incoming request path.
Unicode (non-ASCII) symbols are processed transparently on both \*route
adding\* and \*resolving\* (internally everything is converted to
:term:`percent-encoding` form by :term:`yarl` library).
But in case of custom regular expressions for
:ref:`aiohttp-web-variable-handler` please take care that URL is
\*percent encoded\*: if you pass Unicode patterns they don't match to
\*requoted\* path.
.. \_aiohttp-web-peer-disconnection:
Peer disconnection
------------------
\*aiohttp\* has 2 approaches to handling client disconnections.
If you are familiar with asyncio, or scalability is a concern for
your application, we recommend using the handler cancellation method.
Raise on read/write (default)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When a client peer is gone, a subsequent reading or writing raises :exc:`OSError`
or a more specific exception like :exc:`ConnectionResetError`.
This behavior is similar to classic WSGI frameworks like Flask and Django.
The reason for disconnection varies; it can be a network issue or explicit
socket closing on the peer side without reading the full server response.
\*aiohttp\* handles disconnection properly but you can handle it explicitly, e.g.::
async def handler(request):
try:
text = await request.text()
except OSError:
# disconnected
.. \_web-handler-cancellation:
Web handler cancellation
^^^^^^^^^^^^^^^^^^^^^^^^
This method can be enabled using the ``handler\_cancellation`` parameter
to :func:`run\_app`.
When a client disconnects, the web handler task will be cancelled. This
is recommended as it can reduce the load on your server when there is no
client to receive a response. It can also help make your application
more resilient to DoS attacks (by requiring an attacker to keep a
connection open in order to waste server resources).
This behavior is very different from classic WSGI frameworks like
Flask and Django. It requires a reasonable level of asyncio knowledge to
use correctly without causing issues in your code. We provide some
examples here to help understand the complexity and methods
needed to deal with them.
.. warning::
:term:`web-handler` execution could be canceled on every ``await`` or
``async with`` if client drops connection without reading entire response's BODY.
Sometimes it is a desirable behavior: on processing ``GET`` request the
code might fetch data from a database or other web resource, the
fetching is potentially slow.
Canceling this fetch is a good idea: the client dropped the connection
already, so there is no reason to waste time and resources (memory etc)
by getting data from a DB without any chance to send it back to the client.
But sometimes the cancellation is bad: on ``POST`` requests very often
it is needed to save data to a DB regardless of connection closing.
Cancellation prevention could be implemented in several ways:
\* Applying :func:`aiojobs.aiohttp.shield` to a coroutine that saves data.
\* Using aiojobs\_ or another third party library to run a task in the background.
:func:`aiojobs.aiohttp.shield` can work well. The only disadvantage is you
need to split the web handler into two async functions: one for the handler
itself and another for protected code.
.. warning::
We don't recommend using :func:`asyncio.shield` for this because the shielded
task cannot be tracked by the application and therefore there is a risk that
the task will get cancelled during application shutdown. The function provided
by aiojobs\_ operates in the same way except the inner task will be tracked
by the Scheduler and will get waited on during the cleanup phase.
For example the following snippet is not safe::
from aiojobs.aiohttp import shield
async def handler(request):
await shield(request, write\_to\_redis(request))
await shield(request, write\_to\_postgres(request))
return web.Response(text="OK")
Cancellation might occur while saving data in REDIS, so the
``write\_to\_postgres`` function will not be called, potentially
leaving your data in an inconsistent state.
Instead, you would need to write something like::
async def write\_data(request):
await write\_to\_redis(request)
await write\_to\_postgres(request)
async def handler(request):
await shield(request, write\_data(request))
return web.Response(text="OK")
Alternatively, if you want to spawn a task without waiting for
its completion, you can use aiojobs\_ which provides an API for
spawning new background jobs. It stores all scheduled activity in
internal data structures and can terminate them gracefully::
from aiojobs.aiohttp import setup, spawn
async def handler(request):
await spawn(request, write\_data())
return web.Response()
app = web.Application()
setup(app)
app.router.add\_get("/", handler)
.. warning::
Don't use :func:`asyncio.create\_task` for this. All tasks
should be awaited at some point in your code (``aiojobs`` handles
this for you), otherwise you will hide legitimate exceptions
and result in warnings being emitted.
A good case for using :func:`asyncio.create\_task` is when
you want to run something while you are processing other data,
but still want to ensure the task is complete before returning::
async def handler(request):
t = asyncio.create\_task(get\_some\_data())
... # Do some other things, while data is being fetched.
data = await t
return web.Response(text=data)
One more approach would be to use :func:`aiojobs.aiohttp.atomic`
decorator to execute the entire handler as a new job. Essentially
restoring the default disconnection behavior only for specific handlers::
from aiojobs.aiohttp import atomic
@atomic
async def handler(request):
await write\_to\_db()
return web.Response()
app = web.Application()
setup(app)
app.router.add\_post("/", handler)
It prevents all of the ``handler`` async function from cancellation,
so ``write\_to\_db`` will never be interrupted.
.. \_aiojobs: http://aiojobs.readthedocs.io/en/latest/
Passing a coroutine into run\_app and Gunicorn
---------------------------------------------
:func:`run\_app` accepts either application instance or a coroutine for
making an application. The coroutine based approach allows to perform
async IO before making an app::
async def app\_factory():
await pre\_init()
app = web.Application()
app.router.add\_get(...)
return app
web.run\_app(app\_factory())
Gunicorn worker supports a factory as well. For Gunicorn the factory
should accept zero parameters::
async def my\_web\_app():
app = web.Application()
app.router.add\_get(...)
return app
Start gunicorn:
.. code-block:: shell
$ gunicorn my\_app\_module:my\_web\_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
.. versionadded:: 3.1
Custom Routing Criteria
-----------------------
Sometimes you need to register :ref:`handlers ` on
more complex criteria than simply a \*HTTP method\* and \*path\* pair.
Although :class:`UrlDispatcher` does not support any extra criteria, routing
based on custom conditions can be accomplished by implementing a second layer
of routing in your application.
The following example shows custom routing based on the \*HTTP Accept\* header::
class AcceptChooser:
def \_\_init\_\_(self):
self.\_accepts = {}
async def do\_route(self, request):
for accept in request.headers.getall('ACCEPT', []):
acceptor = self.\_accepts.get(accept)
if acceptor is not None:
return (await acceptor(request))
raise HTTPNotAcceptable()
def reg\_acceptor(self, accept, handler):
self.\_accepts[accept] = handler
async def handle\_json(request):
# do json handling
async def handle\_xml(request):
# do xml handling
chooser = AcceptChooser()
app.add\_routes([web.get('/', chooser.do\_route)])
chooser.reg\_acceptor('application/json', handle\_json)
chooser.reg\_acceptor('application/xml', handle\_xml)
.. \_aiohttp-web-static-file-handling:
Static file handling
--------------------
The best way to handle static files (images, JavaScripts, CSS files
etc.) is using `Reverse Proxy`\_ like `nginx`\_ or `CDN`\_ services.
.. \_Reverse Proxy: https://en.wikipedia.org/wiki/Reverse\_proxy
.. \_nginx: https://nginx.org/
.. \_CDN: https://en.wikipedia.org/wiki/Content\_delivery\_network
But for development it's very convenient to handle static files by
aiohttp server itself.
To do it just register a new static route by
:meth:`RouteTableDef.static` or :func:`static` calls::
app.add\_routes([web.static('/prefix', path\_to\_static\_folder)])
routes.static('/prefix', path\_to\_static\_folder)
When a directory is accessed within a static route then the server responses
to client with ``HTTP/403 Forbidden`` by default. Displaying folder index
instead could be enabled with ``show\_index`` parameter set to ``True``::
web.static('/prefix', path\_to\_static\_folder, show\_index=True)
When a symlink that leads outside the static directory is accessed, the server
responds to the client with ``HTTP/404 Not Found`` by default. To allow the server to
follow symlinks that lead outside the static root, the parameter ``follow\_symlinks``
should be set to ``True``::
web.static('/prefix', path\_to\_static\_folder, follow\_symlinks=True)
.. caution::
Enabling ``follow\_symlinks`` can be a security risk, and may lead to
a directory transversal attack. You do NOT need this option to follow symlinks
which point to somewhere else within the static directory, this option is only
used to break out of the security sandbox. Enabling this option is highly
discouraged, and only expected to be used for edge cases in a local
development setting where remote users do not have access to the server.
When you want to enable cache busting,
parameter ``append\_version`` can be set to ``True``
Cache busting is the process of appending some form of file version hash
to the filename of resources like JavaScript and CSS files.
The performance advantage of doing this is that we can tell the browser
to cache these files indefinitely without worrying about the client not getting
the latest version when the file changes::
web.static('/prefix', path\_to\_static\_folder, append\_version=True)
Template Rendering
------------------
:mod:`aiohttp.web` does not support template rendering out-of-the-box.
However, there is a third-party library, :mod:`aiohttp\_jinja2`, which is
supported by the \*aiohttp\* authors.
Using it is rather simple. First, setup a \*jinja2 environment\* with a call
to :func:`aiohttp\_jinja2.setup`::
app = web.Application()
aiohttp\_jinja2.setup(app,
loader=jinja2.FileSystemLoader('/path/to/templates/folder'))
After that you may use the template engine in your
:ref:`handlers `. The most convenient way is to simply
wrap your handlers with the :func:`aiohttp\_jinja2.template` decorator::
@aiohttp\_jinja2.template('tmpl.jinja2')
async def handler(request):
return {'name': 'Andrew', 'surname': 'Svetlov'}
If you prefer the `Mako`\_ template engine, please take a look at the
`aiohttp\_mako`\_ library.
.. warning::
:func:`aiohttp\_jinja2.template` should be applied \*\*before\*\*
:meth:`RouteTableDef.get` decorator and family, e.g. it must be
the \*first\* (most \*down\* decorator in the chain)::
@routes.get('/path')
@aiohttp\_jinja2.template('tmpl.jinja2')
async def handler(request):
return {'name': 'Andrew', 'surname': 'Svetlov'}
.. \_Mako: http://www.makotemplates.org/
.. \_aiohttp\_mako: https://github.com/aio-libs/aiohttp\_mako
.. \_aiohttp-web-websocket-read-same-task:
Reading from the same task in WebSockets
----------------------------------------
Reading from the \*WebSocket\* (``await ws.receive()``) \*\*must only\*\* be
done inside the request handler \*task\*; however, writing
(``ws.send\_str(...)``) to the \*WebSocket\*, closing (``await
ws.close()``) and canceling the handler task may be delegated to other
tasks. See also :ref:`FAQ section
`.
:mod:`aiohttp.web` creates an implicit :class:`asyncio.Task` for
handling every incoming request.
.. note::
While :mod:`aiohttp.web` itself only supports \*WebSockets\* without
downgrading to \*LONG-POLLING\*, etc., our team supports SockJS\_, an
aiohttp-based library for implementing SockJS-compatible server
code.
.. \_SockJS: https://github.com/aio-libs/sockjs
.. warning::
Parallel reads from websocket are forbidden, there is no
possibility to call :meth:`WebSocketResponse.receive`
from two tasks.
See :ref:`FAQ section ` for
instructions how to solve the problem.
.. \_aiohttp-web-data-sharing:
Data Sharing aka No Singletons Please
-------------------------------------
:mod:`aiohttp.web` discourages the use of \*global variables\*, aka \*singletons\*.
Every variable should have its own context that is \*not global\*.
Global variables are generally considered bad practice due to the complexity
they add in keeping track of state changes to variables.
\*aiohttp\* does not use globals by design, which will reduce the number of bugs
and/or unexpected behaviors for its users. For example, an i18n translated string
being written for one request and then being served to another.
So, :class:`Application` and :class:`Request`
support a :class:`collections.abc.MutableMapping` interface (i.e. they are
dict-like objects), allowing them to be used as data stores.
.. \_aiohttp-web-data-sharing-app-config:
Application's config
^^^^^^^^^^^^^^^^^^^^
For storing \*global-like\* variables, feel free to save them in an
:class:`Application` instance::
app['my\_private\_key'] = data
and get it back in the :term:`web-handler`::
async def handler(request):
data = request.app['my\_private\_key']
Rather than using :class:`str` keys, we recommend using :class:`AppKey`.
This is required for type safety (e.g. when checking with mypy)::
my\_private\_key = web.AppKey("my\_private\_key", str)
app[my\_private\_key] = data
async def handler(request: web.Request):
data = request.app[my\_private\_key]
# reveal\_type(data) -> str
In case of :ref:`nested applications
` the desired lookup strategy could
be the following:
1. Search the key in the current nested application.
2. If the key is not found continue searching in the parent application(s).
For this please use :attr:`Request.config\_dict` read-only property::
async def handler(request):
data = request.config\_dict[my\_private\_key]
The app object can be used in this way to reuse a database connection or anything
else needed throughout the application.
See this reference section for more detail: :ref:`aiohttp-web-app-and-router`.
Request's storage
^^^^^^^^^^^^^^^^^
Variables that are only needed for the lifetime of a :class:`Request`, can be
stored in a :class:`Request`::
async def handler(request):
request['my\_private\_key'] = "data"
...
This is mostly useful for :ref:`aiohttp-web-middlewares` and
:ref:`aiohttp-web-signals` handlers to store data for further processing by the
next handlers in the chain.
Response's storage
^^^^^^^^^^^^^^^^^^
:class:`StreamResponse` and :class:`Response` objects
also support :class:`collections.abc.MutableMapping` interface. This is useful
when you want to share data with signals and middlewares once all the work in
the handler is done::
async def handler(request):
[ do all the work ]
response['my\_metric'] = 123
return response
Naming hint
^^^^^^^^^^^
To avoid clashing with other \*aiohttp\* users and third-party libraries, please
choose a unique key name for storing data.
If your code is published on PyPI, then the project name is most likely unique
and safe to use as the key.
Otherwise, something based on your company name/url would be satisfactory (i.e.
``org.company.app``).
.. \_aiohttp-web-contextvars:
ContextVars support
-------------------
Asyncio has :mod:`Context Variables ` as a context-local storage
(a generalization of thread-local concept that works with asyncio tasks also).
\*aiohttp\* server supports it in the following way:
\* A server inherits the current task's context used when creating it.
:func:`aiohttp.web.run\_app()` runs a task for handling all underlying jobs running
the app, but alternatively :ref:`aiohttp-web-app-runners` can be used.
\* Application initialization / finalization events (:attr:`Application.cleanup\_ctx`,
:attr:`Application.on\_startup` and :attr:`Application.on\_shutdown`,
:attr:`Application.on\_cleanup`) are executed inside the same context.
E.g. all context modifications made on application startup are visible on teardown.
\* On every request handling \*aiohttp\* creates a context copy. :term:`web-handler` has
all variables installed on initialization stage. But the context modification made by
a handler or middleware is invisible to another HTTP request handling call.
An example of context vars usage::
from contextvars import ContextVar
from aiohttp import web
VAR = ContextVar('VAR', default='default')
async def coro():
return VAR.get()
async def handler(request):
var = VAR.get()
VAR.set('handler')
ret = await coro()
return web.Response(text='\n'.join([var,
ret]))
async def on\_startup(app):
print('on\_startup', VAR.get())
VAR.set('on\_startup')
async def on\_cleanup(app):
print('on\_cleanup', VAR.get())
VAR.set('on\_cleanup')
async def init():
print('init', VAR.get())
VAR.set('init')
app = web.Application()
app.router.add\_get('/', handler)
app.on\_startup.append(on\_startup)
app.on\_cleanup.append(on\_cleanup)
return app
web.run\_app(init())
print('done', VAR.get())
.. versionadded:: 3.5
.. \_aiohttp-web-middlewares:
Middlewares
-----------
:mod:`aiohttp.web` provides a powerful mechanism for customizing
:ref:`request handlers` via \*middlewares\*.
A \*middleware\* is a coroutine that can modify either the request or
response. For example, here's a simple \*middleware\* which appends
``' wink'`` to the response::
from aiohttp import web
from typing import Callable, Awaitable
@web.middleware
async def middleware(
request: web.Request,
handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:
resp = await handler(request)
resp.text = resp.text + ' wink'
return resp
.. note::
The example won't work with streamed responses or websockets
Every \*middleware\* should accept two parameters, a :class:`request
` instance and a \*handler\*, and return the response or raise
an exception. If the exception is not an instance of
:exc:`HTTPException` it is converted to ``500``
:exc:`HTTPInternalServerError` after processing the
middlewares chain.
.. warning::
Second argument should be named \*handler\* exactly.
When creating an :class:`Application`, these \*middlewares\* are passed to
the keyword-only ``middlewares`` parameter::
app = web.Application(middlewares=[middleware\_1,
middleware\_2])
Internally, a single :ref:`request handler ` is constructed
by applying the middleware chain to the original handler in reverse order,
and is called by the :class:`~aiohttp.web.RequestHandler` as a regular \*handler\*.
Since \*middlewares\* are themselves coroutines, they may perform extra
``await`` calls when creating a new handler, e.g. call database etc.
\*Middlewares\* usually call the handler, but they may choose to ignore it,
e.g. displaying \*403 Forbidden page\* or raising :exc:`HTTPForbidden` exception
if the user does not have permissions to access the underlying resource.
They may also render errors raised by the handler, perform some pre- or
post-processing like handling \*CORS\* and so on.
The following code demonstrates middlewares execution order::
from aiohttp import web
from typing import Callable, Awaitable
async def test(request: web.Request) -> web.Response:
print('Handler function called')
return web.Response(text="Hello")
@web.middleware
async def middleware1(
request: web.Request,
handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:
print('Middleware 1 called')
response = await handler(request)
print('Middleware 1 finished')
return response
@web.middleware
async def middleware2(
request: web.Request,
handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:
print('Middleware 2 called')
response = await handler(request)
print('Middleware 2 finished')
return response
app = web.Application(middlewares=[middleware1, middleware2])
app.router.add\_get('/', test)
web.run\_app(app)
Produced output::
Middleware 1 called
Middleware 2 called
Handler function called
Middleware 2 finished
Middleware 1 finished
Request Body Stream Consumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. warning::
When middleware reads the request body (using :meth:`~aiohttp.web.BaseRequest.read`,
:meth:`~aiohttp.web.BaseRequest.text`, :meth:`~aiohttp.web.BaseRequest.json`, or
:meth:`~aiohttp.web.BaseRequest.post`), the body stream is consumed. However, these
high-level methods cache their result, so subsequent calls from the handler or other
middleware will return the same cached value.
The important distinction is:
- High-level methods (:meth:`~aiohttp.web.BaseRequest.read`, :meth:`~aiohttp.web.BaseRequest.text`,
:meth:`~aiohttp.web.BaseRequest.json`, :meth:`~aiohttp.web.BaseRequest.post`) cache their
results internally, so they can be called multiple times and will return the same value.
- Direct stream access via :attr:`~aiohttp.web.BaseRequest.content` does NOT have this
caching behavior. Once you read from ``request.content`` directly (e.g., using
``await request.content.read()``), subsequent reads will return empty bytes.
Consider this middleware that logs request bodies::
from aiohttp import web
from typing import Callable, Awaitable
async def logging\_middleware(
request: web.Request,
handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:
# This consumes the request body stream
body = await request.text()
print(f"Request body: {body}")
return await handler(request)
async def handler(request: web.Request) -> web.Response:
# This will return the same value that was read in the middleware
# (i.e., the cached result, not an empty string)
body = await request.text()
return web.Response(text=f"Received: {body}")
In contrast, when accessing the stream directly (not recommended in middleware)::
async def stream\_middleware(
request: web.Request,
handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:
# Reading directly from the stream - this consumes it!
data = await request.content.read()
print(f"Stream data: {data}")
return await handler(request)
async def handler(request: web.Request) -> web.Response:
# This will return empty bytes because the stream was already consumed
data = await request.content.read()
# data will be b'' (empty bytes)
# However, high-level methods would still work if called for the first time:
# body = await request.text() # This would read from internal cache if available
return web.Response(text=f"Received: {data}")
When working with raw stream data that needs to be shared between middleware and handlers::
async def stream\_parsing\_middleware(
request: web.Request,
handler: Callable[[web.Request], Awaitable[web.StreamResponse]]
) -> web.StreamResponse:
# Read stream once and store the data
raw\_data = await request.content.read()
request['raw\_body'] = raw\_data
return await handler(request)
async def handler(request: web.Request) -> web.Response:
# Access the stored data instead of reading the stream again
raw\_data = request.get('raw\_body', b'')
return web.Response(body=raw\_data)
Example
^^^^^^^
A common use of middlewares is to implement custom error pages. The following
example will render 404 errors using a JSON response, as might be appropriate
a JSON REST service::
from aiohttp import web
@web.middleware
async def error\_middleware(request, handler):
try:
response = await handler(request)
if response.status != 404:
return response
message = response.message
except web.HTTPException as ex:
if ex.status != 404:
raise
message = ex.reason
return web.json\_response({'error': message})
app = web.Application(middlewares=[error\_middleware])
Middleware Factory
^^^^^^^^^^^^^^^^^^
A \*middleware factory\* is a function that creates a middleware with passed arguments. For example, here's a trivial \*middleware factory\*::
def middleware\_factory(text):
@middleware
async def sample\_middleware(request, handler):
resp = await handler(request)
resp.text = resp.text + text
return resp
return sample\_middleware
Remember that contrary to regular middlewares you need the result of a middleware factory not the function itself. So when passing a middleware factory to an app you actually need to call it::
app = web.Application(middlewares=[middleware\_factory(' wink')])
.. \_aiohttp-web-signals:
Signals
-------
Although :ref:`middlewares ` can customize
:ref:`request handlers` before or after a :class:`Response`
has been prepared, they can't customize a :class:`Response` \*\*while\*\* it's
being prepared. For this :mod:`aiohttp.web` provides \*signals\*.
For example, a middleware can only change HTTP headers for \*unprepared\*
responses (see :meth:`StreamResponse.prepare`), but sometimes we
need a hook for changing HTTP headers for streamed responses and WebSockets.
This can be accomplished by subscribing to the
:attr:`Application.on\_response\_prepare` signal, which is called after default
headers have been computed and directly before headers are sent::
async def on\_prepare(request, response):
response.headers['My-Header'] = 'value'
app.on\_response\_prepare.append(on\_prepare)
Additionally, the :attr:`Application.on\_startup` and
:attr:`Application.on\_cleanup` signals can be subscribed to for
application component setup and tear down accordingly.
The following example will properly initialize and dispose an asyncpg connection
engine::
from sqlalchemy.ext.asyncio import AsyncEngine, create\_async\_engine
pg\_engine = web.AppKey("pg\_engine", AsyncEngine)
async def create\_pg(app):
app[pg\_engine] = await create\_async\_engine(
"postgresql+asyncpg://postgre:@localhost:5432/postgre"
)
async def dispose\_pg(app):
await app[pg\_engine].dispose()
app.on\_startup.append(create\_pg)
app.on\_cleanup.append(dispose\_pg)
Signal handlers should not return a value but may modify incoming mutable
parameters.
Signal handlers will be run sequentially, in order they were
added. All handlers must be asynchronous since \*aiohttp\* 3.0.
.. \_aiohttp-web-cleanup-ctx:
Cleanup Context
---------------
Bare :attr:`Application.on\_startup` / :attr:`Application.on\_cleanup`
pair still has a pitfall: signals handlers are independent on each other.
E.g. we have ``[create\_pg, create\_redis]`` in \*startup\* signal and
``[dispose\_pg, dispose\_redis]`` in \*cleanup\*.
If, for example, ``create\_pg(app)`` call fails ``create\_redis(app)``
is not called. But on application cleanup both ``dispose\_pg(app)`` and
``dispose\_redis(app)`` are still called: \*cleanup signal\* has no
knowledge about startup/cleanup pairs and their execution state.
The solution is :attr:`Application.cleanup\_ctx` usage::
async def pg\_engine(app: web.Application):
app[pg\_engine] = await create\_async\_engine(
"postgresql+asyncpg://postgre:@localhost:5432/postgre"
)
yield
await app[pg\_engine].dispose()
app.cleanup\_ctx.append(pg\_engine)
The attribute is a list of \*asynchronous generators\*, a code \*before\*
``yield`` is an initialization stage (called on \*startup\*), a code
\*after\* ``yield`` is executed on \*cleanup\*. The generator must have only
one ``yield``.
\*aiohttp\* guarantees that \*cleanup code\* is called if and only if
\*startup code\* was successfully finished.
.. versionadded:: 3.1
.. \_aiohttp-web-nested-applications:
Nested applications
-------------------
Sub applications are designed for solving the problem of the big
monolithic code base.
Let's assume we have a project with own business logic and tools like
administration panel and debug toolbar.
Administration panel is a separate application by its own nature but all
toolbar URLs are served by prefix like ``/admin``.
Thus we'll create a totally separate application named ``admin`` and
connect it to main app with prefix by
:meth:`Application.add\_subapp`::
admin = web.Application()
# setup admin routes, signals and middlewares
app.add\_subapp('/admin/', admin)
Middlewares and signals from ``app`` and ``admin`` are chained.
It means that if URL is ``'/admin/something'`` middlewares from
``app`` are applied first and ``admin.middlewares`` are the next in
the call chain.
The same is going for
:attr:`Application.on\_response\_prepare` signal -- the
signal is delivered to both top level ``app`` and ``admin`` if
processing URL is routed to ``admin`` sub-application.
Common signals like :attr:`Application.on\_startup`,
:attr:`Application.on\_shutdown` and
:attr:`Application.on\_cleanup` are delivered to all
registered sub-applications. The passed parameter is sub-application
instance, not top-level application.
Third level sub-applications can be nested into second level ones --
there are no limitation for nesting level.
Url reversing for sub-applications should generate urls with proper prefix.
But for getting URL sub-application's router should be used::
admin = web.Application()
admin.add\_routes([web.get('/resource', handler, name='name')])
app.add\_subapp('/admin/', admin)
url = admin.router['name'].url\_for()
The generated ``url`` from example will have a value
``URL('/admin/resource')``.
If main application should do URL reversing for sub-application it could
use the following explicit technique::
admin = web.Application()
admin\_key = web.AppKey('admin\_key', web.Application)
admin.add\_routes([web.get('/resource', handler, name='name')])
app.add\_subapp('/admin/', admin)
app[admin\_key] = admin
async def handler(request: web.Request): # main application's handler
admin = request.app[admin\_key]
url = admin.router['name'].url\_for()
.. \_aiohttp-web-expect-header:
\*Expect\* Header
---------------
:mod:`aiohttp.web` supports \*Expect\* header. By default it sends
``HTTP/1.1 100 Continue`` line to client, or raises
:exc:`HTTPExpectationFailed` if header value is not equal to
"100-continue". It is possible to specify custom \*Expect\* header
handler on per route basis. This handler gets called if \*Expect\*
header exist in request after receiving all headers and before
processing application's :ref:`aiohttp-web-middlewares` and
route handler. Handler can return \*None\*, in that case the request
processing continues as usual. If handler returns an instance of class
:class:`StreamResponse`, \*request handler\* uses it as response. Also
handler can raise a subclass of :exc:`HTTPException`. In this case all
further processing will not happen and client will receive appropriate
http response.
.. note::
A server that does not understand or is unable to comply with any of the
expectation values in the Expect field of a request MUST respond with
appropriate error status. The server MUST respond with a 417
(Expectation Failed) status if any of the expectations cannot be met or,
if there are other problems with the request, some other 4xx status.
http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.20
If all checks pass, the custom handler \*must\* write a \*HTTP/1.1 100 Continue\*
status code before returning.
The following example shows how to setup a custom handler for the \*Expect\*
header::
async def check\_auth(request):
if request.version != aiohttp.HttpVersion11:
return
if request.headers.get('EXPECT') != '100-continue':
raise HTTPExpectationFailed(text="Unknown Expect: %s" % expect)
if request.headers.get('AUTHORIZATION') is None:
raise HTTPForbidden()
request.transport.write(b"HTTP/1.1 100 Continue\r\n\r\n")
async def hello(request):
return web.Response(body=b"Hello, world")
app = web.Application()
app.add\_routes([web.add\_get('/', hello, expect\_handler=check\_auth)])
.. \_aiohttp-web-custom-resource:
Custom resource implementation
------------------------------
To register custom resource use :meth:`~aiohttp.web.UrlDispatcher.register\_resource`.
Resource instance must implement `AbstractResource` interface.
.. \_aiohttp-web-app-runners:
Application runners
-------------------
:func:`run\_app` provides a simple \*blocking\* API for running an
:class:`Application`.
For starting the application \*asynchronously\* or serving on multiple
HOST/PORT :class:`AppRunner` exists.
The simple startup code for serving HTTP site on ``'localhost'``, port
``8080`` looks like::
runner = web.AppRunner(app)
await runner.setup()
site = web.TCPSite(runner, 'localhost', 8080)
await site.start()
while True:
await asyncio.sleep(3600) # sleep forever
To stop serving call :meth:`AppRunner.cleanup`::
await runner.cleanup()
.. versionadded:: 3.0
.. \_aiohttp-web-graceful-shutdown:
Graceful shutdown
------------------
Stopping \*aiohttp web server\* by just closing all connections is not
always satisfactory.
When aiohttp is run with :func:`run\_app`, it will attempt a graceful shutdown
by following these steps (if using a :ref:`runner `,
then calling :meth:`AppRunner.cleanup` will perform these steps, excluding
step 7).
1. Stop each site listening on sockets, so new connections will be rejected.
2. Close idle keep-alive connections (and set active ones to close upon completion).
3. Call the :attr:`Application.on\_shutdown` signal. This should be used to shutdown
long-lived connections, such as websockets (see below).
4. Wait a short time for running handlers to complete. This allows any pending handlers
to complete successfully. The timeout can be adjusted with ``shutdown\_timeout``
in :func:`run\_app`.
5. Close any remaining connections and cancel their handlers. It will wait on the
canceling handlers for a short time, again adjustable with ``shutdown\_timeout``.
6. Call the :attr:`Application.on\_cleanup` signal. This should be used to cleanup any
resources (such as DB connections). This includes completing the
:ref:`cleanup contexts` which may be used to ensure
background tasks are completed successfully (see
:ref:`handler cancellation` or aiojobs\_ for examples).
7. Cancel any remaining tasks and wait on them to complete.
Websocket shutdown
^^^^^^^^^^^^^^^^^^
One problem is if the application supports :term:`websockets ` or
\*data streaming\* it most likely has open connections at server shutdown time.
The \*library\* has no knowledge how to close them gracefully but a developer can
help by registering an :attr:`Application.on\_shutdown` signal handler.
A developer should keep a list of opened connections
(:class:`Application` is a good candidate).
The following :term:`websocket` snippet shows an example of a websocket handler::
from aiohttp import web
import weakref
app = web.Application()
websockets = web.AppKey("websockets", weakref.WeakSet)
app[websockets] = weakref.WeakSet()
async def websocket\_handler(request):
ws = web.WebSocketResponse()
await ws.prepare(request)
request.app[websockets].add(ws)
try:
async for msg in ws:
...
finally:
request.app[websockets].discard(ws)
return ws
Then the signal handler may look like::
from aiohttp import WSCloseCode
async def on\_shutdown(app):
for ws in set(app[websockets]):
await ws.close(code=WSCloseCode.GOING\_AWAY, message="Server shutdown")
app.on\_shutdown.append(on\_shutdown)
.. \_aiohttp-web-ceil-absolute-timeout:
Ceil of absolute timeout value
------------------------------
\*aiohttp\* \*\*ceils\*\* internal timeout values if the value is equal or
greater than 5 seconds. The timeout expires at the next integer second
greater than ``current\_time + timeout``.
More details about ceiling absolute timeout values is available here
:ref:`aiohttp-client-timeouts`.
The default threshold can be configured at :class:`aiohttp.web.Application`
level using the ``handler\_args`` parameter.
.. code-block:: python3
app = web.Application(handler\_args={"timeout\_ceil\_threshold": 1})
.. \_aiohttp-web-background-tasks:
Background tasks
-----------------
Sometimes there's a need to perform some asynchronous operations just
after application start-up.
Even more, in some sophisticated systems there could be a need to run some
background tasks in the event loop along with the application's request
handler. Such as listening to message queue or other network message/event
sources (e.g. ZeroMQ, Redis Pub/Sub, AMQP, etc.) to react to received messages
within the application.
For example the background task could listen to ZeroMQ on
``zmq.SUB`` socket, process and forward retrieved messages to
clients connected via WebSocket that are stored somewhere in the
application (e.g. in the ``application['websockets']`` list).
To run such short and long running background tasks aiohttp provides an
ability to register :attr:`Application.on\_startup` signal handler(s) that
will run along with the application's request handler.
For example there's a need to run one quick task and two long running
tasks that will live till the application is alive. The appropriate
background tasks could be registered as an :attr:`Application.on\_startup`
signal handler or :attr:`Application.cleanup\_ctx` as shown in the example
below::
async def listen\_to\_redis(app: web.Application):
client = redis.from\_url("redis://localhost:6379")
channel = "news"
async with client.pubsub() as pubsub:
await pubsub.subscribe(channel)
while True:
msg = await pubsub.get\_message(ignore\_subscribe\_messages=True)
if msg is not None:
for ws in app["websockets"]:
await ws.send\_str("{}: {}".format(channel, msg))
async def background\_tasks(app):
app[redis\_listener] = asyncio.create\_task(listen\_to\_redis(app))
yield
app[redis\_listener].cancel()
with contextlib.suppress(asyncio.CancelledError):
await app[redis\_listener]
app = web.Application()
redis\_listener = web.AppKey("redis\_listener", asyncio.Task[None])
app.cleanup\_ctx.append(background\_tasks)
web.run\_app(app)
The task ``listen\_to\_redis`` will run forever.
To shut it down correctly :attr:`Application.on\_cleanup` signal handler
may be used to send a cancellation to it.
.. \_aiohttp-web-complex-applications:
Complex Applications
^^^^^^^^^^^^^^^^^^^^
Sometimes aiohttp is not the sole part of an application and additional
tasks/processes may need to be run alongside the aiohttp :class:`Application`.
Generally, the best way to achieve this is to use :func:`aiohttp.web.run\_app`
as the entry point for the program. Other tasks can then be run via
:attr:`Application.startup` and :attr:`Application.on\_cleanup`. By having the
:class:`Application` control the lifecycle of the entire program, the code
will be more robust and ensure that the tasks are started and stopped along
with the application.
For example, running a long-lived task alongside the :class:`Application`
can be done with a :ref:`aiohttp-web-cleanup-ctx` function like::
async def run\_other\_task(\_app):
task = asyncio.create\_task(other\_long\_task())
yield
task.cancel()
with suppress(asyncio.CancelledError):
await task # Ensure any exceptions etc. are raised.
app.cleanup\_ctx.append(run\_other\_task)
Or a separate process can be run with something like::
async def run\_process(\_app):
proc = await asyncio.create\_subprocess\_exec(path)
yield
if proc.returncode is None:
proc.terminate()
await proc.wait()
app.cleanup\_ctx.append(run\_process)
Handling error pages
--------------------
Pages like \*404 Not Found\* and \*500 Internal Error\* could be handled
by custom middleware, see :ref:`polls demo `
for example.
.. \_aiohttp-web-forwarded-support:
Deploying behind a Proxy
------------------------
As discussed in :ref:`aiohttp-deployment` the preferable way is
deploying \*aiohttp\* web server behind a \*Reverse Proxy Server\* like
:term:`nginx` for production usage.
In this way properties like :attr:`BaseRequest.scheme`
:attr:`BaseRequest.host` and :attr:`BaseRequest.remote` are
incorrect.
Real values should be given from proxy server, usually either
``Forwarded`` or old-fashion ``X-Forwarded-For``,
``X-Forwarded-Host``, ``X-Forwarded-Proto`` HTTP headers are used.
\*aiohttp\* does not take \*forwarded\* headers into account by default
because it produces \*security issue\*: HTTP client might add these
headers too, pushing non-trusted data values.
That's why \*aiohttp server\* should setup \*forwarded\* headers in custom
middleware in tight conjunction with \*reverse proxy configuration\*.
For changing :attr:`BaseRequest.scheme` :attr:`BaseRequest.host`
:attr:`BaseRequest.remote` and :attr:`BaseRequest.client\_max\_size`
the middleware might use :meth:`BaseRequest.clone`.
.. seealso::
https://github.com/aio-libs/aiohttp-remotes provides secure helpers
for modifying \*scheme\*, \*host\* and \*remote\* attributes according
to ``Forwarded`` and ``X-Forwarded-\*`` HTTP headers.
CORS support
------------
:mod:`aiohttp.web` itself does not support `Cross-Origin Resource
Sharing `\_, but
there is an aiohttp plugin for it:
`aiohttp-cors `\_.
Debug Toolbar
-------------
`aiohttp-debugtoolbar`\_ is a very useful library that provides a
debugging toolbar while you're developing an :mod:`aiohttp.web`
application.
Install it with ``pip``:
.. code-block:: shell
$ pip install aiohttp\_debugtoolbar
Just call :func:`aiohttp\_debugtoolbar.setup`::
import aiohttp\_debugtoolbar
from aiohttp\_debugtoolbar import toolbar\_middleware\_factory
app = web.Application()
aiohttp\_debugtoolbar.setup(app)
The toolbar is ready to use. Enjoy!!!
.. \_aiohttp-debugtoolbar: https://github.com/aio-libs/aiohttp\_debugtoolbar
Dev Tools
---------
`aiohttp-devtools`\_ provides a couple of tools to simplify development of
:mod:`aiohttp.web` applications.
Install with ``pip``:
.. code-block:: shell
$ pip install aiohttp-devtools
``adev runserver`` provides a development server with auto-reload,
live-reload, static file serving.
Documentation and a complete tutorial of creating and running an app
locally are available at `aiohttp-devtools`\_.
.. \_aiohttp-devtools: https://github.com/aio-libs/aiohttp-devtools
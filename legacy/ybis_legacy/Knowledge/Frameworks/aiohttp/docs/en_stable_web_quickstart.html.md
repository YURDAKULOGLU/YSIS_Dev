Web Server Quickstart — aiohttp 3.13.3 documentation

# Web Server Quickstart[¶](#web-server-quickstart "Link to this heading")

## Run a Simple Web Server[¶](#run-a-simple-web-server "Link to this heading")

In order to implement a web server, first create a
[request handler](#aiohttp-web-handler).

A request handler must be a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that
accepts a [`Request`](web_reference.html#aiohttp.web.Request "aiohttp.web.Request") instance as its only parameter and returns a
[`Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response") instance:

```
from aiohttp import web

async def hello(request):
    return web.Response(text="Hello, world")
```

Next, create an [`Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") instance and register the
request handler on a particular *HTTP method* and *path*:

```
app = web.Application()
app.add_routes([web.get('/', hello)])
```

After that, run the application by [`run_app()`](web_reference.html#aiohttp.web.run_app "aiohttp.web.run_app") call:

```
web.run_app(app)
```

That’s it. Now, head over to `http://localhost:8080/` to see the results.

Alternatively if you prefer *route decorators* create a *route table*
and register a [web-handler](glossary.html#term-web-handler):

```
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")

app = web.Application()
app.add_routes(routes)
web.run_app(app)
```

Both ways essentially do the same work, the difference is only in your
taste: do you prefer *Django style* with famous `urls.py` or *Flask*
with shiny route decorators.

*aiohttp* server documentation uses both ways in code snippets to
emphasize their equality, switching from one style to another is very
trivial.

See also

[Graceful shutdown](web_advanced.html#aiohttp-web-graceful-shutdown) section explains what [`run_app()`](web_reference.html#aiohttp.web.run_app "aiohttp.web.run_app")
does and how to implement complex server initialization/finalization
from scratch.

[Application runners](web_advanced.html#aiohttp-web-app-runners) for more handling more complex cases
like *asynchronous* web application serving and multiple hosts
support.

## Command Line Interface (CLI)[¶](#command-line-interface-cli "Link to this heading")

[`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") implements a basic CLI for quickly serving an
[`Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") in *development* over TCP/IP:

```
$ python -m aiohttp.web -H localhost -P 8080 package.module:init_func
```

`package.module:init_func` should be an importable [callable](glossary.html#term-callable) that
accepts a list of any non-parsed command-line arguments and returns an
[`Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") instance after setting it up:

```
def init_func(argv):
    app = web.Application()
    app.router.add_get("/", index_handler)
    return app
```

Note

For local development we typically recommend using
[aiohttp-devtools](https://github.com/aio-libs/aiohttp-devtools).

## Handler[¶](#handler "Link to this heading")

A request handler must be a [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that accepts a
[`Request`](web_reference.html#aiohttp.web.Request "aiohttp.web.Request") instance as its only argument and returns a
[`StreamResponse`](web_reference.html#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse") derived (e.g. [`Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response")) instance:

```
async def handler(request):
    return web.Response()
```

Handlers are setup to handle requests by registering them with the
[`Application.add_routes()`](web_reference.html#aiohttp.web.Application.add_routes "aiohttp.web.Application.add_routes") on a particular route (*HTTP method* and
*path* pair) using helpers like [`get()`](web_reference.html#aiohttp.web.get "aiohttp.web.get") and
[`post()`](web_reference.html#aiohttp.web.post "aiohttp.web.post"):

```
app.add_routes([web.get('/', handler),
                web.post('/post', post_handler),
                web.put('/put', put_handler)])
```

Or use *route decorators*:

```
routes = web.RouteTableDef()

@routes.get('/')
async def get_handler(request):
    ...

@routes.post('/post')
async def post_handler(request):
    ...

@routes.put('/put')
async def put_handler(request):
    ...

app.add_routes(routes)
```

Wildcard *HTTP method* is also supported by [`route()`](web_reference.html#aiohttp.web.route "aiohttp.web.route") or
[`RouteTableDef.route()`](web_reference.html#aiohttp.web.RouteTableDef.route "aiohttp.web.RouteTableDef.route"), allowing a handler to serve incoming
requests on a *path* having **any** *HTTP method*:

```
app.add_routes([web.route('*', '/path', all_handler)])
```

The *HTTP method* can be queried later in the request handler using the
[`aiohttp.web.BaseRequest.method`](web_reference.html#aiohttp.web.BaseRequest.method "aiohttp.web.BaseRequest.method") property.

By default endpoints added with `GET` method will accept
`HEAD` requests and return the same response headers as they would
for a `GET` request. You can also deny `HEAD` requests on a route:

```
web.get('/', handler, allow_head=False)
```

Here `handler` won’t be called on `HEAD` request and the server
will respond with `405: Method Not Allowed`.

See also

[Peer disconnection](web_advanced.html#aiohttp-web-peer-disconnection) section explains how handlers
behave when a client connection drops and ways to optimize handling
of this.

## Resources and Routes[¶](#resources-and-routes "Link to this heading")

Internally routes are served by [`Application.router`](web_reference.html#aiohttp.web.Application.router "aiohttp.web.Application.router")
([`UrlDispatcher`](web_reference.html#aiohttp.web.UrlDispatcher "aiohttp.web.UrlDispatcher") instance).

The *router* is a list of *resources*.

Resource is an entry in *route table* which corresponds to requested URL.

Resource in turn has at least one *route*.

Route corresponds to handling *HTTP method* by calling *web handler*.

Thus when you add a *route* the *resource* object is created under the hood.

The library implementation **merges** all subsequent route additions
for the same path adding the only resource for all HTTP methods.

Consider two examples:

```
app.add_routes([web.get('/path1', get_1),
                web.post('/path1', post_1),
                web.get('/path2', get_2),
                web.post('/path2', post_2)]
```

and:

```
app.add_routes([web.get('/path1', get_1),
                web.get('/path2', get_2),
                web.post('/path2', post_2),
                web.post('/path1', post_1)]
```

First one is *optimized*. You have got the idea.

### Variable Resources[¶](#variable-resources "Link to this heading")

Resource may have *variable path* also. For instance, a resource with
the path `'/a/{name}/c'` would match all incoming requests with
paths such as `'/a/b/c'`, `'/a/1/c'`, and `'/a/etc/c'`.

A variable *part* is specified in the form `{identifier}`, where the
`identifier` can be used later in a
[request handler](#aiohttp-web-handler) to access the matched value for
that *part*. This is done by looking up the `identifier` in the
[`Request.match_info`](web_reference.html#aiohttp.web.Request.match_info "aiohttp.web.Request.match_info") mapping:

```
@routes.get('/{name}')
async def variable_handler(request):
    return web.Response(
        text="Hello, {}".format(request.match_info['name']))
```

By default, each *part* matches the regular expression `[^{}/]+`.

You can also specify a custom regex in the form `{identifier:regex}`:

```
web.get(r'/{name:\d+}', handler)
```

### Reverse URL Constructing using Named Resources[¶](#reverse-url-constructing-using-named-resources "Link to this heading")

Routes can also be given a *name*:

```
@routes.get('/root', name='root')
async def handler(request):
    ...
```

Which can then be used to access and build a *URL* for that resource later (e.g.
in a [request handler](#aiohttp-web-handler)):

```
url = request.app.router['root'].url_for().with_query({"a": "b", "c": "d"})
assert url == URL('/root?a=b&c=d')
```

A more interesting example is building *URLs* for [variable
resources](#aiohttp-web-variable-handler):

```
app.router.add_resource(r'/{user}/info', name='user-info')
```

In this case you can also pass in the *parts* of the route:

```
url = request.app.router['user-info'].url_for(user='john_doe')
url_with_qs = url.with_query("a=b")
assert url_with_qs == '/john_doe/info?a=b'
```

### Organizing Handlers in Classes[¶](#organizing-handlers-in-classes "Link to this heading")

As discussed above, [handlers](#aiohttp-web-handler) can be first-class
coroutines:

```
async def hello(request):
    return web.Response(text="Hello, world")

app.router.add_get('/', hello)
```

But sometimes it’s convenient to group logically similar handlers into a Python
*class*.

Since [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") does not dictate any implementation details,
application developers can organize handlers in classes if they so wish:

```
class Handler:

    def __init__(self):
        pass

    async def handle_intro(self, request):
        return web.Response(text="Hello, world")

    async def handle_greeting(self, request):
        name = request.match_info.get('name', "Anonymous")
        txt = "Hello, {}".format(name)
        return web.Response(text=txt)

handler = Handler()
app.add_routes([web.get('/intro', handler.handle_intro),
                web.get('/greet/{name}', handler.handle_greeting)])
```

### Class Based Views[¶](#class-based-views "Link to this heading")

[`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") has support for *class based views*.

You can derive from [`View`](web_reference.html#aiohttp.web.View "aiohttp.web.View") and define methods for handling http
requests:

```
class MyView(web.View):
    async def get(self):
        return await get_resp(self.request)

    async def post(self):
        return await post_resp(self.request)
```

Handlers should be coroutines accepting *self* only and returning
response object as regular [web-handler](glossary.html#term-web-handler). Request object can be
retrieved by [`View.request`](web_reference.html#aiohttp.web.View.request "aiohttp.web.View.request") property.

After implementing the view (`MyView` from example above) should be
registered in application’s router:

```
web.view('/path/to', MyView)
```

or:

```
@routes.view('/path/to')
class MyView(web.View):
    ...
```

Example will process GET and POST requests for */path/to* but raise
*405 Method not allowed* exception for unimplemented HTTP methods.

### Resource Views[¶](#resource-views "Link to this heading")

*All* registered resources in a router can be viewed using the
[`UrlDispatcher.resources()`](web_reference.html#aiohttp.web.UrlDispatcher.resources "aiohttp.web.UrlDispatcher.resources") method:

```
for resource in app.router.resources():
    print(resource)
```

A *subset* of the resources that were registered with a *name* can be
viewed using the [`UrlDispatcher.named_resources()`](web_reference.html#aiohttp.web.UrlDispatcher.named_resources "aiohttp.web.UrlDispatcher.named_resources") method:

```
for name, resource in app.router.named_resources().items():
    print(name, resource)
```

## Alternative ways for registering routes[¶](#alternative-ways-for-registering-routes "Link to this heading")

Code examples shown above use *imperative* style for adding new
routes: they call `app.router.add_get(...)` etc.

There are two alternatives: route tables and route decorators.

Route tables look like Django way:

```
async def handle_get(request):
    ...


async def handle_post(request):
    ...

app.router.add_routes([web.get('/get', handle_get),
                       web.post('/post', handle_post),
```

The snippet calls [`add_routes()`](web_reference.html#aiohttp.web.UrlDispatcher.add_routes "aiohttp.web.UrlDispatcher.add_routes") to
register a list of *route definitions* ([`aiohttp.web.RouteDef`](web_reference.html#aiohttp.web.RouteDef "aiohttp.web.RouteDef")
instances) created by [`aiohttp.web.get()`](web_reference.html#aiohttp.web.get "aiohttp.web.get") or
[`aiohttp.web.post()`](web_reference.html#aiohttp.web.post "aiohttp.web.post") functions.

See also

[RouteDef and StaticDef](web_reference.html#aiohttp-web-route-def) reference.

Route decorators are closer to Flask approach:

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

It is also possible to use decorators with class-based views:

```
routes = web.RouteTableDef()

@routes.view("/view")
class MyView(web.View):
    async def get(self):
        ...

    async def post(self):
        ...

app.router.add_routes(routes)
```

The example creates a [`aiohttp.web.RouteTableDef`](web_reference.html#aiohttp.web.RouteTableDef "aiohttp.web.RouteTableDef") container first.

The container is a list-like object with additional decorators
[`aiohttp.web.RouteTableDef.get()`](web_reference.html#aiohttp.web.RouteTableDef.get "aiohttp.web.RouteTableDef.get"),
[`aiohttp.web.RouteTableDef.post()`](web_reference.html#aiohttp.web.RouteTableDef.post "aiohttp.web.RouteTableDef.post") etc. for registering new
routes.

After filling the container
[`add_routes()`](web_reference.html#aiohttp.web.UrlDispatcher.add_routes "aiohttp.web.UrlDispatcher.add_routes") is used for adding
registered *route definitions* into application’s router.

See also

[RouteTableDef](web_reference.html#aiohttp-web-route-table-def) reference.

All tree ways (imperative calls, route tables and decorators) are
equivalent, you could use what do you prefer or even mix them on your
own.

Added in version 2.3.

## JSON Response[¶](#json-response "Link to this heading")

It is a common case to return JSON data in response, [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web")
provides a shortcut for returning JSON – [`aiohttp.web.json_response()`](web_reference.html#aiohttp.web.json_response "aiohttp.web.json_response"):

```
async def handler(request):
    data = {'some': 'data'}
    return web.json_response(data)
```

The shortcut method returns [`aiohttp.web.Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response") instance
so you can for example set cookies before returning it from handler.

## User Sessions[¶](#user-sessions "Link to this heading")

Often you need a container for storing user data across requests. The concept
is usually called a *session*.

[`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") has no built-in concept of a *session*, however, there is a
third-party library, [`aiohttp_session`](https://aiohttp-session.readthedocs.io/en/stable/reference.html#module-aiohttp_session "(in aiohttp_session v2.12)"), that adds *session* support:

```
import asyncio
import time
import base64
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

async def handler(request):
    session = await get_session(request)

    last_visit = session.get("last_visit")
    session["last_visit"] = time.time()
    text = "Last visited: {}".format(last_visit)

    return web.Response(text=text)

async def make_app():
    app = web.Application()
    # secret_key must be 32 url-safe base64-encoded bytes
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    app.add_routes([web.get('/', handler)])
    return app

web.run_app(make_app())
```

## HTTP Forms[¶](#http-forms "Link to this heading")

HTTP Forms are supported out of the box.

If form’s method is `"GET"` (`<form method="get">`) use
[`aiohttp.web.BaseRequest.query`](web_reference.html#aiohttp.web.BaseRequest.query "aiohttp.web.BaseRequest.query") for getting form data.

To access form data with `"POST"` method use
[`aiohttp.web.BaseRequest.post()`](web_reference.html#aiohttp.web.BaseRequest.post "aiohttp.web.BaseRequest.post") or [`aiohttp.web.BaseRequest.multipart()`](web_reference.html#aiohttp.web.BaseRequest.multipart "aiohttp.web.BaseRequest.multipart").

[`aiohttp.web.BaseRequest.post()`](web_reference.html#aiohttp.web.BaseRequest.post "aiohttp.web.BaseRequest.post") accepts both
`'application/x-www-form-urlencoded'` and `'multipart/form-data'`
form’s data encoding (e.g. `<form enctype="multipart/form-data">`).
It stores files data in temporary directory. If client\_max\_size is
specified post raises ValueError exception.
For efficiency use [`aiohttp.web.BaseRequest.multipart()`](web_reference.html#aiohttp.web.BaseRequest.multipart "aiohttp.web.BaseRequest.multipart"), It is especially effective
for uploading large files ([File Uploads](#aiohttp-web-file-upload)).

Values submitted by the following form:

```
<form action="/login" method="post" accept-charset="utf-8"
      enctype="application/x-www-form-urlencoded">

    <label for="login">Login</label>
    <input id="login" name="login" type="text" value="" autofocus/>
    <label for="password">Password</label>
    <input id="password" name="password" type="password" value=""/>

    <input type="submit" value="login"/>
</form>
```

could be accessed as:

```
async def do_login(request):
    data = await request.post()
    login = data['login']
    password = data['password']
```

## File Uploads[¶](#file-uploads "Link to this heading")

[`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") has built-in support for handling files uploaded from the
browser.

First, make sure that the HTML `<form>` element has its *enctype* attribute
set to `enctype="multipart/form-data"`. As an example, here is a form that
accepts an MP3 file:

```
<form action="/store/mp3" method="post" accept-charset="utf-8"
      enctype="multipart/form-data">

    <label for="mp3">Mp3</label>
    <input id="mp3" name="mp3" type="file" value=""/>

    <input type="submit" value="submit"/>
</form>
```

Then, in the [request handler](#aiohttp-web-handler) you can access the
file input field as a [`FileField`](web_reference.html#aiohttp.web.FileField "aiohttp.web.FileField") instance. [`FileField`](web_reference.html#aiohttp.web.FileField "aiohttp.web.FileField") is simply
a container for the file as well as some of its metadata:

```
async def store_mp3_handler(request):

    # WARNING: don't do that if you plan to receive large files!
    data = await request.post()

    mp3 = data['mp3']

    # .filename contains the name of the file in string format.
    filename = mp3.filename

    # .file contains the actual file data that needs to be stored somewhere.
    mp3_file = data['mp3'].file

    content = mp3_file.read()

    return web.Response(body=content,
                        headers=MultiDict(
                            {'CONTENT-DISPOSITION': mp3_file}))
```

You might have noticed a big warning in the example above. The general issue is
that [`aiohttp.web.BaseRequest.post()`](web_reference.html#aiohttp.web.BaseRequest.post "aiohttp.web.BaseRequest.post") reads the whole payload in memory,
resulting in possible
OOM errors. To avoid this, for multipart uploads, you
should use [`aiohttp.web.BaseRequest.multipart()`](web_reference.html#aiohttp.web.BaseRequest.multipart "aiohttp.web.BaseRequest.multipart") which returns a [multipart reader](multipart.html#aiohttp-multipart):

```
async def store_mp3_handler(request):

    reader = await request.multipart()

    # /!\ Don't forget to validate your inputs /!\

    # reader.next() will `yield` the fields of your form

    field = await reader.next()
    assert field.name == 'name'
    name = await field.read(decode=True)

    field = await reader.next()
    assert field.name == 'mp3'
    filename = field.filename
    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    with open(os.path.join('/spool/yarrr-media/mp3/', filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(filename, size))
```

## WebSockets[¶](#websockets "Link to this heading")

[`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") supports *WebSockets* out-of-the-box.

To setup a *WebSocket*, create a [`WebSocketResponse`](web_reference.html#aiohttp.web.WebSocketResponse "aiohttp.web.WebSocketResponse") in a
[request handler](#aiohttp-web-handler) and then use it to communicate
with the peer:

```
async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws
```

The handler should be registered as HTTP GET processor:

```
app.add_routes([web.get('/ws', websocket_handler)])
```

## Redirects[¶](#redirects "Link to this heading")

To redirect user to another endpoint - raise `HTTPFound` with
an absolute URL, relative URL or view name (the argument from router):

```
raise web.HTTPFound('/redirect')
```

The following example shows redirect to view named ‘login’ in routes:

```
async def handler(request):
    location = request.app.router['login'].url_for()
    raise web.HTTPFound(location=location)

router.add_get('/handler', handler)
router.add_get('/login', login_handler, name='login')
```

Example with login validation:

```
@aiohttp_jinja2.template('login.html')
async def login(request):

    if request.method == 'POST':
        form = await request.post()
        error = validate_login(form)
        if error:
            return {'error': error}
        else:
            # login form is valid
            location = request.app.router['index'].url_for()
            raise web.HTTPFound(location=location)

    return {}

app.router.add_get('/', index, name='index')
app.router.add_get('/login', login, name='login')
app.router.add_post('/login', login, name='login')
```

## Exceptions[¶](#exceptions "Link to this heading")

[`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") defines a set of exceptions for every *HTTP status code*.

Each exception is a subclass of [`HTTPException`](web_reference.html#aiohttp.web.HTTPException "aiohttp.web.HTTPException") and relates to a single
HTTP status code:

```
async def handler(request):
    raise aiohttp.web.HTTPFound('/redirect')
```

Warning

Returning [`HTTPException`](web_reference.html#aiohttp.web.HTTPException "aiohttp.web.HTTPException") or its subclasses is deprecated and will
be removed in subsequent aiohttp versions.

Each exception class has a status code according to [**RFC 2068**](https://datatracker.ietf.org/doc/html/rfc2068.html):
codes with 100-300 are not really errors; 400s are client errors,
and 500s are server errors.

HTTP Exception hierarchy chart:

```
Exception
  HTTPException
    HTTPSuccessful
      * 200 - HTTPOk
      * 201 - HTTPCreated
      * 202 - HTTPAccepted
      * 203 - HTTPNonAuthoritativeInformation
      * 204 - HTTPNoContent
      * 205 - HTTPResetContent
      * 206 - HTTPPartialContent
    HTTPRedirection
      * 300 - HTTPMultipleChoices
      * 301 - HTTPMovedPermanently
      * 302 - HTTPFound
      * 303 - HTTPSeeOther
      * 304 - HTTPNotModified
      * 305 - HTTPUseProxy
      * 307 - HTTPTemporaryRedirect
      * 308 - HTTPPermanentRedirect
    HTTPError
      HTTPClientError
        * 400 - HTTPBadRequest
        * 401 - HTTPUnauthorized
        * 402 - HTTPPaymentRequired
        * 403 - HTTPForbidden
        * 404 - HTTPNotFound
        * 405 - HTTPMethodNotAllowed
        * 406 - HTTPNotAcceptable
        * 407 - HTTPProxyAuthenticationRequired
        * 408 - HTTPRequestTimeout
        * 409 - HTTPConflict
        * 410 - HTTPGone
        * 411 - HTTPLengthRequired
        * 412 - HTTPPreconditionFailed
        * 413 - HTTPRequestEntityTooLarge
        * 414 - HTTPRequestURITooLong
        * 415 - HTTPUnsupportedMediaType
        * 416 - HTTPRequestRangeNotSatisfiable
        * 417 - HTTPExpectationFailed
        * 421 - HTTPMisdirectedRequest
        * 422 - HTTPUnprocessableEntity
        * 424 - HTTPFailedDependency
        * 426 - HTTPUpgradeRequired
        * 428 - HTTPPreconditionRequired
        * 429 - HTTPTooManyRequests
        * 431 - HTTPRequestHeaderFieldsTooLarge
        * 451 - HTTPUnavailableForLegalReasons
      HTTPServerError
        * 500 - HTTPInternalServerError
        * 501 - HTTPNotImplemented
        * 502 - HTTPBadGateway
        * 503 - HTTPServiceUnavailable
        * 504 - HTTPGatewayTimeout
        * 505 - HTTPVersionNotSupported
        * 506 - HTTPVariantAlsoNegotiates
        * 507 - HTTPInsufficientStorage
        * 510 - HTTPNotExtended
        * 511 - HTTPNetworkAuthenticationRequired
```

All HTTP exceptions have the same constructor signature:

```
HTTPNotFound(*, headers=None, reason=None,
             body=None, text=None, content_type=None)
```

If not directly specified, *headers* will be added to the *default
response headers*.

Classes `HTTPMultipleChoices`, `HTTPMovedPermanently`,
`HTTPFound`, `HTTPSeeOther`, `HTTPUseProxy`,
`HTTPTemporaryRedirect` have the following constructor signature:

```
HTTPFound(location, *, headers=None, reason=None,
          body=None, text=None, content_type=None)
```

where *location* is value for *Location HTTP header*.

`HTTPMethodNotAllowed` is constructed by providing the incoming
unsupported method and list of allowed methods:

```
HTTPMethodNotAllowed(method, allowed_methods, *,
                     headers=None, reason=None,
                     body=None, text=None, content_type=None)
```

`HTTPUnavailableForLegalReasons` should be constructed with a `link`
to yourself (as the entity implementing the blockage), and an explanation for
the block included in `text`.:

```
HTTPUnavailableForLegalReasons(link, *,
                               headers=None, reason=None,
                               body=None, text=None, content_type=None)
```

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
  + [Tutorial](https://demos.aiohttp.org)
  + [Quickstart](#)
  + [Advanced Usage](web_advanced.html)
  + [Low Level](web_lowlevel.html)
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
[Page source](_sources/web_quickstart.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
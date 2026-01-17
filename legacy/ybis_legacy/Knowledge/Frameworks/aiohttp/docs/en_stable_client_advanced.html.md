Advanced Client Usage — aiohttp 3.13.3 documentation

# Advanced Client Usage[¶](#advanced-client-usage "Link to this heading")

## Client Session[¶](#client-session "Link to this heading")

[`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") is the heart and the main entry point for all
client API operations.

Create the session first, use the instance for performing HTTP
requests and initiating WebSocket connections.

The session contains a cookie storage and connection pool, thus
cookies and connections are shared between HTTP requests sent by the
same session.

## Custom Request Headers[¶](#custom-request-headers "Link to this heading")

If you need to add HTTP headers to a request, pass them in a
[`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") to the *headers* parameter.

For example, if you want to specify the content-type directly:

```
url = 'http://example.com/image'
payload = b'GIF89a\x01\x00\x01\x00\x00\xff\x00,\x00\x00'
          b'\x00\x00\x01\x00\x01\x00\x00\x02\x00;'
headers = {'content-type': 'image/gif'}

await session.post(url,
                   data=payload,
                   headers=headers)
```

You also can set default headers for all session requests:

```
headers={"Authorization": "Basic bG9naW46cGFzcw=="}
async with aiohttp.ClientSession(headers=headers) as session:
    async with session.get("http://httpbin.org/headers") as r:
        json_body = await r.json()
        assert json_body['headers']['Authorization'] == \
            'Basic bG9naW46cGFzcw=='
```

Typical use case is sending JSON body. You can specify content type
directly as shown above, but it is more convenient to use special keyword
`json`:

```
await session.post(url, json={'example': 'text'})
```

For *text/plain*

```
await session.post(url, data='Привет, Мир!')
```

## Authentication[¶](#authentication "Link to this heading")

Instead of setting the `Authorization` header directly,
[`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") and individual request methods provide an `auth`
argument. An instance of [`BasicAuth`](client_reference.html#aiohttp.BasicAuth "aiohttp.BasicAuth") can be passed in like this:

```
auth = BasicAuth(login="...", password="...")
async with ClientSession(auth=auth) as session:
    ...
```

For HTTP digest authentication, use the [`DigestAuthMiddleware`](client_reference.html#aiohttp.DigestAuthMiddleware "aiohttp.DigestAuthMiddleware") client middleware:

```
from aiohttp import ClientSession, DigestAuthMiddleware

# Create the middleware with your credentials
digest_auth = DigestAuthMiddleware(login="user", password="password")

# Pass it to the ClientSession as a tuple
async with ClientSession(middlewares=(digest_auth,)) as session:
    # The middleware will automatically handle auth challenges
    async with session.get("https://example.com/protected") as resp:
        print(await resp.text())
```

The [`DigestAuthMiddleware`](client_reference.html#aiohttp.DigestAuthMiddleware "aiohttp.DigestAuthMiddleware") implements HTTP Digest Authentication according to RFC 7616,
providing a more secure alternative to Basic Authentication. It supports all
standard hash algorithms including MD5, SHA, SHA-256, SHA-512 and their session
variants, as well as both ‘auth’ and ‘auth-int’ quality of protection (qop) options.
The middleware automatically handles the authentication flow by intercepting 401 responses
and retrying with proper credentials.

Note that if the request is redirected and the redirect URL contains
credentials, those credentials will supersede any previously set credentials.
In other words, if `http://user@example.com` redirects to
`http://other_user@example.com`, the second request will be authenticated
as `other_user`. Providing both the `auth` parameter and authentication in
the *initial* URL will result in a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)").

For other authentication flows, the `Authorization` header can be set
directly:

```
headers = {"Authorization": "Bearer eyJh...0M30"}
async with ClientSession(headers=headers) as session:
    ...
```

The authentication header for a session may be updated as and when required.
For example:

```
session.headers["Authorization"] = "Bearer eyJh...1OH0"
```

Note that a *copy* of the headers dictionary is set as an attribute when
creating a [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") instance (as a [`multidict.CIMultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)")
object). Updating the original dictionary does not have any effect.

In cases where the authentication header value expires periodically, an
[`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio "(in Python v3.14)") task may be used to update the session’s default headers in the
background.

Note

`Authorization` header will be removed if you get redirected
to a different host or protocol.

## Client Middleware[¶](#client-middleware "Link to this heading")

The client supports middleware to intercept requests and responses. This can be
useful for authentication, logging, request/response modification, retries etc.

For more examples and common middleware patterns, see the [Client Middleware Cookbook](client_middleware_cookbook.html#aiohttp-client-middleware-cookbook).

### Creating a middleware[¶](#creating-a-middleware "Link to this heading")

To create a middleware, define an async function (or callable class) that accepts a request object
and a handler function, and returns a response. Middlewares must follow the
[`ClientMiddlewareType`](client_reference.html#aiohttp.ClientMiddlewareType "aiohttp.ClientMiddlewareType") signature:

```
async def auth_middleware(req: ClientRequest, handler: ClientHandlerType) -> ClientResponse:
    req.headers["Authorization"] = get_auth_header()
    return await handler(req)
```

### Using Middlewares[¶](#using-middlewares "Link to this heading")

You can apply middlewares to a client session or to individual requests:

```
# Apply to all requests in a session
async with ClientSession(middlewares=(my_middleware,)) as session:
    resp = await session.get("http://example.com")

# Apply to a specific request
async with ClientSession() as session:
    resp = await session.get("http://example.com", middlewares=(my_middleware,))
```

### Middleware Chaining[¶](#middleware-chaining "Link to this heading")

Multiple middlewares are applied in the order they are listed:

```
# Middlewares are applied in order: logging -> auth -> request
async with ClientSession(middlewares=(logging_middleware, auth_middleware)) as session:
    async with session.get("http://example.com") as resp:
        ...
```

A key aspect to understand about the middleware sequence is that the execution flow follows this pattern:

1. The first middleware in the list is called first and executes its code before calling the handler
2. The handler is the next middleware in the chain (or the request handler if there are no more middlewares)
3. When the handler returns a response, execution continues from the last middleware right after the handler call
4. This creates a nested “onion-like” pattern for execution

For example, with `middlewares=(middleware1, middleware2)`, the execution order would be:

1. Enter `middleware1` (pre-request code)
2. Enter `middleware2` (pre-request code)
3. Execute the actual request handler
4. Exit `middleware2` (post-response code)
5. Exit `middleware1` (post-response code)

This flat structure means that a middleware is applied on each retry attempt inside the client’s retry loop,
not just once before all retries. This allows middleware to modify requests freshly on each retry attempt.

For example, if we had a retry middleware and a logging middleware, and we want every retried request to be
logged separately, then we’d need to specify `middlewares=(retry_mw, logging_mw)`. If we reversed the order
to `middlewares=(logging_mw, retry_mw)`, then we’d only log once regardless of how many retries are done.

Note

Client middleware is a powerful feature but should be used judiciously.
Each middleware adds overhead to request processing. For simple use cases
like adding static headers, you can often use request parameters
(e.g., `headers`) or session configuration instead.

## Custom Cookies[¶](#custom-cookies "Link to this heading")

To send your own cookies to the server, you can use the *cookies*
parameter of [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") constructor:

```
url = 'http://httpbin.org/cookies'
cookies = {'cookies_are': 'working'}
async with ClientSession(cookies=cookies) as session:
    async with session.get(url) as resp:
        assert await resp.json() == {
           "cookies": {"cookies_are": "working"}}
```

Note

`httpbin.org/cookies` endpoint returns request cookies
in JSON-encoded body.
To access session cookies see [`ClientSession.cookie_jar`](client_reference.html#aiohttp.ClientSession.cookie_jar "aiohttp.ClientSession.cookie_jar").

[`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") may be used for sharing cookies
between multiple requests:

```
async with aiohttp.ClientSession() as session:
    async with session.get(
        "http://httpbin.org/cookies/set?my_cookie=my_value",
        allow_redirects=False
    ) as resp:
        assert resp.cookies["my_cookie"].value == "my_value"
    async with session.get("http://httpbin.org/cookies") as r:
        json_body = await r.json()
        assert json_body["cookies"]["my_cookie"] == "my_value"
```

## Response Headers and Cookies[¶](#response-headers-and-cookies "Link to this heading")

We can view the server’s response [`ClientResponse.headers`](client_reference.html#aiohttp.ClientResponse.headers "aiohttp.ClientResponse.headers") using
a [`CIMultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDictProxy "(in multidict v6.7)"):

```
assert resp.headers == {
    'ACCESS-CONTROL-ALLOW-ORIGIN': '*',
    'CONTENT-TYPE': 'application/json',
    'DATE': 'Tue, 15 Jul 2014 16:49:51 GMT',
    'SERVER': 'gunicorn/18.0',
    'CONTENT-LENGTH': '331',
    'CONNECTION': 'keep-alive'}
```

The dictionary is special, though: it’s made just for HTTP
headers. According to [RFC 7230](http://tools.ietf.org/html/rfc7230#section-3.2), HTTP Header names
are case-insensitive. It also supports multiple values for the same
key as HTTP protocol does.

So, we can access the headers using any capitalization we want:

```
assert resp.headers['Content-Type'] == 'application/json'

assert resp.headers.get('content-type') == 'application/json'
```

All headers are converted from binary data using UTF-8 with
`surrogateescape` option. That works fine on most cases but
sometimes unconverted data is needed if a server uses nonstandard
encoding. While these headers are malformed from [**RFC 7230**](https://datatracker.ietf.org/doc/html/rfc7230.html)
perspective they may be retrieved by using
[`ClientResponse.raw_headers`](client_reference.html#aiohttp.ClientResponse.raw_headers "aiohttp.ClientResponse.raw_headers") property:

```
assert resp.raw_headers == (
    (b'SERVER', b'nginx'),
    (b'DATE', b'Sat, 09 Jan 2016 20:28:40 GMT'),
    (b'CONTENT-TYPE', b'text/html; charset=utf-8'),
    (b'CONTENT-LENGTH', b'12150'),
    (b'CONNECTION', b'keep-alive'))
```

If a response contains some *HTTP Cookies*, you can quickly access them:

```
url = 'http://example.com/some/cookie/setting/url'
async with session.get(url) as resp:
    print(resp.cookies['example_cookie_name'])
```

Note

Response cookies contain only values, that were in `Set-Cookie` headers
of the **last** request in redirection chain. To gather cookies between all
redirection requests please use [aiohttp.ClientSession](#aiohttp-client-session) object.

## Redirection History[¶](#redirection-history "Link to this heading")

If a request was redirected, it is possible to view previous responses using
the [`history`](client_reference.html#aiohttp.ClientResponse.history "aiohttp.ClientResponse.history") attribute:

```
resp = await session.get('http://example.com/some/redirect/')
assert resp.status == 200
assert resp.url = URL('http://example.com/some/other/url/')
assert len(resp.history) == 1
assert resp.history[0].status == 301
assert resp.history[0].url = URL(
    'http://example.com/some/redirect/')
```

If no redirects occurred or `allow_redirects` is set to `False`,
history will be an empty sequence.

## Cookie Jar[¶](#cookie-jar "Link to this heading")

### Cookie Safety[¶](#cookie-safety "Link to this heading")

By default [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") uses strict version of
[`aiohttp.CookieJar`](client_reference.html#aiohttp.CookieJar "aiohttp.CookieJar"). [**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html) explicitly forbids cookie
accepting from URLs with IP address instead of DNS name
(e.g. `http://127.0.0.1:80/cookie`).

It’s good but sometimes for testing we need to enable support for such
cookies. It should be done by passing `unsafe=True` to
[`aiohttp.CookieJar`](client_reference.html#aiohttp.CookieJar "aiohttp.CookieJar") constructor:

```
jar = aiohttp.CookieJar(unsafe=True)
session = aiohttp.ClientSession(cookie_jar=jar)
```

### Cookie Quoting Routine[¶](#cookie-quoting-routine "Link to this heading")

The client uses the `SimpleCookie` quoting routines
conform to the [**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html), which in turn references the character definitions
from [**RFC 2068**](https://datatracker.ietf.org/doc/html/rfc2068.html). They provide a two-way quoting algorithm where any non-text
character is translated into a 4 character sequence: a forward-slash
followed by the three-digit octal equivalent of the character.
Any `\` or `"` is quoted with a preceding `\` slash.
Because of the way browsers really handle cookies (as opposed to what the RFC
says) we also encode `,` and `;`.

Some backend systems does not support quoted cookies. You can skip this
quotation routine by passing `quote_cookie=False` to the
[`CookieJar`](client_reference.html#aiohttp.CookieJar "aiohttp.CookieJar") constructor:

```
jar = aiohttp.CookieJar(quote_cookie=False)
session = aiohttp.ClientSession(cookie_jar=jar)
```

### Dummy Cookie Jar[¶](#dummy-cookie-jar "Link to this heading")

Sometimes cookie processing is not desirable. For this purpose it’s
possible to pass [`aiohttp.DummyCookieJar`](client_reference.html#aiohttp.DummyCookieJar "aiohttp.DummyCookieJar") instance into client
session:

```
jar = aiohttp.DummyCookieJar()
session = aiohttp.ClientSession(cookie_jar=jar)
```

## Uploading pre-compressed data[¶](#uploading-pre-compressed-data "Link to this heading")

To upload data that is already compressed before passing it to
aiohttp, call the request function with the used compression algorithm
name (usually `deflate` or `gzip`) as the value of the
`Content-Encoding` header:

```
async def my_coroutine(session, headers, my_data):
    data = zlib.compress(my_data)
    headers = {'Content-Encoding': 'deflate'}
    async with session.post('http://httpbin.org/post',
                            data=data,
                            headers=headers)
        pass
```

## Disabling content type validation for JSON responses[¶](#disabling-content-type-validation-for-json-responses "Link to this heading")

The standard explicitly restricts JSON `Content-Type` HTTP header to
`application/json` or any extended form, e.g. `application/vnd.custom-type+json`.
Unfortunately, some servers send a wrong type, like `text/html`.

This can be worked around in two ways:

1. Pass the expected type explicitly (in this case checking will be strict, without the extended form support,
   so `custom/xxx+type` won’t be accepted):

   `await resp.json(content_type='custom/type')`.
2. Disable the check entirely:

   `await resp.json(content_type=None)`.

## Client Tracing[¶](#client-tracing "Link to this heading")

The execution flow of a specific request can be followed attaching
listeners coroutines to the signals provided by the
[`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") instance, this instance will be used as a
parameter for the [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") constructor having as a
result a client that triggers the different signals supported by the
[`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig"). By default any instance of
[`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") class comes with the signals ability
disabled. The following snippet shows how the start and the end
signals of a request flow can be followed:

```
async def on_request_start(
        session, trace_config_ctx, params):
    print("Starting request")

async def on_request_end(session, trace_config_ctx, params):
    print("Ending request")

trace_config = aiohttp.TraceConfig()
trace_config.on_request_start.append(on_request_start)
trace_config.on_request_end.append(on_request_end)
async with aiohttp.ClientSession(
        trace_configs=[trace_config]) as client:
    client.get('http://example.com/some/redirect/')
```

The `trace_configs` is a list that can contain instances of
[`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") class that allow run the signals handlers coming
from different [`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") instances. The following example
shows how two different [`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") that have a different
nature are installed to perform their job in each signal handle:

```
from mylib.traceconfig import AuditRequest
from mylib.traceconfig import XRay

async with aiohttp.ClientSession(
        trace_configs=[AuditRequest(), XRay()]) as client:
    client.get('http://example.com/some/redirect/')
```

All signals take as a parameters first, the [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession")
instance used by the specific request related to that signals and
second, a [`SimpleNamespace`](https://docs.python.org/3/library/types.html#types.SimpleNamespace "(in Python v3.14)") instance called
`trace_config_ctx`. The `trace_config_ctx` object can be used to
share the state through to the different signals that belong to the
same request and to the same [`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") class, perhaps:

```
async def on_request_start(
        session, trace_config_ctx, params):
    trace_config_ctx.start = asyncio.get_event_loop().time()

async def on_request_end(session, trace_config_ctx, params):
    elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
    print("Request took {}".format(elapsed))
```

The `trace_config_ctx` param is by default a
[`SimpleNamespace`](https://docs.python.org/3/library/types.html#types.SimpleNamespace "(in Python v3.14)") that is initialized at the beginning of the
request flow. However, the factory used to create this object can be
overwritten using the `trace_config_ctx_factory` constructor param of
the [`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") class.

The `trace_request_ctx` param can given at the beginning of the
request execution, accepted by all of the HTTP verbs, and will be
passed as a keyword argument for the `trace_config_ctx_factory`
factory. This param is useful to pass data that is only available at
request time, perhaps:

```
async def on_request_start(
        session, trace_config_ctx, params):
    print(trace_config_ctx.trace_request_ctx)


session.get('http://example.com/some/redirect/',
            trace_request_ctx={'foo': 'bar'})
```

See also

[Tracing Reference](tracing_reference.html#aiohttp-client-tracing-reference) section for
more information about the different signals supported.

## Connectors[¶](#connectors "Link to this heading")

To tweak or change *transport* layer of requests you can pass a custom
*connector* to [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") and family. For example:

```
conn = aiohttp.TCPConnector()
session = aiohttp.ClientSession(connector=conn)
```

Note

By default *session* object takes the ownership of the connector, among
other things closing the connections once the *session* is closed. If
you are keen on share the same *connector* through different *session*
instances you must give the *connector\_owner* parameter as **False**
for each *session* instance.

See also

[Connectors](client_reference.html#aiohttp-client-reference-connectors) section for
more information about different connector types and
configuration options.

### Limiting connection pool size[¶](#limiting-connection-pool-size "Link to this heading")

To limit amount of simultaneously opened connections you can pass *limit*
parameter to *connector*:

```
conn = aiohttp.TCPConnector(limit=30)
```

The example limits total amount of parallel connections to 30.

The default is 100.

If you explicitly want not to have limits, pass 0. For example:

```
conn = aiohttp.TCPConnector(limit=0)
```

To limit amount of simultaneously opened connection to the same
endpoint (`(host, port, is_ssl)` triple) you can pass *limit\_per\_host*
parameter to *connector*:

```
conn = aiohttp.TCPConnector(limit_per_host=30)
```

The example limits amount of parallel connections to the same to 30.

The default is 0 (no limit on per host bases).

### Tuning the DNS cache[¶](#tuning-the-dns-cache "Link to this heading")

By default [`TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") comes with the DNS cache
table enabled, and resolutions will be cached by default for 10 seconds.
This behavior can be changed either to change of the TTL for a resolution,
as can be seen in the following example:

```
conn = aiohttp.TCPConnector(ttl_dns_cache=300)
```

or disabling the use of the DNS cache table, meaning that all requests will
end up making a DNS resolution, as the following example shows:

```
conn = aiohttp.TCPConnector(use_dns_cache=False)
```

### Resolving using custom nameservers[¶](#resolving-using-custom-nameservers "Link to this heading")

In order to specify the nameservers to when resolving the hostnames,
[aiodns](glossary.html#term-aiodns) is required:

```
from aiohttp.resolver import AsyncResolver

resolver = AsyncResolver(nameservers=["8.8.8.8", "8.8.4.4"])
conn = aiohttp.TCPConnector(resolver=resolver)
```

### Unix domain sockets[¶](#unix-domain-sockets "Link to this heading")

If your HTTP server uses UNIX domain sockets you can use
[`UnixConnector`](client_reference.html#aiohttp.UnixConnector "aiohttp.UnixConnector"):

```
conn = aiohttp.UnixConnector(path='/path/to/socket')
session = aiohttp.ClientSession(connector=conn)
```

### Custom socket creation[¶](#custom-socket-creation "Link to this heading")

If the default socket is insufficient for your use case, pass an optional
`socket_factory` to the [`TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector"), which implements
[`SocketFactoryType`](client_reference.html#aiohttp.SocketFactoryType "aiohttp.SocketFactoryType"). This will be used to create all sockets for the
lifetime of the class object. For example, we may want to change the
conditions under which we consider a connection dead. The following would
make all sockets respect 9\*7200 = 18 hours:

```
import socket

def socket_factory(addr_info):
    family, type_, proto, _, _ = addr_info
    sock = socket.socket(family=family, type=type_, proto=proto)
    sock.setsockopt(socket.SOL_SOCKET,  socket.SO_KEEPALIVE,  True)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE,  7200)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT,      9)
    return sock

conn = aiohttp.TCPConnector(socket_factory=socket_factory)
```

`socket_factory` may also be used for binding to the specific network
interface on supported platforms:

```
def socket_factory(addr_info):
    family, type_, proto, _, _ = addr_info
    sock = socket.socket(family=family, type=type_, proto=proto)
    sock.setsockopt(
        socket.SOL_SOCKET, socket.SO_BINDTODEVICE, b'eth0'
    )
    return sock

conn = aiohttp.TCPConnector(socket_factory=socket_factory)
```

### Named pipes in Windows[¶](#named-pipes-in-windows "Link to this heading")

If your HTTP server uses Named pipes you can use
`NamedPipeConnector`:

```
conn = aiohttp.NamedPipeConnector(path=r'\\.\pipe\<name-of-pipe>')
session = aiohttp.ClientSession(connector=conn)
```

It will only work with the ProactorEventLoop

## SSL control for TCP sockets[¶](#ssl-control-for-tcp-sockets "Link to this heading")

By default *aiohttp* uses strict checks for HTTPS protocol. Certification
checks can be relaxed by setting *ssl* to `False`:

```
r = await session.get('https://example.com', ssl=False)
```

If you need to setup custom ssl parameters (use own certification
files for example) you can create a [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") instance and
pass it into the [`ClientSession.request()`](client_reference.html#aiohttp.ClientSession.request "aiohttp.ClientSession.request") methods or set it for the
entire session with `ClientSession(connector=TCPConnector(ssl=ssl_context))`.

There are explicit errors when ssl verification fails

[`aiohttp.ClientConnectorSSLError`](client_reference.html#aiohttp.ClientConnectorSSLError "aiohttp.ClientConnectorSSLError"):

```
try:
    await session.get('https://expired.badssl.com/')
except aiohttp.ClientConnectorSSLError as e:
    assert isinstance(e, ssl.SSLError)
```

[`aiohttp.ClientConnectorCertificateError`](client_reference.html#aiohttp.ClientConnectorCertificateError "aiohttp.ClientConnectorCertificateError"):

```
try:
    await session.get('https://wrong.host.badssl.com/')
except aiohttp.ClientConnectorCertificateError as e:
    assert isinstance(e, ssl.CertificateError)
```

If you need to skip both ssl related errors

[`aiohttp.ClientSSLError`](client_reference.html#aiohttp.ClientSSLError "aiohttp.ClientSSLError"):

```
try:
    await session.get('https://expired.badssl.com/')
except aiohttp.ClientSSLError as e:
    assert isinstance(e, ssl.SSLError)

try:
    await session.get('https://wrong.host.badssl.com/')
except aiohttp.ClientSSLError as e:
    assert isinstance(e, ssl.CertificateError)
```

### Example: Use certifi[¶](#example-use-certifi "Link to this heading")

By default, Python uses the system CA certificates. In rare cases, these may not be
installed or Python is unable to find them, resulting in a error like
ssl.SSLCertVerificationError: [SSL: CERTIFICATE\_VERIFY\_FAILED] certificate verify failed: unable to get local issuer certificate

One way to work around this problem is to use the certifi package:

```
ssl_context = ssl.create_default_context(cafile=certifi.where())
async with ClientSession(connector=TCPConnector(ssl=ssl_context)) as sess:
    ...
```

### Example: Use self-signed certificate[¶](#example-use-self-signed-certificate "Link to this heading")

If you need to verify *self-signed* certificates, you need to add a call to
[`ssl.SSLContext.load_cert_chain()`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_cert_chain "(in Python v3.14)") with the key pair:

```
ssl_context = ssl.create_default_context()
ssl_context.load_cert_chain("/path/to/client/public/device.pem",
                            "/path/to/client/private/device.key")
async with sess.get("https://example.com", ssl=ssl_context) as resp:
    ...
```

### Example: Verify certificate fingerprint[¶](#example-verify-certificate-fingerprint "Link to this heading")

You may also verify certificates via *SHA256* fingerprint:

```
# Attempt to connect to https://www.python.org
# with a pin to a bogus certificate:
bad_fp = b'0'*64
exc = None
try:
    r = await session.get('https://www.python.org',
                          ssl=aiohttp.Fingerprint(bad_fp))
except aiohttp.FingerprintMismatch as e:
    exc = e
assert exc is not None
assert exc.expected == bad_fp

# www.python.org cert's actual fingerprint
assert exc.got == b'...'
```

Note that this is the fingerprint of the DER-encoded certificate.
If you have the certificate in PEM format, you can convert it to
DER with e.g:

```
openssl x509 -in crt.pem -inform PEM -outform DER > crt.der
```

Note

Tip: to convert from a hexadecimal digest to a binary byte-string,
you can use [`binascii.unhexlify()`](https://docs.python.org/3/library/binascii.html#binascii.unhexlify "(in Python v3.14)").

*ssl* parameter could be passed
to [`TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") as default, the value from
[`ClientSession.get()`](client_reference.html#aiohttp.ClientSession.get "aiohttp.ClientSession.get") and others override default.

## Proxy support[¶](#proxy-support "Link to this heading")

aiohttp supports plain HTTP proxies and HTTP proxies that can be
upgraded to HTTPS via the HTTP CONNECT method. aiohttp has a limited
support for proxies that must be connected to via `https://` — see
the info box below for more details.
To connect, use the *proxy* parameter:

```
async with aiohttp.ClientSession() as session:
    async with session.get("http://python.org",
                           proxy="http://proxy.com") as resp:
        print(resp.status)
```

It also supports proxy authorization:

```
async with aiohttp.ClientSession() as session:
    proxy_auth = aiohttp.BasicAuth('user', 'pass')
    async with session.get("http://python.org",
                           proxy="http://proxy.com",
                           proxy_auth=proxy_auth) as resp:
        print(resp.status)
```

Authentication credentials can be passed in proxy URL:

```
session.get("http://python.org",
            proxy="http://user:pass@some.proxy.com")
```

And you may set default proxy:

```
proxy_auth = aiohttp.BasicAuth('user', 'pass')
async with aiohttp.ClientSession(proxy="http://proxy.com", proxy_auth=proxy_auth) as session:
    async with session.get("http://python.org") as resp:
        print(resp.status)
```

Contrary to the `requests` library, it won’t read environment
variables by default. But you can do so by passing
`trust_env=True` into [`aiohttp.ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession")
constructor.:

```
async with aiohttp.ClientSession(trust_env=True) as session:
    async with session.get("http://python.org") as resp:
        print(resp.status)
```

Note

aiohttp uses [`urllib.request.getproxies()`](https://docs.python.org/3/library/urllib.request.html#urllib.request.getproxies "(in Python v3.14)")
for reading the proxy configuration (e.g. from the *HTTP\_PROXY* etc. environment variables) and applies them for the *HTTP*, *HTTPS*, *WS* and *WSS* schemes.

Hosts defined in `no_proxy` will bypass the proxy.

Added in version 3.8: *WS\_PROXY* and *WSS\_PROXY* are supported since aiohttp v3.8.

Proxy credentials are given from `~/.netrc` file if present (see
[`aiohttp.ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") for more details).

Attention

As of now (Python 3.10), support for TLS in TLS is disabled for the transports that
[`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio "(in Python v3.14)") uses. If the further release of Python (say v3.11)
toggles one attribute, it’ll *just work™*.

aiohttp v3.8 and higher is ready for this to happen and has code in
place supports TLS-in-TLS, hence sending HTTPS requests over HTTPS
proxy tunnels.

⚠️ For as long as your Python runtime doesn’t declare the support for
TLS-in-TLS, please don’t file bugs with aiohttp but rather try to
help the CPython upstream enable this feature. Meanwhile, if you
*really* need this to work, there’s a patch that may help you make
it happen, include it into your app’s code base:
<https://github.com/aio-libs/aiohttp/discussions/6044#discussioncomment-1432443>.

Important

When supplying a custom [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") instance, bear in
mind that it will be used not only to establish a TLS session with
the HTTPS endpoint you’re hitting but also to establish a TLS tunnel
to the HTTPS proxy. To avoid surprises, make sure to set up the trust
chain that would recognize TLS certificates used by both the endpoint
and the proxy.

## Graceful Shutdown[¶](#graceful-shutdown "Link to this heading")

When [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") closes at the end of an `async with`
block (or through a direct [`ClientSession.close()`](client_reference.html#aiohttp.ClientSession.close "aiohttp.ClientSession.close") call), the
underlying connection remains open due to asyncio internal details. In
practice, the underlying connection will close after a short
while. However, if the event loop is stopped before the underlying
connection is closed, a `ResourceWarning: unclosed transport`
warning is emitted (when warnings are enabled).

To avoid this situation, a small delay must be added before closing
the event loop to allow any open underlying connections to close.

For a [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") without SSL, a simple zero-sleep (`await
asyncio.sleep(0)`) will suffice:

```
async def read_website():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://example.org/') as resp:
            await resp.read()
    # Zero-sleep to allow underlying connections to close
    await asyncio.sleep(0)
```

For a [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") with SSL, the application must wait a
short duration before closing:

```
...
# Wait 250 ms for the underlying SSL connections to close
await asyncio.sleep(0.250)
```

Note that the appropriate amount of time to wait will vary from
application to application.

All if this will eventually become obsolete when the asyncio internals
are changed so that aiohttp itself can wait on the underlying
connection to close. Please follow issue [#1925](https://github.com/aio-libs/aiohttp/issues/1925) for the progress
on this.

## Character Set Detection[¶](#character-set-detection "Link to this heading")

If you encounter a [`UnicodeDecodeError`](https://docs.python.org/3/library/exceptions.html#UnicodeDecodeError "(in Python v3.14)") when using [`ClientResponse.text()`](client_reference.html#aiohttp.ClientResponse.text "aiohttp.ClientResponse.text")
this may be because the response does not include the charset needed
to decode the body.

If you know the correct encoding for a request, you can simply specify
the encoding as a parameter (e.g. `resp.text("windows-1252")`).

Alternatively, [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") accepts a `fallback_charset_resolver` parameter which
can be used to introduce charset guessing functionality. When a charset is not found
in the Content-Type header, this function will be called to get the charset encoding. For
example, this can be used with the `chardetng_py` library.:

```
from chardetng_py import detect

def charset_resolver(resp: ClientResponse, body: bytes) -> str:
    tld = resp.url.host.rsplit(".", maxsplit=1)[-1]
    return detect(body, allow_utf8=True, tld=tld.encode())

ClientSession(fallback_charset_resolver=charset_resolver)
```

Or, if `chardetng_py` doesn’t work for you, then `charset-normalizer` is another option:

```
from charset_normalizer import detect

ClientSession(fallback_charset_resolver=lambda r, b: detect(b)["encoding"] or "utf-8")
```

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
  + [Quickstart](client_quickstart.html)
  + [Advanced Usage](#)
  + [Client Middleware Cookbook](client_middleware_cookbook.html)
  + [Reference](client_reference.html)
  + [Tracing Reference](tracing_reference.html)
  + [The aiohttp Request Lifecycle](http_request_lifecycle.html)
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
[Page source](_sources/client_advanced.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
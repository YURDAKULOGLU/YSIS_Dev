.. \_aiohttp-client-reference:
Client Reference
================
.. currentmodule:: aiohttp
Client Session
--------------
Client session is the recommended interface for making HTTP requests.
Session encapsulates a \*connection pool\* (\*connector\* instance) and
supports keepalives by default. Unless you are connecting to a large,
unknown number of different servers over the lifetime of your
application, it is suggested you use a single session for the
lifetime of your application to benefit from connection pooling.
Usage example::
import aiohttp
import asyncio
async def fetch(client):
async with client.get('http://python.org') as resp:
assert resp.status == 200
return await resp.text()
async def main():
async with aiohttp.ClientSession() as client:
html = await fetch(client)
print(html)
asyncio.run(main())
The client session supports the context manager protocol for self closing.
.. class:: ClientSession(base\_url=None, \*, \
connector=None, cookies=None, \
headers=None, skip\_auto\_headers=None, \
auth=None, json\_serialize=json.dumps, \
request\_class=ClientRequest, \
response\_class=ClientResponse, \
ws\_response\_class=ClientWebSocketResponse, \
version=aiohttp.HttpVersion11, \
cookie\_jar=None, \
connector\_owner=True, \
raise\_for\_status=False, \
timeout=sentinel, \
auto\_decompress=True, \
trust\_env=False, \
requote\_redirect\_url=True, \
trace\_configs=None, \
middlewares=(), \
read\_bufsize=2\*\*16, \
max\_line\_size=8190, \
max\_field\_size=8190, \
fallback\_charset\_resolver=lambda r, b: "utf-8", \
ssl\_shutdown\_timeout=0)
The class for creating client sessions and making requests.
:param base\_url: Base part of the URL (optional)
If set, allows to join a base part to relative URLs in request calls.
If the URL has a path it must have a trailing ``/`` (as in
https://docs.aiohttp.org/en/stable/).
Note that URL joining follows :rfc:`3986`. This means, in the most
common case the request URLs should have no leading slash, e.g.::
session = ClientSession(base\_url="http://example.com/foo/")
await session.request("GET", "bar")
# request for http://example.com/foo/bar
await session.request("GET", "/bar")
# request for http://example.com/bar
.. versionadded:: 3.8
.. versionchanged:: 3.12
Added support for overriding the base URL with an absolute one in client sessions.
:param aiohttp.BaseConnector connector: BaseConnector
sub-class instance to support connection pooling.
:param dict cookies: Cookies to send with the request (optional)
:param headers: HTTP Headers to send with every request (optional).
May be either \*iterable of key-value pairs\* or
:class:`~collections.abc.Mapping`
(e.g. :class:`dict`,
:class:`~multidict.CIMultiDict`).
:param skip\_auto\_headers: set of headers for which autogeneration
should be skipped.
\*aiohttp\* autogenerates headers like ``User-Agent`` or
``Content-Type`` if these headers are not explicitly
passed. Using ``skip\_auto\_headers`` parameter allows to skip
that generation. Note that ``Content-Length`` autogeneration can't
be skipped.
Iterable of :class:`str` or :class:`~multidict.istr` (optional)
:param aiohttp.BasicAuth auth: an object that represents HTTP Basic
Authorization (optional). It will be included
with any request. However, if the
``\_base\_url`` parameter is set, the request
URL's origin must match the base URL's origin;
otherwise, the default auth will not be
included.
:param collections.abc.Callable json\_serialize: Json \*serializer\* callable.
By default :func:`json.dumps` function.
:param aiohttp.ClientRequest request\_class: Custom class to use for client requests.
:param ClientResponse response\_class: Custom class to use for client responses.
:param ClientWebSocketResponse ws\_response\_class: Custom class to use for websocket responses.
:param version: supported HTTP version, ``HTTP 1.1`` by default.
:param cookie\_jar: Cookie Jar, :class:`~aiohttp.abc.AbstractCookieJar` instance.
By default every session instance has own private cookie jar for
automatic cookies processing but user may redefine this behavior
by providing own jar implementation.
One example is not processing cookies at all when working in
proxy mode.
If no cookie processing is needed, a
:class:`aiohttp.DummyCookieJar` instance can be
provided.
:param bool connector\_owner:
Close connector instance on session closing.
Setting the parameter to ``False`` allows to share
connection pool between sessions without sharing session state:
cookies etc.
:param bool raise\_for\_status:
Automatically call :meth:`ClientResponse.raise\_for\_status` for
each response, ``False`` by default.
This parameter can be overridden when making a request, e.g.::
client\_session = aiohttp.ClientSession(raise\_for\_status=True)
resp = await client\_session.get(url, raise\_for\_status=False)
async with resp:
assert resp.status == 200
Set the parameter to ``True`` if you need ``raise\_for\_status``
for most of cases but override ``raise\_for\_status`` for those
requests where you need to handle responses with status 400 or
higher.
You can also provide a coroutine which takes the response as an
argument and can raise an exception based on custom logic, e.g.::
async def custom\_check(response):
if response.status not in {201, 202}:
raise RuntimeError('expected either 201 or 202')
text = await response.text()
if 'apple pie' not in text:
raise RuntimeError('I wanted to see "apple pie" in response')
client\_session = aiohttp.ClientSession(raise\_for\_status=custom\_check)
...
As with boolean values, you're free to set this on the session and/or
overwrite it on a per-request basis.
:param timeout: a :class:`ClientTimeout` settings structure, 300 seconds (5min)
total timeout, 30 seconds socket connect timeout by default.
.. versionadded:: 3.3
.. versionchanged:: 3.10.9
The default value for the ``sock\_connect`` timeout has been changed to 30 seconds.
:param bool auto\_decompress: Automatically decompress response body (``True`` by default).
.. versionadded:: 2.3
:param bool trust\_env: Trust environment settings for proxy configuration if the parameter
is ``True`` (``False`` by default). See :ref:`aiohttp-client-proxy-support` for
more information.
Get proxy credentials from ``~/.netrc`` file if present.
Get HTTP Basic Auth credentials from :file:`~/.netrc` file if present.
If :envvar:`NETRC` environment variable is set, read from file specified
there rather than from :file:`~/.netrc`.
.. seealso::
``.netrc`` documentation: https://www.gnu.org/software/inetutils/manual/html\_node/The-\_002enetrc-file.html
.. versionadded:: 2.3
.. versionchanged:: 3.0
Added support for ``~/.netrc`` file.
.. versionchanged:: 3.9
Added support for reading HTTP Basic Auth credentials from :file:`~/.netrc` file.
:param bool requote\_redirect\_url: Apply \*URL requoting\* for redirection URLs if
automatic redirection is enabled (``True`` by
default).
.. versionadded:: 3.5
:param trace\_configs: A list of :class:`TraceConfig` instances used for client
tracing. ``None`` (default) is used for request tracing
disabling. See :ref:`aiohttp-client-tracing-reference` for
more information.
:param middlewares: A sequence of middleware instances to apply to all session requests.
Each middleware must match the :type:`ClientMiddlewareType` signature.
``()`` (empty tuple, default) is used when no middleware is needed.
See :ref:`aiohttp-client-middleware` for more information.
.. versionadded:: 3.12
:param int read\_bufsize: Size of the read buffer (:attr:`ClientResponse.content`).
64 KiB by default.
.. versionadded:: 3.7
:param int max\_line\_size: Maximum allowed size of lines in responses.
:param int max\_field\_size: Maximum allowed size of header fields in responses.
:param Callable[[ClientResponse,bytes],str] fallback\_charset\_resolver:
A :term:`callable` that accepts a :class:`ClientResponse` and the
:class:`bytes` contents, and returns a :class:`str` which will be used as
the encoding parameter to :meth:`bytes.decode()`.
This function will be called when the charset is not known (e.g. not specified in the
Content-Type header). The default function simply defaults to ``utf-8``.
.. versionadded:: 3.8.6
:param float ssl\_shutdown\_timeout: \*\*(DEPRECATED)\*\* This parameter is deprecated
and will be removed in aiohttp 4.0. Grace period for SSL shutdown handshake on
TLS connections when the connector is closed (``0`` seconds by default).
By default (``0``), SSL connections are aborted immediately when the
connector is closed, without performing the shutdown handshake. During
normal operation, SSL connections use Python's default SSL shutdown
behavior. Setting this to a positive value (e.g., ``0.1``) will perform
a graceful shutdown when closing the connector, notifying the remote
peer which can help prevent "connection reset" errors at the cost of
additional cleanup time. This timeout is passed to the underlying
:class:`TCPConnector` when one is created automatically.
Note: On Python versions prior to 3.11, only a value of ``0`` is supported;
other values will trigger a warning.
.. versionadded:: 3.12.5
.. versionchanged:: 3.12.11
Changed default from ``0.1`` to ``0`` to abort SSL connections
immediately when the connector is closed. Added support for
``ssl\_shutdown\_timeout=0`` on all Python versions. A :exc:`RuntimeWarning`
is issued when non-zero values are passed on Python < 3.11.
.. deprecated:: 3.12.11
This parameter is deprecated and will be removed in aiohttp 4.0.
.. attribute:: closed
``True`` if the session has been closed, ``False`` otherwise.
A read-only property.
.. attribute:: connector
:class:`aiohttp.BaseConnector` derived instance used
for the session.
A read-only property.
.. attribute:: cookie\_jar
The session cookies, :class:`~aiohttp.abc.AbstractCookieJar` instance.
Gives access to cookie jar's content and modifiers.
A read-only property.
.. attribute:: requote\_redirect\_url
aiohttp re quote's redirect urls by default, but some servers
require exact url from location header. To disable \*re-quote\* system
set :attr:`requote\_redirect\_url` attribute to ``False``.
.. versionadded:: 2.1
.. note:: This parameter affects all subsequent requests.
.. deprecated:: 3.5
The attribute modification is deprecated.
.. attribute:: loop
A loop instance used for session creation.
A read-only property.
.. deprecated:: 3.5
.. attribute:: timeout
Default client timeouts, :class:`ClientTimeout` instance. The value can
be tuned by passing \*timeout\* parameter to :class:`ClientSession`
constructor.
.. versionadded:: 3.7
.. attribute:: headers
HTTP Headers that sent with every request
May be either \*iterable of key-value pairs\* or
:class:`~collections.abc.Mapping`
(e.g. :class:`dict`,
:class:`~multidict.CIMultiDict`).
.. versionadded:: 3.7
.. attribute:: skip\_auto\_headers
Set of headers for which autogeneration skipped.
:class:`frozenset` of :class:`str` or :class:`~multidict.istr` (optional)
.. versionadded:: 3.7
.. attribute:: auth
An object that represents HTTP Basic Authorization.
:class:`~aiohttp.BasicAuth` (optional)
.. versionadded:: 3.7
.. attribute:: json\_serialize
Json serializer callable.
By default :func:`json.dumps` function.
.. versionadded:: 3.7
.. attribute:: connector\_owner
Should connector be closed on session closing
:class:`bool` (optional)
.. versionadded:: 3.7
.. attribute:: raise\_for\_status
Should :meth:`ClientResponse.raise\_for\_status` be called for each response
Either :class:`bool` or :class:`collections.abc.Callable`
.. versionadded:: 3.7
.. attribute:: auto\_decompress
Should the body response be automatically decompressed
:class:`bool` default is ``True``
.. versionadded:: 3.7
.. attribute:: trust\_env
Trust environment settings for proxy configuration
or ~/.netrc file if present. See :ref:`aiohttp-client-proxy-support` for
more information.
:class:`bool` default is ``False``
.. versionadded:: 3.7
.. attribute:: trace\_configs
A list of :class:`TraceConfig` instances used for client
tracing. ``None`` (default) is used for request tracing
disabling. See :ref:`aiohttp-client-tracing-reference` for more information.
.. versionadded:: 3.7
.. method:: request(method, url, \*, params=None, data=None, json=None,\
cookies=None, headers=None, skip\_auto\_headers=None, \
auth=None, allow\_redirects=True,\
max\_redirects=10,\
compress=None, chunked=None, expect100=False, raise\_for\_status=None,\
read\_until\_eof=True, \
proxy=None, proxy\_auth=None,\
timeout=sentinel, ssl=True, \
server\_hostname=None, \
proxy\_headers=None, \
trace\_request\_ctx=None, \
middlewares=None, \
read\_bufsize=None, \
auto\_decompress=None, \
max\_line\_size=None, \
max\_field\_size=None)
:async:
:noindexentry:
Performs an asynchronous HTTP request. Returns a response object that
should be used as an async context manager.
:param str method: HTTP method
:param url: Request URL, :class:`~yarl.URL` or :class:`str` that will
be encoded with :class:`~yarl.URL` (see :class:`~yarl.URL`
to skip encoding).
:param params: Mapping, iterable of tuple of \*key\*/\*value\* pairs or
string to be sent as parameters in the query
string of the new request. Ignored for subsequent
redirected requests (optional)
Allowed values are:
- :class:`collections.abc.Mapping` e.g. :class:`dict`,
:class:`multidict.MultiDict` or
:class:`multidict.MultiDictProxy`
- :class:`collections.abc.Iterable` e.g. :class:`tuple` or
:class:`list`
- :class:`str` with preferably url-encoded content
(\*\*Warning:\*\* content will not be encoded by \*aiohttp\*)
:param data: The data to send in the body of the request. This can be a
:class:`FormData` object or anything that can be passed into
:class:`FormData`, e.g. a dictionary, bytes, or file-like object.
(optional)
:param json: Any json compatible python object
(optional). \*json\* and \*data\* parameters could not
be used at the same time.
:param dict cookies: HTTP Cookies to send with
the request (optional)
Global session cookies and the explicitly set cookies will be merged
when sending the request.
.. versionadded:: 3.5
:param dict headers: HTTP Headers to send with
the request (optional)
:param skip\_auto\_headers: set of headers for which autogeneration
should be skipped.
\*aiohttp\* autogenerates headers like ``User-Agent`` or
``Content-Type`` if these headers are not explicitly
passed. Using ``skip\_auto\_headers`` parameter allows to skip
that generation.
Iterable of :class:`str` or :class:`~multidict.istr`
(optional)
:param aiohttp.BasicAuth auth: an object that represents HTTP
Basic Authorization (optional)
:param bool allow\_redirects: Whether to process redirects or not.
When ``True``, redirects are followed (up to ``max\_redirects`` times)
and logged into :attr:`ClientResponse.history` and ``trace\_configs``.
When ``False``, the original response is returned.
``True`` by default (optional).
:param int max\_redirects: Maximum number of redirects to follow.
:exc:`TooManyRedirects` is raised if the number is exceeded.
Ignored when ``allow\_redirects=False``.
``10`` by default.
:param bool compress: Set to ``True`` if request has to be compressed
with deflate encoding. If `compress` can not be combined
with a \*Content-Encoding\* and \*Content-Length\* headers.
``None`` by default (optional).
:param int chunked: Enable chunked transfer encoding.
It is up to the developer
to decide how to chunk data streams. If chunking is enabled, aiohttp
encodes the provided chunks in the "Transfer-encoding: chunked" format.
If \*chunked\* is set, then the \*Transfer-encoding\* and \*content-length\*
headers are disallowed. ``None`` by default (optional).
:param bool expect100: Expect 100-continue response from server.
``False`` by default (optional).
:param bool raise\_for\_status: Automatically call :meth:`ClientResponse.raise\_for\_status` for
response if set to ``True``.
If set to ``None`` value from ``ClientSession`` will be used.
``None`` by default (optional).
.. versionadded:: 3.4
:param bool read\_until\_eof: Read response until EOF if response
does not have Content-Length header.
``True`` by default (optional).
:param proxy: Proxy URL, :class:`str` or :class:`~yarl.URL` (optional)
:param aiohttp.BasicAuth proxy\_auth: an object that represents proxy HTTP
Basic Authorization (optional)
:param int timeout: override the session's timeout.
.. versionchanged:: 3.3
The parameter is :class:`ClientTimeout` instance,
:class:`float` is still supported for sake of backward
compatibility.
If :class:`float` is passed it is a \*total\* timeout (in seconds).
:param ssl: SSL validation mode. ``True`` for default SSL check
(:func:`ssl.create\_default\_context` is used),
``False`` for skip SSL certificate validation,
:class:`aiohttp.Fingerprint` for fingerprint
validation, :class:`ssl.SSLContext` for custom SSL
certificate validation.
Supersedes \*verify\_ssl\*, \*ssl\_context\* and
\*fingerprint\* parameters.
.. versionadded:: 3.0
:param str server\_hostname: Sets or overrides the host name that the
target server's certificate will be matched against.
See :py:meth:`asyncio.loop.create\_connection` for more information.
.. versionadded:: 3.9
:param collections.abc.Mapping proxy\_headers: HTTP headers to send to the proxy if the
parameter proxy has been provided.
.. versionadded:: 2.3
:param trace\_request\_ctx: Object used to give as a kw param for each new
:class:`TraceConfig` object instantiated,
used to give information to the
tracers that is only available at request time.
.. versionadded:: 3.0
:param middlewares: A sequence of middleware instances to apply to this request only.
Each middleware must match the :type:`ClientMiddlewareType` signature.
``None`` by default which uses session middlewares.
See :ref:`aiohttp-client-middleware` for more information.
.. versionadded:: 3.12
:param int read\_bufsize: Size of the read buffer (:attr:`ClientResponse.content`).
``None`` by default,
it means that the session global value is used.
.. versionadded:: 3.7
:param bool auto\_decompress: Automatically decompress response body.
Overrides :attr:`ClientSession.auto\_decompress`.
May be used to enable/disable auto decompression on a per-request basis.
:param int max\_line\_size: Maximum allowed size of lines in responses.
:param int max\_field\_size: Maximum allowed size of header fields in responses.
:return ClientResponse: a :class:`client response `
object.
.. method:: get(url, \*, allow\_redirects=True, \*\*kwargs)
:async:
Perform a ``GET`` request. Returns an async context manager.
In order to modify inner
:meth:`request`
parameters, provide `kwargs`.
:param url: Request URL, :class:`str` or :class:`~yarl.URL`
:param bool allow\_redirects: Whether to process redirects or not.
When ``True``, redirects are followed and logged into
:attr:`ClientResponse.history`.
When ``False``, the original response is returned.
``True`` by default (optional).
:return ClientResponse: a :class:`client response
` object.
.. method:: post(url, \*, data=None, \*\*kwargs)
:async:
Perform a ``POST`` request. Returns an async context manager.
In order to modify inner
:meth:`request`
parameters, provide `kwargs`.
:param url: Request URL, :class:`str` or :class:`~yarl.URL`
:param data: Data to send in the body of the request; see
:meth:`request`
for details (optional)
:return ClientResponse: a :class:`client response
` object.
.. method:: put(url, \*, data=None, \*\*kwargs)
:async:
Perform a ``PUT`` request. Returns an async context manager.
In order to modify inner
:meth:`request`
parameters, provide `kwargs`.
:param url: Request URL, :class:`str` or :class:`~yarl.URL`
:param data: Data to send in the body of the request; see
:meth:`request`
for details (optional)
:return ClientResponse: a :class:`client response
` object.
.. method:: delete(url, \*\*kwargs)
:async:
Perform a ``DELETE`` request. Returns an async context manager.
In order to modify inner
:meth:`request`
parameters, provide `kwargs`.
:param url: Request URL, :class:`str` or :class:`~yarl.URL`
:return ClientResponse: a :class:`client response
` object.
.. method:: head(url, \*, allow\_redirects=False, \*\*kwargs)
:async:
Perform a ``HEAD`` request. Returns an async context manager.
In order to modify inner
:meth:`request`
parameters, provide `kwargs`.
:param url: Request URL, :class:`str` or :class:`~yarl.URL`
:param bool allow\_redirects: Whether to process redirects or not.
When ``True``, redirects are followed and logged into
:attr:`ClientResponse.history`.
When ``False``, the original response is returned.
``False`` by default (optional).
:return ClientResponse: a :class:`client response
` object.
.. method:: options(url, \*, allow\_redirects=True, \*\*kwargs)
:async:
Perform an ``OPTIONS`` request. Returns an async context manager.
In order to modify inner
:meth:`request`
parameters, provide `kwargs`.
:param url: Request URL, :class:`str` or :class:`~yarl.URL`
:param bool allow\_redirects: Whether to process redirects or not.
When ``True``, redirects are followed and logged into
:attr:`ClientResponse.history`.
When ``False``, the original response is returned.
``True`` by default (optional).
:return ClientResponse: a :class:`client response
` object.
.. method:: patch(url, \*, data=None, \*\*kwargs)
:async:
Perform a ``PATCH`` request. Returns an async context manager.
In order to modify inner
:meth:`request`
parameters, provide `kwargs`.
:param url: Request URL, :class:`str` or :class:`~yarl.URL`
:param data: Data to send in the body of the request; see
:meth:`request`
for details (optional)
:return ClientResponse: a :class:`client response
` object.
.. method:: ws\_connect(url, \*, method='GET', \
protocols=(), \
timeout=sentinel,\
auth=None,\
autoclose=True,\
autoping=True,\
heartbeat=None,\
origin=None, \
params=None, \
headers=None, \
proxy=None, proxy\_auth=None, ssl=True, \
verify\_ssl=None, fingerprint=None, \
ssl\_context=None, proxy\_headers=None, \
compress=0, max\_msg\_size=4194304)
:async:
Create a websocket connection. Returns a
:class:`ClientWebSocketResponse` async context manager object.
:param url: Websocket server url, :class:`~yarl.URL` or :class:`str` that
will be encoded with :class:`~yarl.URL` (see :class:`~yarl.URL`
to skip encoding).
:param tuple protocols: Websocket protocols
:param timeout: a :class:`ClientWSTimeout` timeout for websocket.
By default, the value
`ClientWSTimeout(ws\_receive=None, ws\_close=10.0)` is used
(``10.0`` seconds for the websocket to close).
``None`` means no timeout will be used.
:param aiohttp.BasicAuth auth: an object that represents HTTP
Basic Authorization (optional)
:param bool autoclose: Automatically close websocket connection on close
message from server. If \*autoclose\* is False
then close procedure has to be handled manually.
``True`` by default
:param bool autoping: automatically send \*pong\* on \*ping\*
message from server. ``True`` by default
:param float heartbeat: Send \*ping\* message every \*heartbeat\*
seconds and wait \*pong\* response, if
\*pong\* response is not received then
close connection. The timer is reset on any data
reception.(optional)
:param str origin: Origin header to send to server(optional)
:param params: Mapping, iterable of tuple of \*key\*/\*value\* pairs or
string to be sent as parameters in the query
string of the new request. Ignored for subsequent
redirected requests (optional)
Allowed values are:
- :class:`collections.abc.Mapping` e.g. :class:`dict`,
:class:`multidict.MultiDict` or
:class:`multidict.MultiDictProxy`
- :class:`collections.abc.Iterable` e.g. :class:`tuple` or
:class:`list`
- :class:`str` with preferably url-encoded content
(\*\*Warning:\*\* content will not be encoded by \*aiohttp\*)
:param dict headers: HTTP Headers to send with
the request (optional)
:param str proxy: Proxy URL, :class:`str` or :class:`~yarl.URL` (optional)
:param aiohttp.BasicAuth proxy\_auth: an object that represents proxy HTTP
Basic Authorization (optional)
:param ssl: SSL validation mode. ``True`` for default SSL check
(:func:`ssl.create\_default\_context` is used),
``False`` for skip SSL certificate validation,
:class:`aiohttp.Fingerprint` for fingerprint
validation, :class:`ssl.SSLContext` for custom SSL
certificate validation.
Supersedes \*verify\_ssl\*, \*ssl\_context\* and
\*fingerprint\* parameters.
.. versionadded:: 3.0
:param bool verify\_ssl: Perform SSL certificate validation for
\*HTTPS\* requests (enabled by default). May be disabled to
skip validation for sites with invalid certificates.
.. versionadded:: 2.3
.. deprecated:: 3.0
Use ``ssl=False``
:param bytes fingerprint: Pass the SHA256 digest of the expected
certificate in DER format to verify that the certificate the
server presents matches. Useful for `certificate pinning
`\_.
Note: use of MD5 or SHA1 digests is insecure and deprecated.
.. versionadded:: 2.3
.. deprecated:: 3.0
Use ``ssl=aiohttp.Fingerprint(digest)``
:param ssl.SSLContext ssl\_context: ssl context used for processing
\*HTTPS\* requests (optional).
\*ssl\_context\* may be used for configuring certification
authority channel, supported SSL options etc.
.. versionadded:: 2.3
.. deprecated:: 3.0
Use ``ssl=ssl\_context``
:param dict proxy\_headers: HTTP headers to send to the proxy if the
parameter proxy has been provided.
.. versionadded:: 2.3
:param int compress: Enable Per-Message Compress Extension support.
0 for disable, 9 to 15 for window bit support.
Default value is 0.
.. versionadded:: 2.3
:param int max\_msg\_size: maximum size of read websocket message,
4 MB by default. To disable the size
limit use ``0``.
.. versionadded:: 3.3
:param str method: HTTP method to establish WebSocket connection,
``'GET'`` by default.
.. versionadded:: 3.5
.. method:: close()
:async:
Close underlying connector.
Release all acquired resources.
.. method:: detach()
Detach connector from session without closing the former.
Session is switched to closed state anyway.
Basic API
---------
While we encourage :class:`ClientSession` usage we also provide simple
coroutines for making HTTP requests.
Basic API is good for performing simple HTTP requests without
keepaliving, cookies and complex connection stuff like properly configured SSL
certification chaining.
.. function:: request(method, url, \*, params=None, data=None, \
json=None,\
cookies=None, headers=None, skip\_auto\_headers=None, auth=None, \
allow\_redirects=True, max\_redirects=10, \
compress=False, chunked=None, expect100=False, raise\_for\_status=None, \
read\_until\_eof=True, \
proxy=None, proxy\_auth=None, \
timeout=sentinel, ssl=True, \
server\_hostname=None, \
proxy\_headers=None, \
trace\_request\_ctx=None, \
read\_bufsize=None, \
auto\_decompress=None, \
max\_line\_size=None, \
max\_field\_size=None, \
version=aiohttp.HttpVersion11, \
connector=None)
:async:
Asynchronous context manager for performing an asynchronous HTTP
request. Returns a :class:`ClientResponse` response object. Use as
an async context manager.
:param str method: HTTP method
:param url: Request URL, :class:`~yarl.URL` or :class:`str` that will
be encoded with :class:`~yarl.URL` (see :class:`~yarl.URL`
to skip encoding).
:param params: Mapping, iterable of tuple of \*key\*/\*value\* pairs or
string to be sent as parameters in the query
string of the new request. Ignored for subsequent
redirected requests (optional)
Allowed values are:
- :class:`collections.abc.Mapping` e.g. :class:`dict`,
:class:`multidict.MultiDict` or
:class:`multidict.MultiDictProxy`
- :class:`collections.abc.Iterable` e.g. :class:`tuple` or
:class:`list`
- :class:`str` with preferably url-encoded content
(\*\*Warning:\*\* content will not be encoded by \*aiohttp\*)
:param data: The data to send in the body of the request. This can be a
:class:`FormData` object or anything that can be passed into
:class:`FormData`, e.g. a dictionary, bytes, or file-like object.
(optional)
:param json: Any json compatible python object (optional). \*json\* and \*data\*
parameters could not be used at the same time.
:param dict cookies: HTTP Cookies to send with the request (optional)
:param dict headers: HTTP Headers to send with the request (optional)
:param skip\_auto\_headers: set of headers for which autogeneration
should be skipped.
\*aiohttp\* autogenerates headers like ``User-Agent`` or
``Content-Type`` if these headers are not explicitly
passed. Using ``skip\_auto\_headers`` parameter allows to skip
that generation.
Iterable of :class:`str` or :class:`~multidict.istr`
(optional)
:param aiohttp.BasicAuth auth: an object that represents HTTP Basic
Authorization (optional)
:param bool allow\_redirects: Whether to process redirects or not.
When ``True``, redirects are followed (up to ``max\_redirects`` times)
and logged into :attr:`ClientResponse.history` and ``trace\_configs``.
When ``False``, the original response is returned.
``True`` by default (optional).
:param int max\_redirects: Maximum number of redirects to follow.
:exc:`TooManyRedirects` is raised if the number is exceeded.
Ignored when ``allow\_redirects=False``.
``10`` by default.
:param bool compress: Set to ``True`` if request has to be compressed
with deflate encoding. If `compress` can not be combined
with a \*Content-Encoding\* and \*Content-Length\* headers.
``None`` by default (optional).
:param int chunked: Enables chunked transfer encoding.
It is up to the developer
to decide how to chunk data streams. If chunking is enabled, aiohttp
encodes the provided chunks in the "Transfer-encoding: chunked" format.
If \*chunked\* is set, then the \*Transfer-encoding\* and \*content-length\*
headers are disallowed. ``None`` by default (optional).
:param bool expect100: Expect 100-continue response from server.
``False`` by default (optional).
:param bool raise\_for\_status: Automatically call
:meth:`ClientResponse.raise\_for\_status`
for response if set to ``True``. If
set to ``None`` value from
``ClientSession`` will be used.
``None`` by default (optional).
.. versionadded:: 3.4
:param bool read\_until\_eof: Read response until EOF if response
does not have Content-Length header.
``True`` by default (optional).
:param proxy: Proxy URL, :class:`str` or :class:`~yarl.URL` (optional)
:param aiohttp.BasicAuth proxy\_auth: an object that represents proxy HTTP
Basic Authorization (optional)
:param timeout: a :class:`ClientTimeout` settings structure, 300 seconds (5min)
total timeout, 30 seconds socket connect timeout by default.
:param ssl: SSL validation mode. ``True`` for default SSL check
(:func:`ssl.create\_default\_context` is used),
``False`` for skip SSL certificate validation,
:class:`aiohttp.Fingerprint` for fingerprint
validation, :class:`ssl.SSLContext` for custom SSL
certificate validation.
Supersedes \*verify\_ssl\*, \*ssl\_context\* and
\*fingerprint\* parameters.
:param str server\_hostname: Sets or overrides the host name that the
target server's certificate will be matched against.
See :py:meth:`asyncio.loop.create\_connection`
for more information.
:param collections.abc.Mapping proxy\_headers: HTTP headers to send to the proxy
if the parameter proxy has been provided.
:param trace\_request\_ctx: Object used to give as a kw param for each new
:class:`TraceConfig` object instantiated,
used to give information to the
tracers that is only available at request time.
:param int read\_bufsize: Size of the read buffer (:attr:`ClientResponse.content`).
``None`` by default,
it means that the session global value is used.
.. versionadded:: 3.7
:param bool auto\_decompress: Automatically decompress response body.
May be used to enable/disable auto decompression on a per-request basis.
:param int max\_line\_size: Maximum allowed size of lines in responses.
:param int max\_field\_size: Maximum allowed size of header fields in responses.
:param aiohttp.protocol.HttpVersion version: Request HTTP version,
``HTTP 1.1`` by default. (optional)
:param aiohttp.BaseConnector connector: BaseConnector sub-class
instance to support connection pooling. (optional)
:return ClientResponse: a :class:`client response ` object.
Usage::
import aiohttp
async def fetch():
async with aiohttp.request('GET',
'http://python.org/') as resp:
assert resp.status == 200
print(await resp.text())
.. \_aiohttp-client-reference-connectors:
Connectors
----------
Connectors are transports for aiohttp client API.
There are standard connectors:
1. :class:`TCPConnector` for regular \*TCP sockets\* (both \*HTTP\* and
\*HTTPS\* schemes supported).
2. :class:`UnixConnector` for connecting via UNIX socket (it's used mostly for
testing purposes).
All connector classes should be derived from :class:`BaseConnector`.
By default all \*connectors\* support \*keep-alive connections\* (behavior
is controlled by \*force\_close\* constructor's parameter).
.. class:: BaseConnector(\*, keepalive\_timeout=15, \
force\_close=False, limit=100, limit\_per\_host=0, \
enable\_cleanup\_closed=False, loop=None)
Base class for all connectors.
:param float keepalive\_timeout: timeout for connection reusing
after releasing (optional). Values
``0``. For disabling \*keep-alive\*
feature use ``force\_close=True``
flag.
:param int limit: total number simultaneous connections. If \*limit\* is
``0`` the connector has no limit (default: 100).
:param int limit\_per\_host: limit simultaneous connections to the same
endpoint. Endpoints are the same if they are
have equal ``(host, port, is\_ssl)`` triple.
If \*limit\* is ``0`` the connector has no limit (default: 0).
:param bool force\_close: close underlying sockets after
connection releasing (optional).
:param bool enable\_cleanup\_closed: some SSL servers do not properly complete
SSL shutdown process, in that case asyncio leaks SSL connections.
If this parameter is set to True, aiohttp additionally aborts underlining
transport after 2 seconds. It is off by default.
For Python version 3.12.7+, or 3.13.1 and later,
this parameter is ignored because the asyncio SSL connection
leak is fixed in these versions of Python.
:param loop: :ref:`event loop`
used for handling connections.
If param is ``None``, :func:`asyncio.get\_event\_loop`
is used for getting default event loop.
.. deprecated:: 2.0
.. attribute:: closed
Read-only property, ``True`` if connector is closed.
.. attribute:: force\_close
Read-only property, ``True`` if connector should ultimately
close connections on releasing.
.. attribute:: limit
The total number for simultaneous connections.
If limit is 0 the connector has no limit. The default limit size is 100.
.. attribute:: limit\_per\_host
The limit for simultaneous connections to the same
endpoint.
Endpoints are the same if they are have equal ``(host, port,
is\_ssl)`` triple.
If \*limit\_per\_host\* is ``0`` the connector has no limit per host.
Read-only property.
.. method:: close()
:async:
Close all opened connections.
.. method:: connect(request)
:async:
Get a free connection from pool or create new one if connection
is absent in the pool.
The call may be paused if :attr:`limit` is exhausted until used
connections returns to pool.
:param aiohttp.ClientRequest request: request object
which is connection
initiator.
:return: :class:`Connection` object.
.. method:: \_create\_connection(req)
:async:
Abstract method for actual connection establishing, should be
overridden in subclasses.
.. py:class:: AddrInfoType
Refer to :py:data:`aiohappyeyeballs.AddrInfoType` for more info.
.. warning::
Be sure to use ``aiohttp.AddrInfoType`` rather than
``aiohappyeyeballs.AddrInfoType`` to avoid import breakage, as
it is likely to be removed from :mod:`aiohappyeyeballs` in the
future.
.. py:class:: SocketFactoryType
Refer to :py:data:`aiohappyeyeballs.SocketFactoryType` for more info.
.. warning::
Be sure to use ``aiohttp.SocketFactoryType`` rather than
``aiohappyeyeballs.SocketFactoryType`` to avoid import breakage,
as it is likely to be removed from :mod:`aiohappyeyeballs` in the
future.
.. class:: TCPConnector(\*, ssl=True, verify\_ssl=True, fingerprint=None, \
use\_dns\_cache=True, ttl\_dns\_cache=10, \
family=0, ssl\_context=None, local\_addr=None, \
resolver=None, keepalive\_timeout=sentinel, \
force\_close=False, limit=100, limit\_per\_host=0, \
enable\_cleanup\_closed=False, timeout\_ceil\_threshold=5, \
happy\_eyeballs\_delay=0.25, interleave=None, loop=None, \
socket\_factory=None, ssl\_shutdown\_timeout=0)
Connector for working with \*HTTP\* and \*HTTPS\* via \*TCP\* sockets.
The most common transport. When you don't know what connector type
to use, use a :class:`TCPConnector` instance.
:class:`TCPConnector` inherits from :class:`BaseConnector`.
Constructor accepts all parameters suitable for
:class:`BaseConnector` plus several TCP-specific ones:
:param ssl: SSL validation mode. ``True`` for default SSL check
(:func:`ssl.create\_default\_context` is used),
``False`` for skip SSL certificate validation,
:class:`aiohttp.Fingerprint` for fingerprint
validation, :class:`ssl.SSLContext` for custom SSL
certificate validation.
Supersedes \*verify\_ssl\*, \*ssl\_context\* and
\*fingerprint\* parameters.
.. versionadded:: 3.0
:param bool verify\_ssl: perform SSL certificate validation for
\*HTTPS\* requests (enabled by default). May be disabled to
skip validation for sites with invalid certificates.
.. deprecated:: 2.3
Pass \*verify\_ssl\* to ``ClientSession.get()`` etc.
:param bytes fingerprint: pass the SHA256 digest of the expected
certificate in DER format to verify that the certificate the
server presents matches. Useful for `certificate pinning
`\_.
Note: use of MD5 or SHA1 digests is insecure and deprecated.
.. deprecated:: 2.3
Pass \*verify\_ssl\* to ``ClientSession.get()`` etc.
:param bool use\_dns\_cache: use internal cache for DNS lookups, ``True``
by default.
Enabling an option \*may\* speedup connection
establishing a bit but may introduce some
\*side effects\* also.
:param int ttl\_dns\_cache: expire after some seconds the DNS entries, ``None``
means cached forever. By default 10 seconds (optional).
In some environments the IP addresses related to a specific HOST can
change after a specific time. Use this option to keep the DNS cache
updated refreshing each entry after N seconds.
:param int limit: total number simultaneous connections. If \*limit\* is
``0`` the connector has no limit (default: 100).
:param int limit\_per\_host: limit simultaneous connections to the same
endpoint. Endpoints are the same if they are
have equal ``(host, port, is\_ssl)`` triple.
If \*limit\* is ``0`` the connector has no limit (default: 0).
:param aiohttp.abc.AbstractResolver resolver: custom resolver
instance to use. ``aiohttp.DefaultResolver`` by
default (asynchronous if ``aiodns>=1.1`` is installed).
Custom resolvers allow to resolve hostnames differently than the
way the host is configured.
The resolver is ``aiohttp.ThreadedResolver`` by default,
asynchronous version is pretty robust but might fail in
very rare cases.
:param int family: TCP socket family, both IPv4 and IPv6 by default.
For \*IPv4\* only use :data:`socket.AF\_INET`,
for \*IPv6\* only -- :data:`socket.AF\_INET6`.
\*family\* is ``0`` by default, that means both
IPv4 and IPv6 are accepted. To specify only
concrete version please pass
:data:`socket.AF\_INET` or
:data:`socket.AF\_INET6` explicitly.
:param ssl.SSLContext ssl\_context: SSL context used for processing
\*HTTPS\* requests (optional).
\*ssl\_context\* may be used for configuring certification
authority channel, supported SSL options etc.
:param tuple local\_addr: tuple of ``(local\_host, local\_port)`` used to bind
socket locally if specified.
:param bool force\_close: close underlying sockets after
connection releasing (optional).
:param bool enable\_cleanup\_closed: Some ssl servers do not properly complete
SSL shutdown process, in that case asyncio leaks SSL connections.
If this parameter is set to True, aiohttp additionally aborts underlining
transport after 2 seconds. It is off by default.
:param float happy\_eyeballs\_delay: The amount of time in seconds to wait for a
connection attempt to complete, before starting the next attempt in parallel.
This is the “Connection Attempt Delay” as defined in RFC 8305. To disable
Happy Eyeballs, set this to ``None``. The default value recommended by the
RFC is 0.25 (250 milliseconds).
.. versionadded:: 3.10
:param int interleave: controls address reordering when a host name resolves
to multiple IP addresses. If ``0`` or unspecified, no reordering is done, and
addresses are tried in the order returned by the resolver. If a positive
integer is specified, the addresses are interleaved by address family, and
the given integer is interpreted as “First Address Family Count” as defined
in RFC 8305. The default is ``0`` if happy\_eyeballs\_delay is not specified, and
``1`` if it is.
.. versionadded:: 3.10
:param SocketFactoryType socket\_factory: This function takes an
:py:data:`AddrInfoType` and is used in lieu of
:py:func:`socket.socket` when creating TCP connections.
.. versionadded:: 3.12
:param float ssl\_shutdown\_timeout: \*\*(DEPRECATED)\*\* This parameter is deprecated
and will be removed in aiohttp 4.0. Grace period for SSL shutdown on TLS
connections when the connector is closed (``0`` seconds by default).
By default (``0``), SSL connections are aborted immediately when the
connector is closed, without performing the shutdown handshake. During
normal operation, SSL connections use Python's default SSL shutdown
behavior. Setting this to a positive value (e.g., ``0.1``) will perform
a graceful shutdown when closing the connector, notifying the remote
server which can help prevent "connection reset" errors at the cost of
additional cleanup time. Note: On Python versions prior to 3.11, only
a value of ``0`` is supported; other values will trigger a warning.
.. versionadded:: 3.12.5
.. versionchanged:: 3.12.11
Changed default from ``0.1`` to ``0`` to abort SSL connections
immediately when the connector is closed. Added support for
``ssl\_shutdown\_timeout=0`` on all Python versions. A :exc:`RuntimeWarning`
is issued when non-zero values are passed on Python < 3.11.
.. deprecated:: 3.12.11
This parameter is deprecated and will be removed in aiohttp 4.0.
.. attribute:: family
\*TCP\* socket family e.g. :data:`socket.AF\_INET` or
:data:`socket.AF\_INET6`
Read-only property.
.. attribute:: dns\_cache
Use quick lookup in internal \*DNS\* cache for host names if ``True``.
Read-only :class:`bool` property.
.. attribute:: cached\_hosts
The cache of resolved hosts if :attr:`dns\_cache` is enabled.
Read-only :class:`types.MappingProxyType` property.
.. method:: clear\_dns\_cache(self, host=None, port=None)
Clear internal \*DNS\* cache.
Remove specific entry if both \*host\* and \*port\* are specified,
clear all cache otherwise.
.. class:: UnixConnector(path, \*, conn\_timeout=None, \
keepalive\_timeout=30, limit=100, \
force\_close=False, loop=None)
Unix socket connector.
Use :class:`UnixConnector` for sending \*HTTP/HTTPS\* requests
through \*UNIX Sockets\* as underlying transport.
UNIX sockets are handy for writing tests and making very fast
connections between processes on the same host.
:class:`UnixConnector` is inherited from :class:`BaseConnector`.
Usage::
conn = UnixConnector(path='/path/to/socket')
session = ClientSession(connector=conn)
async with session.get('http://python.org') as resp:
...
Constructor accepts all parameters suitable for
:class:`BaseConnector` plus UNIX-specific one:
:param str path: Unix socket path
.. attribute:: path
Path to \*UNIX socket\*, read-only :class:`str` property.
.. class:: Connection
Encapsulates single connection in connector object.
End user should never create :class:`Connection` instances manually
but get it by :meth:`BaseConnector.connect` coroutine.
.. attribute:: closed
:class:`bool` read-only property, ``True`` if connection was
closed, released or detached.
.. attribute:: loop
Event loop used for connection
.. deprecated:: 3.5
.. attribute:: transport
Connection transport
.. method:: close()
Close connection with forcibly closing underlying socket.
.. method:: release()
Release connection back to connector.
Underlying socket is not closed, the connection may be reused
later if timeout (30 seconds by default) for connection was not
expired.
Response object
---------------
.. class:: ClientResponse
Client response returned by :meth:`aiohttp.ClientSession.request` and family.
User never creates the instance of ClientResponse class but gets it
from API calls.
:class:`ClientResponse` supports async context manager protocol, e.g.::
resp = await client\_session.get(url)
async with resp:
assert resp.status == 200
After exiting from ``async with`` block response object will be
\*released\* (see :meth:`release` method).
.. attribute:: version
Response's version, :class:`~aiohttp.protocol.HttpVersion` instance.
.. attribute:: status
HTTP status code of response (:class:`int`), e.g. ``200``.
.. attribute:: reason
HTTP status reason of response (:class:`str`), e.g. ``"OK"``.
.. attribute:: ok
Boolean representation of HTTP status code (:class:`bool`).
``True`` if ``status`` is less than ``400``; otherwise, ``False``.
.. attribute:: method
Request's method (:class:`str`).
.. attribute:: url
URL of request (:class:`~yarl.URL`).
.. attribute:: real\_url
Unmodified URL of request with URL fragment unstripped (:class:`~yarl.URL`).
.. versionadded:: 3.2
.. attribute:: connection
:class:`Connection` used for handling response.
.. attribute:: content
Payload stream, which contains response's BODY (:class:`StreamReader`).
It supports various reading methods depending on the expected format.
When chunked transfer encoding is used by the server, allows retrieving
the actual http chunks.
Reading from the stream may raise
:exc:`aiohttp.ClientPayloadError` if the response object is
closed before response receives all data or in case if any
transfer encoding related errors like malformed chunked
encoding of broken compression data.
.. attribute:: cookies
HTTP cookies of response (\*Set-Cookie\* HTTP header,
:class:`~http.cookies.SimpleCookie`).
.. note::
Since :class:`~http.cookies.SimpleCookie` uses cookie name as the
key, cookies with the same name but different domains or paths will
be overwritten. Only the last cookie with a given name will be
accessible via this attribute.
To access all cookies, including duplicates with the same name,
use :meth:`response.headers.getall('Set-Cookie') `.
The session's cookie jar will correctly store all cookies, even if
they are not accessible via this attribute.
.. attribute:: headers
A case-insensitive multidict proxy with HTTP headers of
response, :class:`~multidict.CIMultiDictProxy`.
.. attribute:: raw\_headers
Unmodified HTTP headers of response as unconverted bytes, a sequence of
``(key, value)`` pairs.
.. attribute:: links
Link HTTP header parsed into a :class:`~multidict.MultiDictProxy`.
For each link, key is link param `rel` when it exists, or link url as
:class:`str` otherwise, and value is :class:`~multidict.MultiDictProxy`
of link params and url at key `url` as :class:`~yarl.URL` instance.
.. versionadded:: 3.2
.. attribute:: content\_type
Read-only property with \*content\* part of \*Content-Type\* header.
.. note::
Returns ``'application/octet-stream'`` if no Content-Type header
is present or the value contains invalid syntax according to
:rfc:`9110`. To see the original header check
``resp.headers["Content-Type"]``.
To make sure Content-Type header is not present in
the server reply, use :attr:`headers` or :attr:`raw\_headers`, e.g.
``'Content-Type' not in resp.headers``.
.. attribute:: charset
Read-only property that specifies the \*encoding\* for the request's BODY.
The value is parsed from the \*Content-Type\* HTTP header.
Returns :class:`str` like ``'utf-8'`` or ``None`` if no \*Content-Type\*
header present in HTTP headers or it has no charset information.
.. attribute:: content\_disposition
Read-only property that specified the \*Content-Disposition\* HTTP header.
Instance of :class:`ContentDisposition` or ``None`` if no \*Content-Disposition\*
header present in HTTP headers.
.. attribute:: history
A :class:`~collections.abc.Sequence` of :class:`ClientResponse`
objects of preceding requests (earliest request first) if there were
redirects, an empty sequence otherwise.
.. method:: close()
Close response and underlying connection.
For :term:`keep-alive` support see :meth:`release`.
.. method:: read()
:async:
Read the whole response's body as :class:`bytes`.
Close underlying connection if data reading gets an error,
release connection otherwise.
Raise an :exc:`aiohttp.ClientResponseError` if the data can't
be read.
:return bytes: read \*BODY\*.
.. seealso:: :meth:`close`, :meth:`release`.
.. method:: release()
It is not required to call `release` on the response
object. When the client fully receives the payload, the
underlying connection automatically returns back to pool. If the
payload is not fully read, the connection is closed
.. method:: raise\_for\_status()
Raise an :exc:`aiohttp.ClientResponseError` if the response
status is 400 or higher.
Do nothing for success responses (less than 400).
.. method:: text(encoding=None)
:async:
Read response's body and return decoded :class:`str` using
specified \*encoding\* parameter.
If \*encoding\* is ``None`` content encoding is determined from the
Content-Type header, or using the ``fallback\_charset\_resolver`` function.
Close underlying connection if data reading gets an error,
release connection otherwise.
:param str encoding: text encoding used for \*BODY\* decoding, or
``None`` for encoding autodetection
(default).
:raises: :exc:`UnicodeDecodeError` if decoding fails. See also
:meth:`get\_encoding`.
:return str: decoded \*BODY\*
.. method:: json(\*, encoding=None, loads=json.loads, \
content\_type='application/json')
:async:
Read response's body as \*JSON\*, return :class:`dict` using
specified \*encoding\* and \*loader\*. If data is not still available
a ``read`` call will be done.
If response's `content-type` does not match `content\_type` parameter
:exc:`aiohttp.ContentTypeError` get raised.
To disable content type check pass ``None`` value.
:param str encoding: text encoding used for \*BODY\* decoding, or
``None`` for encoding autodetection
(default).
By the standard JSON encoding should be
``UTF-8`` but practice beats purity: some
servers return non-UTF
responses. Autodetection works pretty fine
anyway.
:param collections.abc.Callable loads: :term:`callable` used for loading \*JSON\*
data, :func:`json.loads` by default.
:param str content\_type: specify response's content-type, if content type
does not match raise :exc:`aiohttp.ClientResponseError`.
To disable `content-type` check, pass ``None`` as value.
(default: `application/json`).
:return: \*BODY\* as \*JSON\* data parsed by \*loads\* parameter or
``None`` if \*BODY\* is empty or contains white-spaces only.
.. attribute:: request\_info
A :class:`typing.NamedTuple` with request URL and headers from :class:`~aiohttp.ClientRequest`
object, :class:`aiohttp.RequestInfo` instance.
.. method:: get\_encoding()
Retrieve content encoding using ``charset`` info in ``Content-Type`` HTTP header.
If no charset is present or the charset is not understood by Python, the
``fallback\_charset\_resolver`` function associated with the ``ClientSession`` is called.
.. versionadded:: 3.0
ClientWebSocketResponse
-----------------------
To connect to a websocket server :func:`aiohttp.ws\_connect` or
:meth:`aiohttp.ClientSession.ws\_connect` coroutines should be used, do
not create an instance of class :class:`ClientWebSocketResponse`
manually.
.. class:: ClientWebSocketResponse()
Class for handling client-side websockets.
.. attribute:: closed
Read-only property, ``True`` if :meth:`close` has been called or
:const:`~aiohttp.WSMsgType.CLOSE` message has been received from peer.
.. attribute:: protocol
Websocket \*subprotocol\* chosen after :meth:`start` call.
May be ``None`` if server and client protocols are
not overlapping.
.. method:: get\_extra\_info(name, default=None)
Reads optional extra information from the connection's transport.
If no value associated with ``name`` is found, ``default`` is returned.
See :meth:`asyncio.BaseTransport.get\_extra\_info`
:param str name: The key to look up in the transport extra information.
:param default: Default value to be used when no value for ``name`` is
found (default is ``None``).
.. method:: exception()
Returns exception if any occurs or returns None.
.. method:: ping(message=b'')
:async:
Send :const:`~aiohttp.WSMsgType.PING` to peer.
:param message: optional payload of \*ping\* message,
:class:`str` (converted to \*UTF-8\* encoded bytes)
or :class:`bytes`.
.. versionchanged:: 3.0
The method is converted into :term:`coroutine`
.. method:: pong(message=b'')
:async:
Send :const:`~aiohttp.WSMsgType.PONG` to peer.
:param message: optional payload of \*pong\* message,
:class:`str` (converted to \*UTF-8\* encoded bytes)
or :class:`bytes`.
.. versionchanged:: 3.0
The method is converted into :term:`coroutine`
.. method:: send\_str(data, compress=None)
:async:
Send \*data\* to peer as :const:`~aiohttp.WSMsgType.TEXT` message.
:param str data: data to send.
:param int compress: sets specific level of compression for
single message,
``None`` for not overriding per-socket setting.
:raise TypeError: if data is not :class:`str`
.. versionchanged:: 3.0
The method is converted into :term:`coroutine`,
\*compress\* parameter added.
.. method:: send\_bytes(data, compress=None)
:async:
Send \*data\* to peer as :const:`~aiohttp.WSMsgType.BINARY` message.
:param data: data to send.
:param int compress: sets specific level of compression for
single message,
``None`` for not overriding per-socket setting.
:raise TypeError: if data is not :class:`bytes`,
:class:`bytearray` or :class:`memoryview`.
.. versionchanged:: 3.0
The method is converted into :term:`coroutine`,
\*compress\* parameter added.
.. method:: send\_json(data, compress=None, \*, dumps=json.dumps)
:async:
Send \*data\* to peer as JSON string.
:param data: data to send.
:param int compress: sets specific level of compression for
single message,
``None`` for not overriding per-socket setting.
:param collections.abc.Callable dumps: any :term:`callable` that accepts an object and
returns a JSON string
(:func:`json.dumps` by default).
:raise RuntimeError: if connection is not started or closing
:raise ValueError: if data is not serializable object
:raise TypeError: if value returned by ``dumps(data)`` is not
:class:`str`
.. versionchanged:: 3.0
The method is converted into :term:`coroutine`,
\*compress\* parameter added.
.. method:: send\_frame(message, opcode, compress=None)
:async:
Send a :const:`~aiohttp.WSMsgType` message \*message\* to peer.
This method is low-level and should be used with caution as it
only accepts bytes which must conform to the correct message type
for \*message\*.
It is recommended to use the :meth:`send\_str`, :meth:`send\_bytes`
or :meth:`send\_json` methods instead of this method.
The primary use case for this method is to send bytes that are
have already been encoded without having to decode and
re-encode them.
:param bytes message: message to send.
:param ~aiohttp.WSMsgType opcode: opcode of the message.
:param int compress: sets specific level of compression for
single message,
``None`` for not overriding per-socket setting.
.. versionadded:: 3.11
.. method:: close(\*, code=WSCloseCode.OK, message=b'')
:async:
A :ref:`coroutine` that initiates closing handshake by sending
:const:`~aiohttp.WSMsgType.CLOSE` message. It waits for
close response from server. To add a timeout to `close()` call
just wrap the call with `asyncio.wait()` or `asyncio.wait\_for()`.
:param int code: closing code. See also :class:`~aiohttp.WSCloseCode`.
:param message: optional payload of \*close\* message,
:class:`str` (converted to \*UTF-8\* encoded bytes) or :class:`bytes`.
.. method:: receive()
:async:
A :ref:`coroutine` that waits upcoming \*data\*
message from peer and returns it.
The coroutine implicitly handles
:const:`~aiohttp.WSMsgType.PING`,
:const:`~aiohttp.WSMsgType.PONG` and
:const:`~aiohttp.WSMsgType.CLOSE` without returning the
message.
It process \*ping-pong game\* and performs \*closing handshake\* internally.
:return: :class:`~aiohttp.WSMessage`
.. method:: receive\_str()
:async:
A :ref:`coroutine` that calls :meth:`receive` but
also asserts the message type is
:const:`~aiohttp.WSMsgType.TEXT`.
:return str: peer's message content.
:raise aiohttp.WSMessageTypeError: if message is not :const:`~aiohttp.WSMsgType.TEXT`.
.. method:: receive\_bytes()
:async:
A :ref:`coroutine` that calls :meth:`receive` but
also asserts the message type is
:const:`~aiohttp.WSMsgType.BINARY`.
:return bytes: peer's message content.
:raise aiohttp.WSMessageTypeError: if message is not :const:`~aiohttp.WSMsgType.BINARY`.
.. method:: receive\_json(\*, loads=json.loads)
:async:
A :ref:`coroutine` that calls :meth:`receive\_str` and loads
the JSON string to a Python dict.
:param collections.abc.Callable loads: any :term:`callable` that accepts
:class:`str` and returns :class:`dict`
with parsed JSON (:func:`json.loads` by
default).
:return dict: loaded JSON content
:raise TypeError: if message is :const:`~aiohttp.WSMsgType.BINARY`.
:raise ValueError: if message is not valid JSON.
ClientRequest
-------------
.. class:: ClientRequest
Represents an HTTP request to be sent by the client.
This object encapsulates all the details of an HTTP request before it is sent.
It is primarily used within client middleware to inspect or modify requests.
.. note::
You typically don't create ``ClientRequest`` instances directly. They are
created internally by :class:`ClientSession` methods and passed to middleware.
For more information about using middleware, see :ref:`aiohttp-client-middleware`.
.. attribute:: body
:type: Payload | Literal[b""]
The request body payload (defaults to ``b""`` if no body passed).
.. danger::
\*\*DO NOT set this attribute directly!\*\* Direct assignment will cause resource
leaks. Always use :meth:`update\_body` instead:
.. code-block:: python
# WRONG - This will leak resources!
request.body = b"new data"
# CORRECT - Use update\_body
await request.update\_body(b"new data")
Setting body directly bypasses cleanup of the previous payload, which can
leave file handles open, streams unclosed, and buffers unreleased.
Additionally, setting body directly must be done from within an event loop
and is not thread-safe. Setting body outside of an event loop may raise
RuntimeError when closing file-based payloads.
.. attribute:: chunked
:type: bool | None
Whether to use chunked transfer encoding:
- ``True``: Use chunked encoding
- ``False``: Don't use chunked encoding
- ``None``: Automatically determine based on body
.. attribute:: compress
:type: str | None
The compression encoding for the request body. Common values include
``'gzip'`` and ``'deflate'``, but any string value is technically allowed.
``None`` means no compression.
.. attribute:: headers
:type: multidict.CIMultiDict
The HTTP headers that will be sent with the request. This is a case-insensitive
multidict that can be modified by middleware.
.. code-block:: python
# Add or modify headers
request.headers['X-Custom-Header'] = 'value'
request.headers['User-Agent'] = 'MyApp/1.0'
.. attribute:: is\_ssl
:type: bool
``True`` if the request uses a secure scheme (e.g., HTTPS, WSS), ``False`` otherwise.
.. attribute:: method
:type: str
The HTTP method of the request (e.g., ``'GET'``, ``'POST'``, ``'PUT'``, etc.).
.. attribute:: original\_url
:type: yarl.URL
The original URL passed to the request method, including any fragment.
This preserves the exact URL as provided by the user.
.. attribute:: proxy
:type: yarl.URL | None
The proxy URL if the request will be sent through a proxy, ``None`` otherwise.
.. attribute:: proxy\_headers
:type: multidict.CIMultiDict | None
Headers to be sent to the proxy server (e.g., ``Proxy-Authorization``).
Only set when :attr:`proxy` is not ``None``.
.. attribute:: response\_class
:type: type[ClientResponse]
The class to use for creating the response object. Defaults to
:class:`ClientResponse` but can be customized for special handling.
.. attribute:: server\_hostname
:type: str | None
Override the hostname for SSL certificate verification. Useful when
connecting through proxies or to IP addresses.
.. attribute:: session
:type: ClientSession
The client session that created this request. Useful for accessing
session-level configuration or making additional requests within middleware.
.. warning::
Be careful when making requests with the same session inside middleware
to avoid infinite recursion. Use ``middlewares=()`` parameter when needed.
.. attribute:: ssl
:type: ssl.SSLContext | bool | Fingerprint
SSL validation configuration for this request:
- ``True``: Use default SSL verification
- ``False``: Skip SSL verification
- :class:`ssl.SSLContext`: Custom SSL context
- :class:`Fingerprint`: Verify specific certificate fingerprint
.. attribute:: url
:type: yarl.URL
The target URL of the request with the fragment (``#...``) part stripped.
This is the actual URL that will be used for the connection.
.. note::
To access the original URL with fragment, use :attr:`original\_url`.
.. attribute:: version
:type: HttpVersion
The HTTP version to use for the request (e.g., ``HttpVersion(1, 1)`` for HTTP/1.1).
.. method:: update\_body(body)
Update the request body and close any existing payload to prevent resource leaks.
\*\*This is the ONLY correct way to modify a request body.\*\* Never set the
:attr:`body` attribute directly.
This method is particularly useful in middleware when you need to modify the
request body after the request has been created but before it's sent.
:param body: The new body content. Can be:
- ``bytes``/``bytearray``: Raw binary data
- ``str``: Text data (encoded using charset from Content-Type)
- :class:`FormData`: Form data encoded as multipart/form-data
- :class:`Payload`: A pre-configured payload object
- ``AsyncIterable[bytes]``: Async iterable of bytes chunks
- File-like object: Will be read and sent as binary data
- ``None``: Clears the body
.. code-block:: python
async def middleware(request, handler):
# Modify request body in middleware
if request.method == 'POST':
# CORRECT: Always use update\_body
await request.update\_body(b'{"modified": true}')
# WRONG: Never set body directly!
# request.body = b'{"modified": true}' # This leaks resources!
# Or add authentication data to form
if isinstance(request.body, FormData):
form = FormData()
# Copy existing fields and add auth token
form.add\_field('auth\_token', 'secret123')
await request.update\_body(form)
return await handler(request)
.. note::
This method is async because it may need to close file handles or
other resources associated with the previous payload. Always await
this method to ensure proper cleanup.
.. danger::
\*\*Never set :attr:`ClientRequest.body` directly!\*\* Direct assignment will cause resource
leaks. Always use this method instead. Setting the body attribute directly:
- Bypasses cleanup of the previous payload
- Leaves file handles and streams open
- Can cause memory leaks
- May result in unexpected behavior with async iterables
.. warning::
When updating the body, ensure that the Content-Type header is
appropriate for the new body content. The Content-Length header
will be updated automatically. When using :class:`FormData` or
:class:`Payload` objects, headers are updated automatically,
but you may need to set Content-Type manually for raw bytes or text.
It is not recommended to change the payload type in middleware. If the
body was already set (e.g., as bytes), it's best to keep the same type
rather than converting it (e.g., to str) as this may result in unexpected
behavior.
.. versionadded:: 3.12
Utilities
---------
.. class:: ClientTimeout(\*, total=None, connect=None, \
sock\_connect=None, sock\_read=None)
A data class for client timeout settings.
See :ref:`aiohttp-client-timeouts` for usage examples.
.. attribute:: total
Total number of seconds for the whole request.
:class:`float`, ``None`` by default.
.. attribute:: connect
Maximal number of seconds for acquiring a connection from pool. The time
consists connection establishment for a new connection or
waiting for a free connection from a pool if pool connection
limits are exceeded.
For pure socket connection establishment time use
:attr:`sock\_connect`.
:class:`float`, ``None`` by default.
.. attribute:: sock\_connect
Maximal number of seconds for connecting to a peer for a new connection, not
given from a pool. See also :attr:`connect`.
:class:`float`, ``None`` by default.
.. attribute:: sock\_read
Maximal number of seconds for reading a portion of data from a peer.
:class:`float`, ``None`` by default.
.. class:: ClientWSTimeout(\*, ws\_receive=None, ws\_close=None)
A data class for websocket client timeout settings.
.. attribute:: ws\_receive
A timeout for websocket to receive a complete message.
:class:`float`, ``None`` by default.
.. attribute:: ws\_close
A timeout for the websocket to close.
:class:`float`, ``10.0`` by default.
.. versionadded:: 4.0
.. note::
Timeouts of 5 seconds or more are rounded for scheduling on the next
second boundary (an absolute time where microseconds part is zero) for the
sake of performance.
E.g., assume a timeout is ``10``, absolute time when timeout should expire
is ``loop.time() + 5``, and it points to ``12345.67 + 10`` which is equal
to ``12355.67``.
The absolute time for the timeout cancellation is ``12356``.
It leads to grouping all close scheduled timeout expirations to exactly
the same time to reduce amount of loop wakeups.
.. versionchanged:: 3.7
Rounding to the next seconds boundary is disabled for timeouts smaller
than 5 seconds for the sake of easy debugging.
In turn, tiny timeouts can lead to significant performance degradation
on production environment.
.. class:: ETag(name, is\_weak=False)
Represents `ETag` identifier.
.. attribute:: value
Value of corresponding etag without quotes.
.. attribute:: is\_weak
Flag indicates that etag is weak (has `W/` prefix).
.. versionadded:: 3.8
.. class:: ContentDisposition
A data class to represent the Content-Disposition header,
available as :attr:`ClientResponse.content\_disposition` attribute.
.. attribute:: type
A :class:`str` instance. Value of Content-Disposition header
itself, e.g. ``attachment``.
.. attribute:: filename
A :class:`str` instance. Content filename extracted from
parameters. May be ``None``.
.. attribute:: parameters
Read-only mapping contains all parameters.
.. class:: RequestInfo()
A :class:`typing.NamedTuple` with request URL and headers from :class:`~aiohttp.ClientRequest`
object, available as :attr:`ClientResponse.request\_info` attribute.
.. attribute:: url
Requested \*url\*, :class:`yarl.URL` instance.
.. attribute:: method
Request HTTP method like ``'GET'`` or ``'POST'``, :class:`str`.
.. attribute:: headers
HTTP headers for request, :class:`multidict.CIMultiDict` instance.
.. attribute:: real\_url
Requested \*url\* with URL fragment unstripped, :class:`yarl.URL` instance.
.. versionadded:: 3.2
.. class:: BasicAuth(login, password='', encoding='latin1')
HTTP basic authentication helper.
:param str login: login
:param str password: password
:param str encoding: encoding (``'latin1'`` by default)
Should be used for specifying authorization data in client API,
e.g. \*auth\* parameter for :meth:`ClientSession.request() `.
.. classmethod:: decode(auth\_header, encoding='latin1')
Decode HTTP basic authentication credentials.
:param str auth\_header: The ``Authorization`` header to decode.
:param str encoding: (optional) encoding ('latin1' by default)
:return: decoded authentication data, :class:`BasicAuth`.
.. classmethod:: from\_url(url)
Constructed credentials info from url's \*user\* and \*password\*
parts.
:return: credentials data, :class:`BasicAuth` or ``None`` is
credentials are not provided.
.. versionadded:: 2.3
.. method:: encode()
Encode credentials into string suitable for ``Authorization``
header etc.
:return: encoded authentication data, :class:`str`.
.. class:: DigestAuthMiddleware(login, password, \*, preemptive=True)
HTTP digest authentication client middleware.
:param str login: login
:param str password: password
:param bool preemptive: Enable preemptive authentication (default: ``True``)
This middleware supports HTTP digest authentication with both `auth` and
`auth-int` quality of protection (qop) modes, and a variety of hashing algorithms.
It automatically handles the digest authentication handshake by:
- Parsing 401 Unauthorized responses with `WWW-Authenticate: Digest` headers
- Generating appropriate `Authorization: Digest` headers on retry
- Maintaining nonce counts and challenge data per request
- When ``preemptive=True``, reusing authentication credentials for subsequent
requests to the same protection space (following RFC 7616 Section 3.6)
\*\*Preemptive Authentication\*\*
By default (``preemptive=True``), the middleware remembers successful authentication
challenges and automatically includes the Authorization header in subsequent requests
to the same protection space. This behavior:
- Improves server efficiency by avoiding extra round trips
- Matches how modern web browsers handle digest authentication
- Follows the recommendation in RFC 7616 Section 3.6
The server may still respond with a 401 status and ``stale=true`` if the nonce
has expired, in which case the middleware will automatically retry with the new nonce.
To disable preemptive authentication and require a 401 challenge for every request,
set ``preemptive=False``::
# Default behavior - preemptive auth enabled
digest\_auth\_middleware = DigestAuthMiddleware(login="user", password="pass")
# Disable preemptive auth - always wait for 401 challenge
digest\_auth\_middleware = DigestAuthMiddleware(login="user", password="pass",
preemptive=False)
Usage::
digest\_auth\_middleware = DigestAuthMiddleware(login="user", password="pass")
async with ClientSession(middlewares=(digest\_auth\_middleware,)) as session:
async with session.get("http://protected.example.com") as resp:
# The middleware automatically handles the digest auth handshake
assert resp.status == 200
# Subsequent requests include auth header preemptively
async with session.get("http://protected.example.com/other") as resp:
assert resp.status == 200 # No 401 round trip needed
.. versionadded:: 3.12
.. versionchanged:: 3.12.8
Added ``preemptive`` parameter to enable/disable preemptive authentication.
.. class:: CookieJar(\*, unsafe=False, quote\_cookie=True, treat\_as\_secure\_origin = [])
The cookie jar instance is available as :attr:`ClientSession.cookie\_jar`.
The jar contains :class:`~http.cookies.Morsel` items for storing
internal cookie data.
API provides a count of saved cookies::
len(session.cookie\_jar)
These cookies may be iterated over::
for cookie in session.cookie\_jar:
print(cookie.key)
print(cookie["domain"])
The class implements :class:`collections.abc.Iterable`,
:class:`collections.abc.Sized` and
:class:`aiohttp.abc.AbstractCookieJar` interfaces.
Implements cookie storage adhering to RFC 6265.
:param bool unsafe: (optional) Whether to accept cookies from IPs.
:param bool quote\_cookie: (optional) Whether to quote cookies according to
:rfc:`2109`. Some backend systems
(not compatible with RFC mentioned above)
does not support quoted cookies.
.. versionadded:: 3.7
:param treat\_as\_secure\_origin: (optional) Mark origins as secure
for cookies marked as Secured. Possible types are
Possible types are:
- :class:`tuple` or :class:`list` of
:class:`str` or :class:`yarl.URL`
- :class:`str`
- :class:`yarl.URL`
.. versionadded:: 3.8
.. method:: update\_cookies(cookies, response\_url=None)
Update cookies returned by server in ``Set-Cookie`` header.
:param cookies: a :class:`collections.abc.Mapping`
(e.g. :class:`dict`, :class:`~http.cookies.SimpleCookie`) or
\*iterable\* of \*pairs\* with cookies returned by server's
response.
:param ~yarl.URL response\_url: URL of response, ``None`` for \*shared
cookies\*. Regular cookies are coupled with server's URL and
are sent only to this server, shared ones are sent in every
client request.
.. method:: filter\_cookies(request\_url)
Return jar's cookies acceptable for URL and available in
``Cookie`` header for sending client requests for given URL.
:param ~yarl.URL response\_url: request's URL for which cookies are asked.
:return: :class:`http.cookies.SimpleCookie` with filtered
cookies for given URL.
.. method:: save(file\_path)
Write a pickled representation of cookies into the file
at provided path.
:param file\_path: Path to file where cookies will be serialized,
:class:`str` or :class:`pathlib.Path` instance.
.. method:: load(file\_path)
Load a pickled representation of cookies from the file
at provided path.
:param file\_path: Path to file from where cookies will be
imported, :class:`str` or :class:`pathlib.Path` instance.
.. method:: clear(predicate=None)
Removes all cookies from the jar if the predicate is ``None``. Otherwise remove only those :class:`~http.cookies.Morsel` that ``predicate(morsel)`` returns ``True``.
:param predicate: callable that gets :class:`~http.cookies.Morsel` as a parameter and returns ``True`` if this :class:`~http.cookies.Morsel` must be deleted from the jar.
.. versionadded:: 4.0
.. method:: clear\_domain(domain)
Remove all cookies from the jar that belongs to the specified domain or its subdomains.
:param str domain: domain for which cookies must be deleted from the jar.
.. versionadded:: 4.0
.. class:: DummyCookieJar(\*, loop=None)
Dummy cookie jar which does not store cookies but ignores them.
Could be useful e.g. for web crawlers to iterate over Internet
without blowing up with saved cookies information.
To install dummy cookie jar pass it into session instance::
jar = aiohttp.DummyCookieJar()
session = aiohttp.ClientSession(cookie\_jar=DummyCookieJar())
.. class:: Fingerprint(digest)
Fingerprint helper for checking SSL certificates by \*SHA256\* digest.
:param bytes digest: \*SHA256\* digest for certificate in DER-encoded
binary form (see
:meth:`ssl.SSLSocket.getpeercert`).
To check fingerprint pass the object into :meth:`ClientSession.get`
call, e.g.::
import hashlib
with open(path\_to\_cert, 'rb') as f:
digest = hashlib.sha256(f.read()).digest()
await session.get(url, ssl=aiohttp.Fingerprint(digest))
.. versionadded:: 3.0
.. function:: set\_zlib\_backend(lib)
Sets the compression backend for zlib-based operations.
This function allows you to override the default zlib backend
used internally by passing a module that implements the standard
compression interface.
The module should implement at minimum the exact interface offered by the
latest version of zlib.
:param types.ModuleType lib: A module that implements the zlib-compatible compression API.
Example usage::
import zlib\_ng.zlib\_ng as zng
import aiohttp
aiohttp.set\_zlib\_backend(zng)
.. note:: aiohttp has been tested internally with :mod:`zlib`, :mod:`zlib\_ng.zlib\_ng`, and :mod:`isal.isal\_zlib`.
.. versionadded:: 3.12
FormData
^^^^^^^^
A :class:`FormData` object contains the form data and also handles
encoding it into a body that is either ``multipart/form-data`` or
``application/x-www-form-urlencoded``. ``multipart/form-data`` is
used if at least one field is an :class:`io.IOBase` object or was
added with at least one optional argument to :meth:`add\_field`
(``content\_type``, ``filename``, or ``content\_transfer\_encoding``).
Otherwise, ``application/x-www-form-urlencoded`` is used.
:class:`FormData` instances are callable and return a :class:`aiohttp.payload.Payload`
on being called.
.. class:: FormData(fields, quote\_fields=True, charset=None)
Helper class for multipart/form-data and application/x-www-form-urlencoded body generation.
:param fields: A container for the key/value pairs of this form.
Possible types are:
- :class:`dict`
- :class:`tuple` or :class:`list`
- :class:`io.IOBase`, e.g. a file-like object
- :class:`multidict.MultiDict` or :class:`multidict.MultiDictProxy`
If it is a :class:`tuple` or :class:`list`, it must be a valid argument
for :meth:`add\_fields`.
For :class:`dict`, :class:`multidict.MultiDict`, and :class:`multidict.MultiDictProxy`,
the keys and values must be valid `name` and `value` arguments to
:meth:`add\_field`, respectively.
.. method:: add\_field(name, value, content\_type=None, filename=None,\
content\_transfer\_encoding=None)
Add a field to the form.
:param str name: Name of the field
:param value: Value of the field
Possible types are:
- :class:`str`
- :class:`bytes`, :class:`bytearray`, or :class:`memoryview`
- :class:`io.IOBase`, e.g. a file-like object
:param str content\_type: The field's content-type header (optional)
:param str filename: The field's filename (optional)
If this is not set and ``value`` is a :class:`bytes`, :class:`bytearray`,
or :class:`memoryview` object, the `name` argument is used as the filename
unless ``content\_transfer\_encoding`` is specified.
If ``filename`` is not set and ``value`` is an :class:`io.IOBase`
object, the filename is extracted from the object if possible.
:param str content\_transfer\_encoding: The field's content-transfer-encoding
header (optional)
.. method:: add\_fields(fields)
Add one or more fields to the form.
:param fields: An iterable containing:
- :class:`io.IOBase`, e.g. a file-like object
- :class:`multidict.MultiDict` or :class:`multidict.MultiDictProxy`
- :class:`tuple` or :class:`list` of length two, containing a name-value pair
Client exceptions
-----------------
Exception hierarchy has been significantly modified in version
2.0. aiohttp defines only exceptions that covers connection handling
and server response misbehaviors. For developer specific mistakes,
aiohttp uses python standard exceptions like :exc:`ValueError` or
:exc:`TypeError`.
Reading a response content may raise a :exc:`ClientPayloadError`
exception. This exception indicates errors specific to the payload
encoding. Such as invalid compressed data, malformed chunked-encoded
chunks or not enough data that satisfy the content-length header.
All exceptions are available as members of \*aiohttp\* module.
.. exception:: ClientError
Base class for all client specific exceptions.
Derived from :exc:`Exception`
.. class:: ClientPayloadError
This exception can only be raised while reading the response
payload if one of these errors occurs:
1. invalid compression
2. malformed chunked encoding
3. not enough data that satisfy ``Content-Length`` HTTP header.
Derived from :exc:`ClientError`
.. exception:: InvalidURL
URL used for fetching is malformed, e.g. it does not contain host
part.
Derived from :exc:`ClientError` and :exc:`ValueError`
.. attribute:: url
Invalid URL, :class:`yarl.URL` instance.
.. attribute:: description
Invalid URL description, :class:`str` instance or :data:`None`.
.. exception:: InvalidUrlClientError
Base class for all errors related to client url.
Derived from :exc:`InvalidURL`
.. exception:: RedirectClientError
Base class for all errors related to client redirects.
Derived from :exc:`ClientError`
.. exception:: NonHttpUrlClientError
Base class for all errors related to non http client urls.
Derived from :exc:`ClientError`
.. exception:: InvalidUrlRedirectClientError
Redirect URL is malformed, e.g. it does not contain host part.
Derived from :exc:`InvalidUrlClientError` and :exc:`RedirectClientError`
.. exception:: NonHttpUrlRedirectClientError
Redirect URL does not contain http schema.
Derived from :exc:`RedirectClientError` and :exc:`NonHttpUrlClientError`
Response errors
^^^^^^^^^^^^^^^
.. exception:: ClientResponseError
These exceptions could happen after we get response from server.
Derived from :exc:`ClientError`
.. attribute:: request\_info
Instance of :class:`RequestInfo` object, contains information
about request.
.. attribute:: status
HTTP status code of response (:class:`int`), e.g. ``400``.
.. attribute:: message
Message of response (:class:`str`), e.g. ``"OK"``.
.. attribute:: headers
Headers in response, a list of pairs.
.. attribute:: history
History from failed response, if available, else empty tuple.
A :class:`tuple` of :class:`ClientResponse` objects used for
handle redirection responses.
.. attribute:: code
HTTP status code of response (:class:`int`), e.g. ``400``.
.. deprecated:: 3.1
.. class:: ContentTypeError
Invalid content type.
Derived from :exc:`ClientResponseError`
.. versionadded:: 2.3
.. class:: TooManyRedirects
Client was redirected too many times.
Maximum number of redirects can be configured by using
parameter ``max\_redirects`` in :meth:`request`.
Derived from :exc:`ClientResponseError`
.. versionadded:: 3.2
.. class:: WSServerHandshakeError
Web socket server response error.
Derived from :exc:`ClientResponseError`
.. exception:: WSMessageTypeError
Received WebSocket message of unexpected type
Derived from :exc:`TypeError`
Connection errors
^^^^^^^^^^^^^^^^^
.. class:: ClientConnectionError
These exceptions related to low-level connection problems.
Derived from :exc:`ClientError`
.. class:: ClientConnectionResetError
Derived from :exc:`ClientConnectionError` and :exc:`ConnectionResetError`
.. class:: ClientOSError
Subset of connection errors that are initiated by an :exc:`OSError`
exception.
Derived from :exc:`ClientConnectionError` and :exc:`OSError`
.. class:: ClientConnectorError
Connector related exceptions.
Derived from :exc:`ClientOSError`
.. class:: ClientConnectorDNSError
DNS resolution error.
Derived from :exc:`ClientConnectorError`
.. class:: ClientProxyConnectionError
Derived from :exc:`ClientConnectorError`
.. class:: ClientSSLError
Derived from :exc:`ClientConnectorError`
.. class:: ClientConnectorSSLError
Response ssl error.
Derived from :exc:`ClientSSLError` and :exc:`ssl.SSLError`
.. class:: ClientConnectorCertificateError
Response certificate error.
Derived from :exc:`ClientSSLError` and :exc:`ssl.CertificateError`
.. class:: UnixClientConnectorError
Derived from :exc:`ClientConnectorError`
.. class:: ServerConnectionError
Derived from :exc:`ClientConnectionError`
.. class:: ServerDisconnectedError
Server disconnected.
Derived from :exc:`~aiohttp.ServerConnectionError`
.. attribute:: message
Partially parsed HTTP message (optional).
.. class:: ServerFingerprintMismatch
Server fingerprint mismatch.
Derived from :exc:`ServerConnectionError`
.. class:: ServerTimeoutError
Server operation timeout: read timeout, etc.
To catch all timeouts, including the ``total`` timeout, use
:exc:`asyncio.TimeoutError`.
Derived from :exc:`ServerConnectionError` and :exc:`asyncio.TimeoutError`
.. class:: ConnectionTimeoutError
Connection timeout on ``connect`` and ``sock\_connect`` timeouts.
Derived from :exc:`ServerTimeoutError`
.. class:: SocketTimeoutError
Reading from socket timeout on ``sock\_read`` timeout.
Derived from :exc:`ServerTimeoutError`
Hierarchy of exceptions
^^^^^^^^^^^^^^^^^^^^^^^
\* :exc:`ClientError`
\* :exc:`ClientConnectionError`
\* :exc:`ClientConnectionResetError`
\* :exc:`ClientOSError`
\* :exc:`ClientConnectorError`
\* :exc:`ClientProxyConnectionError`
\* :exc:`ClientConnectorDNSError`
\* :exc:`ClientSSLError`
\* :exc:`ClientConnectorCertificateError`
\* :exc:`ClientConnectorSSLError`
\* :exc:`UnixClientConnectorError`
\* :exc:`ServerConnectionError`
\* :exc:`ServerDisconnectedError`
\* :exc:`ServerFingerprintMismatch`
\* :exc:`ServerTimeoutError`
\* :exc:`ConnectionTimeoutError`
\* :exc:`SocketTimeoutError`
\* :exc:`ClientPayloadError`
\* :exc:`ClientResponseError`
\* :exc:`~aiohttp.ClientHttpProxyError`
\* :exc:`ContentTypeError`
\* :exc:`TooManyRedirects`
\* :exc:`WSServerHandshakeError`
\* :exc:`InvalidURL`
\* :exc:`InvalidUrlClientError`
\* :exc:`InvalidUrlRedirectClientError`
\* :exc:`NonHttpUrlClientError`
\* :exc:`NonHttpUrlRedirectClientError`
\* :exc:`RedirectClientError`
\* :exc:`InvalidUrlRedirectClientError`
\* :exc:`NonHttpUrlRedirectClientError`
Client Types
------------
.. type:: ClientMiddlewareType
Type alias for client middleware functions. Middleware functions must have this signature::
Callable[
[ClientRequest, ClientHandlerType],
Awaitable[ClientResponse]
]
.. type:: ClientHandlerType
Type alias for client request handler functions::
Callable[[ClientRequest], Awaitable[ClientResponse]]
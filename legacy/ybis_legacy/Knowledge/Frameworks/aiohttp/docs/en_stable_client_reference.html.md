Client Reference — aiohttp 3.13.3 documentation

# Client Reference[¶](#client-reference "Link to this heading")

## Client Session[¶](#client-session "Link to this heading")

Client session is the recommended interface for making HTTP requests.

Session encapsulates a *connection pool* (*connector* instance) and
supports keepalives by default. Unless you are connecting to a large,
unknown number of different servers over the lifetime of your
application, it is suggested you use a single session for the
lifetime of your application to benefit from connection pooling.

Usage example:

```
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
```

The client session supports the context manager protocol for self closing.

class aiohttp.ClientSession(*base\_url=None*, *\**, *connector=None*, *cookies=None*, *headers=None*, *skip\_auto\_headers=None*, *auth=None*, *json\_serialize=json.dumps*, *request\_class=ClientRequest*, *response\_class=ClientResponse*, *ws\_response\_class=ClientWebSocketResponse*, *version=aiohttp.HttpVersion11*, *cookie\_jar=None*, *connector\_owner=True*, *raise\_for\_status=False*, *timeout=sentinel*, *auto\_decompress=True*, *trust\_env=False*, *requote\_redirect\_url=True*, *trace\_configs=None*, *middlewares=()*, *read\_bufsize=2\*\*16*, *max\_line\_size=8190*, *max\_field\_size=8190*, *fallback\_charset\_resolver=lambda r, b: ...*, *ssl\_shutdown\_timeout=0*)[[source]](_modules/aiohttp/client.html#ClientSession)[¶](#aiohttp.ClientSession "Link to this definition")
:   The class for creating client sessions and making requests.

    Parameters:
    :   * **base\_url** –

          Base part of the URL (optional)
          If set, allows to join a base part to relative URLs in request calls.
          If the URL has a path it must have a trailing `/` (as in
          <https://docs.aiohttp.org/en/stable/>).

          Note that URL joining follows [**RFC 3986**](https://datatracker.ietf.org/doc/html/rfc3986.html). This means, in the most
          common case the request URLs should have no leading slash, e.g.:

          ```
          session = ClientSession(base_url="http://example.com/foo/")

          await session.request("GET", "bar")
          # request for http://example.com/foo/bar

          await session.request("GET", "/bar")
          # request for http://example.com/bar
          ```

          Added in version 3.8.

          Changed in version 3.12: Added support for overriding the base URL with an absolute one in client sessions.
        * **connector** ([*aiohttp.BaseConnector*](#aiohttp.BaseConnector "aiohttp.BaseConnector")) – BaseConnector
          sub-class instance to support connection pooling.
        * **cookies** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")) – Cookies to send with the request (optional)
        * **headers** –

          HTTP Headers to send with every request (optional).

          May be either *iterable of key-value pairs* or
          [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)")
          (e.g. [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)"),
          [`CIMultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)")).
        * **skip\_auto\_headers** –

          set of headers for which autogeneration
          should be skipped.

          *aiohttp* autogenerates headers like `User-Agent` or
          `Content-Type` if these headers are not explicitly
          passed. Using `skip_auto_headers` parameter allows to skip
          that generation. Note that `Content-Length` autogeneration can’t
          be skipped.

          Iterable of [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`istr`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.istr "(in multidict v6.7)") (optional)
        * **auth** ([*aiohttp.BasicAuth*](#aiohttp.BasicAuth "aiohttp.BasicAuth")) – an object that represents HTTP Basic
          Authorization (optional). It will be included
          with any request. However, if the
          `_base_url` parameter is set, the request
          URL’s origin must match the base URL’s origin;
          otherwise, the default auth will not be
          included.
        * **json\_serialize** ([*collections.abc.Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) –

          Json *serializer* callable.

          By default [`json.dumps()`](https://docs.python.org/3/library/json.html#json.dumps "(in Python v3.14)") function.
        * **request\_class** ([*aiohttp.ClientRequest*](#aiohttp.ClientRequest "aiohttp.ClientRequest")) – Custom class to use for client requests.
        * **response\_class** ([*ClientResponse*](#aiohttp.ClientResponse "aiohttp.ClientResponse")) – Custom class to use for client responses.
        * **ws\_response\_class** ([*ClientWebSocketResponse*](#aiohttp.ClientWebSocketResponse "aiohttp.ClientWebSocketResponse")) – Custom class to use for websocket responses.
        * **version** – supported HTTP version, `HTTP 1.1` by default.
        * **cookie\_jar** –

          Cookie Jar, [`AbstractCookieJar`](abc.html#aiohttp.abc.AbstractCookieJar "aiohttp.abc.AbstractCookieJar") instance.

          By default every session instance has own private cookie jar for
          automatic cookies processing but user may redefine this behavior
          by providing own jar implementation.

          One example is not processing cookies at all when working in
          proxy mode.

          If no cookie processing is needed, a
          [`aiohttp.DummyCookieJar`](#aiohttp.DummyCookieJar "aiohttp.DummyCookieJar") instance can be
          provided.
        * **connector\_owner** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          Close connector instance on session closing.

          Setting the parameter to `False` allows to share
          connection pool between sessions without sharing session state:
          cookies etc.
        * **raise\_for\_status** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          Automatically call [`ClientResponse.raise_for_status()`](#aiohttp.ClientResponse.raise_for_status "aiohttp.ClientResponse.raise_for_status") for
          each response, `False` by default.

          This parameter can be overridden when making a request, e.g.:

          ```
          client_session = aiohttp.ClientSession(raise_for_status=True)
          resp = await client_session.get(url, raise_for_status=False)
          async with resp:
              assert resp.status == 200
          ```

          Set the parameter to `True` if you need `raise_for_status`
          for most of cases but override `raise_for_status` for those
          requests where you need to handle responses with status 400 or
          higher.

          You can also provide a coroutine which takes the response as an
          argument and can raise an exception based on custom logic, e.g.:

          ```
          async def custom_check(response):
              if response.status not in {201, 202}:
                  raise RuntimeError('expected either 201 or 202')
              text = await response.text()
              if 'apple pie' not in text:
                  raise RuntimeError('I wanted to see "apple pie" in response')

          client_session = aiohttp.ClientSession(raise_for_status=custom_check)
          ...
          ```

          As with boolean values, you’re free to set this on the session and/or
          overwrite it on a per-request basis.
        * **timeout** –

          a [`ClientTimeout`](#aiohttp.ClientTimeout "aiohttp.ClientTimeout") settings structure, 300 seconds (5min)
          :   total timeout, 30 seconds socket connect timeout by default.

          Added in version 3.3.

          Changed in version 3.10.9: The default value for the `sock_connect` timeout has been changed to 30 seconds.
        * **auto\_decompress** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          Automatically decompress response body (`True` by default).

          Added in version 2.3.
        * **trust\_env** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          Trust environment settings for proxy configuration if the parameter
          is `True` (`False` by default). See [Proxy support](client_advanced.html#aiohttp-client-proxy-support) for
          more information.

          Get proxy credentials from `~/.netrc` file if present.

          Get HTTP Basic Auth credentials from `~/.netrc` file if present.

          If [`NETRC`](glossary.html#envvar-NETRC) environment variable is set, read from file specified
          there rather than from `~/.netrc`.

          See also

          `.netrc` documentation: <https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html>

          Added in version 2.3.

          Changed in version 3.0: Added support for `~/.netrc` file.

          Changed in version 3.9: Added support for reading HTTP Basic Auth credentials from `~/.netrc` file.
        * **requote\_redirect\_url** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          Apply *URL requoting* for redirection URLs if
          :   automatic redirection is enabled (`True` by
              default).

          Added in version 3.5.
        * **trace\_configs** – A list of [`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") instances used for client
          tracing. `None` (default) is used for request tracing
          disabling. See [Tracing Reference](tracing_reference.html#aiohttp-client-tracing-reference) for
          more information.
        * **middlewares** –

          A sequence of middleware instances to apply to all session requests.
          :   Each middleware must match the [`ClientMiddlewareType`](#aiohttp.ClientMiddlewareType "aiohttp.ClientMiddlewareType") signature.
              `()` (empty tuple, default) is used when no middleware is needed.
              See [Client Middleware](client_advanced.html#aiohttp-client-middleware) for more information.

          Added in version 3.12.
        * **read\_bufsize** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          Size of the read buffer ([`ClientResponse.content`](#aiohttp.ClientResponse.content "aiohttp.ClientResponse.content")).
          :   64 KiB by default.

          Added in version 3.7.
        * **max\_line\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Maximum allowed size of lines in responses.
        * **max\_field\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Maximum allowed size of header fields in responses.
        * **fallback\_charset\_resolver** (*Callable**[**[*[*ClientResponse*](#aiohttp.ClientResponse "aiohttp.ClientResponse")*,*[*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")*]**,*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*]*) –

          A [callable](glossary.html#term-callable) that accepts a [`ClientResponse`](#aiohttp.ClientResponse "aiohttp.ClientResponse") and the
          [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") contents, and returns a [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") which will be used as
          the encoding parameter to [`bytes.decode()`](https://docs.python.org/3/library/stdtypes.html#bytes.decode "(in Python v3.14)").

          This function will be called when the charset is not known (e.g. not specified in the
          Content-Type header). The default function simply defaults to `utf-8`.

          Added in version 3.8.6.
        * **ssl\_shutdown\_timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) –

          **(DEPRECATED)** This parameter is deprecated
          and will be removed in aiohttp 4.0. Grace period for SSL shutdown handshake on
          TLS connections when the connector is closed (`0` seconds by default).
          By default (`0`), SSL connections are aborted immediately when the
          connector is closed, without performing the shutdown handshake. During
          normal operation, SSL connections use Python’s default SSL shutdown
          behavior. Setting this to a positive value (e.g., `0.1`) will perform
          a graceful shutdown when closing the connector, notifying the remote
          peer which can help prevent “connection reset” errors at the cost of
          additional cleanup time. This timeout is passed to the underlying
          [`TCPConnector`](#aiohttp.TCPConnector "aiohttp.TCPConnector") when one is created automatically.
          Note: On Python versions prior to 3.11, only a value of `0` is supported;
          other values will trigger a warning.

          Added in version 3.12.5.

          Changed in version 3.12.11: Changed default from `0.1` to `0` to abort SSL connections
          immediately when the connector is closed. Added support for
          `ssl_shutdown_timeout=0` on all Python versions. A [`RuntimeWarning`](https://docs.python.org/3/library/exceptions.html#RuntimeWarning "(in Python v3.14)")
          is issued when non-zero values are passed on Python < 3.11.

          Deprecated since version 3.12.11: This parameter is deprecated and will be removed in aiohttp 4.0.

    closed[¶](#aiohttp.ClientSession.closed "Link to this definition")
    :   `True` if the session has been closed, `False` otherwise.

        A read-only property.

    connector[¶](#aiohttp.ClientSession.connector "Link to this definition")
    :   [`aiohttp.BaseConnector`](#aiohttp.BaseConnector "aiohttp.BaseConnector") derived instance used
        for the session.

        A read-only property.

    cookie\_jar[¶](#aiohttp.ClientSession.cookie_jar "Link to this definition")
    :   The session cookies, [`AbstractCookieJar`](abc.html#aiohttp.abc.AbstractCookieJar "aiohttp.abc.AbstractCookieJar") instance.

        Gives access to cookie jar’s content and modifiers.

        A read-only property.

    requote\_redirect\_url[¶](#aiohttp.ClientSession.requote_redirect_url "Link to this definition")
    :   aiohttp re quote’s redirect urls by default, but some servers
        require exact url from location header. To disable *re-quote* system
        set [`requote_redirect_url`](#aiohttp.ClientSession.requote_redirect_url "aiohttp.ClientSession.requote_redirect_url") attribute to `False`.

        Added in version 2.1.

        Note

        This parameter affects all subsequent requests.

        Deprecated since version 3.5: The attribute modification is deprecated.

    loop[¶](#aiohttp.ClientSession.loop "Link to this definition")
    :   A loop instance used for session creation.

        A read-only property.

        Deprecated since version 3.5.

    timeout[¶](#aiohttp.ClientSession.timeout "Link to this definition")
    :   Default client timeouts, [`ClientTimeout`](#aiohttp.ClientTimeout "aiohttp.ClientTimeout") instance. The value can
        be tuned by passing *timeout* parameter to [`ClientSession`](#aiohttp.ClientSession "aiohttp.ClientSession")
        constructor.

        Added in version 3.7.

    headers[¶](#aiohttp.ClientSession.headers "Link to this definition")
    :   HTTP Headers that sent with every request

        May be either *iterable of key-value pairs* or
        [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)")
        (e.g. [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)"),
        [`CIMultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)")).

        Added in version 3.7.

    skip\_auto\_headers[¶](#aiohttp.ClientSession.skip_auto_headers "Link to this definition")
    :   Set of headers for which autogeneration skipped.

        [`frozenset`](https://docs.python.org/3/library/stdtypes.html#frozenset "(in Python v3.14)") of [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`istr`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.istr "(in multidict v6.7)") (optional)

        Added in version 3.7.

    auth[¶](#aiohttp.ClientSession.auth "Link to this definition")
    :   An object that represents HTTP Basic Authorization.

        [`BasicAuth`](#aiohttp.BasicAuth "aiohttp.BasicAuth") (optional)

        Added in version 3.7.

    json\_serialize[¶](#aiohttp.ClientSession.json_serialize "Link to this definition")
    :   Json serializer callable.

        By default [`json.dumps()`](https://docs.python.org/3/library/json.html#json.dumps "(in Python v3.14)") function.

        Added in version 3.7.

    connector\_owner[¶](#aiohttp.ClientSession.connector_owner "Link to this definition")
    :   Should connector be closed on session closing

        [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") (optional)

        Added in version 3.7.

    raise\_for\_status[¶](#aiohttp.ClientSession.raise_for_status "Link to this definition")
    :   Should [`ClientResponse.raise_for_status()`](#aiohttp.ClientResponse.raise_for_status "aiohttp.ClientResponse.raise_for_status") be called for each response

        Either [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") or [`collections.abc.Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")

        Added in version 3.7.

    auto\_decompress[¶](#aiohttp.ClientSession.auto_decompress "Link to this definition")
    :   Should the body response be automatically decompressed

        [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") default is `True`

        Added in version 3.7.

    trust\_env[¶](#aiohttp.ClientSession.trust_env "Link to this definition")
    :   Trust environment settings for proxy configuration
        or ~/.netrc file if present. See [Proxy support](client_advanced.html#aiohttp-client-proxy-support) for
        more information.

        [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") default is `False`

        Added in version 3.7.

    trace\_configs[¶](#aiohttp.ClientSession.trace_configs "Link to this definition")
    :   A list of [`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") instances used for client
        tracing. `None` (default) is used for request tracing
        disabling. See [Tracing Reference](tracing_reference.html#aiohttp-client-tracing-reference) for more information.

        Added in version 3.7.

    async request(*method*, *url*, *\**, *params=None*, *data=None*, *json=None*, *cookies=None*, *headers=None*, *skip\_auto\_headers=None*, *auth=None*, *allow\_redirects=True*, *max\_redirects=10*, *compress=None*, *chunked=None*, *expect100=False*, *raise\_for\_status=None*, *read\_until\_eof=True*, *proxy=None*, *proxy\_auth=None*, *timeout=sentinel*, *ssl=True*, *server\_hostname=None*, *proxy\_headers=None*, *trace\_request\_ctx=None*, *middlewares=None*, *read\_bufsize=None*, *auto\_decompress=None*, *max\_line\_size=None*, *max\_field\_size=None*)[[source]](_modules/aiohttp/client.html#ClientSession.request)[¶](#aiohttp.ClientSession.request "Link to this definition")
    :   Performs an asynchronous HTTP request. Returns a response object that
        should be used as an async context manager.

        Parameters:
        :   * **method** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – HTTP method
            * **url** – Request URL, [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") or [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") that will
              be encoded with [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") (see [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
              to skip encoding).
            * **params** –

              Mapping, iterable of tuple of *key*/*value* pairs or
              string to be sent as parameters in the query
              string of the new request. Ignored for subsequent
              redirected requests (optional)

              Allowed values are:

              + [`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") e.g. [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)"),
                [`multidict.MultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDict "(in multidict v6.7)") or
                [`multidict.MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)")
              + [`collections.abc.Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)") e.g. [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") or
                [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")
              + [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") with preferably url-encoded content
                (**Warning:** content will not be encoded by *aiohttp*)
            * **data** – The data to send in the body of the request. This can be a
              [`FormData`](#aiohttp.FormData "aiohttp.FormData") object or anything that can be passed into
              [`FormData`](#aiohttp.FormData "aiohttp.FormData"), e.g. a dictionary, bytes, or file-like object.
              (optional)
            * **json** – Any json compatible python object
              (optional). *json* and *data* parameters could not
              be used at the same time.
            * **cookies** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")) –

              HTTP Cookies to send with
              :   the request (optional)

              Global session cookies and the explicitly set cookies will be merged
              when sending the request.

              Added in version 3.5.
            * **headers** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")) – HTTP Headers to send with
              the request (optional)
            * **skip\_auto\_headers** –

              set of headers for which autogeneration
              should be skipped.

              *aiohttp* autogenerates headers like `User-Agent` or
              `Content-Type` if these headers are not explicitly
              passed. Using `skip_auto_headers` parameter allows to skip
              that generation.

              Iterable of [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`istr`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.istr "(in multidict v6.7)")
              (optional)
            * **auth** ([*aiohttp.BasicAuth*](#aiohttp.BasicAuth "aiohttp.BasicAuth")) – an object that represents HTTP
              Basic Authorization (optional)
            * **allow\_redirects** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Whether to process redirects or not.
              When `True`, redirects are followed (up to `max_redirects` times)
              and logged into [`ClientResponse.history`](#aiohttp.ClientResponse.history "aiohttp.ClientResponse.history") and `trace_configs`.
              When `False`, the original response is returned.
              `True` by default (optional).
            * **max\_redirects** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Maximum number of redirects to follow.
              [`TooManyRedirects`](#aiohttp.TooManyRedirects "aiohttp.TooManyRedirects") is raised if the number is exceeded.
              Ignored when `allow_redirects=False`.
              `10` by default.
            * **compress** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Set to `True` if request has to be compressed
              with deflate encoding. If compress can not be combined
              with a *Content-Encoding* and *Content-Length* headers.
              `None` by default (optional).
            * **chunked** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Enable chunked transfer encoding.
              It is up to the developer
              to decide how to chunk data streams. If chunking is enabled, aiohttp
              encodes the provided chunks in the “Transfer-encoding: chunked” format.
              If *chunked* is set, then the *Transfer-encoding* and *content-length*
              headers are disallowed. `None` by default (optional).
            * **expect100** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Expect 100-continue response from server.
              `False` by default (optional).
            * **raise\_for\_status** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

              Automatically call [`ClientResponse.raise_for_status()`](#aiohttp.ClientResponse.raise_for_status "aiohttp.ClientResponse.raise_for_status") for
              :   response if set to `True`.
                  If set to `None` value from `ClientSession` will be used.
                  `None` by default (optional).

              Added in version 3.4.
            * **read\_until\_eof** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Read response until EOF if response
              does not have Content-Length header.
              `True` by default (optional).
            * **proxy** – Proxy URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") (optional)
            * **proxy\_auth** ([*aiohttp.BasicAuth*](#aiohttp.BasicAuth "aiohttp.BasicAuth")) – an object that represents proxy HTTP
              Basic Authorization (optional)
            * **timeout** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

              override the session’s timeout.

              Changed in version 3.3: The parameter is [`ClientTimeout`](#aiohttp.ClientTimeout "aiohttp.ClientTimeout") instance,
              [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)") is still supported for sake of backward
              compatibility.

              If [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)") is passed it is a *total* timeout (in seconds).
            * **ssl** –

              SSL validation mode. `True` for default SSL check
              :   ([`ssl.create_default_context()`](https://docs.python.org/3/library/ssl.html#ssl.create_default_context "(in Python v3.14)") is used),
                  `False` for skip SSL certificate validation,
                  [`aiohttp.Fingerprint`](#aiohttp.Fingerprint "aiohttp.Fingerprint") for fingerprint
                  validation, [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") for custom SSL
                  certificate validation.

                  Supersedes *verify\_ssl*, *ssl\_context* and
                  *fingerprint* parameters.

              Added in version 3.0.
            * **server\_hostname** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

              Sets or overrides the host name that the
              target server’s certificate will be matched against.

              See [`asyncio.loop.create_connection()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_connection "(in Python v3.14)") for more information.

              Added in version 3.9.
            * **proxy\_headers** ([*collections.abc.Mapping*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)")) –

              HTTP headers to send to the proxy if the
              parameter proxy has been provided.

              Added in version 2.3.
            * **trace\_request\_ctx** –

              Object used to give as a kw param for each new
              [`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") object instantiated,
              used to give information to the
              tracers that is only available at request time.

              > Added in version 3.0.
            * **middlewares** –

              A sequence of middleware instances to apply to this request only.
              :   Each middleware must match the [`ClientMiddlewareType`](#aiohttp.ClientMiddlewareType "aiohttp.ClientMiddlewareType") signature.
                  `None` by default which uses session middlewares.
                  See [Client Middleware](client_advanced.html#aiohttp-client-middleware) for more information.

              Added in version 3.12.
            * **read\_bufsize** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

              Size of the read buffer ([`ClientResponse.content`](#aiohttp.ClientResponse.content "aiohttp.ClientResponse.content")).
              :   `None` by default,
                  it means that the session global value is used.

              Added in version 3.7.
            * **auto\_decompress** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Automatically decompress response body.
              Overrides [`ClientSession.auto_decompress`](#aiohttp.ClientSession.auto_decompress "aiohttp.ClientSession.auto_decompress").
              May be used to enable/disable auto decompression on a per-request basis.
            * **max\_line\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Maximum allowed size of lines in responses.
            * **max\_field\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Maximum allowed size of header fields in responses.

        Return ClientResponse:
        :   a [`client response`](#aiohttp.ClientResponse "aiohttp.ClientResponse")
            object.

    async get(*url*, *\**, *allow\_redirects=True*, *\*\*kwargs*)[[source]](_modules/aiohttp/client.html#ClientSession.get)[¶](#aiohttp.ClientSession.get "Link to this definition")
    :   Perform a `GET` request. Returns an async context manager.

        In order to modify inner
        [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
        parameters, provide kwargs.

        Parameters:
        :   * **url** – Request URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
            * **allow\_redirects** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Whether to process redirects or not.
              When `True`, redirects are followed and logged into
              [`ClientResponse.history`](#aiohttp.ClientResponse.history "aiohttp.ClientResponse.history").
              When `False`, the original response is returned.
              `True` by default (optional).

        Return ClientResponse:
        :   a [`client response`](#aiohttp.ClientResponse "aiohttp.ClientResponse") object.

    async post(*url*, *\**, *data=None*, *\*\*kwargs*)[[source]](_modules/aiohttp/client.html#ClientSession.post)[¶](#aiohttp.ClientSession.post "Link to this definition")
    :   Perform a `POST` request. Returns an async context manager.

        In order to modify inner
        [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
        parameters, provide kwargs.

        Parameters:
        :   * **url** – Request URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
            * **data** – Data to send in the body of the request; see
              [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
              for details (optional)

        Return ClientResponse:
        :   a [`client response`](#aiohttp.ClientResponse "aiohttp.ClientResponse") object.

    async put(*url*, *\**, *data=None*, *\*\*kwargs*)[[source]](_modules/aiohttp/client.html#ClientSession.put)[¶](#aiohttp.ClientSession.put "Link to this definition")
    :   Perform a `PUT` request. Returns an async context manager.

        In order to modify inner
        [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
        parameters, provide kwargs.

        Parameters:
        :   * **url** – Request URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
            * **data** – Data to send in the body of the request; see
              [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
              for details (optional)

        Return ClientResponse:
        :   a [`client response`](#aiohttp.ClientResponse "aiohttp.ClientResponse") object.

    async delete(*url*, *\*\*kwargs*)[[source]](_modules/aiohttp/client.html#ClientSession.delete)[¶](#aiohttp.ClientSession.delete "Link to this definition")
    :   Perform a `DELETE` request. Returns an async context manager.

        In order to modify inner
        [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
        parameters, provide kwargs.

        Parameters:
        :   **url** – Request URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")

        Return ClientResponse:
        :   a [`client response`](#aiohttp.ClientResponse "aiohttp.ClientResponse") object.

    async head(*url*, *\**, *allow\_redirects=False*, *\*\*kwargs*)[[source]](_modules/aiohttp/client.html#ClientSession.head)[¶](#aiohttp.ClientSession.head "Link to this definition")
    :   Perform a `HEAD` request. Returns an async context manager.

        In order to modify inner
        [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
        parameters, provide kwargs.

        Parameters:
        :   * **url** – Request URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
            * **allow\_redirects** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Whether to process redirects or not.
              When `True`, redirects are followed and logged into
              [`ClientResponse.history`](#aiohttp.ClientResponse.history "aiohttp.ClientResponse.history").
              When `False`, the original response is returned.
              `False` by default (optional).

        Return ClientResponse:
        :   a [`client response`](#aiohttp.ClientResponse "aiohttp.ClientResponse") object.

    async options(*url*, *\**, *allow\_redirects=True*, *\*\*kwargs*)[[source]](_modules/aiohttp/client.html#ClientSession.options)[¶](#aiohttp.ClientSession.options "Link to this definition")
    :   Perform an `OPTIONS` request. Returns an async context manager.

        In order to modify inner
        [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
        parameters, provide kwargs.

        Parameters:
        :   * **url** – Request URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
            * **allow\_redirects** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Whether to process redirects or not.
              When `True`, redirects are followed and logged into
              [`ClientResponse.history`](#aiohttp.ClientResponse.history "aiohttp.ClientResponse.history").
              When `False`, the original response is returned.
              `True` by default (optional).

        Return ClientResponse:
        :   a [`client response`](#aiohttp.ClientResponse "aiohttp.ClientResponse") object.

    async patch(*url*, *\**, *data=None*, *\*\*kwargs*)[[source]](_modules/aiohttp/client.html#ClientSession.patch)[¶](#aiohttp.ClientSession.patch "Link to this definition")
    :   Perform a `PATCH` request. Returns an async context manager.

        In order to modify inner
        [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
        parameters, provide kwargs.

        Parameters:
        :   * **url** – Request URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
            * **data** – Data to send in the body of the request; see
              [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request")
              for details (optional)

        Return ClientResponse:
        :   a [`client response`](#aiohttp.ClientResponse "aiohttp.ClientResponse") object.

    async ws\_connect(*url*, *\**, *method='GET'*, *protocols=()*, *timeout=sentinel*, *auth=None*, *autoclose=True*, *autoping=True*, *heartbeat=None*, *origin=None*, *params=None*, *headers=None*, *proxy=None*, *proxy\_auth=None*, *ssl=True*, *verify\_ssl=None*, *fingerprint=None*, *ssl\_context=None*, *proxy\_headers=None*, *compress=0*, *max\_msg\_size=4194304*)[[source]](_modules/aiohttp/client.html#ClientSession.ws_connect)[¶](#aiohttp.ClientSession.ws_connect "Link to this definition")
    :   Create a websocket connection. Returns a
        [`ClientWebSocketResponse`](#aiohttp.ClientWebSocketResponse "aiohttp.ClientWebSocketResponse") async context manager object.

        Parameters:
        :   * **url** – Websocket server url, [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") or [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") that
              will be encoded with [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") (see [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
              to skip encoding).
            * **protocols** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")) – Websocket protocols
            * **timeout** – a [`ClientWSTimeout`](#aiohttp.ClientWSTimeout "aiohttp.ClientWSTimeout") timeout for websocket.
              By default, the value
              ClientWSTimeout(ws\_receive=None, ws\_close=10.0) is used
              (`10.0` seconds for the websocket to close).
              `None` means no timeout will be used.
            * **auth** ([*aiohttp.BasicAuth*](#aiohttp.BasicAuth "aiohttp.BasicAuth")) – an object that represents HTTP
              Basic Authorization (optional)
            * **autoclose** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Automatically close websocket connection on close
              message from server. If *autoclose* is False
              then close procedure has to be handled manually.
              `True` by default
            * **autoping** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – automatically send *pong* on *ping*
              message from server. `True` by default
            * **heartbeat** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Send *ping* message every *heartbeat*
              seconds and wait *pong* response, if
              *pong* response is not received then
              close connection. The timer is reset on any data
              reception.(optional)
            * **origin** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Origin header to send to server(optional)
            * **params** –

              Mapping, iterable of tuple of *key*/*value* pairs or
              string to be sent as parameters in the query
              string of the new request. Ignored for subsequent
              redirected requests (optional)

              Allowed values are:

              + [`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") e.g. [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)"),
                [`multidict.MultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDict "(in multidict v6.7)") or
                [`multidict.MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)")
              + [`collections.abc.Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)") e.g. [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") or
                [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")
              + [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") with preferably url-encoded content
                (**Warning:** content will not be encoded by *aiohttp*)
            * **headers** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")) – HTTP Headers to send with
              the request (optional)
            * **proxy** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Proxy URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") (optional)
            * **proxy\_auth** ([*aiohttp.BasicAuth*](#aiohttp.BasicAuth "aiohttp.BasicAuth")) – an object that represents proxy HTTP
              Basic Authorization (optional)
            * **ssl** –

              SSL validation mode. `True` for default SSL check
              :   ([`ssl.create_default_context()`](https://docs.python.org/3/library/ssl.html#ssl.create_default_context "(in Python v3.14)") is used),
                  `False` for skip SSL certificate validation,
                  [`aiohttp.Fingerprint`](#aiohttp.Fingerprint "aiohttp.Fingerprint") for fingerprint
                  validation, [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") for custom SSL
                  certificate validation.

                  Supersedes *verify\_ssl*, *ssl\_context* and
                  *fingerprint* parameters.

              Added in version 3.0.
            * **verify\_ssl** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

              Perform SSL certificate validation for
              *HTTPS* requests (enabled by default). May be disabled to
              skip validation for sites with invalid certificates.

              Added in version 2.3.

              Deprecated since version 3.0: Use `ssl=False`
            * **fingerprint** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")) –

              Pass the SHA256 digest of the expected
              certificate in DER format to verify that the certificate the
              server presents matches. Useful for [certificate pinning](https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning).

              Note: use of MD5 or SHA1 digests is insecure and deprecated.

              Added in version 2.3.

              Deprecated since version 3.0: Use `ssl=aiohttp.Fingerprint(digest)`
            * **ssl\_context** ([*ssl.SSLContext*](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)")) –

              ssl context used for processing
              *HTTPS* requests (optional).

              *ssl\_context* may be used for configuring certification
              authority channel, supported SSL options etc.

              Added in version 2.3.

              Deprecated since version 3.0: Use `ssl=ssl_context`
            * **proxy\_headers** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")) –

              HTTP headers to send to the proxy if the
              parameter proxy has been provided.

              Added in version 2.3.
            * **compress** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

              Enable Per-Message Compress Extension support.
              :   0 for disable, 9 to 15 for window bit support.
                  Default value is 0.

              Added in version 2.3.
            * **max\_msg\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

              maximum size of read websocket message,
              :   4 MB by default. To disable the size
                  limit use `0`.

              Added in version 3.3.
            * **method** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

              HTTP method to establish WebSocket connection,
              :   `'GET'` by default.

              Added in version 3.5.

    async close()[[source]](_modules/aiohttp/client.html#ClientSession.close)[¶](#aiohttp.ClientSession.close "Link to this definition")
    :   Close underlying connector.

        Release all acquired resources.

    detach()[[source]](_modules/aiohttp/client.html#ClientSession.detach)[¶](#aiohttp.ClientSession.detach "Link to this definition")
    :   Detach connector from session without closing the former.

        Session is switched to closed state anyway.

## Basic API[¶](#basic-api "Link to this heading")

While we encourage [`ClientSession`](#aiohttp.ClientSession "aiohttp.ClientSession") usage we also provide simple
coroutines for making HTTP requests.

Basic API is good for performing simple HTTP requests without
keepaliving, cookies and complex connection stuff like properly configured SSL
certification chaining.

async aiohttp.request(*method*, *url*, *\**, *params=None*, *data=None*, *json=None*, *cookies=None*, *headers=None*, *skip\_auto\_headers=None*, *auth=None*, *allow\_redirects=True*, *max\_redirects=10*, *compress=False*, *chunked=None*, *expect100=False*, *raise\_for\_status=None*, *read\_until\_eof=True*, *proxy=None*, *proxy\_auth=None*, *timeout=sentinel*, *ssl=True*, *server\_hostname=None*, *proxy\_headers=None*, *trace\_request\_ctx=None*, *read\_bufsize=None*, *auto\_decompress=None*, *max\_line\_size=None*, *max\_field\_size=None*, *version=aiohttp.HttpVersion11*, *connector=None*)[[source]](_modules/aiohttp/client.html#request)[¶](#aiohttp.request "Link to this definition")
:   Asynchronous context manager for performing an asynchronous HTTP
    request. Returns a [`ClientResponse`](#aiohttp.ClientResponse "aiohttp.ClientResponse") response object. Use as
    an async context manager.

    Parameters:
    :   * **method** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – HTTP method
        * **url** – Request URL, [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") or [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") that will
          be encoded with [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") (see [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
          to skip encoding).
        * **params** –

          Mapping, iterable of tuple of *key*/*value* pairs or
          string to be sent as parameters in the query
          string of the new request. Ignored for subsequent
          redirected requests (optional)

          Allowed values are:

          + [`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") e.g. [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)"),
            :   [`multidict.MultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDict "(in multidict v6.7)") or
                [`multidict.MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)")
          + [`collections.abc.Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)") e.g. [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") or
            :   [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")
          + [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") with preferably url-encoded content
            :   (**Warning:** content will not be encoded by *aiohttp*)
        * **data** – The data to send in the body of the request. This can be a
          [`FormData`](#aiohttp.FormData "aiohttp.FormData") object or anything that can be passed into
          [`FormData`](#aiohttp.FormData "aiohttp.FormData"), e.g. a dictionary, bytes, or file-like object.
          (optional)
        * **json** – Any json compatible python object (optional). *json* and *data*
          parameters could not be used at the same time.
        * **cookies** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")) – HTTP Cookies to send with the request (optional)
        * **headers** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")) – HTTP Headers to send with the request (optional)
        * **skip\_auto\_headers** –

          set of headers for which autogeneration
          should be skipped.

          *aiohttp* autogenerates headers like `User-Agent` or
          `Content-Type` if these headers are not explicitly
          passed. Using `skip_auto_headers` parameter allows to skip
          that generation.

          Iterable of [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`istr`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.istr "(in multidict v6.7)")
          (optional)
        * **auth** ([*aiohttp.BasicAuth*](#aiohttp.BasicAuth "aiohttp.BasicAuth")) – an object that represents HTTP Basic
          Authorization (optional)
        * **allow\_redirects** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Whether to process redirects or not.
          When `True`, redirects are followed (up to `max_redirects` times)
          and logged into [`ClientResponse.history`](#aiohttp.ClientResponse.history "aiohttp.ClientResponse.history") and `trace_configs`.
          When `False`, the original response is returned.
          `True` by default (optional).
        * **max\_redirects** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Maximum number of redirects to follow.
          [`TooManyRedirects`](#aiohttp.TooManyRedirects "aiohttp.TooManyRedirects") is raised if the number is exceeded.
          Ignored when `allow_redirects=False`.
          `10` by default.
        * **compress** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Set to `True` if request has to be compressed
          with deflate encoding. If compress can not be combined
          with a *Content-Encoding* and *Content-Length* headers.
          `None` by default (optional).
        * **chunked** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Enables chunked transfer encoding.
          It is up to the developer
          to decide how to chunk data streams. If chunking is enabled, aiohttp
          encodes the provided chunks in the “Transfer-encoding: chunked” format.
          If *chunked* is set, then the *Transfer-encoding* and *content-length*
          headers are disallowed. `None` by default (optional).
        * **expect100** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Expect 100-continue response from server.
          `False` by default (optional).
        * **raise\_for\_status** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          Automatically call
          :   [`ClientResponse.raise_for_status()`](#aiohttp.ClientResponse.raise_for_status "aiohttp.ClientResponse.raise_for_status")
              for response if set to `True`. If
              set to `None` value from
              `ClientSession` will be used.
              `None` by default (optional).

          Added in version 3.4.
        * **read\_until\_eof** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Read response until EOF if response
          does not have Content-Length header.
          `True` by default (optional).
        * **proxy** – Proxy URL, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") (optional)
        * **proxy\_auth** ([*aiohttp.BasicAuth*](#aiohttp.BasicAuth "aiohttp.BasicAuth")) – an object that represents proxy HTTP
          Basic Authorization (optional)
        * **timeout** – a [`ClientTimeout`](#aiohttp.ClientTimeout "aiohttp.ClientTimeout") settings structure, 300 seconds (5min)
          total timeout, 30 seconds socket connect timeout by default.
        * **ssl** –

          SSL validation mode. `True` for default SSL check
          ([`ssl.create_default_context()`](https://docs.python.org/3/library/ssl.html#ssl.create_default_context "(in Python v3.14)") is used),
          `False` for skip SSL certificate validation,
          [`aiohttp.Fingerprint`](#aiohttp.Fingerprint "aiohttp.Fingerprint") for fingerprint
          validation, [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") for custom SSL
          certificate validation.

          Supersedes *verify\_ssl*, *ssl\_context* and
          *fingerprint* parameters.
        * **server\_hostname** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

          Sets or overrides the host name that the
          target server’s certificate will be matched against.

          See [`asyncio.loop.create_connection()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_connection "(in Python v3.14)")
          for more information.
        * **proxy\_headers** ([*collections.abc.Mapping*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)")) – HTTP headers to send to the proxy
          if the parameter proxy has been provided.
        * **trace\_request\_ctx** – Object used to give as a kw param for each new
          [`TraceConfig`](tracing_reference.html#aiohttp.TraceConfig "aiohttp.TraceConfig") object instantiated,
          used to give information to the
          tracers that is only available at request time.
        * **read\_bufsize** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          Size of the read buffer ([`ClientResponse.content`](#aiohttp.ClientResponse.content "aiohttp.ClientResponse.content")).
          :   `None` by default,
              it means that the session global value is used.

          Added in version 3.7.
        * **auto\_decompress** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Automatically decompress response body.
          May be used to enable/disable auto decompression on a per-request basis.
        * **max\_line\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Maximum allowed size of lines in responses.
        * **max\_field\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Maximum allowed size of header fields in responses.
        * **version** (*aiohttp.protocol.HttpVersion*) – Request HTTP version,
          `HTTP 1.1` by default. (optional)
        * **connector** ([*aiohttp.BaseConnector*](#aiohttp.BaseConnector "aiohttp.BaseConnector")) – BaseConnector sub-class
          instance to support connection pooling. (optional)

    Return ClientResponse:
    :   a [`client response`](#aiohttp.ClientResponse "aiohttp.ClientResponse") object.

    Usage:

    ```
    import aiohttp

    async def fetch():
        async with aiohttp.request('GET',
                'http://python.org/') as resp:
            assert resp.status == 200
            print(await resp.text())
    ```

## Connectors[¶](#connectors "Link to this heading")

Connectors are transports for aiohttp client API.

There are standard connectors:

1. [`TCPConnector`](#aiohttp.TCPConnector "aiohttp.TCPConnector") for regular *TCP sockets* (both *HTTP* and
   *HTTPS* schemes supported).
2. [`UnixConnector`](#aiohttp.UnixConnector "aiohttp.UnixConnector") for connecting via UNIX socket (it’s used mostly for
   testing purposes).

All connector classes should be derived from [`BaseConnector`](#aiohttp.BaseConnector "aiohttp.BaseConnector").

By default all *connectors* support *keep-alive connections* (behavior
is controlled by *force\_close* constructor’s parameter).

class aiohttp.BaseConnector(*\**, *keepalive\_timeout=15*, *force\_close=False*, *limit=100*, *limit\_per\_host=0*, *enable\_cleanup\_closed=False*, *loop=None*)[[source]](_modules/aiohttp/connector.html#BaseConnector)[¶](#aiohttp.BaseConnector "Link to this definition")
:   Base class for all connectors.

    Parameters:
    :   * **keepalive\_timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – timeout for connection reusing
          after releasing (optional). Values
          `0`. For disabling *keep-alive*
          feature use `force_close=True`
          flag.
        * **limit** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – total number simultaneous connections. If *limit* is
          `0` the connector has no limit (default: 100).
        * **limit\_per\_host** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – limit simultaneous connections to the same
          endpoint. Endpoints are the same if they are
          have equal `(host, port, is_ssl)` triple.
          If *limit* is `0` the connector has no limit (default: 0).
        * **force\_close** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – close underlying sockets after
          connection releasing (optional).
        * **enable\_cleanup\_closed** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          some SSL servers do not properly complete
          SSL shutdown process, in that case asyncio leaks SSL connections.
          If this parameter is set to True, aiohttp additionally aborts underlining
          transport after 2 seconds. It is off by default.

          For Python version 3.12.7+, or 3.13.1 and later,
          this parameter is ignored because the asyncio SSL connection
          leak is fixed in these versions of Python.
        * **loop** –

          [event loop](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio-event-loop "(in Python v3.14)")
          used for handling connections.
          If param is `None`, [`asyncio.get_event_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_event_loop "(in Python v3.14)")
          is used for getting default event loop.

          Deprecated since version 2.0.

    closed[¶](#aiohttp.BaseConnector.closed "Link to this definition")
    :   Read-only property, `True` if connector is closed.

    force\_close[¶](#aiohttp.BaseConnector.force_close "Link to this definition")
    :   Read-only property, `True` if connector should ultimately
        close connections on releasing.

    limit[¶](#aiohttp.BaseConnector.limit "Link to this definition")
    :   The total number for simultaneous connections.
        If limit is 0 the connector has no limit. The default limit size is 100.

    limit\_per\_host[¶](#aiohttp.BaseConnector.limit_per_host "Link to this definition")
    :   The limit for simultaneous connections to the same
        endpoint.

        Endpoints are the same if they are have equal `(host, port,
        is_ssl)` triple.

        If *limit\_per\_host* is `0` the connector has no limit per host.

        Read-only property.

    async close()[[source]](_modules/aiohttp/connector.html#BaseConnector.close)[¶](#aiohttp.BaseConnector.close "Link to this definition")
    :   Close all opened connections.

    async connect(*request*)[[source]](_modules/aiohttp/connector.html#BaseConnector.connect)[¶](#aiohttp.BaseConnector.connect "Link to this definition")
    :   Get a free connection from pool or create new one if connection
        is absent in the pool.

        The call may be paused if [`limit`](#aiohttp.BaseConnector.limit "aiohttp.BaseConnector.limit") is exhausted until used
        connections returns to pool.

        Parameters:
        :   **request** ([*aiohttp.ClientRequest*](#aiohttp.ClientRequest "aiohttp.ClientRequest")) – request object
            which is connection
            initiator.

        Returns:
        :   [`Connection`](#aiohttp.Connection "aiohttp.Connection") object.

    async \_create\_connection(*req*)[[source]](_modules/aiohttp/connector.html#BaseConnector._create_connection)[¶](#aiohttp.BaseConnector._create_connection "Link to this definition")
    :   Abstract method for actual connection establishing, should be
        overridden in subclasses.

class aiohttp.AddrInfoType[¶](#aiohttp.AddrInfoType "Link to this definition")
:   Refer to [`aiohappyeyeballs.AddrInfoType`](https://aiohappyeyeballs.aio-libs.org/en/latest/api_reference.html#aiohappyeyeballs.AddrInfoType "(in aiohappyeyeballs)") for more info.

Warning

Be sure to use `aiohttp.AddrInfoType` rather than
`aiohappyeyeballs.AddrInfoType` to avoid import breakage, as
it is likely to be removed from [`aiohappyeyeballs`](https://aiohappyeyeballs.aio-libs.org/en/latest/api_reference.html#module-aiohappyeyeballs "(in aiohappyeyeballs)") in the
future.

class aiohttp.SocketFactoryType[¶](#aiohttp.SocketFactoryType "Link to this definition")
:   Refer to [`aiohappyeyeballs.SocketFactoryType`](https://aiohappyeyeballs.aio-libs.org/en/latest/api_reference.html#aiohappyeyeballs.SocketFactoryType "(in aiohappyeyeballs)") for more info.

Warning

Be sure to use `aiohttp.SocketFactoryType` rather than
`aiohappyeyeballs.SocketFactoryType` to avoid import breakage,
as it is likely to be removed from [`aiohappyeyeballs`](https://aiohappyeyeballs.aio-libs.org/en/latest/api_reference.html#module-aiohappyeyeballs "(in aiohappyeyeballs)") in the
future.

class aiohttp.TCPConnector(*\**, *ssl=True*, *verify\_ssl=True*, *fingerprint=None*, *use\_dns\_cache=True*, *ttl\_dns\_cache=10*, *family=0*, *ssl\_context=None*, *local\_addr=None*, *resolver=None*, *keepalive\_timeout=sentinel*, *force\_close=False*, *limit=100*, *limit\_per\_host=0*, *enable\_cleanup\_closed=False*, *timeout\_ceil\_threshold=5*, *happy\_eyeballs\_delay=0.25*, *interleave=None*, *loop=None*, *socket\_factory=None*, *ssl\_shutdown\_timeout=0*)[[source]](_modules/aiohttp/connector.html#TCPConnector)[¶](#aiohttp.TCPConnector "Link to this definition")
:   Connector for working with *HTTP* and *HTTPS* via *TCP* sockets.

    The most common transport. When you don’t know what connector type
    to use, use a [`TCPConnector`](#aiohttp.TCPConnector "aiohttp.TCPConnector") instance.

    [`TCPConnector`](#aiohttp.TCPConnector "aiohttp.TCPConnector") inherits from [`BaseConnector`](#aiohttp.BaseConnector "aiohttp.BaseConnector").

    Constructor accepts all parameters suitable for
    [`BaseConnector`](#aiohttp.BaseConnector "aiohttp.BaseConnector") plus several TCP-specific ones:

    > param ssl:
    > :   SSL validation mode. `True` for default SSL check
    >     :   ([`ssl.create_default_context()`](https://docs.python.org/3/library/ssl.html#ssl.create_default_context "(in Python v3.14)") is used),
    >         `False` for skip SSL certificate validation,
    >         [`aiohttp.Fingerprint`](#aiohttp.Fingerprint "aiohttp.Fingerprint") for fingerprint
    >         validation, [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") for custom SSL
    >         certificate validation.
    >
    >         Supersedes *verify\_ssl*, *ssl\_context* and
    >         *fingerprint* parameters.
    >
    >     Added in version 3.0.

    Parameters:
    :   * **verify\_ssl** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          perform SSL certificate validation for
          *HTTPS* requests (enabled by default). May be disabled to
          skip validation for sites with invalid certificates.

          Deprecated since version 2.3: Pass *verify\_ssl* to `ClientSession.get()` etc.
        * **fingerprint** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")) –

          pass the SHA256 digest of the expected
          certificate in DER format to verify that the certificate the
          server presents matches. Useful for [certificate pinning](https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning).

          Note: use of MD5 or SHA1 digests is insecure and deprecated.

          Deprecated since version 2.3: Pass *verify\_ssl* to `ClientSession.get()` etc.
        * **use\_dns\_cache** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          use internal cache for DNS lookups, `True`
          by default.

          Enabling an option *may* speedup connection
          establishing a bit but may introduce some
          *side effects* also.
        * **ttl\_dns\_cache** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          expire after some seconds the DNS entries, `None`
          means cached forever. By default 10 seconds (optional).

          In some environments the IP addresses related to a specific HOST can
          change after a specific time. Use this option to keep the DNS cache
          updated refreshing each entry after N seconds.
        * **limit** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – total number simultaneous connections. If *limit* is
          `0` the connector has no limit (default: 100).
        * **limit\_per\_host** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – limit simultaneous connections to the same
          endpoint. Endpoints are the same if they are
          have equal `(host, port, is_ssl)` triple.
          If *limit* is `0` the connector has no limit (default: 0).
        * **resolver** ([*aiohttp.abc.AbstractResolver*](abc.html#aiohttp.abc.AbstractResolver "aiohttp.abc.AbstractResolver")) –

          custom resolver
          instance to use. `aiohttp.DefaultResolver` by
          default (asynchronous if `aiodns>=1.1` is installed).

          Custom resolvers allow to resolve hostnames differently than the
          way the host is configured.

          The resolver is `aiohttp.ThreadedResolver` by default,
          asynchronous version is pretty robust but might fail in
          very rare cases.
        * **family** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          TCP socket family, both IPv4 and IPv6 by default.
          For *IPv4* only use [`socket.AF_INET`](https://docs.python.org/3/library/socket.html#socket.AF_INET "(in Python v3.14)"),
          for *IPv6* only – [`socket.AF_INET6`](https://docs.python.org/3/library/socket.html#socket.AF_INET6 "(in Python v3.14)").

          *family* is `0` by default, that means both
          IPv4 and IPv6 are accepted. To specify only
          concrete version please pass
          [`socket.AF_INET`](https://docs.python.org/3/library/socket.html#socket.AF_INET "(in Python v3.14)") or
          [`socket.AF_INET6`](https://docs.python.org/3/library/socket.html#socket.AF_INET6 "(in Python v3.14)") explicitly.
        * **ssl\_context** ([*ssl.SSLContext*](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)")) –

          SSL context used for processing
          *HTTPS* requests (optional).

          *ssl\_context* may be used for configuring certification
          authority channel, supported SSL options etc.
        * **local\_addr** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")) – tuple of `(local_host, local_port)` used to bind
          socket locally if specified.
        * **force\_close** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – close underlying sockets after
          connection releasing (optional).
        * **enable\_cleanup\_closed** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Some ssl servers do not properly complete
          SSL shutdown process, in that case asyncio leaks SSL connections.
          If this parameter is set to True, aiohttp additionally aborts underlining
          transport after 2 seconds. It is off by default.
        * **happy\_eyeballs\_delay** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) –

          The amount of time in seconds to wait for a
          connection attempt to complete, before starting the next attempt in parallel.
          This is the “Connection Attempt Delay” as defined in RFC 8305. To disable
          Happy Eyeballs, set this to `None`. The default value recommended by the
          RFC is 0.25 (250 milliseconds).

          > Added in version 3.10.
        * **interleave** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          controls address reordering when a host name resolves
          to multiple IP addresses. If `0` or unspecified, no reordering is done, and
          addresses are tried in the order returned by the resolver. If a positive
          integer is specified, the addresses are interleaved by address family, and
          the given integer is interpreted as “First Address Family Count” as defined
          in RFC 8305. The default is `0` if happy\_eyeballs\_delay is not specified, and
          `1` if it is.

          > Added in version 3.10.
        * **socket\_factory** ([*SocketFactoryType*](#aiohttp.SocketFactoryType "aiohttp.SocketFactoryType")) –

          This function takes an
          [`AddrInfoType`](#aiohttp.AddrInfoType "aiohttp.AddrInfoType") and is used in lieu of
          `socket.socket()` when creating TCP connections.

          > Added in version 3.12.
        * **ssl\_shutdown\_timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) –

          **(DEPRECATED)** This parameter is deprecated
          and will be removed in aiohttp 4.0. Grace period for SSL shutdown on TLS
          connections when the connector is closed (`0` seconds by default).
          By default (`0`), SSL connections are aborted immediately when the
          connector is closed, without performing the shutdown handshake. During
          normal operation, SSL connections use Python’s default SSL shutdown
          behavior. Setting this to a positive value (e.g., `0.1`) will perform
          a graceful shutdown when closing the connector, notifying the remote
          server which can help prevent “connection reset” errors at the cost of
          additional cleanup time. Note: On Python versions prior to 3.11, only
          a value of `0` is supported; other values will trigger a warning.

          > Added in version 3.12.5.
          >
          > Changed in version 3.12.11: Changed default from `0.1` to `0` to abort SSL connections
          > immediately when the connector is closed. Added support for
          > `ssl_shutdown_timeout=0` on all Python versions. A [`RuntimeWarning`](https://docs.python.org/3/library/exceptions.html#RuntimeWarning "(in Python v3.14)")
          > is issued when non-zero values are passed on Python < 3.11.
          >
          > Deprecated since version 3.12.11: This parameter is deprecated and will be removed in aiohttp 4.0.

    family[¶](#aiohttp.TCPConnector.family "Link to this definition")
    :   *TCP* socket family e.g. [`socket.AF_INET`](https://docs.python.org/3/library/socket.html#socket.AF_INET "(in Python v3.14)") or
        [`socket.AF_INET6`](https://docs.python.org/3/library/socket.html#socket.AF_INET6 "(in Python v3.14)")

        Read-only property.

    dns\_cache[¶](#aiohttp.TCPConnector.dns_cache "Link to this definition")
    :   Use quick lookup in internal *DNS* cache for host names if `True`.

        Read-only [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") property.

    cached\_hosts[¶](#aiohttp.TCPConnector.cached_hosts "Link to this definition")
    :   The cache of resolved hosts if [`dns_cache`](#aiohttp.TCPConnector.dns_cache "aiohttp.TCPConnector.dns_cache") is enabled.

        Read-only [`types.MappingProxyType`](https://docs.python.org/3/library/types.html#types.MappingProxyType "(in Python v3.14)") property.

    clear\_dns\_cache(*self*, *host=None*, *port=None*)[[source]](_modules/aiohttp/connector.html#TCPConnector.clear_dns_cache)[¶](#aiohttp.TCPConnector.clear_dns_cache "Link to this definition")
    :   Clear internal *DNS* cache.

        Remove specific entry if both *host* and *port* are specified,
        clear all cache otherwise.

class aiohttp.UnixConnector(*path*, *\**, *conn\_timeout=None*, *keepalive\_timeout=30*, *limit=100*, *force\_close=False*, *loop=None*)[[source]](_modules/aiohttp/connector.html#UnixConnector)[¶](#aiohttp.UnixConnector "Link to this definition")
:   Unix socket connector.

    Use [`UnixConnector`](#aiohttp.UnixConnector "aiohttp.UnixConnector") for sending *HTTP/HTTPS* requests
    through *UNIX Sockets* as underlying transport.

    UNIX sockets are handy for writing tests and making very fast
    connections between processes on the same host.

    [`UnixConnector`](#aiohttp.UnixConnector "aiohttp.UnixConnector") is inherited from [`BaseConnector`](#aiohttp.BaseConnector "aiohttp.BaseConnector").

    > Usage:
    >
    > ```
    > conn = UnixConnector(path='/path/to/socket')
    > session = ClientSession(connector=conn)
    > async with session.get('http://python.org') as resp:
    >     ...
    > ```

    Constructor accepts all parameters suitable for
    [`BaseConnector`](#aiohttp.BaseConnector "aiohttp.BaseConnector") plus UNIX-specific one:

    Parameters:
    :   **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Unix socket path

    path[¶](#aiohttp.UnixConnector.path "Link to this definition")
    :   Path to *UNIX socket*, read-only [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

class aiohttp.Connection[¶](#aiohttp.Connection "Link to this definition")
:   Encapsulates single connection in connector object.

    End user should never create [`Connection`](#aiohttp.Connection "aiohttp.Connection") instances manually
    but get it by [`BaseConnector.connect()`](#aiohttp.BaseConnector.connect "aiohttp.BaseConnector.connect") coroutine.

    closed[¶](#aiohttp.Connection.closed "Link to this definition")
    :   [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") read-only property, `True` if connection was
        closed, released or detached.

    loop[¶](#aiohttp.Connection.loop "Link to this definition")
    :   Event loop used for connection

        Deprecated since version 3.5.

    transport[¶](#aiohttp.Connection.transport "Link to this definition")
    :   Connection transport

    close()[¶](#aiohttp.Connection.close "Link to this definition")
    :   Close connection with forcibly closing underlying socket.

    release()[¶](#aiohttp.Connection.release "Link to this definition")
    :   Release connection back to connector.

        Underlying socket is not closed, the connection may be reused
        later if timeout (30 seconds by default) for connection was not
        expired.

## Response object[¶](#response-object "Link to this heading")

class aiohttp.ClientResponse[[source]](_modules/aiohttp/client_reqrep.html#ClientResponse)[¶](#aiohttp.ClientResponse "Link to this definition")
:   Client response returned by [`aiohttp.ClientSession.request()`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request") and family.

    User never creates the instance of ClientResponse class but gets it
    from API calls.

    [`ClientResponse`](#aiohttp.ClientResponse "aiohttp.ClientResponse") supports async context manager protocol, e.g.:

    ```
    resp = await client_session.get(url)
    async with resp:
        assert resp.status == 200
    ```

    After exiting from `async with` block response object will be
    *released* (see [`release()`](#aiohttp.ClientResponse.release "aiohttp.ClientResponse.release") method).

    version[¶](#aiohttp.ClientResponse.version "Link to this definition")
    :   Response’s version, `HttpVersion` instance.

    status[¶](#aiohttp.ClientResponse.status "Link to this definition")
    :   HTTP status code of response ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")), e.g. `200`.

    reason[¶](#aiohttp.ClientResponse.reason "Link to this definition")
    :   HTTP status reason of response ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")), e.g. `"OK"`.

    ok[¶](#aiohttp.ClientResponse.ok "Link to this definition")
    :   Boolean representation of HTTP status code ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")).
        `True` if `status` is less than `400`; otherwise, `False`.

    method[¶](#aiohttp.ClientResponse.method "Link to this definition")
    :   Request’s method ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")).

    url[¶](#aiohttp.ClientResponse.url "Link to this definition")
    :   URL of request ([`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")).

    real\_url[¶](#aiohttp.ClientResponse.real_url "Link to this definition")
    :   Unmodified URL of request with URL fragment unstripped ([`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")).

        Added in version 3.2.

    connection[¶](#aiohttp.ClientResponse.connection "Link to this definition")
    :   [`Connection`](#aiohttp.Connection "aiohttp.Connection") used for handling response.

    content[¶](#aiohttp.ClientResponse.content "Link to this definition")
    :   Payload stream, which contains response’s BODY ([`StreamReader`](streams.html#aiohttp.StreamReader "aiohttp.StreamReader")).
        It supports various reading methods depending on the expected format.
        When chunked transfer encoding is used by the server, allows retrieving
        the actual http chunks.

        Reading from the stream may raise
        [`aiohttp.ClientPayloadError`](#aiohttp.ClientPayloadError "aiohttp.ClientPayloadError") if the response object is
        closed before response receives all data or in case if any
        transfer encoding related errors like malformed chunked
        encoding of broken compression data.

    cookies[¶](#aiohttp.ClientResponse.cookies "Link to this definition")
    :   HTTP cookies of response (*Set-Cookie* HTTP header,
        [`SimpleCookie`](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie "(in Python v3.14)")).

        Note

        Since [`SimpleCookie`](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie "(in Python v3.14)") uses cookie name as the
        key, cookies with the same name but different domains or paths will
        be overwritten. Only the last cookie with a given name will be
        accessible via this attribute.

        To access all cookies, including duplicates with the same name,
        use [`response.headers.getall('Set-Cookie')`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy.getall "(in multidict v6.7)").

        The session’s cookie jar will correctly store all cookies, even if
        they are not accessible via this attribute.

    headers[¶](#aiohttp.ClientResponse.headers "Link to this definition")
    :   A case-insensitive multidict proxy with HTTP headers of
        response, [`CIMultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDictProxy "(in multidict v6.7)").

    raw\_headers[¶](#aiohttp.ClientResponse.raw_headers "Link to this definition")
    :   Unmodified HTTP headers of response as unconverted bytes, a sequence of
        `(key, value)` pairs.

    links[¶](#aiohttp.ClientResponse.links "Link to this definition")
    :   Link HTTP header parsed into a [`MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)").

        For each link, key is link param rel when it exists, or link url as
        [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") otherwise, and value is [`MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)")
        of link params and url at key url as [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") instance.

        Added in version 3.2.

    content\_type[¶](#aiohttp.ClientResponse.content_type "Link to this definition")
    :   Read-only property with *content* part of *Content-Type* header.

        Note

        Returns `'application/octet-stream'` if no Content-Type header
        is present or the value contains invalid syntax according to
        [**RFC 9110**](https://datatracker.ietf.org/doc/html/rfc9110.html). To see the original header check
        `resp.headers["Content-Type"]`.

        To make sure Content-Type header is not present in
        the server reply, use [`headers`](#aiohttp.ClientResponse.headers "aiohttp.ClientResponse.headers") or [`raw_headers`](#aiohttp.ClientResponse.raw_headers "aiohttp.ClientResponse.raw_headers"), e.g.
        `'Content-Type' not in resp.headers`.

    charset[¶](#aiohttp.ClientResponse.charset "Link to this definition")
    :   Read-only property that specifies the *encoding* for the request’s BODY.

        The value is parsed from the *Content-Type* HTTP header.

        Returns [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") like `'utf-8'` or `None` if no *Content-Type*
        header present in HTTP headers or it has no charset information.

    content\_disposition[¶](#aiohttp.ClientResponse.content_disposition "Link to this definition")
    :   Read-only property that specified the *Content-Disposition* HTTP header.

        Instance of [`ContentDisposition`](#aiohttp.ContentDisposition "aiohttp.ContentDisposition") or `None` if no *Content-Disposition*
        header present in HTTP headers.

    history[¶](#aiohttp.ClientResponse.history "Link to this definition")
    :   A [`Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") of [`ClientResponse`](#aiohttp.ClientResponse "aiohttp.ClientResponse")
        objects of preceding requests (earliest request first) if there were
        redirects, an empty sequence otherwise.

    close()[[source]](_modules/aiohttp/client_reqrep.html#ClientResponse.close)[¶](#aiohttp.ClientResponse.close "Link to this definition")
    :   Close response and underlying connection.

        For [keep-alive](glossary.html#term-keep-alive) support see [`release()`](#aiohttp.ClientResponse.release "aiohttp.ClientResponse.release").

    async read()[[source]](_modules/aiohttp/client_reqrep.html#ClientResponse.read)[¶](#aiohttp.ClientResponse.read "Link to this definition")
    :   Read the whole response’s body as [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)").

        Close underlying connection if data reading gets an error,
        release connection otherwise.

        Raise an [`aiohttp.ClientResponseError`](#aiohttp.ClientResponseError "aiohttp.ClientResponseError") if the data can’t
        be read.

        Return bytes:
        :   read *BODY*.

        See also

        [`close()`](#aiohttp.ClientResponse.close "aiohttp.ClientResponse.close"), [`release()`](#aiohttp.ClientResponse.release "aiohttp.ClientResponse.release").

    release()[[source]](_modules/aiohttp/client_reqrep.html#ClientResponse.release)[¶](#aiohttp.ClientResponse.release "Link to this definition")
    :   It is not required to call release on the response
        object. When the client fully receives the payload, the
        underlying connection automatically returns back to pool. If the
        payload is not fully read, the connection is closed

    raise\_for\_status()[[source]](_modules/aiohttp/client_reqrep.html#ClientResponse.raise_for_status)[¶](#aiohttp.ClientResponse.raise_for_status "Link to this definition")
    :   Raise an [`aiohttp.ClientResponseError`](#aiohttp.ClientResponseError "aiohttp.ClientResponseError") if the response
        status is 400 or higher.

        Do nothing for success responses (less than 400).

    async text(*encoding=None*)[[source]](_modules/aiohttp/client_reqrep.html#ClientResponse.text)[¶](#aiohttp.ClientResponse.text "Link to this definition")
    :   Read response’s body and return decoded [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") using
        specified *encoding* parameter.

        If *encoding* is `None` content encoding is determined from the
        Content-Type header, or using the `fallback_charset_resolver` function.

        Close underlying connection if data reading gets an error,
        release connection otherwise.

        Parameters:
        :   **encoding** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – text encoding used for *BODY* decoding, or
            `None` for encoding autodetection
            (default).

        Raises:
        :   [`UnicodeDecodeError`](https://docs.python.org/3/library/exceptions.html#UnicodeDecodeError "(in Python v3.14)") if decoding fails. See also
            [`get_encoding()`](#aiohttp.ClientResponse.get_encoding "aiohttp.ClientResponse.get_encoding").

        Return str:
        :   decoded *BODY*

    async json(*\**, *encoding=None*, *loads=json.loads*, *content\_type='application/json'*)[[source]](_modules/aiohttp/client_reqrep.html#ClientResponse.json)[¶](#aiohttp.ClientResponse.json "Link to this definition")
    :   Read response’s body as *JSON*, return [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") using
        specified *encoding* and *loader*. If data is not still available
        a `read` call will be done.

        If response’s content-type does not match content\_type parameter
        [`aiohttp.ContentTypeError`](#aiohttp.ContentTypeError "aiohttp.ContentTypeError") get raised.
        To disable content type check pass `None` value.

        Parameters:
        :   * **encoding** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

              text encoding used for *BODY* decoding, or
              `None` for encoding autodetection
              (default).

              By the standard JSON encoding should be
              `UTF-8` but practice beats purity: some
              servers return non-UTF
              responses. Autodetection works pretty fine
              anyway.
            * **loads** ([*collections.abc.Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) – [callable](glossary.html#term-callable) used for loading *JSON*
              data, [`json.loads()`](https://docs.python.org/3/library/json.html#json.loads "(in Python v3.14)") by default.
            * **content\_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – specify response’s content-type, if content type
              does not match raise [`aiohttp.ClientResponseError`](#aiohttp.ClientResponseError "aiohttp.ClientResponseError").
              To disable content-type check, pass `None` as value.
              (default: application/json).

        Returns:
        :   *BODY* as *JSON* data parsed by *loads* parameter or
            `None` if *BODY* is empty or contains white-spaces only.

    request\_info[¶](#aiohttp.ClientResponse.request_info "Link to this definition")
    :   A [`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple "(in Python v3.14)") with request URL and headers from [`ClientRequest`](#aiohttp.ClientRequest "aiohttp.ClientRequest")
        object, [`aiohttp.RequestInfo`](#aiohttp.RequestInfo "aiohttp.RequestInfo") instance.

    get\_encoding()[[source]](_modules/aiohttp/client_reqrep.html#ClientResponse.get_encoding)[¶](#aiohttp.ClientResponse.get_encoding "Link to this definition")
    :   Retrieve content encoding using `charset` info in `Content-Type` HTTP header.
        If no charset is present or the charset is not understood by Python, the
        `fallback_charset_resolver` function associated with the `ClientSession` is called.

        Added in version 3.0.

## ClientWebSocketResponse[¶](#clientwebsocketresponse "Link to this heading")

To connect to a websocket server `aiohttp.ws_connect()` or
[`aiohttp.ClientSession.ws_connect()`](#aiohttp.ClientSession.ws_connect "aiohttp.ClientSession.ws_connect") coroutines should be used, do
not create an instance of class [`ClientWebSocketResponse`](#aiohttp.ClientWebSocketResponse "aiohttp.ClientWebSocketResponse")
manually.

class aiohttp.ClientWebSocketResponse[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse)[¶](#aiohttp.ClientWebSocketResponse "Link to this definition")
:   Class for handling client-side websockets.

    closed[¶](#aiohttp.ClientWebSocketResponse.closed "Link to this definition")
    :   Read-only property, `True` if [`close()`](#aiohttp.ClientWebSocketResponse.close "aiohttp.ClientWebSocketResponse.close") has been called or
        [`CLOSE`](websocket_utilities.html#aiohttp.WSMsgType.CLOSE "aiohttp.WSMsgType.CLOSE") message has been received from peer.

    protocol[¶](#aiohttp.ClientWebSocketResponse.protocol "Link to this definition")
    :   Websocket *subprotocol* chosen after `start()` call.

        May be `None` if server and client protocols are
        not overlapping.

    get\_extra\_info(*name*, *default=None*)[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.get_extra_info)[¶](#aiohttp.ClientWebSocketResponse.get_extra_info "Link to this definition")
    :   Reads optional extra information from the connection’s transport.
        If no value associated with `name` is found, `default` is returned.

        See [`asyncio.BaseTransport.get_extra_info()`](https://docs.python.org/3/library/asyncio-protocol.html#asyncio.BaseTransport.get_extra_info "(in Python v3.14)")

        Parameters:
        :   * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The key to look up in the transport extra information.
            * **default** – Default value to be used when no value for `name` is
              found (default is `None`).

    exception()[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.exception)[¶](#aiohttp.ClientWebSocketResponse.exception "Link to this definition")
    :   Returns exception if any occurs or returns None.

    async ping(*message=b''*)[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.ping)[¶](#aiohttp.ClientWebSocketResponse.ping "Link to this definition")
    :   Send [`PING`](websocket_utilities.html#aiohttp.WSMsgType.PING "aiohttp.WSMsgType.PING") to peer.

        Parameters:
        :   **message** – optional payload of *ping* message,
            [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") (converted to *UTF-8* encoded bytes)
            or [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)").

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)")

    async pong(*message=b''*)[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.pong)[¶](#aiohttp.ClientWebSocketResponse.pong "Link to this definition")
    :   Send [`PONG`](websocket_utilities.html#aiohttp.WSMsgType.PONG "aiohttp.WSMsgType.PONG") to peer.

        Parameters:
        :   **message** – optional payload of *pong* message,
            [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") (converted to *UTF-8* encoded bytes)
            or [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)").

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)")

    async send\_str(*data*, *compress=None*)[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.send_str)[¶](#aiohttp.ClientWebSocketResponse.send_str "Link to this definition")
    :   Send *data* to peer as [`TEXT`](websocket_utilities.html#aiohttp.WSMsgType.TEXT "aiohttp.WSMsgType.TEXT") message.

        Parameters:
        :   * **data** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – data to send.
            * **compress** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – sets specific level of compression for
              single message,
              `None` for not overriding per-socket setting.

        Raises:
        :   [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") – if data is not [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)"),
        *compress* parameter added.

    async send\_bytes(*data*, *compress=None*)[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.send_bytes)[¶](#aiohttp.ClientWebSocketResponse.send_bytes "Link to this definition")
    :   Send *data* to peer as [`BINARY`](websocket_utilities.html#aiohttp.WSMsgType.BINARY "aiohttp.WSMsgType.BINARY") message.

        Parameters:
        :   * **data** – data to send.
            * **compress** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – sets specific level of compression for
              single message,
              `None` for not overriding per-socket setting.

        Raises:
        :   [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") – if data is not [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)"),
            [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)") or [`memoryview`](https://docs.python.org/3/library/stdtypes.html#memoryview "(in Python v3.14)").

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)"),
        *compress* parameter added.

    async send\_json(*data*, *compress=None*, *\**, *dumps=json.dumps*)[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.send_json)[¶](#aiohttp.ClientWebSocketResponse.send_json "Link to this definition")
    :   Send *data* to peer as JSON string.

        Parameters:
        :   * **data** – data to send.
            * **compress** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – sets specific level of compression for
              single message,
              `None` for not overriding per-socket setting.
            * **dumps** ([*collections.abc.Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) – any [callable](glossary.html#term-callable) that accepts an object and
              returns a JSON string
              ([`json.dumps()`](https://docs.python.org/3/library/json.html#json.dumps "(in Python v3.14)") by default).

        Raises:
        :   * [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – if connection is not started or closing
            * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)") – if data is not serializable object
            * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") – if value returned by `dumps(data)` is not
              [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)"),
        *compress* parameter added.

    async send\_frame(*message*, *opcode*, *compress=None*)[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.send_frame)[¶](#aiohttp.ClientWebSocketResponse.send_frame "Link to this definition")
    :   Send a [`WSMsgType`](websocket_utilities.html#aiohttp.WSMsgType "aiohttp.WSMsgType") message *message* to peer.

        This method is low-level and should be used with caution as it
        only accepts bytes which must conform to the correct message type
        for *message*.

        It is recommended to use the [`send_str()`](#aiohttp.ClientWebSocketResponse.send_str "aiohttp.ClientWebSocketResponse.send_str"), [`send_bytes()`](#aiohttp.ClientWebSocketResponse.send_bytes "aiohttp.ClientWebSocketResponse.send_bytes")
        or [`send_json()`](#aiohttp.ClientWebSocketResponse.send_json "aiohttp.ClientWebSocketResponse.send_json") methods instead of this method.

        The primary use case for this method is to send bytes that are
        have already been encoded without having to decode and
        re-encode them.

        Parameters:
        :   * **message** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")) – message to send.
            * **opcode** ([*WSMsgType*](websocket_utilities.html#aiohttp.WSMsgType "aiohttp.WSMsgType")) – opcode of the message.
            * **compress** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – sets specific level of compression for
              single message,
              `None` for not overriding per-socket setting.

        Added in version 3.11.

    async close(*\**, *code=WSCloseCode.OK*, *message=b''*)[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.close)[¶](#aiohttp.ClientWebSocketResponse.close "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that initiates closing handshake by sending
        [`CLOSE`](websocket_utilities.html#aiohttp.WSMsgType.CLOSE "aiohttp.WSMsgType.CLOSE") message. It waits for
        close response from server. To add a timeout to close() call
        just wrap the call with asyncio.wait() or asyncio.wait\_for().

        Parameters:
        :   * **code** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – closing code. See also [`WSCloseCode`](websocket_utilities.html#aiohttp.WSCloseCode "aiohttp.WSCloseCode").
            * **message** – optional payload of *close* message,
              [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") (converted to *UTF-8* encoded bytes) or [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)").

    async receive()[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.receive)[¶](#aiohttp.ClientWebSocketResponse.receive "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that waits upcoming *data*
        message from peer and returns it.

        The coroutine implicitly handles
        [`PING`](websocket_utilities.html#aiohttp.WSMsgType.PING "aiohttp.WSMsgType.PING"),
        [`PONG`](websocket_utilities.html#aiohttp.WSMsgType.PONG "aiohttp.WSMsgType.PONG") and
        [`CLOSE`](websocket_utilities.html#aiohttp.WSMsgType.CLOSE "aiohttp.WSMsgType.CLOSE") without returning the
        message.

        It process *ping-pong game* and performs *closing handshake* internally.

        Returns:
        :   [`WSMessage`](websocket_utilities.html#aiohttp.WSMessage "aiohttp.WSMessage")

    async receive\_str()[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.receive_str)[¶](#aiohttp.ClientWebSocketResponse.receive_str "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that calls [`receive()`](#aiohttp.ClientWebSocketResponse.receive "aiohttp.ClientWebSocketResponse.receive") but
        also asserts the message type is
        [`TEXT`](websocket_utilities.html#aiohttp.WSMsgType.TEXT "aiohttp.WSMsgType.TEXT").

        Return str:
        :   peer’s message content.

        Raises:
        :   [**aiohttp.WSMessageTypeError**](#aiohttp.WSMessageTypeError "aiohttp.WSMessageTypeError") – if message is not [`TEXT`](websocket_utilities.html#aiohttp.WSMsgType.TEXT "aiohttp.WSMsgType.TEXT").

    async receive\_bytes()[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.receive_bytes)[¶](#aiohttp.ClientWebSocketResponse.receive_bytes "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that calls [`receive()`](#aiohttp.ClientWebSocketResponse.receive "aiohttp.ClientWebSocketResponse.receive") but
        also asserts the message type is
        [`BINARY`](websocket_utilities.html#aiohttp.WSMsgType.BINARY "aiohttp.WSMsgType.BINARY").

        Return bytes:
        :   peer’s message content.

        Raises:
        :   [**aiohttp.WSMessageTypeError**](#aiohttp.WSMessageTypeError "aiohttp.WSMessageTypeError") – if message is not [`BINARY`](websocket_utilities.html#aiohttp.WSMsgType.BINARY "aiohttp.WSMsgType.BINARY").

    async receive\_json(*\**, *loads=json.loads*)[[source]](_modules/aiohttp/client_ws.html#ClientWebSocketResponse.receive_json)[¶](#aiohttp.ClientWebSocketResponse.receive_json "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that calls [`receive_str()`](#aiohttp.ClientWebSocketResponse.receive_str "aiohttp.ClientWebSocketResponse.receive_str") and loads
        the JSON string to a Python dict.

        Parameters:
        :   **loads** ([*collections.abc.Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) – any [callable](glossary.html#term-callable) that accepts
            [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") and returns [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")
            with parsed JSON ([`json.loads()`](https://docs.python.org/3/library/json.html#json.loads "(in Python v3.14)") by
            default).

        Return dict:
        :   loaded JSON content

        Raises:
        :   * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") – if message is [`BINARY`](websocket_utilities.html#aiohttp.WSMsgType.BINARY "aiohttp.WSMsgType.BINARY").
            * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)") – if message is not valid JSON.

## ClientRequest[¶](#clientrequest "Link to this heading")

class aiohttp.ClientRequest[[source]](_modules/aiohttp/client_reqrep.html#ClientRequest)[¶](#aiohttp.ClientRequest "Link to this definition")
:   Represents an HTTP request to be sent by the client.

    This object encapsulates all the details of an HTTP request before it is sent.
    It is primarily used within client middleware to inspect or modify requests.

    Note

    You typically don’t create `ClientRequest` instances directly. They are
    created internally by [`ClientSession`](#aiohttp.ClientSession "aiohttp.ClientSession") methods and passed to middleware.

    For more information about using middleware, see [Client Middleware](client_advanced.html#aiohttp-client-middleware).

    body: Payload | Literal[b''][¶](#aiohttp.ClientRequest.body "Link to this definition")
    :   The request body payload (defaults to `b""` if no body passed).

        Danger

        **DO NOT set this attribute directly!** Direct assignment will cause resource
        leaks. Always use [`update_body()`](#aiohttp.ClientRequest.update_body "aiohttp.ClientRequest.update_body") instead:

        ```
        # WRONG - This will leak resources!
        request.body = b"new data"

        # CORRECT - Use update_body
        await request.update_body(b"new data")
        ```

        Setting body directly bypasses cleanup of the previous payload, which can
        leave file handles open, streams unclosed, and buffers unreleased.

        Additionally, setting body directly must be done from within an event loop
        and is not thread-safe. Setting body outside of an event loop may raise
        RuntimeError when closing file-based payloads.

    chunked: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")[¶](#aiohttp.ClientRequest.chunked "Link to this definition")
    :   Whether to use chunked transfer encoding:

        * `True`: Use chunked encoding
        * `False`: Don’t use chunked encoding
        * `None`: Automatically determine based on body

    compress: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")[¶](#aiohttp.ClientRequest.compress "Link to this definition")
    :   The compression encoding for the request body. Common values include
        `'gzip'` and `'deflate'`, but any string value is technically allowed.
        `None` means no compression.

    headers: [multidict.CIMultiDict](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)")[¶](#aiohttp.ClientRequest.headers "Link to this definition")
    :   The HTTP headers that will be sent with the request. This is a case-insensitive
        multidict that can be modified by middleware.

        ```
        # Add or modify headers
        request.headers['X-Custom-Header'] = 'value'
        request.headers['User-Agent'] = 'MyApp/1.0'
        ```

    is\_ssl: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")[[source]](_modules/aiohttp/client_reqrep.html#ClientRequest.is_ssl)[¶](#aiohttp.ClientRequest.is_ssl "Link to this definition")
    :   `True` if the request uses a secure scheme (e.g., HTTPS, WSS), `False` otherwise.

    method: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")[¶](#aiohttp.ClientRequest.method "Link to this definition")
    :   The HTTP method of the request (e.g., `'GET'`, `'POST'`, `'PUT'`, etc.).

    original\_url: [yarl.URL](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")[¶](#aiohttp.ClientRequest.original_url "Link to this definition")
    :   The original URL passed to the request method, including any fragment.
        This preserves the exact URL as provided by the user.

    proxy: [yarl.URL](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")[¶](#aiohttp.ClientRequest.proxy "Link to this definition")
    :   The proxy URL if the request will be sent through a proxy, `None` otherwise.

    proxy\_headers: [multidict.CIMultiDict](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")[¶](#aiohttp.ClientRequest.proxy_headers "Link to this definition")
    :   Headers to be sent to the proxy server (e.g., `Proxy-Authorization`).
        Only set when [`proxy`](#aiohttp.ClientRequest.proxy "aiohttp.ClientRequest.proxy") is not `None`.

    response\_class: [type](#aiohttp.ContentDisposition.type "aiohttp.ContentDisposition.type")[[ClientResponse](#aiohttp.ClientResponse "aiohttp.ClientResponse")][¶](#aiohttp.ClientRequest.response_class "Link to this definition")
    :   The class to use for creating the response object. Defaults to
        [`ClientResponse`](#aiohttp.ClientResponse "aiohttp.ClientResponse") but can be customized for special handling.

    server\_hostname: [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")[¶](#aiohttp.ClientRequest.server_hostname "Link to this definition")
    :   Override the hostname for SSL certificate verification. Useful when
        connecting through proxies or to IP addresses.

    session: [ClientSession](#aiohttp.ClientSession "aiohttp.ClientSession")[¶](#aiohttp.ClientRequest.session "Link to this definition")
    :   The client session that created this request. Useful for accessing
        session-level configuration or making additional requests within middleware.

        Warning

        Be careful when making requests with the same session inside middleware
        to avoid infinite recursion. Use `middlewares=()` parameter when needed.

    ssl: [ssl.SSLContext](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") | [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [Fingerprint](#aiohttp.Fingerprint "aiohttp.Fingerprint")[¶](#aiohttp.ClientRequest.ssl "Link to this definition")
    :   SSL validation configuration for this request:

        * `True`: Use default SSL verification
        * `False`: Skip SSL verification
        * [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)"): Custom SSL context
        * [`Fingerprint`](#aiohttp.Fingerprint "aiohttp.Fingerprint"): Verify specific certificate fingerprint

    url: [yarl.URL](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")[¶](#aiohttp.ClientRequest.url "Link to this definition")
    :   The target URL of the request with the fragment (`#...`) part stripped.
        This is the actual URL that will be used for the connection.

        Note

        To access the original URL with fragment, use [`original_url`](#aiohttp.ClientRequest.original_url "aiohttp.ClientRequest.original_url").

    version: HttpVersion[¶](#aiohttp.ClientRequest.version "Link to this definition")
    :   The HTTP version to use for the request (e.g., `HttpVersion(1, 1)` for HTTP/1.1).

    update\_body(*body*)[[source]](_modules/aiohttp/client_reqrep.html#ClientRequest.update_body)[¶](#aiohttp.ClientRequest.update_body "Link to this definition")
    :   Update the request body and close any existing payload to prevent resource leaks.

        **This is the ONLY correct way to modify a request body.** Never set the
        [`body`](#aiohttp.ClientRequest.body "aiohttp.ClientRequest.body") attribute directly.

        This method is particularly useful in middleware when you need to modify the
        request body after the request has been created but before it’s sent.

        Parameters:
        :   **body** –

            The new body content. Can be:

            * `bytes`/`bytearray`: Raw binary data
            * `str`: Text data (encoded using charset from Content-Type)
            * [`FormData`](#aiohttp.FormData "aiohttp.FormData"): Form data encoded as multipart/form-data
            * `Payload`: A pre-configured payload object
            * `AsyncIterable[bytes]`: Async iterable of bytes chunks
            * File-like object: Will be read and sent as binary data
            * `None`: Clears the body

        ```
        async def middleware(request, handler):
            # Modify request body in middleware
            if request.method == 'POST':
                # CORRECT: Always use update_body
                await request.update_body(b'{"modified": true}')

                # WRONG: Never set body directly!
                # request.body = b'{"modified": true}'  # This leaks resources!

            # Or add authentication data to form
            if isinstance(request.body, FormData):
                form = FormData()
                # Copy existing fields and add auth token
                form.add_field('auth_token', 'secret123')
                await request.update_body(form)

            return await handler(request)
        ```

        Note

        This method is async because it may need to close file handles or
        other resources associated with the previous payload. Always await
        this method to ensure proper cleanup.

        Danger

        **Never set :attr:`ClientRequest.body` directly!** Direct assignment will cause resource
        leaks. Always use this method instead. Setting the body attribute directly:

        * Bypasses cleanup of the previous payload
        * Leaves file handles and streams open
        * Can cause memory leaks
        * May result in unexpected behavior with async iterables

        Warning

        When updating the body, ensure that the Content-Type header is
        appropriate for the new body content. The Content-Length header
        will be updated automatically. When using [`FormData`](#aiohttp.FormData "aiohttp.FormData") or
        `Payload` objects, headers are updated automatically,
        but you may need to set Content-Type manually for raw bytes or text.

        It is not recommended to change the payload type in middleware. If the
        body was already set (e.g., as bytes), it’s best to keep the same type
        rather than converting it (e.g., to str) as this may result in unexpected
        behavior.

        Added in version 3.12.

## Utilities[¶](#utilities "Link to this heading")

class aiohttp.ClientTimeout(*\**, *total=None*, *connect=None*, *sock\_connect=None*, *sock\_read=None*)[[source]](_modules/aiohttp/client.html#ClientTimeout)[¶](#aiohttp.ClientTimeout "Link to this definition")
:   A data class for client timeout settings.

    See [Timeouts](client_quickstart.html#aiohttp-client-timeouts) for usage examples.

    total[¶](#aiohttp.ClientTimeout.total "Link to this definition")
    :   Total number of seconds for the whole request.

        [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)"), `None` by default.

    connect[¶](#aiohttp.ClientTimeout.connect "Link to this definition")
    :   Maximal number of seconds for acquiring a connection from pool. The time
        consists connection establishment for a new connection or
        waiting for a free connection from a pool if pool connection
        limits are exceeded.

        For pure socket connection establishment time use
        [`sock_connect`](#aiohttp.ClientTimeout.sock_connect "aiohttp.ClientTimeout.sock_connect").

        [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)"), `None` by default.

    sock\_connect[¶](#aiohttp.ClientTimeout.sock_connect "Link to this definition")
    :   Maximal number of seconds for connecting to a peer for a new connection, not
        given from a pool. See also [`connect`](#aiohttp.ClientTimeout.connect "aiohttp.ClientTimeout.connect").

        [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)"), `None` by default.

    sock\_read[¶](#aiohttp.ClientTimeout.sock_read "Link to this definition")
    :   Maximal number of seconds for reading a portion of data from a peer.

        [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)"), `None` by default.

class aiohttp.ClientWSTimeout(*\**, *ws\_receive=None*, *ws\_close=None*)[[source]](_modules/aiohttp/client_ws.html#ClientWSTimeout)[¶](#aiohttp.ClientWSTimeout "Link to this definition")
:   A data class for websocket client timeout settings.

    ws\_receive[¶](#aiohttp.ClientWSTimeout.ws_receive "Link to this definition")
    :   A timeout for websocket to receive a complete message.

        [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)"), `None` by default.

    ws\_close[¶](#aiohttp.ClientWSTimeout.ws_close "Link to this definition")
    :   A timeout for the websocket to close.

        [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)"), `10.0` by default.

    Added in version 4.0.

    Note

    Timeouts of 5 seconds or more are rounded for scheduling on the next
    second boundary (an absolute time where microseconds part is zero) for the
    sake of performance.

    E.g., assume a timeout is `10`, absolute time when timeout should expire
    is `loop.time() + 5`, and it points to `12345.67 + 10` which is equal
    to `12355.67`.

    The absolute time for the timeout cancellation is `12356`.

    It leads to grouping all close scheduled timeout expirations to exactly
    the same time to reduce amount of loop wakeups.

    Changed in version 3.7: Rounding to the next seconds boundary is disabled for timeouts smaller
    than 5 seconds for the sake of easy debugging.

    In turn, tiny timeouts can lead to significant performance degradation
    on production environment.

class aiohttp.ETag(*name*, *is\_weak=False*)[[source]](_modules/aiohttp/helpers.html#ETag)[¶](#aiohttp.ETag "Link to this definition")
:   Represents ETag identifier.

    value[¶](#aiohttp.ETag.value "Link to this definition")
    :   Value of corresponding etag without quotes.

    is\_weak[¶](#aiohttp.ETag.is_weak "Link to this definition")
    :   Flag indicates that etag is weak (has W/ prefix).

    Added in version 3.8.

class aiohttp.ContentDisposition[¶](#aiohttp.ContentDisposition "Link to this definition")
:   A data class to represent the Content-Disposition header,
    available as [`ClientResponse.content_disposition`](#aiohttp.ClientResponse.content_disposition "aiohttp.ClientResponse.content_disposition") attribute.

    type[¶](#aiohttp.ContentDisposition.type "Link to this definition")

    A [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") instance. Value of Content-Disposition header
    itself, e.g. `attachment`.

    filename[¶](#aiohttp.ContentDisposition.filename "Link to this definition")

    A [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") instance. Content filename extracted from
    parameters. May be `None`.

    parameters[¶](#aiohttp.ContentDisposition.parameters "Link to this definition")

    Read-only mapping contains all parameters.

class aiohttp.RequestInfo[[source]](_modules/aiohttp/client_reqrep.html#RequestInfo)[¶](#aiohttp.RequestInfo "Link to this definition")
:   A [`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple "(in Python v3.14)") with request URL and headers from [`ClientRequest`](#aiohttp.ClientRequest "aiohttp.ClientRequest")
    object, available as [`ClientResponse.request_info`](#aiohttp.ClientResponse.request_info "aiohttp.ClientResponse.request_info") attribute.

    url[¶](#aiohttp.RequestInfo.url "Link to this definition")
    :   Requested *url*, [`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") instance.

    method[¶](#aiohttp.RequestInfo.method "Link to this definition")
    :   Request HTTP method like `'GET'` or `'POST'`, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)").

    headers[¶](#aiohttp.RequestInfo.headers "Link to this definition")
    :   HTTP headers for request, [`multidict.CIMultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)") instance.

    real\_url[¶](#aiohttp.RequestInfo.real_url "Link to this definition")
    :   Requested *url* with URL fragment unstripped, [`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") instance.

        Added in version 3.2.

class aiohttp.BasicAuth(*login*, *password=''*, *encoding='latin1'*)[[source]](_modules/aiohttp/helpers.html#BasicAuth)[¶](#aiohttp.BasicAuth "Link to this definition")
:   HTTP basic authentication helper.

    Parameters:
    :   * **login** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – login
        * **password** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – password
        * **encoding** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – encoding (`'latin1'` by default)

    Should be used for specifying authorization data in client API,
    e.g. *auth* parameter for [`ClientSession.request()`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request").

    classmethod decode(*auth\_header*, *encoding='latin1'*)[[source]](_modules/aiohttp/helpers.html#BasicAuth.decode)[¶](#aiohttp.BasicAuth.decode "Link to this definition")
    :   Decode HTTP basic authentication credentials.

        Parameters:
        :   * **auth\_header** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The `Authorization` header to decode.
            * **encoding** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – (optional) encoding (‘latin1’ by default)

        Returns:
        :   decoded authentication data, [`BasicAuth`](#aiohttp.BasicAuth "aiohttp.BasicAuth").

    classmethod from\_url(*url*)[[source]](_modules/aiohttp/helpers.html#BasicAuth.from_url)[¶](#aiohttp.BasicAuth.from_url "Link to this definition")
    :   Constructed credentials info from url’s *user* and *password*
        parts.

        Returns:
        :   credentials data, [`BasicAuth`](#aiohttp.BasicAuth "aiohttp.BasicAuth") or `None` is
            credentials are not provided.

        Added in version 2.3.

    encode()[[source]](_modules/aiohttp/helpers.html#BasicAuth.encode)[¶](#aiohttp.BasicAuth.encode "Link to this definition")
    :   Encode credentials into string suitable for `Authorization`
        header etc.

        Returns:
        :   encoded authentication data, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)").

class aiohttp.DigestAuthMiddleware(*login*, *password*, *\**, *preemptive=True*)[[source]](_modules/aiohttp/client_middleware_digest_auth.html#DigestAuthMiddleware)[¶](#aiohttp.DigestAuthMiddleware "Link to this definition")
:   HTTP digest authentication client middleware.

    Parameters:
    :   * **login** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – login
        * **password** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – password
        * **preemptive** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Enable preemptive authentication (default: `True`)

    This middleware supports HTTP digest authentication with both auth and
    auth-int quality of protection (qop) modes, and a variety of hashing algorithms.

    It automatically handles the digest authentication handshake by:

    * Parsing 401 Unauthorized responses with WWW-Authenticate: Digest headers
    * Generating appropriate Authorization: Digest headers on retry
    * Maintaining nonce counts and challenge data per request
    * When `preemptive=True`, reusing authentication credentials for subsequent
      requests to the same protection space (following RFC 7616 Section 3.6)

    **Preemptive Authentication**

    By default (`preemptive=True`), the middleware remembers successful authentication
    challenges and automatically includes the Authorization header in subsequent requests
    to the same protection space. This behavior:

    * Improves server efficiency by avoiding extra round trips
    * Matches how modern web browsers handle digest authentication
    * Follows the recommendation in RFC 7616 Section 3.6

    The server may still respond with a 401 status and `stale=true` if the nonce
    has expired, in which case the middleware will automatically retry with the new nonce.

    To disable preemptive authentication and require a 401 challenge for every request,
    set `preemptive=False`:

    ```
    # Default behavior - preemptive auth enabled
    digest_auth_middleware = DigestAuthMiddleware(login="user", password="pass")

    # Disable preemptive auth - always wait for 401 challenge
    digest_auth_middleware = DigestAuthMiddleware(login="user", password="pass",
                                                   preemptive=False)
    ```

    Usage:

    ```
    digest_auth_middleware = DigestAuthMiddleware(login="user", password="pass")
    async with ClientSession(middlewares=(digest_auth_middleware,)) as session:
        async with session.get("http://protected.example.com") as resp:
            # The middleware automatically handles the digest auth handshake
            assert resp.status == 200

        # Subsequent requests include auth header preemptively
        async with session.get("http://protected.example.com/other") as resp:
            assert resp.status == 200  # No 401 round trip needed
    ```

    Added in version 3.12.

    Changed in version 3.12.8: Added `preemptive` parameter to enable/disable preemptive authentication.

class aiohttp.CookieJar(*\**, *unsafe=False*, *quote\_cookie=True*, *treat\_as\_secure\_origin=[]*)[[source]](_modules/aiohttp/cookiejar.html#CookieJar)[¶](#aiohttp.CookieJar "Link to this definition")
:   The cookie jar instance is available as [`ClientSession.cookie_jar`](#aiohttp.ClientSession.cookie_jar "aiohttp.ClientSession.cookie_jar").

    The jar contains [`Morsel`](https://docs.python.org/3/library/http.cookies.html#http.cookies.Morsel "(in Python v3.14)") items for storing
    internal cookie data.

    API provides a count of saved cookies:

    ```
    len(session.cookie_jar)
    ```

    These cookies may be iterated over:

    ```
    for cookie in session.cookie_jar:
        print(cookie.key)
        print(cookie["domain"])
    ```

    The class implements [`collections.abc.Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)"),
    [`collections.abc.Sized`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sized "(in Python v3.14)") and
    [`aiohttp.abc.AbstractCookieJar`](abc.html#aiohttp.abc.AbstractCookieJar "aiohttp.abc.AbstractCookieJar") interfaces.

    Implements cookie storage adhering to RFC 6265.

    Parameters:
    :   * **unsafe** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – (optional) Whether to accept cookies from IPs.
        * **quote\_cookie** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          (optional) Whether to quote cookies according to
          :   [**RFC 2109**](https://datatracker.ietf.org/doc/html/rfc2109.html). Some backend systems
              (not compatible with RFC mentioned above)
              does not support quoted cookies.

          Added in version 3.7.
        * **treat\_as\_secure\_origin** –

          (optional) Mark origins as secure
          :   for cookies marked as Secured. Possible types are

              Possible types are:

              + [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") or [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of
                [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
              + [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
              + [`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")

          Added in version 3.8.

    update\_cookies(*cookies*, *response\_url=None*)[[source]](_modules/aiohttp/cookiejar.html#CookieJar.update_cookies)[¶](#aiohttp.CookieJar.update_cookies "Link to this definition")
    :   Update cookies returned by server in `Set-Cookie` header.

        Parameters:
        :   * **cookies** – a [`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)")
              (e.g. [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)"), [`SimpleCookie`](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie "(in Python v3.14)")) or
              *iterable* of *pairs* with cookies returned by server’s
              response.
            * **response\_url** ([*URL*](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")) – URL of response, `None` for *shared
              cookies*. Regular cookies are coupled with server’s URL and
              are sent only to this server, shared ones are sent in every
              client request.

    filter\_cookies(*request\_url*)[[source]](_modules/aiohttp/cookiejar.html#CookieJar.filter_cookies)[¶](#aiohttp.CookieJar.filter_cookies "Link to this definition")
    :   Return jar’s cookies acceptable for URL and available in
        `Cookie` header for sending client requests for given URL.

        Parameters:
        :   **response\_url** ([*URL*](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")) – request’s URL for which cookies are asked.

        Returns:
        :   [`http.cookies.SimpleCookie`](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie "(in Python v3.14)") with filtered
            cookies for given URL.

    save(*file\_path*)[[source]](_modules/aiohttp/cookiejar.html#CookieJar.save)[¶](#aiohttp.CookieJar.save "Link to this definition")
    :   Write a pickled representation of cookies into the file
        at provided path.

        Parameters:
        :   **file\_path** – Path to file where cookies will be serialized,
            [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)") instance.

    load(*file\_path*)[[source]](_modules/aiohttp/cookiejar.html#CookieJar.load)[¶](#aiohttp.CookieJar.load "Link to this definition")
    :   Load a pickled representation of cookies from the file
        at provided path.

        Parameters:
        :   **file\_path** – Path to file from where cookies will be
            imported, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)") instance.

    clear(*predicate=None*)[[source]](_modules/aiohttp/cookiejar.html#CookieJar.clear)[¶](#aiohttp.CookieJar.clear "Link to this definition")
    :   Removes all cookies from the jar if the predicate is `None`. Otherwise remove only those [`Morsel`](https://docs.python.org/3/library/http.cookies.html#http.cookies.Morsel "(in Python v3.14)") that `predicate(morsel)` returns `True`.

        Parameters:
        :   **predicate** –

            callable that gets [`Morsel`](https://docs.python.org/3/library/http.cookies.html#http.cookies.Morsel "(in Python v3.14)") as a parameter and returns `True` if this [`Morsel`](https://docs.python.org/3/library/http.cookies.html#http.cookies.Morsel "(in Python v3.14)") must be deleted from the jar.

            Added in version 4.0.

    clear\_domain(*domain*)[[source]](_modules/aiohttp/cookiejar.html#CookieJar.clear_domain)[¶](#aiohttp.CookieJar.clear_domain "Link to this definition")
    :   Remove all cookies from the jar that belongs to the specified domain or its subdomains.

        Parameters:
        :   **domain** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – domain for which cookies must be deleted from the jar.

        Added in version 4.0.

class aiohttp.DummyCookieJar(*\**, *loop=None*)[[source]](_modules/aiohttp/cookiejar.html#DummyCookieJar)[¶](#aiohttp.DummyCookieJar "Link to this definition")
:   Dummy cookie jar which does not store cookies but ignores them.

    Could be useful e.g. for web crawlers to iterate over Internet
    without blowing up with saved cookies information.

    To install dummy cookie jar pass it into session instance:

    ```
    jar = aiohttp.DummyCookieJar()
    session = aiohttp.ClientSession(cookie_jar=DummyCookieJar())
    ```

class aiohttp.Fingerprint(*digest*)[[source]](_modules/aiohttp/client_reqrep.html#Fingerprint)[¶](#aiohttp.Fingerprint "Link to this definition")
:   Fingerprint helper for checking SSL certificates by *SHA256* digest.

    Parameters:
    :   **digest** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")) – *SHA256* digest for certificate in DER-encoded
        binary form (see
        [`ssl.SSLSocket.getpeercert()`](https://docs.python.org/3/library/ssl.html#ssl.SSLSocket.getpeercert "(in Python v3.14)")).

    To check fingerprint pass the object into [`ClientSession.get()`](#aiohttp.ClientSession.get "aiohttp.ClientSession.get")
    call, e.g.:

    ```
    import hashlib

    with open(path_to_cert, 'rb') as f:
        digest = hashlib.sha256(f.read()).digest()

    await session.get(url, ssl=aiohttp.Fingerprint(digest))
    ```

    Added in version 3.0.

aiohttp.set\_zlib\_backend(*lib*)[[source]](_modules/aiohttp/compression_utils.html#set_zlib_backend)[¶](#aiohttp.set_zlib_backend "Link to this definition")
:   Sets the compression backend for zlib-based operations.

    This function allows you to override the default zlib backend
    used internally by passing a module that implements the standard
    compression interface.

    The module should implement at minimum the exact interface offered by the
    latest version of zlib.

    Parameters:
    :   **lib** ([*types.ModuleType*](https://docs.python.org/3/library/types.html#types.ModuleType "(in Python v3.14)")) – A module that implements the zlib-compatible compression API.

    Example usage:

    ```
    import zlib_ng.zlib_ng as zng
    import aiohttp

    aiohttp.set_zlib_backend(zng)
    ```

    Note

    aiohttp has been tested internally with [`zlib`](https://docs.python.org/3/library/zlib.html#module-zlib "(in Python v3.14)"), [`zlib_ng.zlib_ng`](https://python-zlib-ng.readthedocs.io/en/stable/index.html#module-zlib_ng.zlib_ng "(in python-zlib-ng v1.0.0)"), and [`isal.isal_zlib`](https://python-isal.readthedocs.io/en/stable/index.html#module-isal.isal_zlib "(in python-isal v0.1.dev703+gbcaaa9b07)").

    Added in version 3.12.

### FormData[¶](#formdata "Link to this heading")

A [`FormData`](#aiohttp.FormData "aiohttp.FormData") object contains the form data and also handles
encoding it into a body that is either `multipart/form-data` or
`application/x-www-form-urlencoded`. `multipart/form-data` is
used if at least one field is an [`io.IOBase`](https://docs.python.org/3/library/io.html#io.IOBase "(in Python v3.14)") object or was
added with at least one optional argument to [`add_field`](#aiohttp.FormData.add_field "aiohttp.FormData.add_field")
(`content_type`, `filename`, or `content_transfer_encoding`).
Otherwise, `application/x-www-form-urlencoded` is used.

[`FormData`](#aiohttp.FormData "aiohttp.FormData") instances are callable and return a `aiohttp.payload.Payload`
on being called.

class aiohttp.FormData(*fields*, *quote\_fields=True*, *charset=None*)[[source]](_modules/aiohttp/formdata.html#FormData)[¶](#aiohttp.FormData "Link to this definition")
:   Helper class for multipart/form-data and application/x-www-form-urlencoded body generation.

    Parameters:
    :   **fields** –

        A container for the key/value pairs of this form.

        Possible types are:

        * [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")
        * [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") or [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)")
        * [`io.IOBase`](https://docs.python.org/3/library/io.html#io.IOBase "(in Python v3.14)"), e.g. a file-like object
        * [`multidict.MultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDict "(in multidict v6.7)") or [`multidict.MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)")

        If it is a [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") or [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)"), it must be a valid argument
        for [`add_fields`](#aiohttp.FormData.add_fields "aiohttp.FormData.add_fields").

        For [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)"), [`multidict.MultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDict "(in multidict v6.7)"), and [`multidict.MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)"),
        the keys and values must be valid name and value arguments to
        [`add_field`](#aiohttp.FormData.add_field "aiohttp.FormData.add_field"), respectively.

    add\_field(*name*, *value*, *content\_type=None*, *filename=None*, *content\_transfer\_encoding=None*)[[source]](_modules/aiohttp/formdata.html#FormData.add_field)[¶](#aiohttp.FormData.add_field "Link to this definition")
    :   Add a field to the form.

        Parameters:
        :   * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Name of the field
            * **value** –

              Value of the field

              Possible types are:

              + [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
              + [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)"), [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)"), or [`memoryview`](https://docs.python.org/3/library/stdtypes.html#memoryview "(in Python v3.14)")
              + [`io.IOBase`](https://docs.python.org/3/library/io.html#io.IOBase "(in Python v3.14)"), e.g. a file-like object
            * **content\_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The field’s content-type header (optional)
            * **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

              The field’s filename (optional)

              If this is not set and `value` is a [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)"), [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)"),
              or [`memoryview`](https://docs.python.org/3/library/stdtypes.html#memoryview "(in Python v3.14)") object, the name argument is used as the filename
              unless `content_transfer_encoding` is specified.

              If `filename` is not set and `value` is an [`io.IOBase`](https://docs.python.org/3/library/io.html#io.IOBase "(in Python v3.14)")
              object, the filename is extracted from the object if possible.
            * **content\_transfer\_encoding** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The field’s content-transfer-encoding
              header (optional)

    add\_fields(*fields*)[[source]](_modules/aiohttp/formdata.html#FormData.add_fields)[¶](#aiohttp.FormData.add_fields "Link to this definition")
    :   Add one or more fields to the form.

        Parameters:
        :   **fields** –

            An iterable containing:

            * [`io.IOBase`](https://docs.python.org/3/library/io.html#io.IOBase "(in Python v3.14)"), e.g. a file-like object
            * [`multidict.MultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDict "(in multidict v6.7)") or [`multidict.MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)")
            * [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") or [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of length two, containing a name-value pair

## Client exceptions[¶](#client-exceptions "Link to this heading")

Exception hierarchy has been significantly modified in version
2.0. aiohttp defines only exceptions that covers connection handling
and server response misbehaviors. For developer specific mistakes,
aiohttp uses python standard exceptions like [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)") or
[`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)").

Reading a response content may raise a [`ClientPayloadError`](#aiohttp.ClientPayloadError "aiohttp.ClientPayloadError")
exception. This exception indicates errors specific to the payload
encoding. Such as invalid compressed data, malformed chunked-encoded
chunks or not enough data that satisfy the content-length header.

All exceptions are available as members of *aiohttp* module.

exception aiohttp.ClientError[[source]](_modules/aiohttp/client_exceptions.html#ClientError)[¶](#aiohttp.ClientError "Link to this definition")
:   Base class for all client specific exceptions.

    Derived from [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception "(in Python v3.14)")

class aiohttp.ClientPayloadError[[source]](_modules/aiohttp/client_exceptions.html#ClientPayloadError)[¶](#aiohttp.ClientPayloadError "Link to this definition")
:   This exception can only be raised while reading the response
    payload if one of these errors occurs:

    1. invalid compression
    2. malformed chunked encoding
    3. not enough data that satisfy `Content-Length` HTTP header.

    Derived from [`ClientError`](#aiohttp.ClientError "aiohttp.ClientError")

exception aiohttp.InvalidURL[[source]](_modules/aiohttp/client_exceptions.html#InvalidURL)[¶](#aiohttp.InvalidURL "Link to this definition")
:   URL used for fetching is malformed, e.g. it does not contain host
    part.

    Derived from [`ClientError`](#aiohttp.ClientError "aiohttp.ClientError") and [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)")

    url[¶](#aiohttp.InvalidURL.url "Link to this definition")
    :   > Invalid URL, [`yarl.URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") instance.

        description[¶](#aiohttp.InvalidURL.description "Link to this definition")
        :   Invalid URL description, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") instance or [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)").

exception aiohttp.InvalidUrlClientError[[source]](_modules/aiohttp/client_exceptions.html#InvalidUrlClientError)[¶](#aiohttp.InvalidUrlClientError "Link to this definition")
:   Base class for all errors related to client url.

    Derived from [`InvalidURL`](#aiohttp.InvalidURL "aiohttp.InvalidURL")

exception aiohttp.RedirectClientError[[source]](_modules/aiohttp/client_exceptions.html#RedirectClientError)[¶](#aiohttp.RedirectClientError "Link to this definition")
:   Base class for all errors related to client redirects.

    Derived from [`ClientError`](#aiohttp.ClientError "aiohttp.ClientError")

exception aiohttp.NonHttpUrlClientError[[source]](_modules/aiohttp/client_exceptions.html#NonHttpUrlClientError)[¶](#aiohttp.NonHttpUrlClientError "Link to this definition")
:   Base class for all errors related to non http client urls.

    Derived from [`ClientError`](#aiohttp.ClientError "aiohttp.ClientError")

exception aiohttp.InvalidUrlRedirectClientError[[source]](_modules/aiohttp/client_exceptions.html#InvalidUrlRedirectClientError)[¶](#aiohttp.InvalidUrlRedirectClientError "Link to this definition")
:   Redirect URL is malformed, e.g. it does not contain host part.

    Derived from [`InvalidUrlClientError`](#aiohttp.InvalidUrlClientError "aiohttp.InvalidUrlClientError") and [`RedirectClientError`](#aiohttp.RedirectClientError "aiohttp.RedirectClientError")

exception aiohttp.NonHttpUrlRedirectClientError[[source]](_modules/aiohttp/client_exceptions.html#NonHttpUrlRedirectClientError)[¶](#aiohttp.NonHttpUrlRedirectClientError "Link to this definition")
:   Redirect URL does not contain http schema.

    Derived from [`RedirectClientError`](#aiohttp.RedirectClientError "aiohttp.RedirectClientError") and [`NonHttpUrlClientError`](#aiohttp.NonHttpUrlClientError "aiohttp.NonHttpUrlClientError")

### Response errors[¶](#response-errors "Link to this heading")

exception aiohttp.ClientResponseError[[source]](_modules/aiohttp/client_exceptions.html#ClientResponseError)[¶](#aiohttp.ClientResponseError "Link to this definition")
:   These exceptions could happen after we get response from server.

    Derived from [`ClientError`](#aiohttp.ClientError "aiohttp.ClientError")

    request\_info[¶](#aiohttp.ClientResponseError.request_info "Link to this definition")
    :   Instance of [`RequestInfo`](#aiohttp.RequestInfo "aiohttp.RequestInfo") object, contains information
        about request.

    status[¶](#aiohttp.ClientResponseError.status "Link to this definition")
    :   HTTP status code of response ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")), e.g. `400`.

    message[¶](#aiohttp.ClientResponseError.message "Link to this definition")
    :   Message of response ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")), e.g. `"OK"`.

    headers[¶](#aiohttp.ClientResponseError.headers "Link to this definition")
    :   Headers in response, a list of pairs.

    history[¶](#aiohttp.ClientResponseError.history "Link to this definition")
    :   History from failed response, if available, else empty tuple.

        A [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") of [`ClientResponse`](#aiohttp.ClientResponse "aiohttp.ClientResponse") objects used for
        handle redirection responses.

    code[¶](#aiohttp.ClientResponseError.code "Link to this definition")
    :   HTTP status code of response ([`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")), e.g. `400`.

        Deprecated since version 3.1.

class aiohttp.ContentTypeError[[source]](_modules/aiohttp/client_exceptions.html#ContentTypeError)[¶](#aiohttp.ContentTypeError "Link to this definition")
:   Invalid content type.

    Derived from [`ClientResponseError`](#aiohttp.ClientResponseError "aiohttp.ClientResponseError")

    Added in version 2.3.

class aiohttp.TooManyRedirects[[source]](_modules/aiohttp/client_exceptions.html#TooManyRedirects)[¶](#aiohttp.TooManyRedirects "Link to this definition")
:   Client was redirected too many times.

    Maximum number of redirects can be configured by using
    parameter `max_redirects` in [`request`](#aiohttp.ClientSession.request "aiohttp.ClientSession.request").

    Derived from [`ClientResponseError`](#aiohttp.ClientResponseError "aiohttp.ClientResponseError")

    Added in version 3.2.

class aiohttp.WSServerHandshakeError[[source]](_modules/aiohttp/client_exceptions.html#WSServerHandshakeError)[¶](#aiohttp.WSServerHandshakeError "Link to this definition")
:   Web socket server response error.

    Derived from [`ClientResponseError`](#aiohttp.ClientResponseError "aiohttp.ClientResponseError")

exception aiohttp.WSMessageTypeError[[source]](_modules/aiohttp/client_exceptions.html#WSMessageTypeError)[¶](#aiohttp.WSMessageTypeError "Link to this definition")
:   Received WebSocket message of unexpected type

    Derived from [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)")

### Connection errors[¶](#connection-errors "Link to this heading")

class aiohttp.ClientConnectionError[[source]](_modules/aiohttp/client_exceptions.html#ClientConnectionError)[¶](#aiohttp.ClientConnectionError "Link to this definition")
:   These exceptions related to low-level connection problems.

    Derived from [`ClientError`](#aiohttp.ClientError "aiohttp.ClientError")

class aiohttp.ClientConnectionResetError[[source]](_modules/aiohttp/client_exceptions.html#ClientConnectionResetError)[¶](#aiohttp.ClientConnectionResetError "Link to this definition")
:   Derived from [`ClientConnectionError`](#aiohttp.ClientConnectionError "aiohttp.ClientConnectionError") and [`ConnectionResetError`](https://docs.python.org/3/library/exceptions.html#ConnectionResetError "(in Python v3.14)")

class aiohttp.ClientOSError[[source]](_modules/aiohttp/client_exceptions.html#ClientOSError)[¶](#aiohttp.ClientOSError "Link to this definition")
:   Subset of connection errors that are initiated by an [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError "(in Python v3.14)")
    exception.

    Derived from [`ClientConnectionError`](#aiohttp.ClientConnectionError "aiohttp.ClientConnectionError") and [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError "(in Python v3.14)")

class aiohttp.ClientConnectorError[[source]](_modules/aiohttp/client_exceptions.html#ClientConnectorError)[¶](#aiohttp.ClientConnectorError "Link to this definition")
:   Connector related exceptions.

    Derived from [`ClientOSError`](#aiohttp.ClientOSError "aiohttp.ClientOSError")

class aiohttp.ClientConnectorDNSError[[source]](_modules/aiohttp/client_exceptions.html#ClientConnectorDNSError)[¶](#aiohttp.ClientConnectorDNSError "Link to this definition")
:   DNS resolution error.

    Derived from [`ClientConnectorError`](#aiohttp.ClientConnectorError "aiohttp.ClientConnectorError")

class aiohttp.ClientProxyConnectionError[[source]](_modules/aiohttp/client_exceptions.html#ClientProxyConnectionError)[¶](#aiohttp.ClientProxyConnectionError "Link to this definition")
:   Derived from [`ClientConnectorError`](#aiohttp.ClientConnectorError "aiohttp.ClientConnectorError")

class aiohttp.ClientSSLError[[source]](_modules/aiohttp/client_exceptions.html#ClientSSLError)[¶](#aiohttp.ClientSSLError "Link to this definition")
:   Derived from [`ClientConnectorError`](#aiohttp.ClientConnectorError "aiohttp.ClientConnectorError")

class aiohttp.ClientConnectorSSLError[[source]](_modules/aiohttp/client_exceptions.html#ClientConnectorSSLError)[¶](#aiohttp.ClientConnectorSSLError "Link to this definition")
:   Response ssl error.

    Derived from [`ClientSSLError`](#aiohttp.ClientSSLError "aiohttp.ClientSSLError") and [`ssl.SSLError`](https://docs.python.org/3/library/ssl.html#ssl.SSLError "(in Python v3.14)")

class aiohttp.ClientConnectorCertificateError[[source]](_modules/aiohttp/client_exceptions.html#ClientConnectorCertificateError)[¶](#aiohttp.ClientConnectorCertificateError "Link to this definition")
:   Response certificate error.

    Derived from [`ClientSSLError`](#aiohttp.ClientSSLError "aiohttp.ClientSSLError") and [`ssl.CertificateError`](https://docs.python.org/3/library/ssl.html#ssl.CertificateError "(in Python v3.14)")

class aiohttp.UnixClientConnectorError[¶](#aiohttp.UnixClientConnectorError "Link to this definition")
:   Derived from [`ClientConnectorError`](#aiohttp.ClientConnectorError "aiohttp.ClientConnectorError")

class aiohttp.ServerConnectionError[[source]](_modules/aiohttp/client_exceptions.html#ServerConnectionError)[¶](#aiohttp.ServerConnectionError "Link to this definition")
:   Derived from [`ClientConnectionError`](#aiohttp.ClientConnectionError "aiohttp.ClientConnectionError")

class aiohttp.ServerDisconnectedError[[source]](_modules/aiohttp/client_exceptions.html#ServerDisconnectedError)[¶](#aiohttp.ServerDisconnectedError "Link to this definition")
:   Server disconnected.

    Derived from [`ServerConnectionError`](#aiohttp.ServerConnectionError "aiohttp.ServerConnectionError")

    message[¶](#aiohttp.ServerDisconnectedError.message "Link to this definition")
    :   Partially parsed HTTP message (optional).

class aiohttp.ServerFingerprintMismatch[[source]](_modules/aiohttp/client_exceptions.html#ServerFingerprintMismatch)[¶](#aiohttp.ServerFingerprintMismatch "Link to this definition")
:   Server fingerprint mismatch.

    Derived from [`ServerConnectionError`](#aiohttp.ServerConnectionError "aiohttp.ServerConnectionError")

class aiohttp.ServerTimeoutError[[source]](_modules/aiohttp/client_exceptions.html#ServerTimeoutError)[¶](#aiohttp.ServerTimeoutError "Link to this definition")
:   Server operation timeout: read timeout, etc.

    To catch all timeouts, including the `total` timeout, use
    [`asyncio.TimeoutError`](https://docs.python.org/3/library/asyncio-exceptions.html#asyncio.TimeoutError "(in Python v3.14)").

    Derived from [`ServerConnectionError`](#aiohttp.ServerConnectionError "aiohttp.ServerConnectionError") and [`asyncio.TimeoutError`](https://docs.python.org/3/library/asyncio-exceptions.html#asyncio.TimeoutError "(in Python v3.14)")

class aiohttp.ConnectionTimeoutError[[source]](_modules/aiohttp/client_exceptions.html#ConnectionTimeoutError)[¶](#aiohttp.ConnectionTimeoutError "Link to this definition")
:   Connection timeout on `connect` and `sock_connect` timeouts.

    Derived from [`ServerTimeoutError`](#aiohttp.ServerTimeoutError "aiohttp.ServerTimeoutError")

class aiohttp.SocketTimeoutError[[source]](_modules/aiohttp/client_exceptions.html#SocketTimeoutError)[¶](#aiohttp.SocketTimeoutError "Link to this definition")
:   Reading from socket timeout on `sock_read` timeout.

    Derived from [`ServerTimeoutError`](#aiohttp.ServerTimeoutError "aiohttp.ServerTimeoutError")

### Hierarchy of exceptions[¶](#hierarchy-of-exceptions "Link to this heading")

* [`ClientError`](#aiohttp.ClientError "aiohttp.ClientError")

  + [`ClientConnectionError`](#aiohttp.ClientConnectionError "aiohttp.ClientConnectionError")

    - [`ClientConnectionResetError`](#aiohttp.ClientConnectionResetError "aiohttp.ClientConnectionResetError")
    - [`ClientOSError`](#aiohttp.ClientOSError "aiohttp.ClientOSError")

      * [`ClientConnectorError`](#aiohttp.ClientConnectorError "aiohttp.ClientConnectorError")

        + [`ClientProxyConnectionError`](#aiohttp.ClientProxyConnectionError "aiohttp.ClientProxyConnectionError")
        + [`ClientConnectorDNSError`](#aiohttp.ClientConnectorDNSError "aiohttp.ClientConnectorDNSError")
        + [`ClientSSLError`](#aiohttp.ClientSSLError "aiohttp.ClientSSLError")

          - [`ClientConnectorCertificateError`](#aiohttp.ClientConnectorCertificateError "aiohttp.ClientConnectorCertificateError")
          - [`ClientConnectorSSLError`](#aiohttp.ClientConnectorSSLError "aiohttp.ClientConnectorSSLError")
        + [`UnixClientConnectorError`](#aiohttp.UnixClientConnectorError "aiohttp.UnixClientConnectorError")
    - [`ServerConnectionError`](#aiohttp.ServerConnectionError "aiohttp.ServerConnectionError")

      * [`ServerDisconnectedError`](#aiohttp.ServerDisconnectedError "aiohttp.ServerDisconnectedError")
      * [`ServerFingerprintMismatch`](#aiohttp.ServerFingerprintMismatch "aiohttp.ServerFingerprintMismatch")
      * [`ServerTimeoutError`](#aiohttp.ServerTimeoutError "aiohttp.ServerTimeoutError")

        + [`ConnectionTimeoutError`](#aiohttp.ConnectionTimeoutError "aiohttp.ConnectionTimeoutError")
        + [`SocketTimeoutError`](#aiohttp.SocketTimeoutError "aiohttp.SocketTimeoutError")
  + [`ClientPayloadError`](#aiohttp.ClientPayloadError "aiohttp.ClientPayloadError")
  + [`ClientResponseError`](#aiohttp.ClientResponseError "aiohttp.ClientResponseError")

    - `ClientHttpProxyError`
    - [`ContentTypeError`](#aiohttp.ContentTypeError "aiohttp.ContentTypeError")
    - [`TooManyRedirects`](#aiohttp.TooManyRedirects "aiohttp.TooManyRedirects")
    - [`WSServerHandshakeError`](#aiohttp.WSServerHandshakeError "aiohttp.WSServerHandshakeError")
  + [`InvalidURL`](#aiohttp.InvalidURL "aiohttp.InvalidURL")

    - [`InvalidUrlClientError`](#aiohttp.InvalidUrlClientError "aiohttp.InvalidUrlClientError")

      * [`InvalidUrlRedirectClientError`](#aiohttp.InvalidUrlRedirectClientError "aiohttp.InvalidUrlRedirectClientError")
  + [`NonHttpUrlClientError`](#aiohttp.NonHttpUrlClientError "aiohttp.NonHttpUrlClientError")

    - [`NonHttpUrlRedirectClientError`](#aiohttp.NonHttpUrlRedirectClientError "aiohttp.NonHttpUrlRedirectClientError")
  + [`RedirectClientError`](#aiohttp.RedirectClientError "aiohttp.RedirectClientError")

    - [`InvalidUrlRedirectClientError`](#aiohttp.InvalidUrlRedirectClientError "aiohttp.InvalidUrlRedirectClientError")
    - [`NonHttpUrlRedirectClientError`](#aiohttp.NonHttpUrlRedirectClientError "aiohttp.NonHttpUrlRedirectClientError")

## Client Types[¶](#client-types "Link to this heading")

type aiohttp.ClientMiddlewareType[¶](#aiohttp.ClientMiddlewareType "Link to this definition")
:   Type alias for client middleware functions. Middleware functions must have this signature:

    ```
    Callable[
        [ClientRequest, ClientHandlerType],
        Awaitable[ClientResponse]
    ]
    ```

type aiohttp.ClientHandlerType[¶](#aiohttp.ClientHandlerType "Link to this definition")
:   Type alias for client request handler functions:

    ```
    Callable[[ClientRequest], Awaitable[ClientResponse]]
    ```

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
  + [Quickstart](client_quickstart.html)
  + [Advanced Usage](client_advanced.html)
  + [Client Middleware Cookbook](client_middleware_cookbook.html)
  + [Reference](#)
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
[Page source](_sources/client_reference.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
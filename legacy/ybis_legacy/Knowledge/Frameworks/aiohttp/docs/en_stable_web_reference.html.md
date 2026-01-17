Server Reference — aiohttp 3.13.3 documentation

# Server Reference[¶](#server-reference "Link to this heading")

## Request and Base Request[¶](#request-and-base-request "Link to this heading")

The Request object contains all the information about an incoming HTTP request.

[`BaseRequest`](#aiohttp.web.BaseRequest "aiohttp.web.BaseRequest") is used for [Low-Level
Servers](web_lowlevel.html#aiohttp-web-lowlevel) (which have no applications, routers,
signals and middlewares). [`Request`](#aiohttp.web.Request "aiohttp.web.Request") has an [`Request.app`](#aiohttp.web.Request.app "aiohttp.web.Request.app")
and [`Request.match_info`](#aiohttp.web.Request.match_info "aiohttp.web.Request.match_info") attributes.

A [`BaseRequest`](#aiohttp.web.BaseRequest "aiohttp.web.BaseRequest") / [`Request`](#aiohttp.web.Request "aiohttp.web.Request") are [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") like objects,
allowing them to be used for [sharing
data](web_advanced.html#aiohttp-web-data-sharing) among [Middlewares](web_advanced.html#aiohttp-web-middlewares)
and [Signals](web_advanced.html#aiohttp-web-signals) handlers.

class aiohttp.web.BaseRequest[[source]](_modules/aiohttp/web_request.html#BaseRequest)[¶](#aiohttp.web.BaseRequest "Link to this definition")
:   version[¶](#aiohttp.web.BaseRequest.version "Link to this definition")
    :   *HTTP version* of request, Read-only property.

        Returns `aiohttp.protocol.HttpVersion` instance.

    method[¶](#aiohttp.web.BaseRequest.method "Link to this definition")
    :   *HTTP method*, read-only property.

        The value is upper-cased [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") like `"GET"`,
        `"POST"`, `"PUT"` etc.

    url[¶](#aiohttp.web.BaseRequest.url "Link to this definition")
    :   A [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") instance with absolute URL to resource
        (*scheme*, *host* and *port* are included).

        Note

        In case of malformed request (e.g. without `"HOST"` HTTP
        header) the absolute url may be unavailable.

    rel\_url[¶](#aiohttp.web.BaseRequest.rel_url "Link to this definition")
    :   A [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") instance with relative URL to resource
        (contains *path*, *query* and *fragment* parts only, *scheme*,
        *host* and *port* are excluded).

        The property is equal to `.url.relative()` but is always present.

        See also

        A note from [`url`](#aiohttp.web.BaseRequest.url "aiohttp.web.BaseRequest.url").

    scheme[¶](#aiohttp.web.BaseRequest.scheme "Link to this definition")
    :   A string representing the scheme of the request.

        The scheme is `'https'` if transport for request handling is
        *SSL*, `'http'` otherwise.

        The value could be overridden by [`clone()`](#aiohttp.web.BaseRequest.clone "aiohttp.web.BaseRequest.clone").

        Read-only [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

        Changed in version 2.3: *Forwarded* and *X-Forwarded-Proto* are not used anymore.

        Call `.clone(scheme=new_scheme)` for setting up the value
        explicitly.

        See also

        [Deploying behind a Proxy](web_advanced.html#aiohttp-web-forwarded-support)

    secure[¶](#aiohttp.web.BaseRequest.secure "Link to this definition")
    :   Shorthand for `request.url.scheme == 'https'`

        Read-only [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") property.

        See also

        [`scheme`](#aiohttp.web.BaseRequest.scheme "aiohttp.web.BaseRequest.scheme")

    forwarded[¶](#aiohttp.web.BaseRequest.forwarded "Link to this definition")
    :   A tuple containing all parsed Forwarded header(s).

        Makes an effort to parse Forwarded headers as specified by [**RFC 7239**](https://datatracker.ietf.org/doc/html/rfc7239.html):

        * It adds one (immutable) dictionary per Forwarded `field-value`, i.e.
          per proxy. The element corresponds to the data in the Forwarded
          `field-value` added by the first proxy encountered by the client.
          Each subsequent item corresponds to those added by later proxies.
        * It checks that every value has valid syntax in general as specified
          in [**RFC 7239 Section 4**](https://datatracker.ietf.org/doc/html/rfc7239.html#section-4): either a `token` or a `quoted-string`.
        * It un-escapes `quoted-pairs`.
        * It does NOT validate ‘by’ and ‘for’ contents as specified in
          [**RFC 7239 Section 6**](https://datatracker.ietf.org/doc/html/rfc7239.html#section-6).
        * It does NOT validate `host` contents (Host ABNF).
        * It does NOT validate `proto` contents for valid URI scheme names.

        Returns a tuple containing one or more `MappingProxy` objects

        See also

        [`scheme`](#aiohttp.web.BaseRequest.scheme "aiohttp.web.BaseRequest.scheme")

        See also

        [`host`](#aiohttp.web.BaseRequest.host "aiohttp.web.BaseRequest.host")

    host[¶](#aiohttp.web.BaseRequest.host "Link to this definition")
    :   Host name of the request, resolved in this order:

        * Overridden value by [`clone()`](#aiohttp.web.BaseRequest.clone "aiohttp.web.BaseRequest.clone") call.
        * *Host* HTTP header
        * [`socket.getfqdn()`](https://docs.python.org/3/library/socket.html#socket.getfqdn "(in Python v3.14)")

        Read-only [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

        Changed in version 2.3: *Forwarded* and *X-Forwarded-Host* are not used anymore.

        Call `.clone(host=new_host)` for setting up the value
        explicitly.

        See also

        [Deploying behind a Proxy](web_advanced.html#aiohttp-web-forwarded-support)

    remote[¶](#aiohttp.web.BaseRequest.remote "Link to this definition")
    :   Originating IP address of a client initiated HTTP request.

        The IP is resolved through the following headers, in this order:

        * Overridden value by [`clone()`](#aiohttp.web.BaseRequest.clone "aiohttp.web.BaseRequest.clone") call.
        * Peer name of opened socket.

        Read-only [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

        Call `.clone(remote=new_remote)` for setting up the value
        explicitly.

        Added in version 2.3.

        See also

        [Deploying behind a Proxy](web_advanced.html#aiohttp-web-forwarded-support)

    client\_max\_size[¶](#aiohttp.web.BaseRequest.client_max_size "Link to this definition")
    :   The maximum size of the request body.

        The value could be overridden by [`clone()`](#aiohttp.web.BaseRequest.clone "aiohttp.web.BaseRequest.clone").

        Read-only [`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") property.

    path\_qs[¶](#aiohttp.web.BaseRequest.path_qs "Link to this definition")
    :   The URL including PATH\_INFO and the query string. e.g.,
        `/app/blog?id=10`

        Read-only [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

    path[¶](#aiohttp.web.BaseRequest.path "Link to this definition")
    :   The URL including *PATH INFO* without the host or scheme. e.g.,
        `/app/blog`. The path is URL-decoded. For raw path info see
        [`raw_path`](#aiohttp.web.BaseRequest.raw_path "aiohttp.web.BaseRequest.raw_path").

        Read-only [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

    raw\_path[¶](#aiohttp.web.BaseRequest.raw_path "Link to this definition")
    :   The URL including raw *PATH INFO* without the host or scheme.
        Warning, the path may be URL-encoded and may contain invalid URL
        characters, e.g.
        `/my%2Fpath%7Cwith%21some%25strange%24characters`.

        For URL-decoded version please take a look on [`path`](#aiohttp.web.BaseRequest.path "aiohttp.web.BaseRequest.path").

        Read-only [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

    query[¶](#aiohttp.web.BaseRequest.query "Link to this definition")
    :   A multidict with all the variables in the query string.

        Read-only [`MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)") lazy property.

    query\_string[¶](#aiohttp.web.BaseRequest.query_string "Link to this definition")
    :   The query string in the URL, e.g., `id=10`

        Read-only [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

    headers[¶](#aiohttp.web.BaseRequest.headers "Link to this definition")
    :   A case-insensitive multidict proxy with all headers.

        Read-only [`CIMultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDictProxy "(in multidict v6.7)") property.

    raw\_headers[¶](#aiohttp.web.BaseRequest.raw_headers "Link to this definition")
    :   HTTP headers of response as unconverted bytes, a sequence of
        `(key, value)` pairs.

    keep\_alive[¶](#aiohttp.web.BaseRequest.keep_alive "Link to this definition")
    :   `True` if keep-alive connection enabled by HTTP client and
        protocol version supports it, otherwise `False`.

        Read-only [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") property.

    transport[¶](#aiohttp.web.BaseRequest.transport "Link to this definition")
    :   A [transport](https://docs.python.org/3/library/asyncio-protocol.html#asyncio-transport "(in Python v3.14)") used to process request.
        Read-only property.

        The property can be used, for example, for getting IP address of
        client’s peer:

        ```
        peername = request.transport.get_extra_info('peername')
        if peername is not None:
            host, port = peername
        ```

    loop[¶](#aiohttp.web.BaseRequest.loop "Link to this definition")
    :   An event loop instance used by HTTP request handling.

        Read-only [`asyncio.AbstractEventLoop`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop "(in Python v3.14)") property.

        Deprecated since version 3.5.

    cookies[¶](#aiohttp.web.BaseRequest.cookies "Link to this definition")
    :   A read-only dictionary-like object containing the request’s cookies.

        Read-only [`MappingProxyType`](https://docs.python.org/3/library/types.html#types.MappingProxyType "(in Python v3.14)") property.

    content[¶](#aiohttp.web.BaseRequest.content "Link to this definition")
    :   A [`StreamReader`](streams.html#aiohttp.StreamReader "aiohttp.StreamReader") instance,
        input stream for reading request’s *BODY*.

        Read-only property.

    body\_exists[¶](#aiohttp.web.BaseRequest.body_exists "Link to this definition")
    :   Return `True` if request has *HTTP BODY*, `False` otherwise.

        Read-only [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") property.

        Added in version 2.3.

    can\_read\_body[¶](#aiohttp.web.BaseRequest.can_read_body "Link to this definition")
    :   Return `True` if request’s *HTTP BODY* can be read, `False` otherwise.

        Read-only [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") property.

        Added in version 2.3.

    has\_body[¶](#aiohttp.web.BaseRequest.has_body "Link to this definition")
    :   Return `True` if request’s *HTTP BODY* can be read, `False` otherwise.

        Read-only [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") property.

        Deprecated since version 2.3: Use [`can_read_body()`](#aiohttp.web.BaseRequest.can_read_body "aiohttp.web.BaseRequest.can_read_body") instead.

    content\_type[¶](#aiohttp.web.BaseRequest.content_type "Link to this definition")
    :   Read-only property with *content* part of *Content-Type* header.

        Returns [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") like `'text/html'`

        Note

        Returns value is `'application/octet-stream'` if no
        Content-Type header present in HTTP headers according to
        [**RFC 2616**](https://datatracker.ietf.org/doc/html/rfc2616.html)

    charset[¶](#aiohttp.web.BaseRequest.charset "Link to this definition")
    :   Read-only property that specifies the *encoding* for the request’s BODY.

        The value is parsed from the *Content-Type* HTTP header.

        Returns [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") like `'utf-8'` or `None` if
        *Content-Type* has no charset information.

    content\_length[¶](#aiohttp.web.BaseRequest.content_length "Link to this definition")
    :   Read-only property that returns length of the request’s BODY.

        The value is parsed from the *Content-Length* HTTP header.

        Returns [`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") or `None` if *Content-Length* is absent.

    http\_range[¶](#aiohttp.web.BaseRequest.http_range "Link to this definition")
    :   Read-only property that returns information about *Range* HTTP header.

        Returns a [`slice`](https://docs.python.org/3/library/functions.html#slice "(in Python v3.14)") where `.start` is *left inclusive
        bound*, `.stop` is *right exclusive bound* and `.step` is
        `1`.

        The property might be used in two manners:

        1. Attribute-access style (example assumes that both left and
           right borders are set, the real logic for case of open bounds
           is more complex):

           ```
           rng = request.http_range
           with open(filename, 'rb') as f:
               f.seek(rng.start)
               return f.read(rng.stop-rng.start)
           ```
        2. Slice-style:

           ```
           return buffer[request.http_range]
           ```

    if\_modified\_since[¶](#aiohttp.web.BaseRequest.if_modified_since "Link to this definition")
    :   Read-only property that returns the date specified in the
        *If-Modified-Since* header.

        Returns [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)") or `None` if
        *If-Modified-Since* header is absent or is not a valid
        HTTP date.

    if\_unmodified\_since[¶](#aiohttp.web.BaseRequest.if_unmodified_since "Link to this definition")
    :   Read-only property that returns the date specified in the
        *If-Unmodified-Since* header.

        Returns [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)") or `None` if
        *If-Unmodified-Since* header is absent or is not a valid
        HTTP date.

        Added in version 3.1.

    if\_match[¶](#aiohttp.web.BaseRequest.if_match "Link to this definition")
    :   Read-only property that returns [`ETag`](client_reference.html#aiohttp.ETag "aiohttp.ETag") objects specified
        in the *If-Match* header.

        Returns [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") of [`ETag`](client_reference.html#aiohttp.ETag "aiohttp.ETag") or `None` if
        *If-Match* header is absent.

        Added in version 3.8.

    if\_none\_match[¶](#aiohttp.web.BaseRequest.if_none_match "Link to this definition")
    :   Read-only property that returns [`ETag`](client_reference.html#aiohttp.ETag "aiohttp.ETag") objects specified
        *If-None-Match* header.

        Returns [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)") of [`ETag`](client_reference.html#aiohttp.ETag "aiohttp.ETag") or `None` if
        *If-None-Match* header is absent.

        Added in version 3.8.

    if\_range[¶](#aiohttp.web.BaseRequest.if_range "Link to this definition")
    :   Read-only property that returns the date specified in the
        *If-Range* header.

        Returns [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)") or `None` if
        *If-Range* header is absent or is not a valid
        HTTP date.

        Added in version 3.1.

    clone(*\**, *method=...*, *rel\_url=...*, *headers=...*)[[source]](_modules/aiohttp/web_request.html#BaseRequest.clone)[¶](#aiohttp.web.BaseRequest.clone "Link to this definition")
    :   Clone itself with replacement some attributes.

        Creates and returns a new instance of Request object. If no parameters
        are given, an exact copy is returned. If a parameter is not passed, it
        will reuse the one from the current request object.

        Parameters:
        :   * **method** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – http method
            * **rel\_url** – url to use, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)")
            * **headers** – [`CIMultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)") or compatible
              headers container.

        Returns:
        :   a cloned [`Request`](#aiohttp.web.Request "aiohttp.web.Request") instance.

    get\_extra\_info(*name*, *default=None*)[[source]](_modules/aiohttp/web_request.html#BaseRequest.get_extra_info)[¶](#aiohttp.web.BaseRequest.get_extra_info "Link to this definition")
    :   Reads extra information from the protocol’s transport.
        If no value associated with `name` is found, `default` is returned.

        See [`asyncio.BaseTransport.get_extra_info()`](https://docs.python.org/3/library/asyncio-protocol.html#asyncio.BaseTransport.get_extra_info "(in Python v3.14)")

        Parameters:
        :   * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The key to look up in the transport extra information.
            * **default** – Default value to be used when no value for `name` is
              found (default is `None`).

        Added in version 3.7.

    async read()[[source]](_modules/aiohttp/web_request.html#BaseRequest.read)[¶](#aiohttp.web.BaseRequest.read "Link to this definition")
    :   Read request body, returns [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") object with body content.

        Note

        The method **does** store read data internally, subsequent
        [`read()`](#aiohttp.web.BaseRequest.read "aiohttp.web.BaseRequest.read") call will return the same value.

    async text()[[source]](_modules/aiohttp/web_request.html#BaseRequest.text)[¶](#aiohttp.web.BaseRequest.text "Link to this definition")
    :   Read request body, decode it using [`charset`](#aiohttp.web.BaseRequest.charset "aiohttp.web.BaseRequest.charset") encoding or
        `UTF-8` if no encoding was specified in *MIME-type*.

        Returns [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") with body content.

        Note

        The method **does** store read data internally, subsequent
        [`text()`](#aiohttp.web.BaseRequest.text "aiohttp.web.BaseRequest.text") call will return the same value.

    async json(*\**, *loads=json.loads*)[[source]](_modules/aiohttp/web_request.html#BaseRequest.json)[¶](#aiohttp.web.BaseRequest.json "Link to this definition")
    :   Read request body decoded as *json*.

        The method is just a boilerplate [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)")
        implemented as:

        ```
        async def json(self, *, loads=json.loads):
            body = await self.text()
            return loads(body)
        ```

        Parameters:
        :   **loads** ([*collections.abc.Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) – any [callable](glossary.html#term-callable) that accepts
            [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") and returns [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")
            with parsed JSON ([`json.loads()`](https://docs.python.org/3/library/json.html#json.loads "(in Python v3.14)") by
            default).

        Note

        The method **does** store read data internally, subsequent
        [`json()`](#aiohttp.web.BaseRequest.json "aiohttp.web.BaseRequest.json") call will return the same value.

    async multipart()[[source]](_modules/aiohttp/web_request.html#BaseRequest.multipart)[¶](#aiohttp.web.BaseRequest.multipart "Link to this definition")
    :   Returns [`aiohttp.MultipartReader`](multipart_reference.html#aiohttp.MultipartReader "aiohttp.MultipartReader") which processes
        incoming *multipart* request.

        The method is just a boilerplate [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)")
        implemented as:

        ```
        async def multipart(self, *, reader=aiohttp.multipart.MultipartReader):
            return reader(self.headers, self._payload)
        ```

        This method is a coroutine for consistency with the else reader methods.

        Warning

        The method **does not** store read data internally. That means once
        you exhausts multipart reader, you cannot get the request payload one
        more time.

        See also

        [Working with Multipart](multipart.html#aiohttp-multipart)

        Changed in version 3.4: Dropped *reader* parameter.

    async post()[[source]](_modules/aiohttp/web_request.html#BaseRequest.post)[¶](#aiohttp.web.BaseRequest.post "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that reads POST parameters from
        request body.

        Returns [`MultiDictProxy`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy "(in multidict v6.7)") instance filled
        with parsed data.

        If [`method`](#aiohttp.web.BaseRequest.method "aiohttp.web.BaseRequest.method") is not *POST*, *PUT*, *PATCH*, *TRACE* or *DELETE* or
        [`content_type`](#aiohttp.web.BaseRequest.content_type "aiohttp.web.BaseRequest.content_type") is not empty or
        *application/x-www-form-urlencoded* or *multipart/form-data*
        returns empty multidict.

        Note

        The method **does** store read data internally, subsequent
        [`post()`](#aiohttp.web.BaseRequest.post "aiohttp.web.BaseRequest.post") call will return the same value.

    async release()[[source]](_modules/aiohttp/web_request.html#BaseRequest.release)[¶](#aiohttp.web.BaseRequest.release "Link to this definition")
    :   Release request.

        Eat unread part of HTTP BODY if present.

        Note

        User code may never call [`release()`](#aiohttp.web.BaseRequest.release "aiohttp.web.BaseRequest.release"), all
        required work will be processed by [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web")
        internal machinery.

class aiohttp.web.Request[[source]](_modules/aiohttp/web_request.html#Request)[¶](#aiohttp.web.Request "Link to this definition")
:   A request used for receiving request’s information by *web handler*.

    Every [handler](web_quickstart.html#aiohttp-web-handler) accepts a request
    instance as the first positional parameter.

    The class in derived from [`BaseRequest`](#aiohttp.web.BaseRequest "aiohttp.web.BaseRequest"), shares all parent’s
    attributes and methods but has a couple of additional properties:

    match\_info[¶](#aiohttp.web.Request.match_info "Link to this definition")
    :   Read-only property with [`AbstractMatchInfo`](abc.html#aiohttp.abc.AbstractMatchInfo "aiohttp.abc.AbstractMatchInfo")
        instance for result of route resolving.

        Note

        Exact type of property depends on used router. If
        `app.router` is [`UrlDispatcher`](#aiohttp.web.UrlDispatcher "aiohttp.web.UrlDispatcher") the property contains
        [`UrlMappingMatchInfo`](#aiohttp.web.UrlMappingMatchInfo "aiohttp.web.UrlMappingMatchInfo") instance.

    app[¶](#aiohttp.web.Request.app "Link to this definition")
    :   An [`Application`](#aiohttp.web.Application "aiohttp.web.Application") instance used to call [request handler](web_quickstart.html#aiohttp-web-handler), Read-only property.

    config\_dict[¶](#aiohttp.web.Request.config_dict "Link to this definition")
    :   A [`aiohttp.ChainMapProxy`](structures.html#aiohttp.ChainMapProxy "aiohttp.ChainMapProxy") instance for mapping all properties
        from the current application returned by [`app`](#aiohttp.web.Request.app "aiohttp.web.Request.app") property
        and all its parents.

        See also

        [Application’s config](web_advanced.html#aiohttp-web-data-sharing-app-config)

        Added in version 3.2.

    Note

    You should never create the [`Request`](#aiohttp.web.Request "aiohttp.web.Request") instance manually
    – [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") does it for you. But
    [`clone()`](#aiohttp.web.BaseRequest.clone "aiohttp.web.BaseRequest.clone") may be used for cloning *modified*
    request copy with changed *path*, *method* etc.

## Response classes[¶](#response-classes "Link to this heading")

For now, [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") has three classes for the *HTTP response*:
[`StreamResponse`](#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse"), [`Response`](#aiohttp.web.Response "aiohttp.web.Response") and [`FileResponse`](#aiohttp.web.FileResponse "aiohttp.web.FileResponse").

Usually you need to use the second one. [`StreamResponse`](#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse") is
intended for streaming data, while [`Response`](#aiohttp.web.Response "aiohttp.web.Response") contains *HTTP
BODY* as an attribute and sends own content as single piece with the
correct *Content-Length HTTP header*.

For sake of design decisions [`Response`](#aiohttp.web.Response "aiohttp.web.Response") is derived from
[`StreamResponse`](#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse") parent class.

The response supports *keep-alive* handling out-of-the-box if
*request* supports it.

You can disable *keep-alive* by [`force_close()`](#aiohttp.web.StreamResponse.force_close "aiohttp.web.StreamResponse.force_close") though.

The common case for sending an answer from
[web-handler](web_quickstart.html#aiohttp-web-handler) is returning a
[`Response`](#aiohttp.web.Response "aiohttp.web.Response") instance:

```
async def handler(request):
    return Response(text="All right!")
```

Response classes are [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") like objects,
allowing them to be used for [sharing
data](web_advanced.html#aiohttp-web-data-sharing) among [Middlewares](web_advanced.html#aiohttp-web-middlewares)
and [Signals](web_advanced.html#aiohttp-web-signals) handlers:

```
resp['key'] = value
```

Added in version 3.0: Dict-like interface support.

class aiohttp.web.StreamResponse(*\**, *status=200*, *reason=None*)[[source]](_modules/aiohttp/web_response.html#StreamResponse)[¶](#aiohttp.web.StreamResponse "Link to this definition")
:   The base class for the *HTTP response* handling.

    Contains methods for setting *HTTP response headers*, *cookies*,
    *response status code*, writing *HTTP response BODY* and so on.

    The most important thing you should know about *response* — it
    is *Finite State Machine*.

    That means you can do any manipulations with *headers*, *cookies*
    and *status code* only before [`prepare()`](#aiohttp.web.StreamResponse.prepare "aiohttp.web.StreamResponse.prepare") coroutine is called.

    Once you call [`prepare()`](#aiohttp.web.StreamResponse.prepare "aiohttp.web.StreamResponse.prepare") any change of
    the *HTTP header* part will raise [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") exception.

    Any [`write()`](#aiohttp.web.StreamResponse.write "aiohttp.web.StreamResponse.write") call after [`write_eof()`](#aiohttp.web.StreamResponse.write_eof "aiohttp.web.StreamResponse.write_eof") is also forbidden.

    Parameters:
    :   * **status** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – HTTP status code, `200` by default.
        * **reason** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – HTTP reason. If param is `None` reason will be
          calculated basing on *status*
          parameter. Otherwise pass [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") with
          arbitrary *status* explanation..

    prepared[¶](#aiohttp.web.StreamResponse.prepared "Link to this definition")
    :   Read-only [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") property, `True` if [`prepare()`](#aiohttp.web.StreamResponse.prepare "aiohttp.web.StreamResponse.prepare") has
        been called, `False` otherwise.

    task[¶](#aiohttp.web.StreamResponse.task "Link to this definition")
    :   A task that serves HTTP request handling.

        May be useful for graceful shutdown of long-running requests
        (streaming, long polling or web-socket).

    status[¶](#aiohttp.web.StreamResponse.status "Link to this definition")
    :   Read-only property for *HTTP response status code*, [`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)").

        `200` (OK) by default.

    reason[¶](#aiohttp.web.StreamResponse.reason "Link to this definition")
    :   Read-only property for *HTTP response reason*, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)").

    set\_status(*status*, *reason=None*)[[source]](_modules/aiohttp/web_response.html#StreamResponse.set_status)[¶](#aiohttp.web.StreamResponse.set_status "Link to this definition")
    :   Set [`status`](#aiohttp.web.StreamResponse.status "aiohttp.web.StreamResponse.status") and [`reason`](#aiohttp.web.StreamResponse.reason "aiohttp.web.StreamResponse.reason").

        *reason* value is auto calculated if not specified (`None`).

    keep\_alive[¶](#aiohttp.web.StreamResponse.keep_alive "Link to this definition")
    :   Read-only property, copy of [`aiohttp.web.BaseRequest.keep_alive`](#aiohttp.web.BaseRequest.keep_alive "aiohttp.web.BaseRequest.keep_alive") by default.

        Can be switched to `False` by [`force_close()`](#aiohttp.web.StreamResponse.force_close "aiohttp.web.StreamResponse.force_close") call.

    force\_close()[[source]](_modules/aiohttp/web_response.html#StreamResponse.force_close)[¶](#aiohttp.web.StreamResponse.force_close "Link to this definition")
    :   Disable [`keep_alive`](#aiohttp.web.StreamResponse.keep_alive "aiohttp.web.StreamResponse.keep_alive") for connection. There are no ways to
        enable it back.

    compression[¶](#aiohttp.web.StreamResponse.compression "Link to this definition")
    :   Read-only [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") property, `True` if compression is enabled.

        `False` by default.

        See also

        [`enable_compression()`](#aiohttp.web.StreamResponse.enable_compression "aiohttp.web.StreamResponse.enable_compression")

    enable\_compression(*force=None*, *strategy=None*)[[source]](_modules/aiohttp/web_response.html#StreamResponse.enable_compression)[¶](#aiohttp.web.StreamResponse.enable_compression "Link to this definition")
    :   Enable compression.

        When *force* is unset compression encoding is selected based on
        the request’s *Accept-Encoding* header.

        *Accept-Encoding* is not checked if *force* is set to a
        [`ContentCoding`](#aiohttp.web.ContentCoding "aiohttp.web.ContentCoding").

        *strategy* accepts a [`zlib`](https://docs.python.org/3/library/zlib.html#module-zlib "(in Python v3.14)") compression strategy.
        See [`zlib.compressobj()`](https://docs.python.org/3/library/zlib.html#zlib.compressobj "(in Python v3.14)") for possible values, or refer to the
        docs for the zlib of your using, should you use [`aiohttp.set_zlib_backend()`](client_reference.html#aiohttp.set_zlib_backend "aiohttp.set_zlib_backend")
        to change zlib backend. If `None`, the default value adopted by
        your zlib backend will be used where applicable.

        See also

        [`compression`](#aiohttp.web.StreamResponse.compression "aiohttp.web.StreamResponse.compression")

    chunked[¶](#aiohttp.web.StreamResponse.chunked "Link to this definition")
    :   Read-only property, indicates if chunked encoding is on.

        Can be enabled by [`enable_chunked_encoding()`](#aiohttp.web.StreamResponse.enable_chunked_encoding "aiohttp.web.StreamResponse.enable_chunked_encoding") call.

        See also

        [`enable_chunked_encoding`](#aiohttp.web.StreamResponse.enable_chunked_encoding "aiohttp.web.StreamResponse.enable_chunked_encoding")

    enable\_chunked\_encoding()[[source]](_modules/aiohttp/web_response.html#StreamResponse.enable_chunked_encoding)[¶](#aiohttp.web.StreamResponse.enable_chunked_encoding "Link to this definition")
    :   Enables [`chunked`](#aiohttp.web.StreamResponse.chunked "aiohttp.web.StreamResponse.chunked") encoding for response. There are no ways to
        disable it back. With enabled [`chunked`](#aiohttp.web.StreamResponse.chunked "aiohttp.web.StreamResponse.chunked") encoding each [`write()`](#aiohttp.web.StreamResponse.write "aiohttp.web.StreamResponse.write")
        operation encoded in separate chunk.

        Warning

        chunked encoding can be enabled for `HTTP/1.1` only.

        Setting up both [`content_length`](#aiohttp.web.StreamResponse.content_length "aiohttp.web.StreamResponse.content_length") and chunked
        encoding is mutually exclusive.

        See also

        [`chunked`](#aiohttp.web.StreamResponse.chunked "aiohttp.web.StreamResponse.chunked")

    headers[¶](#aiohttp.web.StreamResponse.headers "Link to this definition")
    :   [`CIMultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)") instance
        for *outgoing* *HTTP headers*.

    cookies[¶](#aiohttp.web.StreamResponse.cookies "Link to this definition")
    :   An instance of [`http.cookies.SimpleCookie`](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie "(in Python v3.14)") for *outgoing* cookies.

        Warning

        Direct setting up *Set-Cookie* header may be overwritten by
        explicit calls to cookie manipulation.

        We are encourage using of [`cookies`](#aiohttp.web.StreamResponse.cookies "aiohttp.web.StreamResponse.cookies") and
        [`set_cookie()`](#aiohttp.web.StreamResponse.set_cookie "aiohttp.web.StreamResponse.set_cookie"), [`del_cookie()`](#aiohttp.web.StreamResponse.del_cookie "aiohttp.web.StreamResponse.del_cookie") for cookie
        manipulations.

    set\_cookie(*name*, *value*, *\**, *path='/'*, *expires=None*, *domain=None*, *max\_age=None*, *secure=None*, *httponly=None*, *version=None*, *samesite=None*, *partitioned=None*)[[source]](_modules/aiohttp/web_response.html#StreamResponse.set_cookie)[¶](#aiohttp.web.StreamResponse.set_cookie "Link to this definition")
    :   Convenient way for setting [`cookies`](#aiohttp.web.StreamResponse.cookies "aiohttp.web.StreamResponse.cookies"), allows to specify
        some additional properties like *max\_age* in a single call.

        Parameters:
        :   * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – cookie name
            * **value** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – cookie value (will be converted to
              [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") if value has another type).
            * **expires** – expiration date (optional)
            * **domain** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – cookie domain (optional)
            * **max\_age** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – defines the lifetime of the cookie, in
              seconds. The delta-seconds value is a
              decimal non- negative integer. After
              delta-seconds seconds elapse, the client
              should discard the cookie. A value of zero
              means the cookie should be discarded
              immediately. (optional)
            * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – specifies the subset of URLs to
              which this cookie applies. (optional, `'/'` by default)
            * **secure** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – attribute (with no value) directs
              the user agent to use only (unspecified)
              secure means to contact the origin server
              whenever it sends back this cookie.
              The user agent (possibly under the user’s
              control) may determine what level of
              security it considers appropriate for
              “secure” cookies. The *secure* should be
              considered security advice from the server
              to the user agent, indicating that it is in
              the session’s interest to protect the cookie
              contents. (optional)
            * **httponly** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – `True` if the cookie HTTP only (optional)
            * **version** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – a decimal integer, identifies to which
              version of the state management
              specification the cookie
              conforms. (optional)
            * **samesite** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

              Asserts that a cookie must not be sent with
              cross-origin requests, providing some protection
              against cross-site request forgery attacks.
              Generally the value should be one of: `None`,
              `Lax` or `Strict`. (optional)

              > Added in version 3.7.
            * **partitioned** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

              `True` to set a partitioned cookie.
              Available in Python 3.14+. (optional)

              > Added in version 3.12.

        Warning

        In HTTP version 1.1, `expires` was deprecated and replaced with
        the easier-to-use `max-age`, but Internet Explorer (IE6, IE7,
        and IE8) **does not** support `max-age`.

    del\_cookie(*name*, *\**, *path='/'*, *domain=None*)[[source]](_modules/aiohttp/web_response.html#StreamResponse.del_cookie)[¶](#aiohttp.web.StreamResponse.del_cookie "Link to this definition")
    :   Deletes cookie.

        Parameters:
        :   * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – cookie name
            * **domain** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – optional cookie domain
            * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – optional cookie path, `'/'` by default

    content\_length[¶](#aiohttp.web.StreamResponse.content_length "Link to this definition")
    :   *Content-Length* for outgoing response.

    content\_type[¶](#aiohttp.web.StreamResponse.content_type "Link to this definition")
    :   *Content* part of *Content-Type* for outgoing response.

    charset[¶](#aiohttp.web.StreamResponse.charset "Link to this definition")
    :   *Charset* aka *encoding* part of *Content-Type* for outgoing response.

        The value converted to lower-case on attribute assigning.

    last\_modified[¶](#aiohttp.web.StreamResponse.last_modified "Link to this definition")
    :   *Last-Modified* header for outgoing response.

        This property accepts raw [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") values,
        [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime "(in Python v3.14)") objects, Unix timestamps specified
        as an [`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") or a [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)") object, and the
        value `None` to unset the header.

    etag[¶](#aiohttp.web.StreamResponse.etag "Link to this definition")
    :   *ETag* header for outgoing response.

        This property accepts raw [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") values, [`ETag`](client_reference.html#aiohttp.ETag "aiohttp.ETag")
        objects and the value `None` to unset the header.

        In case of [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") input, etag is considered as strong by default.

        **Do not** use double quotes `"` in the etag value,
        they will be added automatically.

        Added in version 3.8.

    async prepare(*request*)[[source]](_modules/aiohttp/web_response.html#StreamResponse.prepare)[¶](#aiohttp.web.StreamResponse.prepare "Link to this definition")
    :   Parameters:
        :   **request** ([*aiohttp.web.Request*](#aiohttp.web.Request "aiohttp.web.Request")) – HTTP request object, that the
            response answers.

        Send *HTTP header*. You should not change any header data after
        calling this method.

        The coroutine calls [`on_response_prepare`](#aiohttp.web.Application.on_response_prepare "aiohttp.web.Application.on_response_prepare")
        signal handlers after default headers have been computed and directly
        before headers are sent.

    async write(*data*)[[source]](_modules/aiohttp/web_response.html#StreamResponse.write)[¶](#aiohttp.web.StreamResponse.write "Link to this definition")
    :   Send byte-ish data as the part of *response BODY*:

        ```
        await resp.write(data)
        ```

        [`prepare()`](#aiohttp.web.StreamResponse.prepare "aiohttp.web.StreamResponse.prepare") must be invoked before the call.

        Raises [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") if data is not [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)"),
        [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)") or [`memoryview`](https://docs.python.org/3/library/stdtypes.html#memoryview "(in Python v3.14)") instance.

        Raises [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") if [`prepare()`](#aiohttp.web.StreamResponse.prepare "aiohttp.web.StreamResponse.prepare") has not been called.

        Raises [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") if [`write_eof()`](#aiohttp.web.StreamResponse.write_eof "aiohttp.web.StreamResponse.write_eof") has been called.

    async write\_eof()[[source]](_modules/aiohttp/web_response.html#StreamResponse.write_eof)[¶](#aiohttp.web.StreamResponse.write_eof "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") *may* be called as a mark of the
        *HTTP response* processing finish.

        *Internal machinery* will call this method at the end of
        the request processing if needed.

        After [`write_eof()`](#aiohttp.web.StreamResponse.write_eof "aiohttp.web.StreamResponse.write_eof") call any manipulations with the *response*
        object are forbidden.

class aiohttp.web.Response(*\**, *body=None*, *status=200*, *reason=None*, *text=None*, *headers=None*, *content\_type=None*, *charset=None*, *zlib\_executor\_size=sentinel*, *zlib\_executor=None*)[[source]](_modules/aiohttp/web_response.html#Response)[¶](#aiohttp.web.Response "Link to this definition")
:   The most usable response class, inherited from [`StreamResponse`](#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse").

    Accepts *body* argument for setting the *HTTP response BODY*.

    The actual [`body`](#aiohttp.web.Response.body "aiohttp.web.Response.body") sending happens in overridden
    [`write_eof()`](#aiohttp.web.StreamResponse.write_eof "aiohttp.web.StreamResponse.write_eof").

    Parameters:
    :   * **body** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")) – response’s BODY
        * **status** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – HTTP status code, 200 OK by default.
        * **headers** ([*collections.abc.Mapping*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)")) – HTTP headers that should be added to
          response’s ones.
        * **text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – response’s BODY
        * **content\_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – response’s content type. `'text/plain'`
          if *text* is passed also,
          `'application/octet-stream'` otherwise.
        * **charset** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – response’s charset. `'utf-8'` if *text* is
          passed also, `None` otherwise.
        * **zlib\_executor\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          length in bytes which will trigger zlib compression
          :   of body to happen in an executor

          Added in version 3.5.
        * **zlib\_executor** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          executor to use for zlib compression

          Added in version 3.5.

    body[¶](#aiohttp.web.Response.body "Link to this definition")
    :   Read-write attribute for storing response’s content aka BODY,
        [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)").

        Assigning [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") to [`body`](#aiohttp.web.Response.body "aiohttp.web.Response.body") will make the [`body`](#aiohttp.web.Response.body "aiohttp.web.Response.body")
        type of `aiohttp.payload.StringPayload`, which tries to encode
        the given data based on *Content-Type* HTTP header, while defaulting
        to `UTF-8`.

    text[¶](#aiohttp.web.Response.text "Link to this definition")
    :   Read-write attribute for storing response’s
        `body`, represented as [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)").

class aiohttp.web.FileResponse(*\**, *path*, *chunk\_size=256 \* 1024*, *status=200*, *reason=None*, *headers=None*)[[source]](_modules/aiohttp/web_fileresponse.html#FileResponse)[¶](#aiohttp.web.FileResponse "Link to this definition")
:   The response class used to send files, inherited from [`StreamResponse`](#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse").

    Supports the `Content-Range` and `If-Range` HTTP Headers in requests.

    The actual `body` sending happens in overridden [`prepare()`](#aiohttp.web.StreamResponse.prepare "aiohttp.web.StreamResponse.prepare").

    Parameters:
    :   * **path** – Path to file. Accepts both [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") and [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)").
        * **chunk\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Chunk size in bytes which will be passed into
          [`io.RawIOBase.read()`](https://docs.python.org/3/library/io.html#io.RawIOBase.read "(in Python v3.14)") in the event that the
          `sendfile` system call is not supported.
        * **status** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – HTTP status code, `200` by default.
        * **reason** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – HTTP reason. If param is `None` reason will be
          calculated basing on *status*
          parameter. Otherwise pass [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") with
          arbitrary *status* explanation..
        * **headers** ([*collections.abc.Mapping*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)")) – HTTP headers that should be added to
          response’s ones. The `Content-Type` response header
          will be overridden if provided.

class aiohttp.web.WebSocketResponse(*\**, *timeout=10.0*, *receive\_timeout=None*, *autoclose=True*, *autoping=True*, *heartbeat=None*, *protocols=()*, *compress=True*, *max\_msg\_size=4194304*, *writer\_limit=65536*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse)[¶](#aiohttp.web.WebSocketResponse "Link to this definition")
:   Class for handling server-side websockets, inherited from
    [`StreamResponse`](#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse").

    After starting (by [`prepare()`](#aiohttp.web.WebSocketResponse.prepare "aiohttp.web.WebSocketResponse.prepare") call) the response you
    cannot use [`write()`](#aiohttp.web.StreamResponse.write "aiohttp.web.StreamResponse.write") method but should to
    communicate with websocket client by [`send_str()`](#aiohttp.web.WebSocketResponse.send_str "aiohttp.web.WebSocketResponse.send_str"),
    [`receive()`](#aiohttp.web.WebSocketResponse.receive "aiohttp.web.WebSocketResponse.receive") and others.

    To enable back-pressure from slow websocket clients treat methods
    [`ping()`](#aiohttp.web.WebSocketResponse.ping "aiohttp.web.WebSocketResponse.ping"), [`pong()`](#aiohttp.web.WebSocketResponse.pong "aiohttp.web.WebSocketResponse.pong"), [`send_str()`](#aiohttp.web.WebSocketResponse.send_str "aiohttp.web.WebSocketResponse.send_str"),
    [`send_bytes()`](#aiohttp.web.WebSocketResponse.send_bytes "aiohttp.web.WebSocketResponse.send_bytes"), [`send_json()`](#aiohttp.web.WebSocketResponse.send_json "aiohttp.web.WebSocketResponse.send_json"), [`send_frame()`](#aiohttp.web.WebSocketResponse.send_frame "aiohttp.web.WebSocketResponse.send_frame") as coroutines.
    By default write buffer size is set to 64k.

    Parameters:
    :   * **autoping** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Automatically send
          [`PONG`](websocket_utilities.html#aiohttp.WSMsgType.PONG "aiohttp.WSMsgType.PONG") on
          [`PING`](websocket_utilities.html#aiohttp.WSMsgType.PING "aiohttp.WSMsgType.PING")
          message from client, and handle
          [`PONG`](websocket_utilities.html#aiohttp.WSMsgType.PONG "aiohttp.WSMsgType.PONG")
          responses from client.
          Note that server does not send
          [`PING`](websocket_utilities.html#aiohttp.WSMsgType.PING "aiohttp.WSMsgType.PING")
          requests, you need to do this explicitly
          using [`ping()`](#aiohttp.web.WebSocketResponse.ping "aiohttp.web.WebSocketResponse.ping") method.
        * **heartbeat** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Send ping message every heartbeat
          seconds and wait pong response, close
          connection if pong response is not
          received. The timer is reset on any data reception.
        * **timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Timeout value for the `close`
          operation. After sending the close websocket message,
          `close` waits for `timeout` seconds for a response.
          Default value is `10.0` (10 seconds for `close`
          operation)
        * **receive\_timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Timeout value for receive
          operations. Default value is [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")
          (no timeout for receive operation)
        * **compress** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Enable per-message deflate extension support.
          [`False`](https://docs.python.org/3/library/constants.html#False "(in Python v3.14)") for disabled, default value is [`True`](https://docs.python.org/3/library/constants.html#True "(in Python v3.14)").
        * **max\_msg\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          maximum size of read websocket message, 4
          :   MB by default. To disable the size limit use `0`.

          Added in version 3.3.
        * **autoclose** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Close connection when the client sends
          a [`CLOSE`](websocket_utilities.html#aiohttp.WSMsgType.CLOSE "aiohttp.WSMsgType.CLOSE") message,
          `True` by default. If set to `False`,
          the connection is not closed and the
          caller is responsible for calling
          `request.transport.close()` to avoid
          leaking resources.
        * **writer\_limit** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          maximum size of write buffer, 64 KB by default.
          :   Once the buffer is full, the websocket will pause
              to drain the buffer.

          Added in version 3.11.

    The class supports `async for` statement for iterating over
    incoming messages:

    ```
    ws = web.WebSocketResponse()
    await ws.prepare(request)

        async for msg in ws:
            print(msg.data)
    ```

    async prepare(*request*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.prepare)[¶](#aiohttp.web.WebSocketResponse.prepare "Link to this definition")
    :   Starts websocket. After the call you can use websocket methods.

        Parameters:
        :   **request** ([*aiohttp.web.Request*](#aiohttp.web.Request "aiohttp.web.Request")) – HTTP request object, that the
            response answers.

        Raises:
        :   [**HTTPException**](#aiohttp.web.HTTPException "aiohttp.web.HTTPException") – if websocket handshake has failed.

    can\_prepare(*request*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.can_prepare)[¶](#aiohttp.web.WebSocketResponse.can_prepare "Link to this definition")
    :   Performs checks for *request* data to figure out if websocket
        can be started on the request.

        If [`can_prepare()`](#aiohttp.web.WebSocketResponse.can_prepare "aiohttp.web.WebSocketResponse.can_prepare") call is success then [`prepare()`](#aiohttp.web.WebSocketResponse.prepare "aiohttp.web.WebSocketResponse.prepare") will
        success too.

        Parameters:
        :   **request** ([*aiohttp.web.Request*](#aiohttp.web.Request "aiohttp.web.Request")) – HTTP request object, that the
            response answers.

        Returns:
        :   [`WebSocketReady`](#aiohttp.web.WebSocketReady "aiohttp.web.WebSocketReady") instance.

            [`WebSocketReady.ok`](#aiohttp.web.WebSocketReady.ok "aiohttp.web.WebSocketReady.ok") is
            `True` on success, [`WebSocketReady.protocol`](#aiohttp.web.WebSocketReady.protocol "aiohttp.web.WebSocketReady.protocol") is
            websocket subprotocol which is passed by client and
            accepted by server (one of *protocols* sequence from
            [`WebSocketResponse`](#aiohttp.web.WebSocketResponse "aiohttp.web.WebSocketResponse") ctor).
            [`WebSocketReady.protocol`](#aiohttp.web.WebSocketReady.protocol "aiohttp.web.WebSocketReady.protocol") may be `None` if
            client and server subprotocols are not overlapping.

        Note

        The method never raises exception.

    closed[¶](#aiohttp.web.WebSocketResponse.closed "Link to this definition")
    :   Read-only property, `True` if connection has been closed or in process
        of closing.
        [`CLOSE`](websocket_utilities.html#aiohttp.WSMsgType.CLOSE "aiohttp.WSMsgType.CLOSE") message has been received from peer.

    prepared[¶](#aiohttp.web.WebSocketResponse.prepared "Link to this definition")
    :   Read-only [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") property, `True` if [`prepare()`](#aiohttp.web.WebSocketResponse.prepare "aiohttp.web.WebSocketResponse.prepare") has
        been called, `False` otherwise.

    close\_code[¶](#aiohttp.web.WebSocketResponse.close_code "Link to this definition")
    :   Read-only property, close code from peer. It is set to `None` on
        opened connection.

    ws\_protocol[¶](#aiohttp.web.WebSocketResponse.ws_protocol "Link to this definition")
    :   Websocket *subprotocol* chosen after `start()` call.

        May be `None` if server and client protocols are
        not overlapping.

    get\_extra\_info(*name*, *default=None*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.get_extra_info)[¶](#aiohttp.web.WebSocketResponse.get_extra_info "Link to this definition")
    :   Reads optional extra information from the writer’s transport.
        If no value associated with `name` is found, `default` is returned.

        See [`asyncio.BaseTransport.get_extra_info()`](https://docs.python.org/3/library/asyncio-protocol.html#asyncio.BaseTransport.get_extra_info "(in Python v3.14)")

        Parameters:
        :   * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – The key to look up in the transport extra information.
            * **default** – Default value to be used when no value for `name` is
              found (default is `None`).

    exception()[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.exception)[¶](#aiohttp.web.WebSocketResponse.exception "Link to this definition")
    :   Returns last occurred exception or None.

    async ping(*message=b''*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.ping)[¶](#aiohttp.web.WebSocketResponse.ping "Link to this definition")
    :   Send [`PING`](websocket_utilities.html#aiohttp.WSMsgType.PING "aiohttp.WSMsgType.PING") to peer.

        Parameters:
        :   **message** – optional payload of *ping* message,
            [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") (converted to *UTF-8* encoded bytes)
            or [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)").

        Raises:
        :   * [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – if the connections is not started.
            * [**aiohttp.ClientConnectionResetError**](client_reference.html#aiohttp.ClientConnectionResetError "aiohttp.ClientConnectionResetError") – if the connection is closing.

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)")

    async pong(*message=b''*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.pong)[¶](#aiohttp.web.WebSocketResponse.pong "Link to this definition")
    :   Send *unsolicited* [`PONG`](websocket_utilities.html#aiohttp.WSMsgType.PONG "aiohttp.WSMsgType.PONG") to peer.

        Parameters:
        :   **message** – optional payload of *pong* message,
            [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") (converted to *UTF-8* encoded bytes)
            or [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)").

        Raises:
        :   * [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – if the connections is not started.
            * [**aiohttp.ClientConnectionResetError**](client_reference.html#aiohttp.ClientConnectionResetError "aiohttp.ClientConnectionResetError") – if the connection is closing.

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)")

    async send\_str(*data*, *compress=None*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.send_str)[¶](#aiohttp.web.WebSocketResponse.send_str "Link to this definition")
    :   Send *data* to peer as [`TEXT`](websocket_utilities.html#aiohttp.WSMsgType.TEXT "aiohttp.WSMsgType.TEXT") message.

        Parameters:
        :   * **data** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – data to send.
            * **compress** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – sets specific level of compression for
              single message,
              `None` for not overriding per-socket setting.

        Raises:
        :   * [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – if the connection is not started.
            * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") – if data is not [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
            * [**aiohttp.ClientConnectionResetError**](client_reference.html#aiohttp.ClientConnectionResetError "aiohttp.ClientConnectionResetError") – if the connection is closing.

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)"),
        *compress* parameter added.

    async send\_bytes(*data*, *compress=None*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.send_bytes)[¶](#aiohttp.web.WebSocketResponse.send_bytes "Link to this definition")
    :   Send *data* to peer as [`BINARY`](websocket_utilities.html#aiohttp.WSMsgType.BINARY "aiohttp.WSMsgType.BINARY") message.

        Parameters:
        :   * **data** – data to send.
            * **compress** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – sets specific level of compression for
              single message,
              `None` for not overriding per-socket setting.

        Raises:
        :   * [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – if the connection is not started.
            * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") – if data is not [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)"),
              [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)") or [`memoryview`](https://docs.python.org/3/library/stdtypes.html#memoryview "(in Python v3.14)").
            * [**aiohttp.ClientConnectionResetError**](client_reference.html#aiohttp.ClientConnectionResetError "aiohttp.ClientConnectionResetError") – if the connection is closing.

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)"),
        *compress* parameter added.

    async send\_json(*data*, *compress=None*, *\**, *dumps=json.dumps*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.send_json)[¶](#aiohttp.web.WebSocketResponse.send_json "Link to this definition")
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
        :   * [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – if the connection is not started.
            * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)") – if data is not serializable object
            * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") – if value returned by `dumps` param is not [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
            * [**aiohttp.ClientConnectionResetError**](client_reference.html#aiohttp.ClientConnectionResetError "aiohttp.ClientConnectionResetError") – if the connection is closing.

        Changed in version 3.0: The method is converted into [coroutine](https://docs.python.org/3/glossary.html#term-coroutine "(in Python v3.14)"),
        *compress* parameter added.

    async send\_frame(*message*, *opcode*, *compress=None*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.send_frame)[¶](#aiohttp.web.WebSocketResponse.send_frame "Link to this definition")
    :   Send a [`WSMsgType`](websocket_utilities.html#aiohttp.WSMsgType "aiohttp.WSMsgType") message *message* to peer.

        This method is low-level and should be used with caution as it
        only accepts bytes which must conform to the correct message type
        for *message*.

        It is recommended to use the [`send_str()`](#aiohttp.web.WebSocketResponse.send_str "aiohttp.web.WebSocketResponse.send_str"), [`send_bytes()`](#aiohttp.web.WebSocketResponse.send_bytes "aiohttp.web.WebSocketResponse.send_bytes")
        or [`send_json()`](#aiohttp.web.WebSocketResponse.send_json "aiohttp.web.WebSocketResponse.send_json") methods instead of this method.

        The primary use case for this method is to send bytes that are
        have already been encoded without having to decode and
        re-encode them.

        Parameters:
        :   * **message** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")) – message to send.
            * **opcode** ([*WSMsgType*](websocket_utilities.html#aiohttp.WSMsgType "aiohttp.WSMsgType")) – opcode of the message.
            * **compress** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – sets specific level of compression for
              single message,
              `None` for not overriding per-socket setting.

        Raises:
        :   * [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – if the connection is not started.
            * [**aiohttp.ClientConnectionResetError**](client_reference.html#aiohttp.ClientConnectionResetError "aiohttp.ClientConnectionResetError") – if the connection is closing.

        Added in version 3.11.

    async close(*\**, *code=WSCloseCode.OK*, *message=b''*, *drain=True*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.close)[¶](#aiohttp.web.WebSocketResponse.close "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that initiates closing
        handshake by sending [`CLOSE`](websocket_utilities.html#aiohttp.WSMsgType.CLOSE "aiohttp.WSMsgType.CLOSE") message.

        It is safe to call close() from different task.

        Parameters:
        :   * **code** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – closing code. See also [`WSCloseCode`](websocket_utilities.html#aiohttp.WSCloseCode "aiohttp.WSCloseCode").
            * **message** – optional payload of *close* message,
              [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") (converted to *UTF-8* encoded bytes)
              or [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)").
            * **drain** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – drain outgoing buffer before closing connection.

        Raises:
        :   [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – if connection is not started

    async receive(*timeout=None*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.receive)[¶](#aiohttp.web.WebSocketResponse.receive "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that waits upcoming *data*
        message from peer and returns it.

        The coroutine implicitly handles
        [`PING`](websocket_utilities.html#aiohttp.WSMsgType.PING "aiohttp.WSMsgType.PING"),
        [`PONG`](websocket_utilities.html#aiohttp.WSMsgType.PONG "aiohttp.WSMsgType.PONG") and
        [`CLOSE`](websocket_utilities.html#aiohttp.WSMsgType.CLOSE "aiohttp.WSMsgType.CLOSE") without returning the
        message.

        It process *ping-pong game* and performs *closing handshake* internally.

        Note

        Can only be called by the request handling task.

        Parameters:
        :   **timeout** –

            timeout for receive operation.

            timeout value overrides response`s receive\_timeout attribute.

        Returns:
        :   [`WSMessage`](websocket_utilities.html#aiohttp.WSMessage "aiohttp.WSMessage")

        Raises:
        :   [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – if connection is not started

    async receive\_str(*\**, *timeout=None*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.receive_str)[¶](#aiohttp.web.WebSocketResponse.receive_str "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that calls [`receive()`](#aiohttp.web.WebSocketResponse.receive "aiohttp.web.WebSocketResponse.receive") but
        also asserts the message type is [`TEXT`](websocket_utilities.html#aiohttp.WSMsgType.TEXT "aiohttp.WSMsgType.TEXT").

        Note

        Can only be called by the request handling task.

        Parameters:
        :   **timeout** –

            timeout for receive operation.

            timeout value overrides response`s receive\_timeout attribute.

        Return str:
        :   peer’s message content.

        Raises:
        :   [**aiohttp.WSMessageTypeError**](client_reference.html#aiohttp.WSMessageTypeError "aiohttp.WSMessageTypeError") – if message is not [`TEXT`](websocket_utilities.html#aiohttp.WSMsgType.TEXT "aiohttp.WSMsgType.TEXT").

    async receive\_bytes(*\**, *timeout=None*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.receive_bytes)[¶](#aiohttp.web.WebSocketResponse.receive_bytes "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that calls [`receive()`](#aiohttp.web.WebSocketResponse.receive "aiohttp.web.WebSocketResponse.receive") but
        also asserts the message type is
        [`BINARY`](websocket_utilities.html#aiohttp.WSMsgType.BINARY "aiohttp.WSMsgType.BINARY").

        Note

        Can only be called by the request handling task.

        Parameters:
        :   **timeout** –

            timeout for receive operation.

            timeout value overrides response`s receive\_timeout attribute.

        Return bytes:
        :   peer’s message content.

        Raises:
        :   [**aiohttp.WSMessageTypeError**](client_reference.html#aiohttp.WSMessageTypeError "aiohttp.WSMessageTypeError") – if message is not [`BINARY`](websocket_utilities.html#aiohttp.WSMsgType.BINARY "aiohttp.WSMsgType.BINARY").

    async receive\_json(*\**, *loads=json.loads*, *timeout=None*)[[source]](_modules/aiohttp/web_ws.html#WebSocketResponse.receive_json)[¶](#aiohttp.web.WebSocketResponse.receive_json "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that calls [`receive_str()`](#aiohttp.web.WebSocketResponse.receive_str "aiohttp.web.WebSocketResponse.receive_str") and loads the
        JSON string to a Python dict.

        Note

        Can only be called by the request handling task.

        Parameters:
        :   * **loads** ([*collections.abc.Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) – any [callable](glossary.html#term-callable) that accepts
              [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") and returns [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")
              with parsed JSON ([`json.loads()`](https://docs.python.org/3/library/json.html#json.loads "(in Python v3.14)") by
              default).
            * **timeout** –

              timeout for receive operation.

              timeout value overrides response`s receive\_timeout attribute.

        Return dict:
        :   loaded JSON content

        Raises:
        :   * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") – if message is [`BINARY`](websocket_utilities.html#aiohttp.WSMsgType.BINARY "aiohttp.WSMsgType.BINARY").
            * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)") – if message is not valid JSON.

See also

[WebSockets handling](web_quickstart.html#aiohttp-web-websockets)

class aiohttp.web.WebSocketReady[[source]](_modules/aiohttp/web_ws.html#WebSocketReady)[¶](#aiohttp.web.WebSocketReady "Link to this definition")
:   A named tuple for returning result from
    [`WebSocketResponse.can_prepare()`](#aiohttp.web.WebSocketResponse.can_prepare "aiohttp.web.WebSocketResponse.can_prepare").

    Has [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") check implemented, e.g.:

    ```
    if not await ws.can_prepare(...):
        cannot_start_websocket()
    ```

    ok[¶](#aiohttp.web.WebSocketReady.ok "Link to this definition")
    :   `True` if websocket connection can be established, `False`
        otherwise.

    protocol[¶](#aiohttp.web.WebSocketReady.protocol "Link to this definition")
    :   [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") represented selected websocket sub-protocol.

    See also

    [`WebSocketResponse.can_prepare()`](#aiohttp.web.WebSocketResponse.can_prepare "aiohttp.web.WebSocketResponse.can_prepare")

aiohttp.web.json\_response([*data*, ]*\**, *text=None*, *body=None*, *status=200*, *reason=None*, *headers=None*, *content\_type='application/json'*, *dumps=json.dumps*)[[source]](_modules/aiohttp/web_response.html#json_response)[¶](#aiohttp.web.json_response "Link to this definition")

Return [`Response`](#aiohttp.web.Response "aiohttp.web.Response") with predefined `'application/json'`
content type and *data* encoded by `dumps` parameter
([`json.dumps()`](https://docs.python.org/3/library/json.html#json.dumps "(in Python v3.14)") by default).

### HTTP Exceptions[¶](#http-exceptions "Link to this heading")

Errors can also be returned by raising a HTTP exception instance from within
the handler.

class aiohttp.web.HTTPException(*\**, *headers=None*, *reason=None*, *text=None*, *content\_type=None*)[[source]](_modules/aiohttp/web_exceptions.html#HTTPException)[¶](#aiohttp.web.HTTPException "Link to this definition")
:   Low-level HTTP failure.

    Parameters:
    :   * **headers** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") *or* [*multidict.CIMultiDict*](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)")) – headers for the response
        * **reason** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – reason included in the response
        * **text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – response’s body
        * **content\_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – response’s content type. This is passed through
          to the [`Response`](#aiohttp.web.Response "aiohttp.web.Response") initializer.

    Sub-classes of `HTTPException` exist for the standard HTTP response codes
    as described in [Exceptions](web_quickstart.html#aiohttp-web-exceptions) and the expected usage is to
    simply raise the appropriate exception type to respond with a specific HTTP
    response code.

    Since `HTTPException` is a sub-class of [`Response`](#aiohttp.web.Response "aiohttp.web.Response"), it contains the
    methods and properties that allow you to directly manipulate details of the
    response.

    status\_code[¶](#aiohttp.web.HTTPException.status_code "Link to this definition")
    :   HTTP status code for this exception class. This attribute is usually
        defined at the class level. `self.status_code` is passed to the
        [`Response`](#aiohttp.web.Response "aiohttp.web.Response") initializer.

## Application and Router[¶](#application-and-router "Link to this heading")

class aiohttp.web.Application(*\**, *logger=<default>*, *router=None*, *middlewares=()*, *handler\_args=None*, *client\_max\_size=1024\*\*2*, *loop=None*, *debug=...*)[[source]](_modules/aiohttp/web_app.html#Application)[¶](#aiohttp.web.Application "Link to this definition")
:   Application is a synonym for web-server.

    To get a fully working example, you have to make an *application*, register
    supported urls in the *router* and pass it to [`aiohttp.web.run_app()`](#aiohttp.web.run_app "aiohttp.web.run_app")
    or [`aiohttp.web.AppRunner`](#aiohttp.web.AppRunner "aiohttp.web.AppRunner").

    *Application* contains a *router* instance and a list of callbacks that
    will be called during application finishing.

    This class is a [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")-like object, so you can use it for
    [sharing data](web_advanced.html#aiohttp-web-data-sharing) globally by storing arbitrary
    properties for later access from a [handler](web_quickstart.html#aiohttp-web-handler) via the
    [`Request.app`](#aiohttp.web.Request.app "aiohttp.web.Request.app") property:

    ```
    app = Application()
    database = AppKey("database", AsyncEngine)
    app[database] = await create_async_engine(db_url)

    async def handler(request):
        async with request.app[database].begin() as conn:
            await conn.execute("DELETE * FROM table")
    ```

    Although it` is a [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")-like object, it can’t be duplicated like one
    using `copy()`.

    The class inherits [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)").

    Parameters:
    :   * **logger** –

          [`logging.Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "(in Python v3.14)") instance for storing application logs.

          By default the value is `logging.getLogger("aiohttp.web")`
        * **router** –

          [`aiohttp.abc.AbstractRouter`](abc.html#aiohttp.abc.AbstractRouter "aiohttp.abc.AbstractRouter") instance, the system
          :   creates [`UrlDispatcher`](#aiohttp.web.UrlDispatcher "aiohttp.web.UrlDispatcher") by default if
              *router* is `None`.

          Deprecated since version 3.3: The custom routers support is deprecated, the parameter will
          be removed in 4.0.
        * **middlewares** – [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of middleware factories, see
          [Middlewares](web_advanced.html#aiohttp-web-middlewares) for details.
        * **handler\_args** – dict-like object that overrides keyword arguments of
          [`Application.make_handler()`](#aiohttp.web.Application.make_handler "aiohttp.web.Application.make_handler")
        * **client\_max\_size** – client’s maximum size in a request, in
          bytes. If a POST request exceeds this
          value, it raises an
          HTTPRequestEntityTooLarge exception.
        * **loop** –

          event loop

          Deprecated since version 2.0: The parameter is deprecated. Loop is get set during freeze
          stage.
        * **debug** –

          Switches debug mode.

          Deprecated since version 3.5: Use asyncio [Debug Mode](https://docs.python.org/3/library/asyncio-dev.html#asyncio-debug-mode "(in Python v3.14)") instead.

    router[¶](#aiohttp.web.Application.router "Link to this definition")
    :   Read-only property that returns *router instance*.

    logger[¶](#aiohttp.web.Application.logger "Link to this definition")
    :   [`logging.Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "(in Python v3.14)") instance for storing application logs.

    loop[¶](#aiohttp.web.Application.loop "Link to this definition")
    :   [event loop](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio-event-loop "(in Python v3.14)") used for processing HTTP requests.

        Deprecated since version 3.5.

    debug[¶](#aiohttp.web.Application.debug "Link to this definition")
    :   Boolean value indicating whether the debug mode is turned on or off.

        Deprecated since version 3.5: Use asyncio [Debug Mode](https://docs.python.org/3/library/asyncio-dev.html#asyncio-debug-mode "(in Python v3.14)") instead.

    on\_response\_prepare[¶](#aiohttp.web.Application.on_response_prepare "Link to this definition")
    :   A [`Signal`](https://aiosignal.aio-libs.org/en/stable/#aiosignal.Signal "(in aiosignal v1.4)") that is fired near the end
        of [`StreamResponse.prepare()`](#aiohttp.web.StreamResponse.prepare "aiohttp.web.StreamResponse.prepare") with parameters *request* and
        *response*. It can be used, for example, to add custom headers to each
        response, or to modify the default headers computed by the application,
        directly before sending the headers to the client.

        Signal handlers should have the following signature:

        ```
        async def on_prepare(request, response):
            pass
        ```

        Note

        The headers are written immediately after these callbacks are run.
        Therefore, if you modify the content of the response, you may need to
        adjust the Content-Length header or similar to match. Aiohttp will
        not make any updates to the headers from this point.

    on\_startup[¶](#aiohttp.web.Application.on_startup "Link to this definition")
    :   A [`Signal`](https://aiosignal.aio-libs.org/en/stable/#aiosignal.Signal "(in aiosignal v1.4)") that is fired on application start-up.

        Subscribers may use the signal to run background tasks in the event
        loop along with the application’s request handler just after the
        application start-up.

        Signal handlers should have the following signature:

        ```
        async def on_startup(app):
            pass
        ```

        See also

        [Signals](web_advanced.html#aiohttp-web-signals).

    on\_shutdown[¶](#aiohttp.web.Application.on_shutdown "Link to this definition")
    :   A [`Signal`](https://aiosignal.aio-libs.org/en/stable/#aiosignal.Signal "(in aiosignal v1.4)") that is fired on application shutdown.

        Subscribers may use the signal for gracefully closing long running
        connections, e.g. websockets and data streaming.

        Signal handlers should have the following signature:

        ```
        async def on_shutdown(app):
            pass
        ```

        It’s up to end user to figure out which [web-handler](glossary.html#term-web-handler)s
        are still alive and how to finish them properly.

        We suggest keeping a list of long running handlers in
        [`Application`](#aiohttp.web.Application "aiohttp.web.Application") dictionary.

        See also

        [Graceful shutdown](web_advanced.html#aiohttp-web-graceful-shutdown) and [`on_cleanup`](#aiohttp.web.Application.on_cleanup "aiohttp.web.Application.on_cleanup").

    on\_cleanup[¶](#aiohttp.web.Application.on_cleanup "Link to this definition")
    :   A [`Signal`](https://aiosignal.aio-libs.org/en/stable/#aiosignal.Signal "(in aiosignal v1.4)") that is fired on application cleanup.

        Subscribers may use the signal for gracefully closing
        connections to database server etc.

        Signal handlers should have the following signature:

        ```
        async def on_cleanup(app):
            pass
        ```

        See also

        [Signals](web_advanced.html#aiohttp-web-signals) and [`on_shutdown`](#aiohttp.web.Application.on_shutdown "aiohttp.web.Application.on_shutdown").

    cleanup\_ctx[¶](#aiohttp.web.Application.cleanup_ctx "Link to this definition")
    :   A list of *context generators* for *startup*/*cleanup* handling.

        Signal handlers should have the following signature:

        ```
        async def context(app):
            # do startup stuff
            yield
            # do cleanup
        ```

        Added in version 3.1.

        See also

        [Cleanup Context](web_advanced.html#aiohttp-web-cleanup-ctx).

    add\_subapp(*prefix*, *subapp*)[[source]](_modules/aiohttp/web_app.html#Application.add_subapp)[¶](#aiohttp.web.Application.add_subapp "Link to this definition")
    :   Register nested sub-application under given path *prefix*.

        In resolving process if request’s path starts with *prefix* then
        further resolving is passed to *subapp*.

        Parameters:
        :   * **prefix** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – path’s prefix for the resource.
            * **subapp** ([*Application*](#aiohttp.web.Application "aiohttp.web.Application")) – nested application attached under *prefix*.

        Returns:
        :   a [`PrefixedSubAppResource`](#aiohttp.web.PrefixedSubAppResource "aiohttp.web.PrefixedSubAppResource") instance.

    add\_domain(*domain*, *subapp*)[[source]](_modules/aiohttp/web_app.html#Application.add_domain)[¶](#aiohttp.web.Application.add_domain "Link to this definition")
    :   Register nested sub-application that serves
        the domain name or domain name mask.

        In resolving process if request.headers[‘host’]
        matches the pattern *domain* then
        further resolving is passed to *subapp*.

        Warning

        Registering many domains using this method may cause performance
        issues with handler routing. If you have a substantial number of
        applications for different domains, you may want to consider
        using a reverse proxy (such as Nginx) to handle routing to
        different apps, rather that registering them as sub-applications.

        Parameters:
        :   * **domain** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – domain or mask of domain for the resource.
            * **subapp** ([*Application*](#aiohttp.web.Application "aiohttp.web.Application")) – nested application.

        Returns:
        :   a `MatchedSubAppResource` instance.

    add\_routes(*routes\_table*)[[source]](_modules/aiohttp/web_app.html#Application.add_routes)[¶](#aiohttp.web.Application.add_routes "Link to this definition")
    :   Register route definitions from *routes\_table*.

        The table is a [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") items or
        [`RouteTableDef`](#aiohttp.web.RouteTableDef "aiohttp.web.RouteTableDef").

        Returns:
        :   [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of registered [`AbstractRoute`](#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") instances.

        The method is a shortcut for
        `app.router.add_routes(routes_table)`, see also
        [`UrlDispatcher.add_routes()`](#aiohttp.web.UrlDispatcher.add_routes "aiohttp.web.UrlDispatcher.add_routes").

        Added in version 3.1.

        Changed in version 3.7: Return value updated from `None` to [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of
        [`AbstractRoute`](#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") instances.

    make\_handler(*loop=None*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_app.html#Application.make_handler)[¶](#aiohttp.web.Application.make_handler "Link to this definition")
    :   Creates HTTP protocol factory for handling requests.

        Parameters:
        :   * **loop** –

              [event loop](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio-event-loop "(in Python v3.14)") used
              for processing HTTP requests.

              If param is `None` [`asyncio.get_event_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_event_loop "(in Python v3.14)")
              used for getting default event loop.

              Deprecated since version 2.0.
            * **tcp\_keepalive** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Enable TCP Keep-Alive. Default: `True`.
            * **keepalive\_timeout** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Number of seconds before closing Keep-Alive
              connection. Default: `75` seconds (NGINX’s default value).
            * **logger** – Custom logger object. Default:
              `aiohttp.log.server_logger`.
            * **access\_log** – Custom logging object. Default:
              `aiohttp.log.access_logger`.
            * **access\_log\_class** – Class for access\_logger. Default:
              `aiohttp.helpers.AccessLogger`.
              Must to be a subclass of [`aiohttp.abc.AbstractAccessLogger`](abc.html#aiohttp.abc.AbstractAccessLogger "aiohttp.abc.AbstractAccessLogger").
            * **access\_log\_format** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Access log format string. Default:
              `helpers.AccessLogger.LOG_FORMAT`.
            * **max\_line\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Optional maximum header line size. Default:
              `8190`.
            * **max\_headers** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Optional maximum header size. Default: `32768`.
            * **max\_field\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Optional maximum header field size. Default:
              `8190`.
            * **lingering\_time** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Maximum time during which the server
              reads and ignores additional data coming from the client when
              lingering close is on. Use `0` to disable lingering on
              server channel closing.

        You should pass result of the method as *protocol\_factory* to
        `create_server()`, e.g.:

        ```
        loop = asyncio.get_event_loop()

        app = Application()

        # setup route table
        # app.router.add_route(...)

        await loop.create_server(app.make_handler(),
                                 '0.0.0.0', 8080)
        ```

        Deprecated since version 3.2: The method is deprecated and will be removed in future
        aiohttp versions. Please use [Application runners](web_advanced.html#aiohttp-web-app-runners) instead.

    async startup()[[source]](_modules/aiohttp/web_app.html#Application.startup)[¶](#aiohttp.web.Application.startup "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that will be called along with the
        application’s request handler.

        The purpose of the method is calling [`on_startup`](#aiohttp.web.Application.on_startup "aiohttp.web.Application.on_startup") signal
        handlers.

    async shutdown()[[source]](_modules/aiohttp/web_app.html#Application.shutdown)[¶](#aiohttp.web.Application.shutdown "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that should be called on
        server stopping but before [`cleanup()`](#aiohttp.web.Application.cleanup "aiohttp.web.Application.cleanup").

        The purpose of the method is calling [`on_shutdown`](#aiohttp.web.Application.on_shutdown "aiohttp.web.Application.on_shutdown") signal
        handlers.

    async cleanup()[[source]](_modules/aiohttp/web_app.html#Application.cleanup)[¶](#aiohttp.web.Application.cleanup "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that should be called on
        server stopping but after [`shutdown()`](#aiohttp.web.Application.shutdown "aiohttp.web.Application.shutdown").

        The purpose of the method is calling [`on_cleanup`](#aiohttp.web.Application.on_cleanup "aiohttp.web.Application.on_cleanup") signal
        handlers.

    Note

    Application object has [`router`](#aiohttp.web.Application.router "aiohttp.web.Application.router") attribute but has no
    `add_route()` method. The reason is: we want to support
    different router implementations (even maybe not url-matching
    based but traversal ones).

    For sake of that fact we have very trivial ABC for
    [`AbstractRouter`](abc.html#aiohttp.abc.AbstractRouter "aiohttp.abc.AbstractRouter"): it should have only
    [`aiohttp.abc.AbstractRouter.resolve()`](abc.html#aiohttp.abc.AbstractRouter.resolve "aiohttp.abc.AbstractRouter.resolve") coroutine.

    No methods for adding routes or route reversing (getting URL by
    route name). All those are router implementation details (but,
    sure, you need to deal with that methods after choosing the
    router for your application).

class aiohttp.web.AppKey(*name*, *t*)[[source]](_modules/aiohttp/helpers.html#AppKey)[¶](#aiohttp.web.AppKey "Link to this definition")
:   This class should be used for the keys in [`Application`](#aiohttp.web.Application "aiohttp.web.Application"). They
    provide a type-safe alternative to str keys when checking your code
    with a type checker (e.g. mypy). They also avoid name clashes with keys
    from different libraries etc.

    Parameters:
    :   * **name** – A name to help with debugging. This should be the same as
          the variable name (much like how [`typing.TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar "(in Python v3.14)")
          is used).
        * **t** – The type that should be used for the value in the dict (e.g.
          str, Iterator[int] etc.)

class aiohttp.web.Server[[source]](_modules/aiohttp/web_server.html#Server)[¶](#aiohttp.web.Server "Link to this definition")
:   A protocol factory compatible with
    `create_server()`.

    The class is responsible for creating HTTP protocol
    objects that can handle HTTP connections.

    connections[¶](#aiohttp.web.Server.connections "Link to this definition")
    :   List of all currently opened connections.

    requests\_count[¶](#aiohttp.web.Server.requests_count "Link to this definition")
    :   Amount of processed requests.

    async shutdown(*timeout*)[[source]](_modules/aiohttp/web_server.html#Server.shutdown)[¶](#aiohttp.web.Server.shutdown "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that should be called to close all opened
        connections.

class aiohttp.web.UrlDispatcher[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher)[¶](#aiohttp.web.UrlDispatcher "Link to this definition")
:   For dispatching URLs to [handlers](web_quickstart.html#aiohttp-web-handler)
    [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") uses *routers*, which is any object that implements
    [`AbstractRouter`](abc.html#aiohttp.abc.AbstractRouter "aiohttp.abc.AbstractRouter") interface.

    This class is a straightforward url-matching router, implementing
    [`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)") for access to *named routes*.

    [`Application`](#aiohttp.web.Application "aiohttp.web.Application") uses this class as
    [`router()`](#aiohttp.web.Application.router "aiohttp.web.Application.router") by default.

    Before running an [`Application`](#aiohttp.web.Application "aiohttp.web.Application") you should fill *route
    table* first by calling [`add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") and [`add_static()`](#aiohttp.web.UrlDispatcher.add_static "aiohttp.web.UrlDispatcher.add_static").

    [Handler](web_quickstart.html#aiohttp-web-handler) lookup is performed by iterating on
    added *routes* in FIFO order. The first matching *route* will be used
    to call the corresponding *handler*.

    If during route creation you specify *name* parameter the result is a
    *named route*.

    A *named route* can be retrieved by a `app.router[name]` call, checking for
    existence can be done with `name in app.router` etc.

    See also

    [Route classes](#aiohttp-web-route)

    add\_resource(*path*, *\**, *name=None*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_resource)[¶](#aiohttp.web.UrlDispatcher.add_resource "Link to this definition")
    :   Append a [resource](glossary.html#term-resource) to the end of route table.

        *path* may be either *constant* string like `'/a/b/c'` or
        *variable rule* like `'/a/{var}'` (see
        [handling variable paths](web_quickstart.html#aiohttp-web-variable-handler))

        Parameters:
        :   * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – resource path spec.
            * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – optional resource name.

        Returns:
        :   created resource instance ([`PlainResource`](#aiohttp.web.PlainResource "aiohttp.web.PlainResource") or
            [`DynamicResource`](#aiohttp.web.DynamicResource "aiohttp.web.DynamicResource")).

    add\_route(*method*, *path*, *handler*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_route)[¶](#aiohttp.web.UrlDispatcher.add_route "Link to this definition")
    :   Append [handler](web_quickstart.html#aiohttp-web-handler) to the end of route table.

        *path* may be either *constant* string like `'/a/b/c'` or
        :   *variable rule* like `'/a/{var}'` (see
            [handling variable paths](web_quickstart.html#aiohttp-web-variable-handler))

        Pay attention please: *handler* is converted to coroutine internally when
        it is a regular function.

        Parameters:
        :   * **method** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

              HTTP method for route. Should be one of
              `'GET'`, `'POST'`, `'PUT'`,
              `'DELETE'`, `'PATCH'`, `'HEAD'`,
              `'OPTIONS'` or `'*'` for any method.

              The parameter is case-insensitive, e.g. you
              can push `'get'` as well as `'GET'`.
            * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – route path. Should be started with slash (`'/'`).
            * **handler** ([*collections.abc.Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) – route handler.
            * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – optional route name.
            * **expect\_handler** ([*collections.abc.Coroutine*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Coroutine "(in Python v3.14)")) – optional *expect* header handler.

        Returns:
        :   new [`AbstractRoute`](#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") instance.

    add\_routes(*routes\_table*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_routes)[¶](#aiohttp.web.UrlDispatcher.add_routes "Link to this definition")
    :   Register route definitions from *routes\_table*.

        The table is a [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") items or
        [`RouteTableDef`](#aiohttp.web.RouteTableDef "aiohttp.web.RouteTableDef").

        Returns:
        :   [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of registered [`AbstractRoute`](#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") instances.

        Added in version 2.3.

        Changed in version 3.7: Return value updated from `None` to [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of
        [`AbstractRoute`](#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") instances.

    add\_get(*path*, *handler*, *\**, *name=None*, *allow\_head=True*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_get)[¶](#aiohttp.web.UrlDispatcher.add_get "Link to this definition")
    :   Shortcut for adding a GET handler. Calls the [`add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") with `method` equals to `'GET'`.

        If *allow\_head* is `True` (default) the route for method HEAD
        is added with the same handler as for GET.

        If *name* is provided the name for HEAD route is suffixed with
        `'-head'`. For example `router.add_get(path, handler,
        name='route')` call adds two routes: first for GET with name
        `'route'` and second for HEAD with name `'route-head'`.

    add\_post(*path*, *handler*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_post)[¶](#aiohttp.web.UrlDispatcher.add_post "Link to this definition")
    :   Shortcut for adding a POST handler. Calls the [`add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") with

        `method` equals to `'POST'`.

    add\_head(*path*, *handler*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_head)[¶](#aiohttp.web.UrlDispatcher.add_head "Link to this definition")
    :   Shortcut for adding a HEAD handler. Calls the [`add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") with `method` equals to `'HEAD'`.

    add\_put(*path*, *handler*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_put)[¶](#aiohttp.web.UrlDispatcher.add_put "Link to this definition")
    :   Shortcut for adding a PUT handler. Calls the [`add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") with `method` equals to `'PUT'`.

    add\_patch(*path*, *handler*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_patch)[¶](#aiohttp.web.UrlDispatcher.add_patch "Link to this definition")
    :   Shortcut for adding a PATCH handler. Calls the [`add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") with `method` equals to `'PATCH'`.

    add\_delete(*path*, *handler*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_delete)[¶](#aiohttp.web.UrlDispatcher.add_delete "Link to this definition")
    :   Shortcut for adding a DELETE handler. Calls the [`add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") with `method` equals to `'DELETE'`.

    add\_view(*path*, *handler*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_view)[¶](#aiohttp.web.UrlDispatcher.add_view "Link to this definition")
    :   Shortcut for adding a class-based view handler. Calls the [`add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") with `method` equals to `'*'`.

        Added in version 3.0.

    add\_static(*prefix*, *path*, *\**, *name=None*, *expect\_handler=None*, *chunk\_size=256 \* 1024*, *response\_factory=StreamResponse*, *show\_index=False*, *follow\_symlinks=False*, *append\_version=False*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.add_static)[¶](#aiohttp.web.UrlDispatcher.add_static "Link to this definition")
    :   Adds a router and a handler for returning static files.

        Useful for serving static content like images, javascript and css files.

        On platforms that support it, the handler will transfer files more
        efficiently using the `sendfile` system call.

        In some situations it might be necessary to avoid using the `sendfile`
        system call even if the platform supports it. This can be accomplished by
        by setting environment variable `AIOHTTP_NOSENDFILE=1`.

        If a Brotli or gzip compressed version of the static content exists at
        the requested path with the `.br` or `.gz` extension, it will be used
        for the response. Brotli will be preferred over gzip if both files exist.

        Warning

        Use [`add_static()`](#aiohttp.web.UrlDispatcher.add_static "aiohttp.web.UrlDispatcher.add_static") for development only. In production,
        static content should be processed by web servers like *nginx*
        or *apache*. Such web servers will be able to provide significantly
        better performance and security for static assets. Several past security
        vulnerabilities in aiohttp only affected applications using
        [`add_static()`](#aiohttp.web.UrlDispatcher.add_static "aiohttp.web.UrlDispatcher.add_static").

        Parameters:
        :   * **prefix** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – URL path prefix for handled static files
            * **path** – path to the folder in file system that contains
              handled static files, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)").
            * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – optional route name.
            * **expect\_handler** ([*collections.abc.Coroutine*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Coroutine "(in Python v3.14)")) – optional *expect* header handler.
            * **chunk\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

              size of single chunk for file
              downloading, 256Kb by default.

              Increasing *chunk\_size* parameter to,
              say, 1Mb may increase file downloading
              speed but consumes more memory.
            * **show\_index** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – flag for allowing to show indexes of a directory,
              by default it’s not allowed and HTTP/403 will
              be returned on directory access.
            * **follow\_symlinks** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – flag for allowing to follow symlinks that lead
              outside the static root directory, by default it’s not allowed and
              HTTP/404 will be returned on access. Enabling `follow_symlinks`
              can be a security risk, and may lead to a directory transversal attack.
              You do NOT need this option to follow symlinks which point to somewhere
              else within the static directory, this option is only used to break out
              of the security sandbox. Enabling this option is highly discouraged,
              and only expected to be used for edge cases in a local development
              setting where remote users do not have access to the server.
            * **append\_version** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – flag for adding file version (hash)
              to the url query string, this value will
              be used as default when you call to
              `url()` and
              [`url_for()`](#aiohttp.web.AbstractRoute.url_for "aiohttp.web.AbstractRoute.url_for") methods.

        Returns:
        :   new [`AbstractRoute`](#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") instance.

    async resolve(*request*)[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.resolve)[¶](#aiohttp.web.UrlDispatcher.resolve "Link to this definition")
    :   A [coroutine](https://docs.python.org/3/library/asyncio-task.html#coroutine "(in Python v3.14)") that returns
        [`AbstractMatchInfo`](abc.html#aiohttp.abc.AbstractMatchInfo "aiohttp.abc.AbstractMatchInfo") for *request*.

        The method never raises exception, but returns
        [`AbstractMatchInfo`](abc.html#aiohttp.abc.AbstractMatchInfo "aiohttp.abc.AbstractMatchInfo") instance with:

        1. [`http_exception`](abc.html#aiohttp.abc.AbstractMatchInfo.http_exception "aiohttp.abc.AbstractMatchInfo.http_exception") assigned to
           [`HTTPException`](#aiohttp.web.HTTPException "aiohttp.web.HTTPException") instance.
        2. [`handler()`](abc.html#aiohttp.abc.AbstractMatchInfo.handler "aiohttp.abc.AbstractMatchInfo.handler") which raises
           `HTTPNotFound` or `HTTPMethodNotAllowed` on handler’s
           execution if there is no registered route for *request*.

           *Middlewares* can process that exceptions to render
           pretty-looking error page for example.

        Used by internal machinery, end user unlikely need to call the method.

        Note

        The method uses [`aiohttp.web.BaseRequest.raw_path`](#aiohttp.web.BaseRequest.raw_path "aiohttp.web.BaseRequest.raw_path") for pattern
        matching against registered routes.

    resources()[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.resources)[¶](#aiohttp.web.UrlDispatcher.resources "Link to this definition")
    :   The method returns a *view* for *all* registered resources.

        The view is an object that allows to:

        1. Get size of the router table:

           ```
           len(app.router.resources())
           ```
        2. Iterate over registered resources:

           ```
           for resource in app.router.resources():
               print(resource)
           ```
        3. Make a check if the resources is registered in the router table:

           ```
           route in app.router.resources()
           ```

    routes()[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.routes)[¶](#aiohttp.web.UrlDispatcher.routes "Link to this definition")
    :   The method returns a *view* for *all* registered routes.

    named\_resources()[[source]](_modules/aiohttp/web_urldispatcher.html#UrlDispatcher.named_resources)[¶](#aiohttp.web.UrlDispatcher.named_resources "Link to this definition")
    :   Returns a [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")-like [`types.MappingProxyType`](https://docs.python.org/3/library/types.html#types.MappingProxyType "(in Python v3.14)") *view* over
        *all* named **resources**.

        The view maps every named resource’s **name** to the
        [`AbstractResource`](#aiohttp.web.AbstractResource "aiohttp.web.AbstractResource") instance. It supports the usual
        [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")-like operations, except for any mutable operations
        (i.e. it’s **read-only**):

        ```
        len(app.router.named_resources())

        for name, resource in app.router.named_resources().items():
            print(name, resource)

        "name" in app.router.named_resources()

        app.router.named_resources()["name"]
        ```

### Resource[¶](#resource "Link to this heading")

Default router [`UrlDispatcher`](#aiohttp.web.UrlDispatcher "aiohttp.web.UrlDispatcher") operates with [resource](glossary.html#term-resource)s.

Resource is an item in *routing table* which has a *path*, an optional
unique *name* and at least one [route](glossary.html#term-route).

[web-handler](glossary.html#term-web-handler) lookup is performed in the following way:

1. The router splits the URL and checks the index from longest to shortest.
   For example, ‘/one/two/three’ will first check the index for
   ‘/one/two/three’, then ‘/one/two’ and finally ‘/’.
2. If the URL part is found in the index, the list of routes for
   that URL part is iterated over. If a route matches to requested HTTP
   method (or `'*'` wildcard) the route’s handler is used as the chosen
   [web-handler](glossary.html#term-web-handler). The lookup is finished.
3. If the route is not found in the index, the router tries to find
   the route in the list of `MatchedSubAppResource`,
   (current only created from [`add_domain()`](#aiohttp.web.Application.add_domain "aiohttp.web.Application.add_domain")),
   and will iterate over the list of
   `MatchedSubAppResource` in a linear fashion
   until a match is found.
4. If no *resource* / *route* pair was found, the *router*
   returns the special [`AbstractMatchInfo`](abc.html#aiohttp.abc.AbstractMatchInfo "aiohttp.abc.AbstractMatchInfo")
   instance with [`aiohttp.abc.AbstractMatchInfo.http_exception`](abc.html#aiohttp.abc.AbstractMatchInfo.http_exception "aiohttp.abc.AbstractMatchInfo.http_exception") is not `None`
   but [`HTTPException`](#aiohttp.web.HTTPException "aiohttp.web.HTTPException") with either *HTTP 404 Not Found* or
   *HTTP 405 Method Not Allowed* status code.
   Registered [`handler()`](abc.html#aiohttp.abc.AbstractMatchInfo.handler "aiohttp.abc.AbstractMatchInfo.handler") raises this exception on call.

Fixed paths are preferred over variable paths. For example,
if you have two routes `/a/b` and `/a/{name}`, then the first
route will always be preferred over the second one.

If there are multiple dynamic paths with the same fixed prefix,
they will be resolved in order of registration.

For example, if you have two dynamic routes that are prefixed
with the fixed `/users` path such as `/users/{x}/{y}/z` and
`/users/{x}/y/z`, the first one will be preferred over the
second one.

User should never instantiate resource classes but give it by
[`UrlDispatcher.add_resource()`](#aiohttp.web.UrlDispatcher.add_resource "aiohttp.web.UrlDispatcher.add_resource") call.

After that he may add a [route](glossary.html#term-route) by calling [`Resource.add_route()`](#aiohttp.web.Resource.add_route "aiohttp.web.Resource.add_route").

[`UrlDispatcher.add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") is just shortcut for:

```
router.add_resource(path).add_route(method, handler)
```

Resource with a *name* is called *named resource*.
The main purpose of *named resource* is constructing URL by route name for
passing it into *template engine* for example:

```
url = app.router['resource_name'].url_for().with_query({'a': 1, 'b': 2})
```

Resource classes hierarchy:

```
AbstractResource
  Resource
    PlainResource
    DynamicResource
  PrefixResource
    StaticResource
    PrefixedSubAppResource
       MatchedSubAppResource
```

class aiohttp.web.AbstractResource[[source]](_modules/aiohttp/web_urldispatcher.html#AbstractResource)[¶](#aiohttp.web.AbstractResource "Link to this definition")
:   A base class for all resources.

    Inherited from [`collections.abc.Sized`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sized "(in Python v3.14)") and
    [`collections.abc.Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)").

    `len(resource)` returns amount of [route](glossary.html#term-route)s belongs to the resource,
    `for route in resource` allows to iterate over these routes.

    name[¶](#aiohttp.web.AbstractResource.name "Link to this definition")
    :   Read-only *name* of resource or `None`.

    canonical[¶](#aiohttp.web.AbstractResource.canonical "Link to this definition")
    :   Read-only *canonical path* associate with the resource. For example
        `/path/to` or `/path/{to}`

        Added in version 3.3.

    async resolve(*request*)[[source]](_modules/aiohttp/web_urldispatcher.html#AbstractResource.resolve)[¶](#aiohttp.web.AbstractResource.resolve "Link to this definition")
    :   Resolve resource by finding appropriate [web-handler](glossary.html#term-web-handler) for
        `(method, path)` combination.

        Returns:
        :   (*match\_info*, *allowed\_methods*) pair.

            *allowed\_methods* is a [`set`](https://docs.python.org/3/library/stdtypes.html#set "(in Python v3.14)") or HTTP methods accepted by
            resource.

            *match\_info* is either [`UrlMappingMatchInfo`](#aiohttp.web.UrlMappingMatchInfo "aiohttp.web.UrlMappingMatchInfo") if
            request is resolved or `None` if no [route](glossary.html#term-route) is
            found.

    get\_info()[[source]](_modules/aiohttp/web_urldispatcher.html#AbstractResource.get_info)[¶](#aiohttp.web.AbstractResource.get_info "Link to this definition")
    :   A resource description, e.g. `{'path': '/path/to'}` or
        `{'formatter': '/path/{to}', 'pattern':
        re.compile(r'^/path/(?P<to>[a-zA-Z][_a-zA-Z0-9]+)$`

    url\_for(*\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#AbstractResource.url_for)[¶](#aiohttp.web.AbstractResource.url_for "Link to this definition")
    :   Construct an URL for route with additional params.

        *args* and **kwargs** depend on a parameters list accepted by
        inherited resource class.

        Returns:
        :   [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") – resulting URL instance.

class aiohttp.web.Resource[[source]](_modules/aiohttp/web_urldispatcher.html#Resource)[¶](#aiohttp.web.Resource "Link to this definition")
:   A base class for new-style resources, inherits [`AbstractResource`](#aiohttp.web.AbstractResource "aiohttp.web.AbstractResource").

    add\_route(*method*, *handler*, *\**, *expect\_handler=None*)[[source]](_modules/aiohttp/web_urldispatcher.html#Resource.add_route)[¶](#aiohttp.web.Resource.add_route "Link to this definition")
    :   Add a [web-handler](glossary.html#term-web-handler) to resource.

        Parameters:
        :   * **method** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) –

              HTTP method for route. Should be one of
              `'GET'`, `'POST'`, `'PUT'`,
              `'DELETE'`, `'PATCH'`, `'HEAD'`,
              `'OPTIONS'` or `'*'` for any method.

              The parameter is case-insensitive, e.g. you
              can push `'get'` as well as `'GET'`.

              The method should be unique for resource.
            * **handler** ([*collections.abc.Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")) – route handler.
            * **expect\_handler** ([*collections.abc.Coroutine*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Coroutine "(in Python v3.14)")) – optional *expect* header handler.

        Returns:
        :   new [`ResourceRoute`](#aiohttp.web.ResourceRoute "aiohttp.web.ResourceRoute") instance.

class aiohttp.web.PlainResource[[source]](_modules/aiohttp/web_urldispatcher.html#PlainResource)[¶](#aiohttp.web.PlainResource "Link to this definition")
:   A resource, inherited from [`Resource`](#aiohttp.web.Resource "aiohttp.web.Resource").

    The class corresponds to resources with plain-text matching,
    `'/path/to'` for example.

    canonical[¶](#aiohttp.web.PlainResource.canonical "Link to this definition")
    :   Read-only *canonical path* associate with the resource. Returns the path
        used to create the PlainResource. For example `/path/to`

        Added in version 3.3.

    url\_for()[[source]](_modules/aiohttp/web_urldispatcher.html#PlainResource.url_for)[¶](#aiohttp.web.PlainResource.url_for "Link to this definition")
    :   Returns a [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") for the resource.

class aiohttp.web.DynamicResource[[source]](_modules/aiohttp/web_urldispatcher.html#DynamicResource)[¶](#aiohttp.web.DynamicResource "Link to this definition")
:   A resource, inherited from [`Resource`](#aiohttp.web.Resource "aiohttp.web.Resource").

    The class corresponds to resources with
    [variable](web_quickstart.html#aiohttp-web-variable-handler) matching,
    e.g. `'/path/{to}/{param}'` etc.

    canonical[¶](#aiohttp.web.DynamicResource.canonical "Link to this definition")
    :   Read-only *canonical path* associate with the resource. Returns the
        formatter obtained from the path used to create the DynamicResource.
        For example, from a path `/get/{num:^\d+}`, it returns `/get/{num}`

        Added in version 3.3.

    url\_for(*\*\*params*)[[source]](_modules/aiohttp/web_urldispatcher.html#DynamicResource.url_for)[¶](#aiohttp.web.DynamicResource.url_for "Link to this definition")
    :   Returns a [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") for the resource.

        Parameters:
        :   **params** –

            – a variable substitutions for dynamic resource.

            E.g. for `'/path/{to}/{param}'` pattern the method should
            be called as `resource.url_for(to='val1', param='val2')`

class aiohttp.web.StaticResource[[source]](_modules/aiohttp/web_urldispatcher.html#StaticResource)[¶](#aiohttp.web.StaticResource "Link to this definition")
:   A resource, inherited from [`Resource`](#aiohttp.web.Resource "aiohttp.web.Resource").

    The class corresponds to resources for [static file serving](web_advanced.html#aiohttp-web-static-file-handling).

    canonical[¶](#aiohttp.web.StaticResource.canonical "Link to this definition")
    :   Read-only *canonical path* associate with the resource. Returns the prefix
        used to create the StaticResource. For example `/prefix`

        Added in version 3.3.

    url\_for(*filename*, *append\_version=None*)[[source]](_modules/aiohttp/web_urldispatcher.html#StaticResource.url_for)[¶](#aiohttp.web.StaticResource.url_for "Link to this definition")
    :   Returns a [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") for file path under resource prefix.

        Parameters:
        :   * **filename** –

              – a file name substitution for static file handler.

              Accepts both [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") and [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)").

              E.g. an URL for `'/prefix/dir/file.txt'` should
              be generated as `resource.url_for(filename='dir/file.txt')`
            * **append\_version** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

              – a flag for adding file version
              :   (hash) to the url query string for
                  cache boosting

              By default has value from a constructor (`False` by default)
              When set to `True` - `v=FILE_HASH` query string param will be added
              When set to `False` has no impact

              if file not found has no impact

class aiohttp.web.PrefixedSubAppResource[[source]](_modules/aiohttp/web_urldispatcher.html#PrefixedSubAppResource)[¶](#aiohttp.web.PrefixedSubAppResource "Link to this definition")
:   A resource for serving nested applications. The class instance is
    returned by [`add_subapp`](#aiohttp.web.Application.add_subapp "aiohttp.web.Application.add_subapp") call.

    canonical[¶](#aiohttp.web.PrefixedSubAppResource.canonical "Link to this definition")
    :   Read-only *canonical path* associate with the resource. Returns the
        prefix used to create the PrefixedSubAppResource.
        For example `/prefix`

        Added in version 3.3.

    url\_for(*\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#PrefixedSubAppResource.url_for)[¶](#aiohttp.web.PrefixedSubAppResource.url_for "Link to this definition")
    :   The call is not allowed, it raises [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)").

### Route[¶](#route "Link to this heading")

Route has *HTTP method* (wildcard `'*'` is an option),
[web-handler](glossary.html#term-web-handler) and optional *expect handler*.

Every route belong to some resource.

Route classes hierarchy:

```
AbstractRoute
  ResourceRoute
  SystemRoute
```

[`ResourceRoute`](#aiohttp.web.ResourceRoute "aiohttp.web.ResourceRoute") is the route used for resources,
[`SystemRoute`](#aiohttp.web.SystemRoute "aiohttp.web.SystemRoute") serves URL resolving errors like *404 Not Found*
and *405 Method Not Allowed*.

class aiohttp.web.AbstractRoute[[source]](_modules/aiohttp/web_urldispatcher.html#AbstractRoute)[¶](#aiohttp.web.AbstractRoute "Link to this definition")
:   Base class for routes served by [`UrlDispatcher`](#aiohttp.web.UrlDispatcher "aiohttp.web.UrlDispatcher").

    method[¶](#aiohttp.web.AbstractRoute.method "Link to this definition")
    :   HTTP method handled by the route, e.g. *GET*, *POST* etc.

    handler[¶](#aiohttp.web.AbstractRoute.handler "Link to this definition")
    :   [handler](web_quickstart.html#aiohttp-web-handler) that processes the route.

    name[¶](#aiohttp.web.AbstractRoute.name "Link to this definition")
    :   Name of the route, always equals to name of resource which owns the route.

    resource[¶](#aiohttp.web.AbstractRoute.resource "Link to this definition")
    :   Resource instance which holds the route, `None` for
        [`SystemRoute`](#aiohttp.web.SystemRoute "aiohttp.web.SystemRoute").

    url\_for(*\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_urldispatcher.html#AbstractRoute.url_for)[¶](#aiohttp.web.AbstractRoute.url_for "Link to this definition")
    :   Abstract method for constructing url handled by the route.

        Actually it’s a shortcut for `route.resource.url_for(...)`.

    async handle\_expect\_header(*request*)[[source]](_modules/aiohttp/web_urldispatcher.html#AbstractRoute.handle_expect_header)[¶](#aiohttp.web.AbstractRoute.handle_expect_header "Link to this definition")
    :   `100-continue` handler.

class aiohttp.web.ResourceRoute[[source]](_modules/aiohttp/web_urldispatcher.html#ResourceRoute)[¶](#aiohttp.web.ResourceRoute "Link to this definition")
:   The route class for handling different HTTP methods for [`Resource`](#aiohttp.web.Resource "aiohttp.web.Resource").

class aiohttp.web.SystemRoute[¶](#aiohttp.web.SystemRoute "Link to this definition")
:   The route class for handling URL resolution errors like like *404 Not Found*
    and *405 Method Not Allowed*.

    status[¶](#aiohttp.web.SystemRoute.status "Link to this definition")
    :   HTTP status code

    reason[¶](#aiohttp.web.SystemRoute.reason "Link to this definition")
    :   HTTP status reason

### RouteDef and StaticDef[¶](#routedef-and-staticdef "Link to this heading")

Route definition, a description for not registered yet route.

Could be used for filing route table by providing a list of route
definitions (Django style).

The definition is created by functions like [`get()`](#aiohttp.web.get "aiohttp.web.get") or
[`post()`](#aiohttp.web.post "aiohttp.web.post"), list of definitions could be added to router by
[`UrlDispatcher.add_routes()`](#aiohttp.web.UrlDispatcher.add_routes "aiohttp.web.UrlDispatcher.add_routes") call:

```
from aiohttp import web

async def handle_get(request):
    ...


async def handle_post(request):
    ...

app.router.add_routes([web.get('/get', handle_get),
                       web.post('/post', handle_post),
```

class aiohttp.web.AbstractRouteDef[[source]](_modules/aiohttp/web_routedef.html#AbstractRouteDef)[¶](#aiohttp.web.AbstractRouteDef "Link to this definition")
:   A base class for route definitions.

    Inherited from [`abc.ABC`](https://docs.python.org/3/library/abc.html#abc.ABC "(in Python v3.14)").

    Added in version 3.1.

    register(*router*)[[source]](_modules/aiohttp/web_routedef.html#AbstractRouteDef.register)[¶](#aiohttp.web.AbstractRouteDef.register "Link to this definition")
    :   Register itself into [`UrlDispatcher`](#aiohttp.web.UrlDispatcher "aiohttp.web.UrlDispatcher").

        Abstract method, should be overridden by subclasses.

        Returns:
        :   [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of registered [`AbstractRoute`](#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") objects.

        Changed in version 3.7: Return value updated from `None` to [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of
        [`AbstractRoute`](#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") instances.

class aiohttp.web.RouteDef[[source]](_modules/aiohttp/web_routedef.html#RouteDef)[¶](#aiohttp.web.RouteDef "Link to this definition")
:   A definition of not registered yet route.

    Implements [`AbstractRouteDef`](#aiohttp.web.AbstractRouteDef "aiohttp.web.AbstractRouteDef").

    Added in version 2.3.

    Changed in version 3.1: The class implements [`AbstractRouteDef`](#aiohttp.web.AbstractRouteDef "aiohttp.web.AbstractRouteDef") interface.

    method[¶](#aiohttp.web.RouteDef.method "Link to this definition")
    :   HTTP method (`GET`, `POST` etc.) ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")).

    path[¶](#aiohttp.web.RouteDef.path "Link to this definition")
    :   Path to resource, e.g. `/path/to`. Could contain `{}`
        brackets for [variable resources](web_quickstart.html#aiohttp-web-variable-handler) ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")).

    handler[¶](#aiohttp.web.RouteDef.handler "Link to this definition")
    :   An async function to handle HTTP request.

    kwargs[¶](#aiohttp.web.RouteDef.kwargs "Link to this definition")
    :   A [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") of additional arguments.

class aiohttp.web.StaticDef[[source]](_modules/aiohttp/web_routedef.html#StaticDef)[¶](#aiohttp.web.StaticDef "Link to this definition")
:   A definition of static file resource.

    Implements [`AbstractRouteDef`](#aiohttp.web.AbstractRouteDef "aiohttp.web.AbstractRouteDef").

    Added in version 3.1.

    prefix[¶](#aiohttp.web.StaticDef.prefix "Link to this definition")
    :   A prefix used for static file handling, e.g. `/static`.

    path[¶](#aiohttp.web.StaticDef.path "Link to this definition")
    :   File system directory to serve, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") or
        [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)")
        (e.g. `'/home/web-service/path/to/static'`.

    kwargs[¶](#aiohttp.web.StaticDef.kwargs "Link to this definition")
    :   A [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") of additional arguments, see
        [`UrlDispatcher.add_static()`](#aiohttp.web.UrlDispatcher.add_static "aiohttp.web.UrlDispatcher.add_static") for a list of supported
        options.

aiohttp.web.get(*path*, *handler*, *\**, *name=None*, *allow\_head=True*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#get)[¶](#aiohttp.web.get "Link to this definition")
:   Return [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") for processing `GET` requests. See
    [`UrlDispatcher.add_get()`](#aiohttp.web.UrlDispatcher.add_get "aiohttp.web.UrlDispatcher.add_get") for information about parameters.

    Added in version 2.3.

aiohttp.web.post(*path*, *handler*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#post)[¶](#aiohttp.web.post "Link to this definition")
:   Return [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") for processing `POST` requests. See
    [`UrlDispatcher.add_post()`](#aiohttp.web.UrlDispatcher.add_post "aiohttp.web.UrlDispatcher.add_post") for information about parameters.

    Added in version 2.3.

aiohttp.web.head(*path*, *handler*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#head)[¶](#aiohttp.web.head "Link to this definition")
:   Return [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") for processing `HEAD` requests. See
    [`UrlDispatcher.add_head()`](#aiohttp.web.UrlDispatcher.add_head "aiohttp.web.UrlDispatcher.add_head") for information about parameters.

    Added in version 2.3.

aiohttp.web.put(*path*, *handler*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#put)[¶](#aiohttp.web.put "Link to this definition")
:   Return [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") for processing `PUT` requests. See
    [`UrlDispatcher.add_put()`](#aiohttp.web.UrlDispatcher.add_put "aiohttp.web.UrlDispatcher.add_put") for information about parameters.

    Added in version 2.3.

aiohttp.web.patch(*path*, *handler*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#patch)[¶](#aiohttp.web.patch "Link to this definition")
:   Return [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") for processing `PATCH` requests. See
    [`UrlDispatcher.add_patch()`](#aiohttp.web.UrlDispatcher.add_patch "aiohttp.web.UrlDispatcher.add_patch") for information about parameters.

    Added in version 2.3.

aiohttp.web.delete(*path*, *handler*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#delete)[¶](#aiohttp.web.delete "Link to this definition")
:   Return [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") for processing `DELETE` requests. See
    [`UrlDispatcher.add_delete()`](#aiohttp.web.UrlDispatcher.add_delete "aiohttp.web.UrlDispatcher.add_delete") for information about parameters.

    Added in version 2.3.

aiohttp.web.view(*path*, *handler*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#view)[¶](#aiohttp.web.view "Link to this definition")
:   Return [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") for processing `ANY` requests. See
    [`UrlDispatcher.add_view()`](#aiohttp.web.UrlDispatcher.add_view "aiohttp.web.UrlDispatcher.add_view") for information about parameters.

    Added in version 3.0.

aiohttp.web.static(*prefix*, *path*, *\**, *name=None*, *expect\_handler=None*, *chunk\_size=256 \* 1024*, *show\_index=False*, *follow\_symlinks=False*, *append\_version=False*)[[source]](_modules/aiohttp/web_routedef.html#static)[¶](#aiohttp.web.static "Link to this definition")
:   Return [`StaticDef`](#aiohttp.web.StaticDef "aiohttp.web.StaticDef") for processing static files.

    See [`UrlDispatcher.add_static()`](#aiohttp.web.UrlDispatcher.add_static "aiohttp.web.UrlDispatcher.add_static") for information
    about supported parameters.

    Added in version 3.1.

aiohttp.web.route(*method*, *path*, *handler*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#route)[¶](#aiohttp.web.route "Link to this definition")
:   Return [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") for processing requests that decided by
    `method`. See [`UrlDispatcher.add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") for information
    about parameters.

    Added in version 2.3.

### RouteTableDef[¶](#routetabledef "Link to this heading")

A routes table definition used for describing routes by decorators
(Flask style):

```
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/get')
async def handle_get(request):
    ...


@routes.post('/post')
async def handle_post(request):
    ...

app.router.add_routes(routes)


@routes.view("/view")
class MyView(web.View):
    async def get(self):
        ...

    async def post(self):
        ...
```

class aiohttp.web.RouteTableDef[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef)[¶](#aiohttp.web.RouteTableDef "Link to this definition")
:   A sequence of [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") instances (implements
    [`collections.abc.Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence "(in Python v3.14)") protocol).

    In addition to all standard [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") methods the class
    provides also methods like `get()` and `post()` for adding new
    route definition.

    Added in version 2.3.

    @get(*path*, *\**, *allow\_head=True*, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef.get)[¶](#aiohttp.web.RouteTableDef.get "Link to this definition")
    :   Add a new [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") item for registering `GET` web-handler.

        See [`UrlDispatcher.add_get()`](#aiohttp.web.UrlDispatcher.add_get "aiohttp.web.UrlDispatcher.add_get") for information about parameters.

    @post(*path*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef.post)[¶](#aiohttp.web.RouteTableDef.post "Link to this definition")
    :   Add a new [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") item for registering `POST` web-handler.

        See [`UrlDispatcher.add_post()`](#aiohttp.web.UrlDispatcher.add_post "aiohttp.web.UrlDispatcher.add_post") for information about parameters.

    @head(*path*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef.head)[¶](#aiohttp.web.RouteTableDef.head "Link to this definition")
    :   Add a new [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") item for registering `HEAD` web-handler.

        See [`UrlDispatcher.add_head()`](#aiohttp.web.UrlDispatcher.add_head "aiohttp.web.UrlDispatcher.add_head") for information about parameters.

    @put(*path*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef.put)[¶](#aiohttp.web.RouteTableDef.put "Link to this definition")
    :   Add a new [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") item for registering `PUT` web-handler.

        See [`UrlDispatcher.add_put()`](#aiohttp.web.UrlDispatcher.add_put "aiohttp.web.UrlDispatcher.add_put") for information about parameters.

    @patch(*path*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef.patch)[¶](#aiohttp.web.RouteTableDef.patch "Link to this definition")
    :   Add a new [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") item for registering `PATCH` web-handler.

        See [`UrlDispatcher.add_patch()`](#aiohttp.web.UrlDispatcher.add_patch "aiohttp.web.UrlDispatcher.add_patch") for information about parameters.

    @delete(*path*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef.delete)[¶](#aiohttp.web.RouteTableDef.delete "Link to this definition")
    :   Add a new [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") item for registering `DELETE` web-handler.

        See [`UrlDispatcher.add_delete()`](#aiohttp.web.UrlDispatcher.add_delete "aiohttp.web.UrlDispatcher.add_delete") for information about parameters.

    @view(*path*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef.view)[¶](#aiohttp.web.RouteTableDef.view "Link to this definition")
    :   Add a new [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") item for registering `ANY` methods
        against a class-based view.

        See [`UrlDispatcher.add_view()`](#aiohttp.web.UrlDispatcher.add_view "aiohttp.web.UrlDispatcher.add_view") for information about parameters.

        Added in version 3.0.

    static(*prefix*, *path*, *\**, *name=None*, *expect\_handler=None*, *chunk\_size=256 \* 1024*, *show\_index=False*, *follow\_symlinks=False*, *append\_version=False*)[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef.static)[¶](#aiohttp.web.RouteTableDef.static "Link to this definition")
    :   Add a new [`StaticDef`](#aiohttp.web.StaticDef "aiohttp.web.StaticDef") item for registering static files processor.

        See [`UrlDispatcher.add_static()`](#aiohttp.web.UrlDispatcher.add_static "aiohttp.web.UrlDispatcher.add_static") for information about
        supported parameters.

        Added in version 3.1.

    @route(*method*, *path*, *\**, *name=None*, *expect\_handler=None*)[[source]](_modules/aiohttp/web_routedef.html#RouteTableDef.route)[¶](#aiohttp.web.RouteTableDef.route "Link to this definition")
    :   Add a new [`RouteDef`](#aiohttp.web.RouteDef "aiohttp.web.RouteDef") item for registering a web-handler
        for arbitrary HTTP method.

        See [`UrlDispatcher.add_route()`](#aiohttp.web.UrlDispatcher.add_route "aiohttp.web.UrlDispatcher.add_route") for information about parameters.

### MatchInfo[¶](#matchinfo "Link to this heading")

After route matching web application calls found handler if any.

Matching result can be accessible from handler as
[`Request.match_info`](#aiohttp.web.Request.match_info "aiohttp.web.Request.match_info") attribute.

In general the result may be any object derived from
[`AbstractMatchInfo`](abc.html#aiohttp.abc.AbstractMatchInfo "aiohttp.abc.AbstractMatchInfo") ([`UrlMappingMatchInfo`](#aiohttp.web.UrlMappingMatchInfo "aiohttp.web.UrlMappingMatchInfo") for default
[`UrlDispatcher`](#aiohttp.web.UrlDispatcher "aiohttp.web.UrlDispatcher") router).

class aiohttp.web.UrlMappingMatchInfo[[source]](_modules/aiohttp/web_urldispatcher.html#UrlMappingMatchInfo)[¶](#aiohttp.web.UrlMappingMatchInfo "Link to this definition")
:   Inherited from [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") and [`AbstractMatchInfo`](abc.html#aiohttp.abc.AbstractMatchInfo "aiohttp.abc.AbstractMatchInfo"). Dict
    items are filled by matching info and is [resource](glossary.html#term-resource)-specific.

    expect\_handler[¶](#aiohttp.web.UrlMappingMatchInfo.expect_handler "Link to this definition")
    :   A coroutine for handling `100-continue`.

    handler[¶](#aiohttp.web.UrlMappingMatchInfo.handler "Link to this definition")
    :   A coroutine for handling request.

    route[¶](#aiohttp.web.UrlMappingMatchInfo.route "Link to this definition")
    :   [`AbstractRoute`](#aiohttp.web.AbstractRoute "aiohttp.web.AbstractRoute") instance for url matching.

### View[¶](#view "Link to this heading")

class aiohttp.web.View(*request*)[[source]](_modules/aiohttp/web_urldispatcher.html#View)[¶](#aiohttp.web.View "Link to this definition")
:   Inherited from [`AbstractView`](abc.html#aiohttp.abc.AbstractView "aiohttp.abc.AbstractView").

    Base class for class based views. Implementations should derive from
    [`View`](#aiohttp.web.View "aiohttp.web.View") and override methods for handling HTTP verbs like
    `get()` or `post()`:

    ```
    class MyView(View):

        async def get(self):
            resp = await get_response(self.request)
            return resp

        async def post(self):
            resp = await post_response(self.request)
            return resp

    app.router.add_view('/view', MyView)
    ```

    The view raises *405 Method Not allowed*
    (`HTTPMethodNotAllowed`) if requested web verb is not
    supported.

    Parameters:
    :   **request** – instance of [`Request`](#aiohttp.web.Request "aiohttp.web.Request") that has initiated a view
        processing.

    request[¶](#aiohttp.web.View.request "Link to this definition")
    :   Request sent to view’s constructor, read-only property.

    Overridable coroutine methods: `connect()`, `delete()`,
    `get()`, `head()`, `options()`, `patch()`, `post()`,
    `put()`, `trace()`.

See also

[Class Based Views](web_quickstart.html#aiohttp-web-class-based-views)

## Running Applications[¶](#running-applications "Link to this heading")

To start web application there is `AppRunner` and site classes.

Runner is a storage for running application, sites are for running
application on specific TCP or Unix socket, e.g.:

```
runner = web.AppRunner(app)
await runner.setup()
site = web.TCPSite(runner, 'localhost', 8080)
await site.start()
# wait for finish signal
await runner.cleanup()
```

Added in version 3.0: [`AppRunner`](#aiohttp.web.AppRunner "aiohttp.web.AppRunner") / [`ServerRunner`](#aiohttp.web.ServerRunner "aiohttp.web.ServerRunner") and [`TCPSite`](#aiohttp.web.TCPSite "aiohttp.web.TCPSite") /
[`UnixSite`](#aiohttp.web.UnixSite "aiohttp.web.UnixSite") / [`SockSite`](#aiohttp.web.SockSite "aiohttp.web.SockSite") are added in aiohttp 3.0

class aiohttp.web.BaseRunner[[source]](_modules/aiohttp/web_runner.html#BaseRunner)[¶](#aiohttp.web.BaseRunner "Link to this definition")
:   A base class for runners. Use [`AppRunner`](#aiohttp.web.AppRunner "aiohttp.web.AppRunner") for serving
    [`Application`](#aiohttp.web.Application "aiohttp.web.Application"), [`ServerRunner`](#aiohttp.web.ServerRunner "aiohttp.web.ServerRunner") for low-level
    [`Server`](#aiohttp.web.Server "aiohttp.web.Server").

    server[¶](#aiohttp.web.BaseRunner.server "Link to this definition")
    :   Low-level web [`Server`](#aiohttp.web.Server "aiohttp.web.Server") for handling HTTP requests,
        read-only attribute.

    addresses[¶](#aiohttp.web.BaseRunner.addresses "Link to this definition")
    :   A [`list`](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") of served sockets addresses.

        See [`socket.getsockname()`](https://docs.python.org/3/library/socket.html#socket.socket.getsockname "(in Python v3.14)") for items type.

        Added in version 3.3.

    sites[¶](#aiohttp.web.BaseRunner.sites "Link to this definition")
    :   A read-only [`set`](https://docs.python.org/3/library/stdtypes.html#set "(in Python v3.14)") of served sites ([`TCPSite`](#aiohttp.web.TCPSite "aiohttp.web.TCPSite") /
        [`UnixSite`](#aiohttp.web.UnixSite "aiohttp.web.UnixSite") / [`NamedPipeSite`](#aiohttp.web.NamedPipeSite "aiohttp.web.NamedPipeSite") / [`SockSite`](#aiohttp.web.SockSite "aiohttp.web.SockSite") instances).

    async setup()[[source]](_modules/aiohttp/web_runner.html#BaseRunner.setup)[¶](#aiohttp.web.BaseRunner.setup "Link to this definition")
    :   Initialize the server. Should be called before adding sites.

    async cleanup()[[source]](_modules/aiohttp/web_runner.html#BaseRunner.cleanup)[¶](#aiohttp.web.BaseRunner.cleanup "Link to this definition")
    :   Stop handling all registered sites and cleanup used resources.

class aiohttp.web.AppRunner(*app*, *\**, *handle\_signals=False*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_runner.html#AppRunner)[¶](#aiohttp.web.AppRunner "Link to this definition")
:   A runner for [`Application`](#aiohttp.web.Application "aiohttp.web.Application"). Used with conjunction with sites
    to serve on specific port.

    Inherited from [`BaseRunner`](#aiohttp.web.BaseRunner "aiohttp.web.BaseRunner").

    Parameters:
    :   * **app** ([*Application*](#aiohttp.web.Application "aiohttp.web.Application")) – web application instance to serve.
        * **handle\_signals** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – add signal handlers for
          [`signal.SIGINT`](https://docs.python.org/3/library/signal.html#signal.SIGINT "(in Python v3.14)") and
          [`signal.SIGTERM`](https://docs.python.org/3/library/signal.html#signal.SIGTERM "(in Python v3.14)") (`False` by
          default). These handlers will raise
          [`GracefulExit`](#aiohttp.web.GracefulExit "aiohttp.web.GracefulExit").
        * **kwargs** – named parameters to pass into
          web protocol.

    Supported *kwargs*:

    Parameters:
    :   * **tcp\_keepalive** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Enable TCP Keep-Alive. Default: `True`.
        * **keepalive\_timeout** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Number of seconds before closing Keep-Alive
          connection. Default: `3630` seconds (when deployed behind a reverse proxy
          it’s important for this value to be higher than the proxy’s timeout. To avoid
          race conditions we always want the proxy to close the connection).
        * **logger** – Custom logger object. Default:
          `aiohttp.log.server_logger`.
        * **access\_log** – Custom logging object. Default:
          `aiohttp.log.access_logger`.
        * **access\_log\_class** – Class for access\_logger. Default:
          `aiohttp.helpers.AccessLogger`.
          Must to be a subclass of [`aiohttp.abc.AbstractAccessLogger`](abc.html#aiohttp.abc.AbstractAccessLogger "aiohttp.abc.AbstractAccessLogger").
        * **access\_log\_format** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Access log format string. Default:
          `helpers.AccessLogger.LOG_FORMAT`.
        * **max\_line\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Optional maximum header line size. Default:
          `8190`.
        * **max\_headers** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Optional maximum header size. Default: `32768`.
        * **max\_field\_size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Optional maximum header field size. Default:
          `8190`.
        * **lingering\_time** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Maximum time during which the server
          reads and ignores additional data coming from the client when
          lingering close is on. Use `0` to disable lingering on
          server channel closing.
        * **read\_bufsize** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          Size of the read buffer ([`BaseRequest.content`](#aiohttp.web.BaseRequest.content "aiohttp.web.BaseRequest.content")).
          :   `None` by default,
              it means that the session global value is used.

          Added in version 3.7.
        * **auto\_decompress** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) –

          Automatically decompress request body,
          `True` by default.

          Added in version 3.8.

    app[¶](#aiohttp.web.AppRunner.app "Link to this definition")
    :   Read-only attribute for accessing to [`Application`](#aiohttp.web.Application "aiohttp.web.Application") served
        instance.

    async setup()[¶](#aiohttp.web.AppRunner.setup "Link to this definition")
    :   Initialize application. Should be called before adding sites.

        The method calls [`Application.on_startup`](#aiohttp.web.Application.on_startup "aiohttp.web.Application.on_startup") registered signals.

    async cleanup()[¶](#aiohttp.web.AppRunner.cleanup "Link to this definition")
    :   Stop handling all registered sites and cleanup used resources.

        [`Application.on_shutdown`](#aiohttp.web.Application.on_shutdown "aiohttp.web.Application.on_shutdown") and
        [`Application.on_cleanup`](#aiohttp.web.Application.on_cleanup "aiohttp.web.Application.on_cleanup") signals are called internally.

class aiohttp.web.ServerRunner(*web\_server*, *\**, *handle\_signals=False*, *\*\*kwargs*)[[source]](_modules/aiohttp/web_runner.html#ServerRunner)[¶](#aiohttp.web.ServerRunner "Link to this definition")
:   A runner for low-level [`Server`](#aiohttp.web.Server "aiohttp.web.Server"). Used with conjunction with sites
    to serve on specific port.

    Inherited from [`BaseRunner`](#aiohttp.web.BaseRunner "aiohttp.web.BaseRunner").

    Parameters:
    :   * **web\_server** ([*Server*](#aiohttp.web.Server "aiohttp.web.Server")) – low-level web server instance to serve.
        * **handle\_signals** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – add signal handlers for
          [`signal.SIGINT`](https://docs.python.org/3/library/signal.html#signal.SIGINT "(in Python v3.14)") and
          [`signal.SIGTERM`](https://docs.python.org/3/library/signal.html#signal.SIGTERM "(in Python v3.14)") (`False` by
          default). These handlers will raise
          [`GracefulExit`](#aiohttp.web.GracefulExit "aiohttp.web.GracefulExit").
        * **kwargs** – named parameters to pass into
          web protocol.

    See also

    [Low Level Server](web_lowlevel.html#aiohttp-web-lowlevel) demonstrates low-level server usage

class aiohttp.web.BaseSite[[source]](_modules/aiohttp/web_runner.html#BaseSite)[¶](#aiohttp.web.BaseSite "Link to this definition")
:   An abstract class for handled sites.

    name[¶](#aiohttp.web.BaseSite.name "Link to this definition")
    :   An identifier for site, read-only [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property. Could
        be a handled URL or UNIX socket path.

    async start()[[source]](_modules/aiohttp/web_runner.html#BaseSite.start)[¶](#aiohttp.web.BaseSite.start "Link to this definition")
    :   Start handling a site.

    async stop()[[source]](_modules/aiohttp/web_runner.html#BaseSite.stop)[¶](#aiohttp.web.BaseSite.stop "Link to this definition")
    :   Stop handling a site.

class aiohttp.web.TCPSite(*runner*, *host=None*, *port=None*, *\**, *shutdown\_timeout=60.0*, *ssl\_context=None*, *backlog=128*, *reuse\_address=None*, *reuse\_port=None*)[[source]](_modules/aiohttp/web_runner.html#TCPSite)[¶](#aiohttp.web.TCPSite "Link to this definition")
:   Serve a runner on TCP socket.

    Parameters:
    :   * **runner** – a runner to serve.
        * **host** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – HOST to listen on, all interfaces if `None` (default).
        * **port** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – PORT to listed on, `8080` if `None` (default).
        * **shutdown\_timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – a timeout used for both waiting on pending
          tasks before application shutdown and for
          closing opened connections on
          [`BaseSite.stop()`](#aiohttp.web.BaseSite.stop "aiohttp.web.BaseSite.stop") call.
        * **ssl\_context** – a [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") instance for serving
          SSL/TLS secure server, `None` for plain HTTP
          server (default).
        * **backlog** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          a number of unaccepted connections that the
          system will allow before refusing new
          connections, see [`socket.socket.listen()`](https://docs.python.org/3/library/socket.html#socket.socket.listen "(in Python v3.14)") for details.

          `128` by default.
        * **reuse\_address** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – tells the kernel to reuse a local socket in
          TIME\_WAIT state, without waiting for its
          natural timeout to expire. If not specified
          will automatically be set to True on UNIX.
        * **reuse\_port** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – tells the kernel to allow this endpoint to be
          bound to the same port as other existing
          endpoints are bound to, so long as they all set
          this flag when being created. This option is not
          supported on Windows.

class aiohttp.web.UnixSite(*runner*, *path*, *\**, *shutdown\_timeout=60.0*, *ssl\_context=None*, *backlog=128*)[[source]](_modules/aiohttp/web_runner.html#UnixSite)[¶](#aiohttp.web.UnixSite "Link to this definition")
:   Serve a runner on UNIX socket.

    Parameters:
    :   * **runner** – a runner to serve.
        * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – PATH to UNIX socket to listen.
        * **shutdown\_timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – a timeout used for both waiting on pending
          tasks before application shutdown and for
          closing opened connections on
          [`BaseSite.stop()`](#aiohttp.web.BaseSite.stop "aiohttp.web.BaseSite.stop") call.
        * **ssl\_context** – a [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") instance for serving
          SSL/TLS secure server, `None` for plain HTTP
          server (default).
        * **backlog** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          a number of unaccepted connections that the
          system will allow before refusing new
          connections, see [`socket.socket.listen()`](https://docs.python.org/3/library/socket.html#socket.socket.listen "(in Python v3.14)") for details.

          `128` by default.

class aiohttp.web.NamedPipeSite(*runner*, *path*, *\**, *shutdown\_timeout=60.0*)[[source]](_modules/aiohttp/web_runner.html#NamedPipeSite)[¶](#aiohttp.web.NamedPipeSite "Link to this definition")
:   Serve a runner on Named Pipe in Windows.

    Parameters:
    :   * **runner** – a runner to serve.
        * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – PATH of named pipe to listen.
        * **shutdown\_timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – a timeout used for both waiting on pending
          tasks before application shutdown and for
          closing opened connections on
          [`BaseSite.stop()`](#aiohttp.web.BaseSite.stop "aiohttp.web.BaseSite.stop") call.

class aiohttp.web.SockSite(*runner*, *sock*, *\**, *shutdown\_timeout=60.0*, *ssl\_context=None*, *backlog=128*)[[source]](_modules/aiohttp/web_runner.html#SockSite)[¶](#aiohttp.web.SockSite "Link to this definition")
:   Serve a runner on UNIX socket.

    Parameters:
    :   * **runner** – a runner to serve.
        * **sock** – A [socket instance](https://docs.python.org/3/library/socket.html#socket-objects "(in Python v3.14)") to listen to.
        * **shutdown\_timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – a timeout used for both waiting on pending
          tasks before application shutdown and for
          closing opened connections on
          [`BaseSite.stop()`](#aiohttp.web.BaseSite.stop "aiohttp.web.BaseSite.stop") call.
        * **ssl\_context** – a [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") instance for serving
          SSL/TLS secure server, `None` for plain HTTP
          server (default).
        * **backlog** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          a number of unaccepted connections that the
          system will allow before refusing new
          connections, see [`socket.socket.listen()`](https://docs.python.org/3/library/socket.html#socket.socket.listen "(in Python v3.14)") for details.

          `128` by default.

exception aiohttp.web.GracefulExit[[source]](_modules/aiohttp/web_runner.html#GracefulExit)[¶](#aiohttp.web.GracefulExit "Link to this definition")
:   Raised by signal handlers for [`signal.SIGINT`](https://docs.python.org/3/library/signal.html#signal.SIGINT "(in Python v3.14)") and [`signal.SIGTERM`](https://docs.python.org/3/library/signal.html#signal.SIGTERM "(in Python v3.14)")
    defined in [`AppRunner`](#aiohttp.web.AppRunner "aiohttp.web.AppRunner") and [`ServerRunner`](#aiohttp.web.ServerRunner "aiohttp.web.ServerRunner")
    when `handle_signals` is set to `True`.

    Inherited from [`SystemExit`](https://docs.python.org/3/library/exceptions.html#SystemExit "(in Python v3.14)"),
    which exits with error code `1` if not handled.

## Utilities[¶](#utilities "Link to this heading")

class aiohttp.web.FileField[[source]](_modules/aiohttp/web_request.html#FileField)[¶](#aiohttp.web.FileField "Link to this definition")
:   A [`dataclass`](https://docs.python.org/3/library/dataclasses.html#module-dataclasses "(in Python v3.14)") instance that is returned as
    multidict value by [`aiohttp.web.BaseRequest.post()`](#aiohttp.web.BaseRequest.post "aiohttp.web.BaseRequest.post") if field is uploaded file.

    name[¶](#aiohttp.web.FileField.name "Link to this definition")
    :   Field name

    filename[¶](#aiohttp.web.FileField.filename "Link to this definition")
    :   File name as specified by uploading (client) side.

    file[¶](#aiohttp.web.FileField.file "Link to this definition")
    :   An [`io.IOBase`](https://docs.python.org/3/library/io.html#io.IOBase "(in Python v3.14)") instance with content of uploaded file.

    content\_type[¶](#aiohttp.web.FileField.content_type "Link to this definition")
    :   *MIME type* of uploaded file, `'text/plain'` by default.

    See also

    [File Uploads](web_quickstart.html#aiohttp-web-file-upload)

aiohttp.web.run\_app(*app*, *\**, *host=None*, *port=None*, *path=None*, *sock=None*, *shutdown\_timeout=60.0*, *keepalive\_timeout=3630*, *ssl\_context=None*, *print=print*, *backlog=128*, *access\_log\_class=aiohttp.helpers.AccessLogger*, *access\_log\_format=aiohttp.helpers.AccessLogger.LOG\_FORMAT*, *access\_log=aiohttp.log.access\_logger*, *handle\_signals=True*, *reuse\_address=None*, *reuse\_port=None*, *handler\_cancellation=False*, *\*\*kwargs*)[[source]](_modules/aiohttp/web.html#run_app)[¶](#aiohttp.web.run_app "Link to this definition")
:   A high-level function for running an application, serving it until
    keyboard interrupt and performing a
    [Graceful shutdown](web_advanced.html#aiohttp-web-graceful-shutdown).

    This is a high-level function very similar to [`asyncio.run()`](https://docs.python.org/3/library/asyncio-runner.html#asyncio.run "(in Python v3.14)") and
    should be used as the main entry point for an application. The
    [`Application`](#aiohttp.web.Application "aiohttp.web.Application") object essentially becomes our main() function.
    If additional tasks need to be run in parallel, see
    [Complex Applications](web_advanced.html#aiohttp-web-complex-applications).

    The server will listen on any host or Unix domain socket path you supply.
    If no hosts or paths are supplied, or only a port is supplied, a TCP server
    listening on 0.0.0.0 (all hosts) will be launched.

    Distributing HTTP traffic to multiple hosts or paths on the same
    application process provides no performance benefit as the requests are
    handled on the same event loop. See [Server Deployment](deployment.html) for ways of
    distributing work for increased performance.

    Parameters:
    :   * **app** – [`Application`](#aiohttp.web.Application "aiohttp.web.Application") instance to run or a *coroutine*
          that returns an application.
        * **host** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – TCP/IP host or a sequence of hosts for HTTP server.
          Default is `'0.0.0.0'` if *port* has been specified
          or if *path* is not supplied.
        * **port** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – TCP/IP port for HTTP server. Default is `8080` for plain
          text HTTP and `8443` for HTTP via SSL (when
          *ssl\_context* parameter is specified).
        * **path** – file system path for HTTP server Unix domain socket.
          A sequence of file system paths can be used to bind
          multiple domain sockets. Listening on Unix domain
          sockets is not supported by all operating systems,
          [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"), [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path "(in Python v3.14)") or an iterable of these.
        * **sock** ([*socket.socket*](https://docs.python.org/3/library/socket.html#socket.socket "(in Python v3.14)")) – a preexisting socket object to accept connections on.
          A sequence of socket objects can be passed.
        * **shutdown\_timeout** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          a delay to wait for graceful server
          shutdown before disconnecting all
          open client sockets hard way.

          This is used as a delay to wait for
          pending tasks to complete and then
          again to close any pending connections.

          A system with properly
          [Graceful shutdown](web_advanced.html#aiohttp-web-graceful-shutdown)
          implemented never waits for the second
          timeout but closes a server in a few
          milliseconds.
        * **keepalive\_timeout** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) –

          a delay before a TCP connection is
          :   closed after a HTTP request. The delay
              allows for reuse of a TCP connection.

              When deployed behind a reverse proxy
              it’s important for this value to be
              higher than the proxy’s timeout. To avoid
              race conditions, we always want the proxy
              to handle connection closing.

          Added in version 3.8.
        * **ssl\_context** – [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)") for HTTPS server,
          `None` for HTTP connection.
        * **print** – a callable compatible with [`print()`](https://docs.python.org/3/library/functions.html#print "(in Python v3.14)"). May be used
          to override STDOUT output or suppress it. Passing None
          disables output.
        * **backlog** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – the number of unaccepted connections that the
          system will allow before refusing new
          connections (`128` by default).
        * **access\_log\_class** – class for access\_logger. Default:
          `aiohttp.helpers.AccessLogger`.
          Must to be a subclass of [`aiohttp.abc.AbstractAccessLogger`](abc.html#aiohttp.abc.AbstractAccessLogger "aiohttp.abc.AbstractAccessLogger").
        * **access\_log** – [`logging.Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "(in Python v3.14)") instance used for saving
          access logs. Use `None` for disabling logs for
          sake of speedup.
        * **access\_log\_format** – access log format, see
          [Format specification](logging.html#aiohttp-logging-access-log-format-spec)
          for details.
        * **handle\_signals** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – override signal TERM handling to gracefully
          exit the application.
        * **reuse\_address** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – tells the kernel to reuse a local socket in
          TIME\_WAIT state, without waiting for its
          natural timeout to expire. If not specified
          will automatically be set to True on UNIX.
        * **reuse\_port** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – tells the kernel to allow this endpoint to be
          bound to the same port as other existing
          endpoints are bound to, so long as they all set
          this flag when being created. This option is not
          supported on Windows.
        * **handler\_cancellation** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – cancels the web handler task if the client
          drops the connection. This is recommended
          if familiar with asyncio behavior or
          scalability is a concern.
          [Peer disconnection](web_advanced.html#aiohttp-web-peer-disconnection)
        * **kwargs** – additional named parameters to pass into
          [`AppRunner`](#aiohttp.web.AppRunner "aiohttp.web.AppRunner") constructor.

    Added in version 3.0: Support *access\_log\_class* parameter.

    Support *reuse\_address*, *reuse\_port* parameter.

    Added in version 3.1: Accept a coroutine as *app* parameter.

    Added in version 3.9: Support handler\_cancellation parameter (this was the default behavior
    in aiohttp <3.7).

## Constants[¶](#constants "Link to this heading")

class aiohttp.web.ContentCoding[[source]](_modules/aiohttp/web_response.html#ContentCoding)[¶](#aiohttp.web.ContentCoding "Link to this definition")
:   An [`enum.Enum`](https://docs.python.org/3/library/enum.html#enum.Enum "(in Python v3.14)") class of available Content Codings.

    deflate[¶](#aiohttp.web.ContentCoding.deflate "Link to this definition")
    :   *DEFLATE compression*

    gzip[¶](#aiohttp.web.ContentCoding.gzip "Link to this definition")
    :   *GZIP compression*

    identity[¶](#aiohttp.web.ContentCoding.identity "Link to this definition")
    :   *no compression*

## Middlewares[¶](#middlewares "Link to this heading")

aiohttp.web.normalize\_path\_middleware(*\**, *append\_slash=True*, *remove\_slash=False*, *merge\_slashes=True*, *redirect\_class=HTTPPermanentRedirect*)[[source]](_modules/aiohttp/web_middlewares.html#normalize_path_middleware)[¶](#aiohttp.web.normalize_path_middleware "Link to this definition")
:   Middleware factory which produces a middleware that normalizes
    the path of a request. By normalizing it means:

    > * Add or remove a trailing slash to the path.
    > * Double slashes are replaced by one.

    The middleware returns as soon as it finds a path that resolves
    correctly. The order if both merge and append/remove are enabled is:

    > 1. *merge\_slashes*
    > 2. *append\_slash* or *remove\_slash*
    > 3. both *merge\_slashes* and *append\_slash* or *remove\_slash*

    If the path resolves with at least one of those conditions, it will
    redirect to the new path.

    Only one of *append\_slash* and *remove\_slash* can be enabled. If both are
    `True` the factory will raise an `AssertionError`

    If *append\_slash* is `True` the middleware will append a slash when
    needed. If a resource is defined with trailing slash and the request
    comes without it, it will append it automatically.

    If *remove\_slash* is `True`, *append\_slash* must be `False`. When enabled
    the middleware will remove trailing slashes and redirect if the resource is
    defined.

    If *merge\_slashes* is `True`, merge multiple consecutive slashes in the
    path into one.

    Added in version 3.4: Support for *remove\_slash*

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
  + [Low Level](web_lowlevel.html)
  + [Reference](#)
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
[Page source](_sources/web_reference.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
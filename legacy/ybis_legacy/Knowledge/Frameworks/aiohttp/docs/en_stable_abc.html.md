Abstract Base Classes — aiohttp 3.13.3 documentation

# Abstract Base Classes[¶](#module-aiohttp.abc "Link to this heading")

## Abstract routing[¶](#abstract-routing "Link to this heading")

aiohttp has abstract classes for managing web interfaces.

The most part of [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") is not intended to be inherited
but few of them are.

aiohttp.web is built on top of few concepts: *application*, *router*,
*request* and *response*.

*router* is a *pluggable* part: a library user may build a *router*
from scratch, all other parts should work with new router seamlessly.

[`aiohttp.abc.AbstractRouter`](#aiohttp.abc.AbstractRouter "aiohttp.abc.AbstractRouter") has the only mandatory method:
[`aiohttp.abc.AbstractRouter.resolve()`](#aiohttp.abc.AbstractRouter.resolve "aiohttp.abc.AbstractRouter.resolve") coroutine. It must return an
[`aiohttp.abc.AbstractMatchInfo`](#aiohttp.abc.AbstractMatchInfo "aiohttp.abc.AbstractMatchInfo") instance.

If the requested URL handler is found
[`aiohttp.abc.AbstractMatchInfo.handler()`](#aiohttp.abc.AbstractMatchInfo.handler "aiohttp.abc.AbstractMatchInfo.handler") is a [web-handler](glossary.html#term-web-handler) for
requested URL and [`aiohttp.abc.AbstractMatchInfo.http_exception`](#aiohttp.abc.AbstractMatchInfo.http_exception "aiohttp.abc.AbstractMatchInfo.http_exception") is `None`.

Otherwise [`aiohttp.abc.AbstractMatchInfo.http_exception`](#aiohttp.abc.AbstractMatchInfo.http_exception "aiohttp.abc.AbstractMatchInfo.http_exception") is an instance of
[`HTTPException`](web_reference.html#aiohttp.web.HTTPException "aiohttp.web.HTTPException") like *404: NotFound* or *405: Method
Not Allowed*. [`aiohttp.abc.AbstractMatchInfo.handler()`](#aiohttp.abc.AbstractMatchInfo.handler "aiohttp.abc.AbstractMatchInfo.handler") raises
[`http_exception`](#aiohttp.abc.AbstractMatchInfo.http_exception "aiohttp.abc.AbstractMatchInfo.http_exception") on call.

class aiohttp.abc.AbstractRouter[[source]](_modules/aiohttp/abc.html#AbstractRouter)[¶](#aiohttp.abc.AbstractRouter "Link to this definition")
:   Abstract router, [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") accepts it as
    *router* parameter and returns as
    [`aiohttp.web.Application.router`](web_reference.html#aiohttp.web.Application.router "aiohttp.web.Application.router").

    async resolve(*request*)[[source]](_modules/aiohttp/abc.html#AbstractRouter.resolve)[¶](#aiohttp.abc.AbstractRouter.resolve "Link to this definition")
    :   Performs URL resolving. It’s an abstract method, should be
        overridden in *router* implementation.

        Parameters:
        :   **request** – [`aiohttp.web.Request`](web_reference.html#aiohttp.web.Request "aiohttp.web.Request") instance for
            resolving, the request has
            [`aiohttp.web.Request.match_info`](web_reference.html#aiohttp.web.Request.match_info "aiohttp.web.Request.match_info") equals to
            `None` at resolving stage.

        Returns:
        :   [`aiohttp.abc.AbstractMatchInfo`](#aiohttp.abc.AbstractMatchInfo "aiohttp.abc.AbstractMatchInfo") instance.

class aiohttp.abc.AbstractMatchInfo[[source]](_modules/aiohttp/abc.html#AbstractMatchInfo)[¶](#aiohttp.abc.AbstractMatchInfo "Link to this definition")
:   Abstract *match info*, returned by [`aiohttp.abc.AbstractRouter.resolve()`](#aiohttp.abc.AbstractRouter.resolve "aiohttp.abc.AbstractRouter.resolve") call.

    http\_exception[¶](#aiohttp.abc.AbstractMatchInfo.http_exception "Link to this definition")
    :   [`aiohttp.web.HTTPException`](web_reference.html#aiohttp.web.HTTPException "aiohttp.web.HTTPException") if no match was found, `None`
        otherwise.

    async handler(*request*)[¶](#aiohttp.abc.AbstractMatchInfo.handler "Link to this definition")
    :   Abstract method performing [web-handler](glossary.html#term-web-handler) processing.

        Parameters:
        :   **request** – [`aiohttp.web.Request`](web_reference.html#aiohttp.web.Request "aiohttp.web.Request") instance for
            resolving, the request has
            [`aiohttp.web.Request.match_info`](web_reference.html#aiohttp.web.Request.match_info "aiohttp.web.Request.match_info") equals to
            `None` at resolving stage.

        Returns:
        :   [`aiohttp.web.StreamResponse`](web_reference.html#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse") or descendants.

        Raise:
        :   [`aiohttp.web.HTTPException`](web_reference.html#aiohttp.web.HTTPException "aiohttp.web.HTTPException") on error

    async expect\_handler(*request*)[¶](#aiohttp.abc.AbstractMatchInfo.expect_handler "Link to this definition")
    :   Abstract method for handling *100-continue* processing.

## Abstract Class Based Views[¶](#abstract-class-based-views "Link to this heading")

For *class based view* support aiohttp has abstract
[`AbstractView`](#aiohttp.abc.AbstractView "aiohttp.abc.AbstractView") class which is *awaitable* (may be uses like
`await Cls()` or `yield from Cls()` and has a *request* as an
attribute.

class aiohttp.abc.AbstractView[[source]](_modules/aiohttp/abc.html#AbstractView)[¶](#aiohttp.abc.AbstractView "Link to this definition")
:   An abstract class, base for all *class based views* implementations.

    Methods `__iter__` and `__await__` should be overridden.

    request[¶](#aiohttp.abc.AbstractView.request "Link to this definition")
    :   [`aiohttp.web.Request`](web_reference.html#aiohttp.web.Request "aiohttp.web.Request") instance for performing the request.

## Abstract Cookie Jar[¶](#abstract-cookie-jar "Link to this heading")

class aiohttp.abc.AbstractCookieJar[[source]](_modules/aiohttp/abc.html#AbstractCookieJar)[¶](#aiohttp.abc.AbstractCookieJar "Link to this definition")
:   The cookie jar instance is available as [`aiohttp.ClientSession.cookie_jar`](client_reference.html#aiohttp.ClientSession.cookie_jar "aiohttp.ClientSession.cookie_jar").

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

    An abstract class for cookie storage. Implements
    [`collections.abc.Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable "(in Python v3.14)") and
    [`collections.abc.Sized`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sized "(in Python v3.14)").

    update\_cookies(*cookies*, *response\_url=None*)[[source]](_modules/aiohttp/abc.html#AbstractCookieJar.update_cookies)[¶](#aiohttp.abc.AbstractCookieJar.update_cookies "Link to this definition")
    :   Update cookies returned by server in `Set-Cookie` header.

        Parameters:
        :   * **cookies** – a [`collections.abc.Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping "(in Python v3.14)")
              (e.g. [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)"), [`SimpleCookie`](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie "(in Python v3.14)")) or
              *iterable* of *pairs* with cookies returned by server’s
              response.
            * **response\_url** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – URL of response, `None` for *shared
              cookies*. Regular cookies are coupled with server’s URL and
              are sent only to this server, shared ones are sent in every
              client request.

    filter\_cookies(*request\_url*)[[source]](_modules/aiohttp/abc.html#AbstractCookieJar.filter_cookies)[¶](#aiohttp.abc.AbstractCookieJar.filter_cookies "Link to this definition")
    :   Return jar’s cookies acceptable for URL and available in
        `Cookie` header for sending client requests for given URL.

        Parameters:
        :   **response\_url** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – request’s URL for which cookies are asked.

        Returns:
        :   [`http.cookies.SimpleCookie`](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie "(in Python v3.14)") with filtered
            cookies for given URL.

    clear(*predicate=None*)[[source]](_modules/aiohttp/abc.html#AbstractCookieJar.clear)[¶](#aiohttp.abc.AbstractCookieJar.clear "Link to this definition")
    :   Removes all cookies from the jar if the predicate is `None`. Otherwise remove only those [`Morsel`](https://docs.python.org/3/library/http.cookies.html#http.cookies.Morsel "(in Python v3.14)") that `predicate(morsel)` returns `True`.

        Parameters:
        :   **predicate** –

            callable that gets [`Morsel`](https://docs.python.org/3/library/http.cookies.html#http.cookies.Morsel "(in Python v3.14)") as a parameter and returns `True` if this [`Morsel`](https://docs.python.org/3/library/http.cookies.html#http.cookies.Morsel "(in Python v3.14)") must be deleted from the jar.

            Added in version 3.8.

    clear\_domain(*domain*)[[source]](_modules/aiohttp/abc.html#AbstractCookieJar.clear_domain)[¶](#aiohttp.abc.AbstractCookieJar.clear_domain "Link to this definition")
    :   Remove all cookies from the jar that belongs to the specified domain or its subdomains.

        Parameters:
        :   **domain** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – domain for which cookies must be deleted from the jar.

        Added in version 3.8.

## Abstract Access Logger[¶](#abstract-access-logger "Link to this heading")

class aiohttp.abc.AbstractAccessLogger[[source]](_modules/aiohttp/abc.html#AbstractAccessLogger)[¶](#aiohttp.abc.AbstractAccessLogger "Link to this definition")
:   An abstract class, base for all `aiohttp.web.RequestHandler`
    `access_logger` implementations

    Method `log` should be overridden.

    log(*request*, *response*, *time*)[[source]](_modules/aiohttp/abc.html#AbstractAccessLogger.log)[¶](#aiohttp.abc.AbstractAccessLogger.log "Link to this definition")
    :   Parameters:
        :   * **request** – [`aiohttp.web.Request`](web_reference.html#aiohttp.web.Request "aiohttp.web.Request") object.
            * **response** – [`aiohttp.web.Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response") object.
            * **time** ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")) – Time taken to serve the request.

    enabled[¶](#aiohttp.abc.AbstractAccessLogger.enabled "Link to this definition")
    :   Return True if logger is enabled.

        Override this property if logging is disabled to avoid the
        overhead of calculating details to feed the logger.

        This property may be omitted if logging is always enabled.

## Abstract Resolver[¶](#abstract-resolver "Link to this heading")

class aiohttp.abc.AbstractResolver[[source]](_modules/aiohttp/abc.html#AbstractResolver)[¶](#aiohttp.abc.AbstractResolver "Link to this definition")
:   An abstract class, base for all resolver implementations.

    Method `resolve` should be overridden.

    resolve(*host*, *port*, *family*)[[source]](_modules/aiohttp/abc.html#AbstractResolver.resolve)[¶](#aiohttp.abc.AbstractResolver.resolve "Link to this definition")
    :   Resolve host name to IP address.

        Parameters:
        :   * **host** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – host name to resolve.
            * **port** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – port number.
            * **family** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – socket family.

        Returns:
        :   list of [`aiohttp.abc.ResolveResult`](#aiohttp.abc.ResolveResult "aiohttp.abc.ResolveResult") instances.

    close()[[source]](_modules/aiohttp/abc.html#AbstractResolver.close)[¶](#aiohttp.abc.AbstractResolver.close "Link to this definition")
    :   Release resolver.

class aiohttp.abc.ResolveResult[[source]](_modules/aiohttp/abc.html#ResolveResult)[¶](#aiohttp.abc.ResolveResult "Link to this definition")
:   Result of host name resolution.

    hostname[¶](#aiohttp.abc.ResolveResult.hostname "Link to this definition")
    :   The host name that was provided.

    host[¶](#aiohttp.abc.ResolveResult.host "Link to this definition")
    :   The IP address that was resolved.

    port[¶](#aiohttp.abc.ResolveResult.port "Link to this definition")
    :   The port that was resolved.

    family[¶](#aiohttp.abc.ResolveResult.family "Link to this definition")
    :   The address family that was resolved.

    proto[¶](#aiohttp.abc.ResolveResult.proto "Link to this definition")
    :   The protocol that was resolved.

    flags[¶](#aiohttp.abc.ResolveResult.flags "Link to this definition")
    :   The flags that were resolved.

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
* [Utilities](utilities.html)
  + [Abstract Base Classes](#)
  + [Working with Multipart](multipart.html)
  + [Multipart reference](multipart_reference.html)
  + [Streaming API](streams.html)
  + [Common data structures](structures.html)
  + [WebSocket utilities](websocket_utilities.html)
* [FAQ](faq.html)
* [Miscellaneous](misc.html)
* [Who uses aiohttp?](external.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/abc.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
Glossary — aiohttp 3.13.3 documentation

# Glossary[¶](#glossary "Link to this heading")

aiodns[¶](#term-aiodns "Link to this term")
:   DNS resolver for asyncio.

    <https://pypi.python.org/pypi/aiodns>

asyncio[¶](#term-asyncio "Link to this term")
:   The library for writing single-threaded concurrent code using
    coroutines, multiplexing I/O access over sockets and other
    resources, running network clients and servers, and other
    related primitives.

    Reference implementation of [**PEP 3156**](https://peps.python.org/pep-3156/)

    <https://pypi.python.org/pypi/asyncio/>

Brotli[¶](#term-Brotli "Link to this term")
:   Brotli is a generic-purpose lossless compression algorithm that
    compresses data using a combination of a modern variant
    of the LZ77 algorithm, Huffman coding and second order context modeling,
    with a compression ratio comparable to the best currently available
    general-purpose compression methods. It is similar in speed with deflate
    but offers more dense compression.

    The specification of the Brotli Compressed Data Format is defined [**RFC 7932**](https://datatracker.ietf.org/doc/html/rfc7932.html)

    <https://pypi.org/project/Brotli/>

brotlicffi[¶](#term-brotlicffi "Link to this term")
:   An alternative implementation of [Brotli](#term-Brotli) built using the CFFI
    library. This implementation supports PyPy correctly.

    <https://pypi.org/project/brotlicffi/>

callable[¶](#term-callable "Link to this term")
:   Any object that can be called. Use [`callable()`](https://docs.python.org/3/library/functions.html#callable "(in Python v3.14)") to check
    that.

gunicorn[¶](#term-gunicorn "Link to this term")
:   Gunicorn ‘Green Unicorn’ is a Python WSGI HTTP Server for
    UNIX.

    <http://gunicorn.org/>

IDNA[¶](#term-IDNA "Link to this term")
:   An Internationalized Domain Name in Applications (IDNA) is an
    industry standard for encoding Internet Domain Names that contain in
    whole or in part, in a language-specific script or alphabet,
    such as Arabic, Chinese, Cyrillic, Tamil, Hebrew or the Latin
    alphabet-based characters with diacritics or ligatures, such as
    French. These writing systems are encoded by computers in
    multi-byte Unicode. Internationalized domain names are stored
    in the Domain Name System as ASCII strings using Punycode
    transcription.

keep-alive[¶](#term-keep-alive "Link to this term")
:   A technique for communicating between HTTP client and server
    when connection is not closed after sending response but kept
    open for sending next request through the same socket.

    It makes communication faster by getting rid of connection
    establishment for every request.

nginx[¶](#term-nginx "Link to this term")
:   Nginx [engine x] is an HTTP and reverse proxy server, a mail
    proxy server, and a generic TCP/UDP proxy server.

    <https://nginx.org/en/>

percent-encoding[¶](#term-percent-encoding "Link to this term")
:   A mechanism for encoding information in a Uniform Resource
    Locator (URL) if URL parts don’t fit in safe characters space.

requests[¶](#term-requests "Link to this term")
:   Currently the most popular synchronous library to make
    HTTP requests in Python.

    <https://requests.readthedocs.io>

requoting[¶](#term-requoting "Link to this term")
:   Applying [percent-encoding](#term-percent-encoding) to non-safe symbols and decode
    percent encoded safe symbols back.

    According to [**RFC 3986**](https://datatracker.ietf.org/doc/html/rfc3986.html) allowed path symbols are:

    ```
    allowed       = unreserved / pct-encoded / sub-delims
                    / ":" / "@" / "/"

    pct-encoded   = "%" HEXDIG HEXDIG

    unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"

    sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
                    / "*" / "+" / "," / ";" / "="
    ```

resource[¶](#term-resource "Link to this term")
:   A concept reflects the HTTP **path**, every resource corresponds
    to *URI*.

    May have a unique name.

    Contains [route](#term-route)'s for different HTTP methods.

route[¶](#term-route "Link to this term")
:   A part of [resource](#term-resource), resource’s *path* coupled with HTTP method.

web-handler[¶](#term-web-handler "Link to this term")
:   An endpoint that returns HTTP response.

websocket[¶](#term-websocket "Link to this term")
:   A protocol providing full-duplex communication channels over a
    single TCP connection. The WebSocket protocol was standardized
    by the IETF as [**RFC 6455**](https://datatracker.ietf.org/doc/html/rfc6455.html)

yarl[¶](#term-yarl "Link to this term")
:   A library for operating with URL objects.

    <https://pypi.python.org/pypi/yarl>

## Environment Variables[¶](#environment-variables "Link to this heading")

AIOHTTP\_NO\_EXTENSIONS[¶](#envvar-AIOHTTP_NO_EXTENSIONS "Link to this definition")
:   If set to a non-empty value while building from source, aiohttp will be built without speedups
    written as C extensions. This option is primarily useful for debugging.

AIOHTTP\_USE\_SYSTEM\_DEPS[¶](#envvar-AIOHTTP_USE_SYSTEM_DEPS "Link to this definition")
:   If set to a non-empty value while building from source, aiohttp will be built against
    the system installation of llhttp rather than the vendored library. This option is primarily
    meant to be used by downstream redistributors.

NETRC[¶](#envvar-NETRC "Link to this definition")
:   If set, HTTP Basic Auth will be read from the file pointed to by this environment variable,
    rather than from `~/.netrc`.

    See also

    `.netrc` documentation: <https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html>

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
* [Utilities](utilities.html)
* [FAQ](faq.html)
* [Miscellaneous](misc.html)
  + [Essays](essays.html)
  + [Glossary](#)
  + [Changelog](changes.html)
  + [Indices and tables](misc.html#indices-and-tables)
* [Who uses aiohttp?](external.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/glossary.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
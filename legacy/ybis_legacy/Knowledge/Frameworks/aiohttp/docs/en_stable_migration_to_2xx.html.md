Migration to 2.x — aiohttp 3.13.3 documentation

# Migration to 2.x[¶](#migration-to-2-x "Link to this heading")

## Client[¶](#client "Link to this heading")

### chunking[¶](#chunking "Link to this heading")

aiohttp does not support custom chunking sizes. It is up to the developer
to decide how to chunk data streams. If chunking is enabled, aiohttp
encodes the provided chunks in the “Transfer-encoding: chunked” format.

aiohttp does not enable chunked encoding automatically even if a
*transfer-encoding* header is supplied: *chunked* has to be set
explicitly. If *chunked* is set, then the *Transfer-encoding* and
*content-length* headers are disallowed.

### compression[¶](#compression "Link to this heading")

Compression has to be enabled explicitly with the *compress* parameter.
If compression is enabled, adding a *content-encoding* header is not allowed.
Compression also enables the *chunked* transfer-encoding.
Compression can not be combined with a *Content-Length* header.

### Client Connector[¶](#client-connector "Link to this heading")

1. By default a connector object manages a total number of concurrent
   connections. This limit was a per host rule in version 1.x. In
   2.x, the limit parameter defines how many concurrent connection
   connector can open and a new limit\_per\_host parameter defines the
   limit per host. By default there is no per-host limit.
2. BaseConnector.close is now a normal function as opposed to
   coroutine in version 1.x
3. BaseConnector.conn\_timeout was moved to ClientSession

### ClientResponse.release[¶](#clientresponse-release "Link to this heading")

Internal implementation was significantly redesigned. It is not
required to call release on the response object. When the client
fully receives the payload, the underlying connection automatically
returns back to pool. If the payload is not fully read, the connection
is closed

### Client exceptions[¶](#client-exceptions "Link to this heading")

Exception hierarchy has been significantly modified. aiohttp now defines only
exceptions that covers connection handling and server response misbehaviors.
For developer specific mistakes, aiohttp uses python standard exceptions
like ValueError or TypeError.

Reading a response content may raise a ClientPayloadError
exception. This exception indicates errors specific to the payload
encoding. Such as invalid compressed data, malformed chunked-encoded
chunks or not enough data that satisfy the content-length header.

All exceptions are moved from aiohttp.errors module to top level
aiohttp module.

New hierarchy of exceptions:

* ClientError - Base class for all client specific exceptions

  + ClientResponseError - exceptions that could happen after we get
    response from server

    - WSServerHandshakeError - web socket server response error

      * ClientHttpProxyError - proxy response
  + ClientConnectionError - exceptions related to low-level
    connection problems

    - ClientOSError - subset of connection errors that are initiated
      by an OSError exception

      * ClientConnectorError - connector related exceptions

        + ClientProxyConnectionError - proxy connection initialization error

          - ServerConnectionError - server connection related errors
        + ServerDisconnectedError - server disconnected
        + ServerTimeoutError - server operation timeout, (read timeout, etc)
        + ServerFingerprintMismatch - server fingerprint mismatch
  + ClientPayloadError - This exception can only be raised while
    reading the response payload if one of these errors occurs:
    invalid compression, malformed chunked encoding or not enough data
    that satisfy content-length header.

### Client payload (form-data)[¶](#client-payload-form-data "Link to this heading")

To unify form-data/payload handling a new Payload system was
introduced. It handles customized handling of existing types and
provide implementation for user-defined types.

1. FormData.\_\_call\_\_ does not take an encoding arg anymore
   and its return value changes from an iterator or bytes to a Payload instance.
   aiohttp provides payload adapters for some standard types like str, byte,
   io.IOBase, StreamReader or DataQueue.
2. a generator is not supported as data provider anymore, streamer
   can be used instead. For example, to upload data from file:

   ```
   @aiohttp.streamer
   def file_sender(writer, file_name=None):
         with open(file_name, 'rb') as f:
             chunk = f.read(2**16)
             while chunk:
                 yield from writer.write(chunk)
                 chunk = f.read(2**16)

   # Then you can use `file_sender` like this:

   async with session.post('http://httpbin.org/post',
                           data=file_sender(file_name='huge_file')) as resp:
          print(await resp.text())
   ```

### Various[¶](#various "Link to this heading")

1. the encoding parameter is deprecated in ClientSession.request().
   Payload encoding is controlled at the payload level.
   It is possible to specify an encoding for each payload instance.
2. the version parameter is removed in ClientSession.request()
   client version can be specified in the ClientSession constructor.
3. aiohttp.MsgType dropped, use aiohttp.WSMsgType instead.
4. ClientResponse.url is an instance of yarl.URL class (url\_obj
   is deprecated)
5. ClientResponse.raise\_for\_status() raises
   [`aiohttp.ClientResponseError`](client_reference.html#aiohttp.ClientResponseError "aiohttp.ClientResponseError") exception
6. ClientResponse.json() is strict about response’s content type. if
   content type does not match, it raises
   [`aiohttp.ClientResponseError`](client_reference.html#aiohttp.ClientResponseError "aiohttp.ClientResponseError") exception. To disable content
   type check you can pass `None` as content\_type parameter.

## Server[¶](#server "Link to this heading")

### ServerHttpProtocol and low-level details[¶](#serverhttpprotocol-and-low-level-details "Link to this heading")

Internal implementation was significantly redesigned to provide
better performance and support HTTP pipelining.
ServerHttpProtocol is dropped, implementation is merged with RequestHandler
a lot of low-level api’s are dropped.

### Application[¶](#application "Link to this heading")

1. Constructor parameter loop is deprecated. Loop is get configured by application runner,
   run\_app function for any of gunicorn workers.
2. Application.router.add\_subapp is dropped, use Application.add\_subapp instead
3. Application.finished is dropped, use Application.cleanup instead

### WebRequest and WebResponse[¶](#webrequest-and-webresponse "Link to this heading")

1. the GET and POST attributes no longer exist. Use the query attribute instead of GET
2. Custom chunking size is not support WebResponse.chunked - developer is
   responsible for actual chunking.
3. Payloads are supported as body. So it is possible to use client response’s content
   object as body parameter for WebResponse
4. FileSender api is dropped, it is replaced with more general FileResponse class:

   ```
   async def handle(request):
       return web.FileResponse('path-to-file.txt')
   ```
5. WebSocketResponse.protocol is renamed to WebSocketResponse.ws\_protocol.
   WebSocketResponse.protocol is instance of RequestHandler class.

### RequestPayloadError[¶](#requestpayloaderror "Link to this heading")

Reading request’s payload may raise a RequestPayloadError exception. The behavior is similar
to ClientPayloadError.

### WSGI[¶](#wsgi "Link to this heading")

*WSGI* support has been dropped, as well as gunicorn wsgi support. We still provide default and uvloop gunicorn workers for web.Application

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
  + [Glossary](glossary.html)
  + [Changelog](changes.html)
  + [Indices and tables](misc.html#indices-and-tables)
* [Who uses aiohttp?](external.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/migration_to_2xx.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
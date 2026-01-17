Streaming API — aiohttp 3.13.3 documentation

# Streaming API[¶](#streaming-api "Link to this heading")

`aiohttp` uses streams for retrieving *BODIES*:
[`aiohttp.web.BaseRequest.content`](web_reference.html#aiohttp.web.BaseRequest.content "aiohttp.web.BaseRequest.content") and
[`aiohttp.ClientResponse.content`](client_reference.html#aiohttp.ClientResponse.content "aiohttp.ClientResponse.content") are properties with stream API.

class aiohttp.StreamReader[[source]](_modules/aiohttp/streams.html#StreamReader)[¶](#aiohttp.StreamReader "Link to this definition")
:   The reader from incoming stream.

    User should never instantiate streams manually but use existing
    [`aiohttp.web.BaseRequest.content`](web_reference.html#aiohttp.web.BaseRequest.content "aiohttp.web.BaseRequest.content") and
    [`aiohttp.ClientResponse.content`](client_reference.html#aiohttp.ClientResponse.content "aiohttp.ClientResponse.content") properties for accessing raw
    BODY data.

## Reading Attributes and Methods[¶](#reading-attributes-and-methods "Link to this heading")

StreamReader.read(*n=-1*)[[source]](_modules/aiohttp/streams.html#StreamReader.read)[¶](#aiohttp.StreamReader.read "Link to this definition")

:async:
:   Read up to a maximum of *n* bytes. If *n* is not provided, or set to `-1`,
    read until EOF and return all read bytes.

    When *n* is provided, data will be returned as soon as it is available.
    Therefore it will return less than *n* bytes if there are less than *n*
    bytes in the buffer.

    If the EOF was received and the internal buffer is empty, return an
    empty bytes object.

    Parameters:
    :   **n** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – maximum number of bytes to read, `-1` for the whole stream.

    Return bytes:
    :   the given data

StreamReader.readany()[[source]](_modules/aiohttp/streams.html#StreamReader.readany)[¶](#aiohttp.StreamReader.readany "Link to this definition")

:async:
:   Read next data portion for the stream.

    Returns immediately if internal buffer has a data.

    Return bytes:
    :   the given data

StreamReader.readexactly(*n*)[[source]](_modules/aiohttp/streams.html#StreamReader.readexactly)[¶](#aiohttp.StreamReader.readexactly "Link to this definition")

:async:
:   Read exactly *n* bytes.

    Raise an [`asyncio.IncompleteReadError`](https://docs.python.org/3/library/asyncio-exceptions.html#asyncio.IncompleteReadError "(in Python v3.14)") if the end of the
    stream is reached before *n* can be read, the
    [`asyncio.IncompleteReadError.partial`](https://docs.python.org/3/library/asyncio-exceptions.html#asyncio.IncompleteReadError.partial "(in Python v3.14)") attribute of the
    exception contains the partial read bytes.

    Parameters:
    :   **n** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – how many bytes to read.

    Return bytes:
    :   the given data

StreamReader.readline()[[source]](_modules/aiohttp/streams.html#StreamReader.readline)[¶](#aiohttp.StreamReader.readline "Link to this definition")

:async:
:   Read one line, where “line” is a sequence of bytes ending
    with `\n`.

    If EOF is received, and `\n` was not found, the method will
    return the partial read bytes.

    If the EOF was received and the internal buffer is empty, return an
    empty bytes object.

    Return bytes:
    :   the given line

StreamReader.readuntil(*separator='\n'*)[[source]](_modules/aiohttp/streams.html#StreamReader.readuntil)[¶](#aiohttp.StreamReader.readuntil "Link to this definition")

:async:
:   Read until separator, where separator is a sequence of bytes.

    If EOF is received, and separator was not found, the method will
    return the partial read bytes.

    If the EOF was received and the internal buffer is empty, return an
    empty bytes object.

    Added in version 3.8.

    Return bytes:
    :   the given data

StreamReader.readchunk()[[source]](_modules/aiohttp/streams.html#StreamReader.readchunk)[¶](#aiohttp.StreamReader.readchunk "Link to this definition")

:async:
:   Read a chunk of data as it was received by the server.

    Returns a tuple of (data, end\_of\_HTTP\_chunk).

    When chunked transfer encoding is used, end\_of\_HTTP\_chunk is a [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")
    indicating if the end of the data corresponds to the end of a HTTP chunk,
    otherwise it is always `False`.

    Return tuple[bytes, bool]:
    :   a chunk of data and a [`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") that is `True`
        when the end of the returned chunk corresponds
        to the end of a HTTP chunk.

StreamReader.total\_raw\_bytes[¶](#aiohttp.StreamReader.total_raw_bytes "Link to this definition")
:   The number of bytes of raw data downloaded (before decompression).

    Readonly [`int`](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)") property.

## Asynchronous Iteration Support[¶](#asynchronous-iteration-support "Link to this heading")

Stream reader supports asynchronous iteration over BODY.

By default it iterates over lines:

```
async for line in response.content:
    print(line)
```

Also there are methods for iterating over data chunks with maximum
size limit and over any available data.

async StreamReader.iter\_chunked(*n*)[¶](#aiohttp.StreamReader.iter_chunked "Link to this definition")
:   Iterates over data chunks with maximum size limit:

    ```
    async for data in response.content.iter_chunked(1024):
        print(data)
    ```

    To get chunks that are exactly *n* bytes, you could use the
    [asyncstdlib.itertools](https://asyncstdlib.readthedocs.io/en/stable/source/api/itertools.html)
    module:

    ```
    chunks = batched(chain.from_iterable(response.content.iter_chunked(n)), n)
    async for data in chunks:
        print(data)
    ```

async StreamReader.iter\_any()[¶](#aiohttp.StreamReader.iter_any "Link to this definition")
:   Iterates over data chunks in order of intaking them into the stream:

    ```
    async for data in response.content.iter_any():
        print(data)
    ```

async StreamReader.iter\_chunks()[¶](#aiohttp.StreamReader.iter_chunks "Link to this definition")
:   Iterates over data chunks as received from the server:

    ```
    async for data, _ in response.content.iter_chunks():
        print(data)
    ```

    If chunked transfer encoding is used, the original http chunks formatting
    can be retrieved by reading the second element of returned tuples:

    ```
    buffer = b""

    async for data, end_of_http_chunk in response.content.iter_chunks():
        buffer += data
        if end_of_http_chunk:
            print(buffer)
            buffer = b""
    ```

## Helpers[¶](#helpers "Link to this heading")

StreamReader.exception()[[source]](_modules/aiohttp/streams.html#StreamReader.exception)[¶](#aiohttp.StreamReader.exception "Link to this definition")
:   Get the exception occurred on data reading.

aiohttp.is\_eof()[¶](#aiohttp.is_eof "Link to this definition")
:   Return `True` if EOF was reached.

    Internal buffer may be not empty at the moment.

    See also

    [`StreamReader.at_eof()`](#aiohttp.StreamReader.at_eof "aiohttp.StreamReader.at_eof")

StreamReader.at\_eof()[[source]](_modules/aiohttp/streams.html#StreamReader.at_eof)[¶](#aiohttp.StreamReader.at_eof "Link to this definition")
:   Return `True` if the buffer is empty and EOF was reached.

StreamReader.read\_nowait(*n=None*)[[source]](_modules/aiohttp/streams.html#StreamReader.read_nowait)[¶](#aiohttp.StreamReader.read_nowait "Link to this definition")
:   Returns data from internal buffer if any, empty bytes object otherwise.

    Raises [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") if other coroutine is waiting for stream.

    Parameters:
    :   **n** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – how many bytes to read, `-1` for the whole internal
        buffer.

    Return bytes:
    :   the given data

StreamReader.unread\_data(*data*)[[source]](_modules/aiohttp/streams.html#StreamReader.unread_data)[¶](#aiohttp.StreamReader.unread_data "Link to this definition")
:   Rollback reading some data from stream, inserting it to buffer head.

    Parameters:
    :   **data** ([*bytes*](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")) – data to push back into the stream.

    Warning

    The method does not wake up waiters.

    E.g. [`read()`](#aiohttp.StreamReader.read "aiohttp.StreamReader.read") will not be resumed.

aiohttp.wait\_eof()[¶](#aiohttp.wait_eof "Link to this definition")

:async:
:   Wait for EOF. The given data may be accessible by upcoming read calls.

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
* [Utilities](utilities.html)
  + [Abstract Base Classes](abc.html)
  + [Working with Multipart](multipart.html)
  + [Multipart reference](multipart_reference.html)
  + [Streaming API](#)
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
[Page source](_sources/streams.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
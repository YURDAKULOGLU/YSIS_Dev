Multipart reference — aiohttp 3.13.3 documentation

# Multipart reference[¶](#multipart-reference "Link to this heading")

class aiohttp.MultipartResponseWrapper(*resp*, *stream*)[¶](#aiohttp.MultipartResponseWrapper "Link to this definition")
:   Wrapper around the [`MultipartReader`](#aiohttp.MultipartReader "aiohttp.MultipartReader") to take care about
    underlying connection and close it when it needs in.

    at\_eof()[¶](#aiohttp.MultipartResponseWrapper.at_eof "Link to this definition")
    :   Returns `True` when all response data had been read.

        Return type:
        :   [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

    async next()[¶](#aiohttp.MultipartResponseWrapper.next "Link to this definition")
    :   Emits next multipart reader object.

    async release()[¶](#aiohttp.MultipartResponseWrapper.release "Link to this definition")
    :   Releases the connection gracefully, reading all the content
        to the void.

class aiohttp.BodyPartReader(*boundary*, *headers*, *content*)[[source]](_modules/aiohttp/multipart.html#BodyPartReader)[¶](#aiohttp.BodyPartReader "Link to this definition")
:   Multipart reader for single body part.

    async read(*\**, *decode=False*)[[source]](_modules/aiohttp/multipart.html#BodyPartReader.read)[¶](#aiohttp.BodyPartReader.read "Link to this definition")
    :   Reads body part data.

        Parameters:
        :   **decode** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – Decodes data following by encoding method
            from `Content-Encoding` header. If it
            missed data remains untouched

        Return type:
        :   [bytearray](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)")

    async read\_chunk(*size=chunk\_size*)[[source]](_modules/aiohttp/multipart.html#BodyPartReader.read_chunk)[¶](#aiohttp.BodyPartReader.read_chunk "Link to this definition")
    :   Reads body part content chunk of the specified size.

        Parameters:
        :   **size** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – chunk size

        Return type:
        :   [bytearray](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)")

    async readline()[[source]](_modules/aiohttp/multipart.html#BodyPartReader.readline)[¶](#aiohttp.BodyPartReader.readline "Link to this definition")
    :   Reads body part by line by line.

        Return type:
        :   [bytearray](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)")

    async release()[[source]](_modules/aiohttp/multipart.html#BodyPartReader.release)[¶](#aiohttp.BodyPartReader.release "Link to this definition")
    :   Like [`read()`](#aiohttp.BodyPartReader.read "aiohttp.BodyPartReader.read"), but reads all the data to the void.

        Return type:
        :   None

    async text(*\**, *encoding=None*)[[source]](_modules/aiohttp/multipart.html#BodyPartReader.text)[¶](#aiohttp.BodyPartReader.text "Link to this definition")
    :   Like [`read()`](#aiohttp.BodyPartReader.read "aiohttp.BodyPartReader.read"), but assumes that body part contains text data.

        Parameters:
        :   **encoding** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Custom text encoding. Overrides specified
            in charset param of `Content-Type` header

        Return type:
        :   [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")

    async json(*\**, *encoding=None*)[[source]](_modules/aiohttp/multipart.html#BodyPartReader.json)[¶](#aiohttp.BodyPartReader.json "Link to this definition")
    :   Like [`read()`](#aiohttp.BodyPartReader.read "aiohttp.BodyPartReader.read"), but assumes that body parts contains JSON data.

        Parameters:
        :   **encoding** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Custom JSON encoding. Overrides specified
            in charset param of `Content-Type` header

    async form(*\**, *encoding=None*)[[source]](_modules/aiohttp/multipart.html#BodyPartReader.form)[¶](#aiohttp.BodyPartReader.form "Link to this definition")
    :   Like [`read()`](#aiohttp.BodyPartReader.read "aiohttp.BodyPartReader.read"), but assumes that body parts contains form
        urlencoded data.

        Parameters:
        :   **encoding** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – Custom form encoding. Overrides specified
            in charset param of `Content-Type` header

    at\_eof()[[source]](_modules/aiohttp/multipart.html#BodyPartReader.at_eof)[¶](#aiohttp.BodyPartReader.at_eof "Link to this definition")
    :   Returns `True` if the boundary was reached or `False` otherwise.

        Return type:
        :   [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

    decode(*data*)[[source]](_modules/aiohttp/multipart.html#BodyPartReader.decode)[¶](#aiohttp.BodyPartReader.decode "Link to this definition")
    :   Decodes data according the specified `Content-Encoding`
        or `Content-Transfer-Encoding` headers value.

        Supports `gzip`, `deflate` and `identity` encodings for
        `Content-Encoding` header.

        Supports `base64`, `quoted-printable`, `binary` encodings for
        `Content-Transfer-Encoding` header.

        Parameters:
        :   **data** ([*bytearray*](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)")) – Data to decode.

        Raises:
        :   [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") - if encoding is unknown.

        Return type:
        :   [bytes](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")

    get\_charset(*default=None*)[[source]](_modules/aiohttp/multipart.html#BodyPartReader.get_charset)[¶](#aiohttp.BodyPartReader.get_charset "Link to this definition")
    :   Returns charset parameter from `Content-Type` header or default.

    name[¶](#aiohttp.BodyPartReader.name "Link to this definition")
    :   A field *name* specified in `Content-Disposition` header or `None`
        if missed or header is malformed.

        Readonly [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

    filename[¶](#aiohttp.BodyPartReader.filename "Link to this definition")
    :   A field *filename* specified in `Content-Disposition` header or `None`
        if missed or header is malformed.

        Readonly [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") property.

class aiohttp.MultipartReader(*headers*, *content*)[[source]](_modules/aiohttp/multipart.html#MultipartReader)[¶](#aiohttp.MultipartReader "Link to this definition")
:   Multipart body reader.

    classmethod from\_response(*cls*, *response*)[[source]](_modules/aiohttp/multipart.html#MultipartReader.from_response)[¶](#aiohttp.MultipartReader.from_response "Link to this definition")
    :   Constructs reader instance from HTTP response.

        Parameters:
        :   **response** – [`ClientResponse`](client_reference.html#aiohttp.ClientResponse "aiohttp.ClientResponse") instance

    at\_eof()[[source]](_modules/aiohttp/multipart.html#MultipartReader.at_eof)[¶](#aiohttp.MultipartReader.at_eof "Link to this definition")
    :   Returns `True` if the final boundary was reached or
        `False` otherwise.

        Return type:
        :   [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")

    async next()[[source]](_modules/aiohttp/multipart.html#MultipartReader.next)[¶](#aiohttp.MultipartReader.next "Link to this definition")
    :   Emits the next multipart body part.

    async release()[[source]](_modules/aiohttp/multipart.html#MultipartReader.release)[¶](#aiohttp.MultipartReader.release "Link to this definition")
    :   Reads all the body parts to the void till the final boundary.

    async fetch\_next\_part()[[source]](_modules/aiohttp/multipart.html#MultipartReader.fetch_next_part)[¶](#aiohttp.MultipartReader.fetch_next_part "Link to this definition")
    :   Returns the next body part reader.

class aiohttp.MultipartWriter(*subtype='mixed'*, *boundary=None*, *close\_boundary=True*)[[source]](_modules/aiohttp/multipart.html#MultipartWriter)[¶](#aiohttp.MultipartWriter "Link to this definition")
:   Multipart body writer.

    `boundary` may be an ASCII-only string.

    boundary[¶](#aiohttp.MultipartWriter.boundary "Link to this definition")
    :   The string ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) representation of the boundary.

        Changed in version 3.0: Property type was changed from [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") to [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)").

    append(*obj*, *headers=None*)[[source]](_modules/aiohttp/multipart.html#MultipartWriter.append)[¶](#aiohttp.MultipartWriter.append "Link to this definition")
    :   Append an object to writer.

    append\_payload(*payload*)[[source]](_modules/aiohttp/multipart.html#MultipartWriter.append_payload)[¶](#aiohttp.MultipartWriter.append_payload "Link to this definition")
    :   Adds a new body part to multipart writer.

    append\_json(*obj*, *headers=None*)[[source]](_modules/aiohttp/multipart.html#MultipartWriter.append_json)[¶](#aiohttp.MultipartWriter.append_json "Link to this definition")
    :   Helper to append JSON part.

    append\_form(*obj*, *headers=None*)[[source]](_modules/aiohttp/multipart.html#MultipartWriter.append_form)[¶](#aiohttp.MultipartWriter.append_form "Link to this definition")
    :   Helper to append form urlencoded part.

    size[¶](#aiohttp.MultipartWriter.size "Link to this definition")
    :   Size of the payload.

    async write(*writer*, *close\_boundary=True*)[[source]](_modules/aiohttp/multipart.html#MultipartWriter.write)[¶](#aiohttp.MultipartWriter.write "Link to this definition")
    :   Write body.

        Parameters:
        :   **close\_boundary** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – The ([`bool`](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) that will emit
            boundary closing. You may want to disable
            when streaming (`multipart/x-mixed-replace`)

        Added in version 3.4: Support `close_boundary` argument.

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
  + [Multipart reference](#)
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
[Page source](_sources/multipart_reference.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
WebSocket utilities — aiohttp 3.13.3 documentation

# WebSocket utilities[¶](#websocket-utilities "Link to this heading")

class aiohttp.WSCloseCode[[source]](_modules/aiohttp/_websocket/models.html#WSCloseCode)[¶](#aiohttp.WSCloseCode "Link to this definition")
:   An [`IntEnum`](https://docs.python.org/3/library/enum.html#enum.IntEnum "(in Python v3.14)") for keeping close message code.

    OK[¶](#aiohttp.WSCloseCode.OK "Link to this definition")
    :   A normal closure, meaning that the purpose for
        which the connection was established has been fulfilled.

    GOING\_AWAY[¶](#aiohttp.WSCloseCode.GOING_AWAY "Link to this definition")
    :   An endpoint is “going away”, such as a server
        going down or a browser having navigated away from a page.

    PROTOCOL\_ERROR[¶](#aiohttp.WSCloseCode.PROTOCOL_ERROR "Link to this definition")
    :   An endpoint is terminating the connection due
        to a protocol error.

    UNSUPPORTED\_DATA[¶](#aiohttp.WSCloseCode.UNSUPPORTED_DATA "Link to this definition")
    :   An endpoint is terminating the connection
        because it has received a type of data it cannot accept (e.g., an
        endpoint that understands only text data MAY send this if it
        receives a binary message).

    INVALID\_TEXT[¶](#aiohttp.WSCloseCode.INVALID_TEXT "Link to this definition")
    :   An endpoint is terminating the connection
        because it has received data within a message that was not
        consistent with the type of the message (e.g., non-UTF-8 [**RFC 3629**](https://datatracker.ietf.org/doc/html/rfc3629.html)
        data within a text message).

    POLICY\_VIOLATION[¶](#aiohttp.WSCloseCode.POLICY_VIOLATION "Link to this definition")
    :   An endpoint is terminating the connection because it has
        received a message that violates its policy. This is a generic
        status code that can be returned when there is no other more
        suitable status code (e.g.,
        [`UNSUPPORTED_DATA`](#aiohttp.WSCloseCode.UNSUPPORTED_DATA "aiohttp.WSCloseCode.UNSUPPORTED_DATA") or
        [`MESSAGE_TOO_BIG`](#aiohttp.WSCloseCode.MESSAGE_TOO_BIG "aiohttp.WSCloseCode.MESSAGE_TOO_BIG")) or if there is a need to
        hide specific details about the policy.

    MESSAGE\_TOO\_BIG[¶](#aiohttp.WSCloseCode.MESSAGE_TOO_BIG "Link to this definition")
    :   An endpoint is terminating the connection
        because it has received a message that is too big for it to
        process.

    MANDATORY\_EXTENSION[¶](#aiohttp.WSCloseCode.MANDATORY_EXTENSION "Link to this definition")
    :   An endpoint (client) is terminating the
        connection because it has expected the server to negotiate one or
        more extension, but the server did not return them in the response
        message of the WebSocket handshake. The list of extensions that
        are needed should appear in the /reason/ part of the Close frame.
        Note that this status code is not used by the server, because it
        can fail the WebSocket handshake instead.

    INTERNAL\_ERROR[¶](#aiohttp.WSCloseCode.INTERNAL_ERROR "Link to this definition")
    :   A server is terminating the connection because
        it encountered an unexpected condition that prevented it from
        fulfilling the request.

    SERVICE\_RESTART[¶](#aiohttp.WSCloseCode.SERVICE_RESTART "Link to this definition")
    :   The service is restarted. a client may reconnect, and if it
        chooses to do, should reconnect using a randomized delay of 5-30s.

    TRY\_AGAIN\_LATER[¶](#aiohttp.WSCloseCode.TRY_AGAIN_LATER "Link to this definition")
    :   The service is experiencing overload. A client should only
        connect to a different IP (when there are multiple for the
        target) or reconnect to the same IP upon user action.

    ABNORMAL\_CLOSURE[¶](#aiohttp.WSCloseCode.ABNORMAL_CLOSURE "Link to this definition")
    :   Used to indicate that a connection was closed abnormally
        (that is, with no close frame being sent) when a status code
        is expected.

    BAD\_GATEWAY[¶](#aiohttp.WSCloseCode.BAD_GATEWAY "Link to this definition")
    :   The server was acting as a gateway or proxy and received
        an invalid response from the upstream server.
        This is similar to 502 HTTP Status Code.

class aiohttp.WSMsgType[[source]](_modules/aiohttp/_websocket/models.html#WSMsgType)[¶](#aiohttp.WSMsgType "Link to this definition")
:   An [`IntEnum`](https://docs.python.org/3/library/enum.html#enum.IntEnum "(in Python v3.14)") for describing [`WSMessage`](#aiohttp.WSMessage "aiohttp.WSMessage") type.

    CONTINUATION[¶](#aiohttp.WSMsgType.CONTINUATION "Link to this definition")
    :   A mark for continuation frame, user will never get the message
        with this type.

    TEXT[¶](#aiohttp.WSMsgType.TEXT "Link to this definition")
    :   Text message, the value has [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") type.

    BINARY[¶](#aiohttp.WSMsgType.BINARY "Link to this definition")
    :   Binary message, the value has [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") type.

    PING[¶](#aiohttp.WSMsgType.PING "Link to this definition")
    :   Ping frame (sent by client peer).

    PONG[¶](#aiohttp.WSMsgType.PONG "Link to this definition")
    :   Pong frame, answer on ping. Sent by server peer.

    CLOSE[¶](#aiohttp.WSMsgType.CLOSE "Link to this definition")
    :   Close frame.

    CLOSED FRAME
    :   Actually not frame but a flag indicating that websocket was
        closed.

    ERROR[¶](#aiohttp.WSMsgType.ERROR "Link to this definition")
    :   Actually not frame but a flag indicating that websocket was
        received an error.

class aiohttp.WSMessage[[source]](_modules/aiohttp/_websocket/models.html#WSMessage)[¶](#aiohttp.WSMessage "Link to this definition")
:   Websocket message, returned by `.receive()` calls.

    type[¶](#aiohttp.WSMessage.type "Link to this definition")
    :   Message type, [`WSMsgType`](#aiohttp.WSMsgType "aiohttp.WSMsgType") instance.

    data[¶](#aiohttp.WSMessage.data "Link to this definition")
    :   Message payload.

        1. [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") for [`WSMsgType.TEXT`](#aiohttp.WSMsgType.TEXT "aiohttp.WSMsgType.TEXT") messages.
        2. [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") for [`WSMsgType.BINARY`](#aiohttp.WSMsgType.BINARY "aiohttp.WSMsgType.BINARY") messages.
        3. [`WSCloseCode`](#aiohttp.WSCloseCode "aiohttp.WSCloseCode") for [`WSMsgType.CLOSE`](#aiohttp.WSMsgType.CLOSE "aiohttp.WSMsgType.CLOSE") messages.
        4. [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") for [`WSMsgType.PING`](#aiohttp.WSMsgType.PING "aiohttp.WSMsgType.PING") messages.
        5. [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") for [`WSMsgType.PONG`](#aiohttp.WSMsgType.PONG "aiohttp.WSMsgType.PONG") messages.

    extra[¶](#aiohttp.WSMessage.extra "Link to this definition")
    :   Additional info, [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)").

        Makes sense only for [`WSMsgType.CLOSE`](#aiohttp.WSMsgType.CLOSE "aiohttp.WSMsgType.CLOSE") messages, contains
        optional message description.

    json(*\**, *loads=json.loads*)[[source]](_modules/aiohttp/_websocket/models.html#WSMessage.json)[¶](#aiohttp.WSMessage.json "Link to this definition")
    :   Returns parsed JSON data.

        Parameters:
        :   **loads** – optional JSON decoder function.

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
  + [Streaming API](streams.html)
  + [Common data structures](structures.html)
  + [WebSocket utilities](#)
* [FAQ](faq.html)
* [Miscellaneous](misc.html)
* [Who uses aiohttp?](external.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/websocket_utilities.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
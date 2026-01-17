Tracing Reference — aiohttp 3.13.3 documentation

# Tracing Reference[¶](#tracing-reference "Link to this heading")

Added in version 3.0.

A reference for client tracing API.

See also

[Client Tracing](client_advanced.html#aiohttp-client-tracing) for tracing usage instructions.

## Request life cycle[¶](#request-life-cycle "Link to this heading")

A request goes through the following stages and corresponding fallbacks.

### Overview[¶](#overview "Link to this heading")

![digraph {

  start[shape=point, xlabel="start", width="0.1"];
  redirect[shape=box];
  end[shape=point, xlabel="end  ", width="0.1"];
  exception[shape=oval];

  acquire_connection[shape=box];
  headers_received[shape=box];
  headers_sent[shape=box];
  chunk_sent[shape=box];
  chunk_received[shape=box];

  start -> acquire_connection;
  acquire_connection -> headers_sent;
  headers_sent -> headers_received;
  headers_sent -> chunk_sent;
  chunk_sent -> chunk_sent;
  chunk_sent -> headers_received;
  headers_received -> chunk_received;
  chunk_received -> chunk_received;
  chunk_received -> end;
  headers_received -> redirect;
  headers_received -> end;
  redirect -> headers_sent;
  chunk_received -> exception;
  chunk_sent -> exception;
  headers_sent -> exception;

}](_images/graphviz-0ebf41ae8fdce42086439544daac336b11d69dd8.png)

| Name | Description |
| --- | --- |
| start | on\_request\_start |
| redirect | on\_request\_redirect |
| acquire\_connection | Connection acquiring |
| headers\_received |  |
| exception | on\_request\_exception |
| end | on\_request\_end |
| headers\_sent | on\_request\_headers\_sent |
| chunk\_sent | on\_request\_chunk\_sent |
| chunk\_received | on\_response\_chunk\_received |

### Connection acquiring[¶](#connection-acquiring "Link to this heading")

![digraph {

  begin[shape=point, xlabel="begin", width="0.1"];
  end[shape=point, xlabel="end ", width="0.1"];
  exception[shape=oval];

  queued_start[shape=box];
  queued_end[shape=box];
  create_start[shape=box];
  create_end[shape=box];
  reuseconn[shape=box];
  resolve_dns[shape=box];
  sock_connect[shape=box];

  begin -> reuseconn;
  begin -> create_start;
  create_start -> resolve_dns;
  resolve_dns -> exception;
  resolve_dns -> sock_connect;
  sock_connect -> exception;
  sock_connect -> create_end -> end;
  begin -> queued_start;
  queued_start -> queued_end;
  queued_end -> reuseconn;
  queued_end -> create_start;
  reuseconn -> end;

}](_images/graphviz-28238e6db6341f9f5ca00c93ce18aa97e5e245cd.png)

| Name | Description |
| --- | --- |
| begin |  |
| end |  |
| queued\_start | on\_connection\_queued\_start |
| create\_start | on\_connection\_create\_start |
| reuseconn | on\_connection\_reuseconn |
| queued\_end | on\_connection\_queued\_end |
| create\_end | on\_connection\_create\_end |
| exception | Exception raised |
| resolve\_dns | DNS resolving |
| sock\_connect | Connection establishment |

### DNS resolving[¶](#dns-resolving "Link to this heading")

![digraph {

  begin[shape=point, xlabel="begin", width="0.1"];
  end[shape=point, xlabel="end", width="0.1"];
  exception[shape=oval];

  resolve_start[shape=box];
  resolve_end[shape=box];
  cache_hit[shape=box];
  cache_miss[shape=box];

  begin -> cache_hit -> end;
  begin -> cache_miss -> resolve_start;
  resolve_start -> resolve_end -> end;
  resolve_start -> exception;

}](_images/graphviz-fdb5fdb9aacd37e4b86d599b9d58b910fa27e9ae.png)

| Name | Description |
| --- | --- |
| begin |  |
| end |  |
| exception | Exception raised |
| resolve\_end | on\_dns\_resolvehost\_end |
| resolve\_start | on\_dns\_resolvehost\_start |
| cache\_hit | on\_dns\_cache\_hit |
| cache\_miss | on\_dns\_cache\_miss |

## Classes[¶](#classes "Link to this heading")

class aiohttp.TraceConfig(*trace\_config\_ctx\_factory=SimpleNamespace*)[[source]](_modules/aiohttp/tracing.html#TraceConfig)[¶](#aiohttp.TraceConfig "Link to this definition")
:   Trace config is the configuration object used to trace requests
    launched by a [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") object using different events
    related to different parts of the request flow.

    Parameters:
    :   **trace\_config\_ctx\_factory** – factory used to create trace contexts,
        default class used [`types.SimpleNamespace`](https://docs.python.org/3/library/types.html#types.SimpleNamespace "(in Python v3.14)")

    trace\_config\_ctx(*trace\_request\_ctx=None*)[[source]](_modules/aiohttp/tracing.html#TraceConfig.trace_config_ctx)[¶](#aiohttp.TraceConfig.trace_config_ctx "Link to this definition")
    :   Parameters:
        :   **trace\_request\_ctx** – Will be used to pass as a kw for the
            `trace_config_ctx_factory`.

        Build a new trace context from the config.

    Every signal handler should have the following signature:

    ```
    async def on_signal(session, context, params): ...
    ```

    where `session` is [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") instance, `context` is an
    object returned by [`trace_config_ctx()`](#aiohttp.TraceConfig.trace_config_ctx "aiohttp.TraceConfig.trace_config_ctx") call and `params` is a
    data class with signal parameters. The type of `params` depends on
    subscribed signal and described below.

    on\_request\_start[¶](#aiohttp.TraceConfig.on_request_start "Link to this definition")
    :   Property that gives access to the signals that will be executed
        when a request starts.

        `params` is [`aiohttp.TraceRequestStartParams`](#aiohttp.TraceRequestStartParams "aiohttp.TraceRequestStartParams") instance.

    on\_request\_chunk\_sent[¶](#aiohttp.TraceConfig.on_request_chunk_sent "Link to this definition")
    :   Property that gives access to the signals that will be executed
        when a chunk of request body is sent.

        `params` is [`aiohttp.TraceRequestChunkSentParams`](#aiohttp.TraceRequestChunkSentParams "aiohttp.TraceRequestChunkSentParams") instance.

        Added in version 3.1.

    on\_response\_chunk\_received[¶](#aiohttp.TraceConfig.on_response_chunk_received "Link to this definition")
    :   Property that gives access to the signals that will be executed
        when a chunk of response body is received.

        `params` is [`aiohttp.TraceResponseChunkReceivedParams`](#aiohttp.TraceResponseChunkReceivedParams "aiohttp.TraceResponseChunkReceivedParams") instance.

        Added in version 3.1.

    on\_request\_redirect[¶](#aiohttp.TraceConfig.on_request_redirect "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        redirect happens during a request flow.

        `params` is [`aiohttp.TraceRequestRedirectParams`](#aiohttp.TraceRequestRedirectParams "aiohttp.TraceRequestRedirectParams") instance.

    on\_request\_end[¶](#aiohttp.TraceConfig.on_request_end "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request ends.

        `params` is [`aiohttp.TraceRequestEndParams`](#aiohttp.TraceRequestEndParams "aiohttp.TraceRequestEndParams") instance.

    on\_request\_exception[¶](#aiohttp.TraceConfig.on_request_exception "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request finishes with an exception.

        `params` is [`aiohttp.TraceRequestExceptionParams`](#aiohttp.TraceRequestExceptionParams "aiohttp.TraceRequestExceptionParams") instance.

    on\_connection\_queued\_start[¶](#aiohttp.TraceConfig.on_connection_queued_start "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request has been queued waiting for an available connection.

        `params` is [`aiohttp.TraceConnectionQueuedStartParams`](#aiohttp.TraceConnectionQueuedStartParams "aiohttp.TraceConnectionQueuedStartParams")
        instance.

    on\_connection\_queued\_end[¶](#aiohttp.TraceConfig.on_connection_queued_end "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request that was queued already has an available connection.

        `params` is [`aiohttp.TraceConnectionQueuedEndParams`](#aiohttp.TraceConnectionQueuedEndParams "aiohttp.TraceConnectionQueuedEndParams")
        instance.

    on\_connection\_create\_start[¶](#aiohttp.TraceConfig.on_connection_create_start "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request creates a new connection.

        `params` is [`aiohttp.TraceConnectionCreateStartParams`](#aiohttp.TraceConnectionCreateStartParams "aiohttp.TraceConnectionCreateStartParams")
        instance.

    on\_connection\_create\_end[¶](#aiohttp.TraceConfig.on_connection_create_end "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request that created a new connection finishes its creation.

        `params` is [`aiohttp.TraceConnectionCreateEndParams`](#aiohttp.TraceConnectionCreateEndParams "aiohttp.TraceConnectionCreateEndParams")
        instance.

    on\_connection\_reuseconn[¶](#aiohttp.TraceConfig.on_connection_reuseconn "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request reuses a connection.

        `params` is [`aiohttp.TraceConnectionReuseconnParams`](#aiohttp.TraceConnectionReuseconnParams "aiohttp.TraceConnectionReuseconnParams")
        instance.

    on\_dns\_resolvehost\_start[¶](#aiohttp.TraceConfig.on_dns_resolvehost_start "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request starts to resolve the domain related with the request.

        `params` is [`aiohttp.TraceDnsResolveHostStartParams`](#aiohttp.TraceDnsResolveHostStartParams "aiohttp.TraceDnsResolveHostStartParams")
        instance.

    on\_dns\_resolvehost\_end[¶](#aiohttp.TraceConfig.on_dns_resolvehost_end "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request finishes to resolve the domain related with the request.

        `params` is [`aiohttp.TraceDnsResolveHostEndParams`](#aiohttp.TraceDnsResolveHostEndParams "aiohttp.TraceDnsResolveHostEndParams") instance.

    on\_dns\_cache\_hit[¶](#aiohttp.TraceConfig.on_dns_cache_hit "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request was able to use a cached DNS resolution for the domain related
        with the request.

        `params` is [`aiohttp.TraceDnsCacheHitParams`](#aiohttp.TraceDnsCacheHitParams "aiohttp.TraceDnsCacheHitParams") instance.

    on\_dns\_cache\_miss[¶](#aiohttp.TraceConfig.on_dns_cache_miss "Link to this definition")
    :   Property that gives access to the signals that will be executed when a
        request was not able to use a cached DNS resolution for the domain related
        with the request.

        `params` is [`aiohttp.TraceDnsCacheMissParams`](#aiohttp.TraceDnsCacheMissParams "aiohttp.TraceDnsCacheMissParams") instance.

    on\_request\_headers\_sent[¶](#aiohttp.TraceConfig.on_request_headers_sent "Link to this definition")
    :   Property that gives access to the signals that will be executed
        when request headers are sent.

        `params` is [`aiohttp.TraceRequestHeadersSentParams`](#aiohttp.TraceRequestHeadersSentParams "aiohttp.TraceRequestHeadersSentParams") instance.

        Added in version 3.8.

class aiohttp.TraceRequestStartParams[[source]](_modules/aiohttp/tracing.html#TraceRequestStartParams)[¶](#aiohttp.TraceRequestStartParams "Link to this definition")
:   See [`TraceConfig.on_request_start`](#aiohttp.TraceConfig.on_request_start "aiohttp.TraceConfig.on_request_start") for details.

    method[¶](#aiohttp.TraceRequestStartParams.method "Link to this definition")
    :   Method that will be used to make the request.

    url[¶](#aiohttp.TraceRequestStartParams.url "Link to this definition")
    :   URL that will be used for the request.

    headers[¶](#aiohttp.TraceRequestStartParams.headers "Link to this definition")
    :   Headers that will be used for the request, can be mutated.

class aiohttp.TraceRequestChunkSentParams[[source]](_modules/aiohttp/tracing.html#TraceRequestChunkSentParams)[¶](#aiohttp.TraceRequestChunkSentParams "Link to this definition")
:   Added in version 3.1.

    See [`TraceConfig.on_request_chunk_sent`](#aiohttp.TraceConfig.on_request_chunk_sent "aiohttp.TraceConfig.on_request_chunk_sent") for details.

    method[¶](#aiohttp.TraceRequestChunkSentParams.method "Link to this definition")
    :   Method that will be used to make the request.

    url[¶](#aiohttp.TraceRequestChunkSentParams.url "Link to this definition")
    :   URL that will be used for the request.

    chunk[¶](#aiohttp.TraceRequestChunkSentParams.chunk "Link to this definition")
    :   Bytes of chunk sent

class aiohttp.TraceResponseChunkReceivedParams[[source]](_modules/aiohttp/tracing.html#TraceResponseChunkReceivedParams)[¶](#aiohttp.TraceResponseChunkReceivedParams "Link to this definition")
:   Added in version 3.1.

    See [`TraceConfig.on_response_chunk_received`](#aiohttp.TraceConfig.on_response_chunk_received "aiohttp.TraceConfig.on_response_chunk_received") for details.

    method[¶](#aiohttp.TraceResponseChunkReceivedParams.method "Link to this definition")
    :   Method that will be used to make the request.

    url[¶](#aiohttp.TraceResponseChunkReceivedParams.url "Link to this definition")
    :   URL that will be used for the request.

    chunk[¶](#aiohttp.TraceResponseChunkReceivedParams.chunk "Link to this definition")
    :   Bytes of chunk received

class aiohttp.TraceRequestEndParams[[source]](_modules/aiohttp/tracing.html#TraceRequestEndParams)[¶](#aiohttp.TraceRequestEndParams "Link to this definition")
:   See [`TraceConfig.on_request_end`](#aiohttp.TraceConfig.on_request_end "aiohttp.TraceConfig.on_request_end") for details.

    method[¶](#aiohttp.TraceRequestEndParams.method "Link to this definition")
    :   Method used to make the request.

    url[¶](#aiohttp.TraceRequestEndParams.url "Link to this definition")
    :   URL used for the request.

    headers[¶](#aiohttp.TraceRequestEndParams.headers "Link to this definition")
    :   Headers used for the request.

    response[¶](#aiohttp.TraceRequestEndParams.response "Link to this definition")
    :   Response [`ClientResponse`](client_reference.html#aiohttp.ClientResponse "aiohttp.ClientResponse").

class aiohttp.TraceRequestExceptionParams[[source]](_modules/aiohttp/tracing.html#TraceRequestExceptionParams)[¶](#aiohttp.TraceRequestExceptionParams "Link to this definition")
:   See [`TraceConfig.on_request_exception`](#aiohttp.TraceConfig.on_request_exception "aiohttp.TraceConfig.on_request_exception") for details.

    method[¶](#aiohttp.TraceRequestExceptionParams.method "Link to this definition")
    :   Method used to make the request.

    url[¶](#aiohttp.TraceRequestExceptionParams.url "Link to this definition")
    :   URL used for the request.

    headers[¶](#aiohttp.TraceRequestExceptionParams.headers "Link to this definition")
    :   Headers used for the request.

    exception[¶](#aiohttp.TraceRequestExceptionParams.exception "Link to this definition")
    :   Exception raised during the request.

class aiohttp.TraceRequestRedirectParams[[source]](_modules/aiohttp/tracing.html#TraceRequestRedirectParams)[¶](#aiohttp.TraceRequestRedirectParams "Link to this definition")
:   See [`TraceConfig.on_request_redirect`](#aiohttp.TraceConfig.on_request_redirect "aiohttp.TraceConfig.on_request_redirect") for details.

    method[¶](#aiohttp.TraceRequestRedirectParams.method "Link to this definition")
    :   Method used to get this redirect request.

    url[¶](#aiohttp.TraceRequestRedirectParams.url "Link to this definition")
    :   URL used for this redirect request.

    headers[¶](#aiohttp.TraceRequestRedirectParams.headers "Link to this definition")
    :   Headers used for this redirect.

    response[¶](#aiohttp.TraceRequestRedirectParams.response "Link to this definition")
    :   Response [`ClientResponse`](client_reference.html#aiohttp.ClientResponse "aiohttp.ClientResponse") got from the redirect.

class aiohttp.TraceConnectionQueuedStartParams[[source]](_modules/aiohttp/tracing.html#TraceConnectionQueuedStartParams)[¶](#aiohttp.TraceConnectionQueuedStartParams "Link to this definition")
:   See [`TraceConfig.on_connection_queued_start`](#aiohttp.TraceConfig.on_connection_queued_start "aiohttp.TraceConfig.on_connection_queued_start") for details.

    There are no attributes right now.

class aiohttp.TraceConnectionQueuedEndParams[[source]](_modules/aiohttp/tracing.html#TraceConnectionQueuedEndParams)[¶](#aiohttp.TraceConnectionQueuedEndParams "Link to this definition")
:   See [`TraceConfig.on_connection_queued_end`](#aiohttp.TraceConfig.on_connection_queued_end "aiohttp.TraceConfig.on_connection_queued_end") for details.

    There are no attributes right now.

class aiohttp.TraceConnectionCreateStartParams[[source]](_modules/aiohttp/tracing.html#TraceConnectionCreateStartParams)[¶](#aiohttp.TraceConnectionCreateStartParams "Link to this definition")
:   See [`TraceConfig.on_connection_create_start`](#aiohttp.TraceConfig.on_connection_create_start "aiohttp.TraceConfig.on_connection_create_start") for details.

    There are no attributes right now.

class aiohttp.TraceConnectionCreateEndParams[[source]](_modules/aiohttp/tracing.html#TraceConnectionCreateEndParams)[¶](#aiohttp.TraceConnectionCreateEndParams "Link to this definition")
:   See [`TraceConfig.on_connection_create_end`](#aiohttp.TraceConfig.on_connection_create_end "aiohttp.TraceConfig.on_connection_create_end") for details.

    There are no attributes right now.

class aiohttp.TraceConnectionReuseconnParams[[source]](_modules/aiohttp/tracing.html#TraceConnectionReuseconnParams)[¶](#aiohttp.TraceConnectionReuseconnParams "Link to this definition")
:   See [`TraceConfig.on_connection_reuseconn`](#aiohttp.TraceConfig.on_connection_reuseconn "aiohttp.TraceConfig.on_connection_reuseconn") for details.

    There are no attributes right now.

class aiohttp.TraceDnsResolveHostStartParams[[source]](_modules/aiohttp/tracing.html#TraceDnsResolveHostStartParams)[¶](#aiohttp.TraceDnsResolveHostStartParams "Link to this definition")
:   See [`TraceConfig.on_dns_resolvehost_start`](#aiohttp.TraceConfig.on_dns_resolvehost_start "aiohttp.TraceConfig.on_dns_resolvehost_start") for details.

    host[¶](#aiohttp.TraceDnsResolveHostStartParams.host "Link to this definition")
    :   Host that will be resolved.

class aiohttp.TraceDnsResolveHostEndParams[[source]](_modules/aiohttp/tracing.html#TraceDnsResolveHostEndParams)[¶](#aiohttp.TraceDnsResolveHostEndParams "Link to this definition")
:   See [`TraceConfig.on_dns_resolvehost_end`](#aiohttp.TraceConfig.on_dns_resolvehost_end "aiohttp.TraceConfig.on_dns_resolvehost_end") for details.

    host[¶](#aiohttp.TraceDnsResolveHostEndParams.host "Link to this definition")
    :   Host that has been resolved.

class aiohttp.TraceDnsCacheHitParams[[source]](_modules/aiohttp/tracing.html#TraceDnsCacheHitParams)[¶](#aiohttp.TraceDnsCacheHitParams "Link to this definition")
:   See [`TraceConfig.on_dns_cache_hit`](#aiohttp.TraceConfig.on_dns_cache_hit "aiohttp.TraceConfig.on_dns_cache_hit") for details.

    host[¶](#aiohttp.TraceDnsCacheHitParams.host "Link to this definition")
    :   Host found in the cache.

class aiohttp.TraceDnsCacheMissParams[[source]](_modules/aiohttp/tracing.html#TraceDnsCacheMissParams)[¶](#aiohttp.TraceDnsCacheMissParams "Link to this definition")
:   See [`TraceConfig.on_dns_cache_miss`](#aiohttp.TraceConfig.on_dns_cache_miss "aiohttp.TraceConfig.on_dns_cache_miss") for details.

    host[¶](#aiohttp.TraceDnsCacheMissParams.host "Link to this definition")
    :   Host didn’t find the cache.

class aiohttp.TraceRequestHeadersSentParams[[source]](_modules/aiohttp/tracing.html#TraceRequestHeadersSentParams)[¶](#aiohttp.TraceRequestHeadersSentParams "Link to this definition")
:   See [`TraceConfig.on_request_headers_sent`](#aiohttp.TraceConfig.on_request_headers_sent "aiohttp.TraceConfig.on_request_headers_sent") for details.

    Added in version 3.8.

    method[¶](#aiohttp.TraceRequestHeadersSentParams.method "Link to this definition")
    :   Method that will be used to make the request.

    url[¶](#aiohttp.TraceRequestHeadersSentParams.url "Link to this definition")
    :   URL that will be used for the request.

    headers[¶](#aiohttp.TraceRequestHeadersSentParams.headers "Link to this definition")
    :   Headers that will be used for the request.

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
  + [Quickstart](client_quickstart.html)
  + [Advanced Usage](client_advanced.html)
  + [Client Middleware Cookbook](client_middleware_cookbook.html)
  + [Reference](client_reference.html)
  + [Tracing Reference](#)
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
[Page source](_sources/tracing_reference.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
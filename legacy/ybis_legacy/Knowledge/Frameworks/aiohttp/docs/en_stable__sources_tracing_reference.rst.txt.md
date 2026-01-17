.. \_aiohttp-client-tracing-reference:
Tracing Reference
=================
.. currentmodule:: aiohttp
.. versionadded:: 3.0
A reference for client tracing API.
.. seealso:: :ref:`aiohttp-client-tracing` for tracing usage instructions.
Request life cycle
------------------
A request goes through the following stages and corresponding fallbacks.
Overview
^^^^^^^^
.. graphviz::
digraph {
start[shape=point, xlabel="start", width="0.1"];
redirect[shape=box];
end[shape=point, xlabel="end ", width="0.1"];
exception[shape=oval];
acquire\_connection[shape=box];
headers\_received[shape=box];
headers\_sent[shape=box];
chunk\_sent[shape=box];
chunk\_received[shape=box];
start -> acquire\_connection;
acquire\_connection -> headers\_sent;
headers\_sent -> headers\_received;
headers\_sent -> chunk\_sent;
chunk\_sent -> chunk\_sent;
chunk\_sent -> headers\_received;
headers\_received -> chunk\_received;
chunk\_received -> chunk\_received;
chunk\_received -> end;
headers\_received -> redirect;
headers\_received -> end;
redirect -> headers\_sent;
chunk\_received -> exception;
chunk\_sent -> exception;
headers\_sent -> exception;
}
.. list-table::
:header-rows: 1
\* - Name
- Description
\* - start
- on\_request\_start
\* - redirect
- on\_request\_redirect
\* - acquire\_connection
- Connection acquiring
\* - headers\_received
-
\* - exception
- on\_request\_exception
\* - end
- on\_request\_end
\* - headers\_sent
- on\_request\_headers\_sent
\* - chunk\_sent
- on\_request\_chunk\_sent
\* - chunk\_received
- on\_response\_chunk\_received
Connection acquiring
^^^^^^^^^^^^^^^^^^^^
.. graphviz::
digraph {
begin[shape=point, xlabel="begin", width="0.1"];
end[shape=point, xlabel="end ", width="0.1"];
exception[shape=oval];
queued\_start[shape=box];
queued\_end[shape=box];
create\_start[shape=box];
create\_end[shape=box];
reuseconn[shape=box];
resolve\_dns[shape=box];
sock\_connect[shape=box];
begin -> reuseconn;
begin -> create\_start;
create\_start -> resolve\_dns;
resolve\_dns -> exception;
resolve\_dns -> sock\_connect;
sock\_connect -> exception;
sock\_connect -> create\_end -> end;
begin -> queued\_start;
queued\_start -> queued\_end;
queued\_end -> reuseconn;
queued\_end -> create\_start;
reuseconn -> end;
}
.. list-table::
:header-rows: 1
\* - Name
- Description
\* - begin
-
\* - end
-
\* - queued\_start
- on\_connection\_queued\_start
\* - create\_start
- on\_connection\_create\_start
\* - reuseconn
- on\_connection\_reuseconn
\* - queued\_end
- on\_connection\_queued\_end
\* - create\_end
- on\_connection\_create\_end
\* - exception
- Exception raised
\* - resolve\_dns
- DNS resolving
\* - sock\_connect
- Connection establishment
DNS resolving
^^^^^^^^^^^^^
.. graphviz::
digraph {
begin[shape=point, xlabel="begin", width="0.1"];
end[shape=point, xlabel="end", width="0.1"];
exception[shape=oval];
resolve\_start[shape=box];
resolve\_end[shape=box];
cache\_hit[shape=box];
cache\_miss[shape=box];
begin -> cache\_hit -> end;
begin -> cache\_miss -> resolve\_start;
resolve\_start -> resolve\_end -> end;
resolve\_start -> exception;
}
.. list-table::
:header-rows: 1
\* - Name
- Description
\* - begin
-
\* - end
-
\* - exception
- Exception raised
\* - resolve\_end
- on\_dns\_resolvehost\_end
\* - resolve\_start
- on\_dns\_resolvehost\_start
\* - cache\_hit
- on\_dns\_cache\_hit
\* - cache\_miss
- on\_dns\_cache\_miss
Classes
-------
.. class:: TraceConfig(trace\_config\_ctx\_factory=SimpleNamespace)
Trace config is the configuration object used to trace requests
launched by a :class:`ClientSession` object using different events
related to different parts of the request flow.
:param trace\_config\_ctx\_factory: factory used to create trace contexts,
default class used :class:`types.SimpleNamespace`
.. method:: trace\_config\_ctx(trace\_request\_ctx=None)
:param trace\_request\_ctx: Will be used to pass as a kw for the
``trace\_config\_ctx\_factory``.
Build a new trace context from the config.
Every signal handler should have the following signature::
async def on\_signal(session, context, params): ...
where ``session`` is :class:`ClientSession` instance, ``context`` is an
object returned by :meth:`trace\_config\_ctx` call and ``params`` is a
data class with signal parameters. The type of ``params`` depends on
subscribed signal and described below.
.. attribute:: on\_request\_start
Property that gives access to the signals that will be executed
when a request starts.
``params`` is :class:`aiohttp.TraceRequestStartParams` instance.
.. attribute:: on\_request\_chunk\_sent
Property that gives access to the signals that will be executed
when a chunk of request body is sent.
``params`` is :class:`aiohttp.TraceRequestChunkSentParams` instance.
.. versionadded:: 3.1
.. attribute:: on\_response\_chunk\_received
Property that gives access to the signals that will be executed
when a chunk of response body is received.
``params`` is :class:`aiohttp.TraceResponseChunkReceivedParams` instance.
.. versionadded:: 3.1
.. attribute:: on\_request\_redirect
Property that gives access to the signals that will be executed when a
redirect happens during a request flow.
``params`` is :class:`aiohttp.TraceRequestRedirectParams` instance.
.. attribute:: on\_request\_end
Property that gives access to the signals that will be executed when a
request ends.
``params`` is :class:`aiohttp.TraceRequestEndParams` instance.
.. attribute:: on\_request\_exception
Property that gives access to the signals that will be executed when a
request finishes with an exception.
``params`` is :class:`aiohttp.TraceRequestExceptionParams` instance.
.. attribute:: on\_connection\_queued\_start
Property that gives access to the signals that will be executed when a
request has been queued waiting for an available connection.
``params`` is :class:`aiohttp.TraceConnectionQueuedStartParams`
instance.
.. attribute:: on\_connection\_queued\_end
Property that gives access to the signals that will be executed when a
request that was queued already has an available connection.
``params`` is :class:`aiohttp.TraceConnectionQueuedEndParams`
instance.
.. attribute:: on\_connection\_create\_start
Property that gives access to the signals that will be executed when a
request creates a new connection.
``params`` is :class:`aiohttp.TraceConnectionCreateStartParams`
instance.
.. attribute:: on\_connection\_create\_end
Property that gives access to the signals that will be executed when a
request that created a new connection finishes its creation.
``params`` is :class:`aiohttp.TraceConnectionCreateEndParams`
instance.
.. attribute:: on\_connection\_reuseconn
Property that gives access to the signals that will be executed when a
request reuses a connection.
``params`` is :class:`aiohttp.TraceConnectionReuseconnParams`
instance.
.. attribute:: on\_dns\_resolvehost\_start
Property that gives access to the signals that will be executed when a
request starts to resolve the domain related with the request.
``params`` is :class:`aiohttp.TraceDnsResolveHostStartParams`
instance.
.. attribute:: on\_dns\_resolvehost\_end
Property that gives access to the signals that will be executed when a
request finishes to resolve the domain related with the request.
``params`` is :class:`aiohttp.TraceDnsResolveHostEndParams` instance.
.. attribute:: on\_dns\_cache\_hit
Property that gives access to the signals that will be executed when a
request was able to use a cached DNS resolution for the domain related
with the request.
``params`` is :class:`aiohttp.TraceDnsCacheHitParams` instance.
.. attribute:: on\_dns\_cache\_miss
Property that gives access to the signals that will be executed when a
request was not able to use a cached DNS resolution for the domain related
with the request.
``params`` is :class:`aiohttp.TraceDnsCacheMissParams` instance.
.. attribute:: on\_request\_headers\_sent
Property that gives access to the signals that will be executed
when request headers are sent.
``params`` is :class:`aiohttp.TraceRequestHeadersSentParams` instance.
.. versionadded:: 3.8
.. class:: TraceRequestStartParams
See :attr:`TraceConfig.on\_request\_start` for details.
.. attribute:: method
Method that will be used to make the request.
.. attribute:: url
URL that will be used for the request.
.. attribute:: headers
Headers that will be used for the request, can be mutated.
.. class:: TraceRequestChunkSentParams
.. versionadded:: 3.1
See :attr:`TraceConfig.on\_request\_chunk\_sent` for details.
.. attribute:: method
Method that will be used to make the request.
.. attribute:: url
URL that will be used for the request.
.. attribute:: chunk
Bytes of chunk sent
.. class:: TraceResponseChunkReceivedParams
.. versionadded:: 3.1
See :attr:`TraceConfig.on\_response\_chunk\_received` for details.
.. attribute:: method
Method that will be used to make the request.
.. attribute:: url
URL that will be used for the request.
.. attribute:: chunk
Bytes of chunk received
.. class:: TraceRequestEndParams
See :attr:`TraceConfig.on\_request\_end` for details.
.. attribute:: method
Method used to make the request.
.. attribute:: url
URL used for the request.
.. attribute:: headers
Headers used for the request.
.. attribute:: response
Response :class:`ClientResponse`.
.. class:: TraceRequestExceptionParams
See :attr:`TraceConfig.on\_request\_exception` for details.
.. attribute:: method
Method used to make the request.
.. attribute:: url
URL used for the request.
.. attribute:: headers
Headers used for the request.
.. attribute:: exception
Exception raised during the request.
.. class:: TraceRequestRedirectParams
See :attr:`TraceConfig.on\_request\_redirect` for details.
.. attribute:: method
Method used to get this redirect request.
.. attribute:: url
URL used for this redirect request.
.. attribute:: headers
Headers used for this redirect.
.. attribute:: response
Response :class:`ClientResponse` got from the redirect.
.. class:: TraceConnectionQueuedStartParams
See :attr:`TraceConfig.on\_connection\_queued\_start` for details.
There are no attributes right now.
.. class:: TraceConnectionQueuedEndParams
See :attr:`TraceConfig.on\_connection\_queued\_end` for details.
There are no attributes right now.
.. class:: TraceConnectionCreateStartParams
See :attr:`TraceConfig.on\_connection\_create\_start` for details.
There are no attributes right now.
.. class:: TraceConnectionCreateEndParams
See :attr:`TraceConfig.on\_connection\_create\_end` for details.
There are no attributes right now.
.. class:: TraceConnectionReuseconnParams
See :attr:`TraceConfig.on\_connection\_reuseconn` for details.
There are no attributes right now.
.. class:: TraceDnsResolveHostStartParams
See :attr:`TraceConfig.on\_dns\_resolvehost\_start` for details.
.. attribute:: host
Host that will be resolved.
.. class:: TraceDnsResolveHostEndParams
See :attr:`TraceConfig.on\_dns\_resolvehost\_end` for details.
.. attribute:: host
Host that has been resolved.
.. class:: TraceDnsCacheHitParams
See :attr:`TraceConfig.on\_dns\_cache\_hit` for details.
.. attribute:: host
Host found in the cache.
.. class:: TraceDnsCacheMissParams
See :attr:`TraceConfig.on\_dns\_cache\_miss` for details.
.. attribute:: host
Host didn't find the cache.
.. class:: TraceRequestHeadersSentParams
See :attr:`TraceConfig.on\_request\_headers\_sent` for details.
.. versionadded:: 3.8
.. attribute:: method
Method that will be used to make the request.
.. attribute:: url
URL that will be used for the request.
.. attribute:: headers
Headers that will be used for the request.
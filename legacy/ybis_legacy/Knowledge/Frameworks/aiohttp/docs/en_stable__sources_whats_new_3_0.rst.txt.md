.. \_aiohttp\_whats\_new\_3\_0:
=========================
What's new in aiohttp 3.0
=========================
async/await everywhere
======================
The main change is dropping ``yield from`` support and using
``async``/``await`` everywhere. Farewell, Python 3.4.
The minimal supported Python version is \*\*3.5.3\*\* now.
Why not \*3.5.0\*? Because \*3.5.3\* has a crucial change:
:func:`asyncio.get\_event\_loop()` returns the running loop instead of
\*default\*, which may be different, e.g.::
loop = asyncio.new\_event\_loop()
loop.run\_until\_complete(f())
Note, :func:`asyncio.set\_event\_loop` was not called and default loop
is not equal to actually executed one.
Application Runners
===================
People constantly asked about ability to run aiohttp servers together
with other asyncio code, but :func:`aiohttp.web.run\_app` is blocking
synchronous call.
aiohttp had support for starting the application without ``run\_app`` but the API
was very low-level and cumbersome.
Now application runners solve the task in a few lines of code, see
:ref:`aiohttp-web-app-runners` for details.
Client Tracing
==============
Other long awaited feature is tracing client request life cycle to
figure out when and why client request spends a time waiting for
connection establishment, getting server response headers etc.
Now it is possible by registering special signal handlers on every
request processing stage. :ref:`aiohttp-client-tracing` provides more
info about the feature.
HTTPS support
=============
Unfortunately asyncio has a bug with checking SSL certificates for
non-ASCII site DNS names, e.g. `https://–Є—Б—В–Њ—А–Є–Ї.—А—Д `\_ or
`https://йЫЬиНЙеЈ•дљЬеЃ§.й¶ЩжЄѓ `\_.
The bug has been fixed in upcoming Python 3.7 only (the change
requires breaking backward compatibility in :mod:`ssl` API).
aiohttp installs a fix for older Python versions (3.5 and 3.6).
Dropped obsolete API
====================
A switch to new major version is a great chance for dropping already
deprecated features.
The release dropped a lot, see :ref:`aiohttp\_changes` for details.
All removals was already marked as deprecated or related to very low
level implementation details.
If user code did not raise :exc:`DeprecationWarning` it is compatible
with aiohttp 3.0 most likely.
Summary
=======
Enjoy aiohttp 3.0 release!
The full change log is here: :ref:`aiohttp\_changes`.
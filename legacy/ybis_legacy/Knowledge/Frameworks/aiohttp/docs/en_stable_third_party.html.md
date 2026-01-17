Third-Party libraries — aiohttp 3.13.3 documentation

# Third-Party libraries[¶](#third-party-libraries "Link to this heading")

aiohttp is not just a library for making HTTP requests and creating web
servers.

It is the foundation for libraries built *on top* of aiohttp.

This page is a list of these tools.

Please feel free to add your open source library if it’s not listed
yet by making a pull request to <https://github.com/aio-libs/aiohttp/>

* Why would you want to include your awesome library in this list?
* Because the list increases your library visibility. People
  will have an easy way to find it.

## Officially supported[¶](#officially-supported "Link to this heading")

This list contains libraries which are supported by the *aio-libs* team
and located on <https://github.com/aio-libs>

### aiohttp extensions[¶](#aiohttp-extensions "Link to this heading")

* [aiohttp-apischema](https://github.com/aio-libs/aiohttp-apischema)
  provides automatic API schema generation and validation of user input
  for [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web").
* [aiohttp-session](https://github.com/aio-libs/aiohttp-session)
  provides sessions for [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web").
* [aiohttp-debugtoolbar](https://github.com/aio-libs/aiohttp-debugtoolbar)
  is a library for *debug toolbar* support for [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web").
* [aiohttp-security](https://github.com/aio-libs/aiohttp-security)
  auth and permissions for [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web").
* [aiohttp-devtools](https://github.com/aio-libs/aiohttp-devtools)
  provides development tools for [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") applications.
* [aiohttp-cors](https://github.com/aio-libs/aiohttp-cors) CORS
  support for aiohttp.
* [aiohttp-sse](https://github.com/aio-libs/aiohttp-sse) Server-sent
  events support for aiohttp.
* [pytest-aiohttp](https://github.com/aio-libs/pytest-aiohttp)
  pytest plugin for aiohttp support.
* [aiohttp-mako](https://github.com/aio-libs/aiohttp-mako) Mako
  template renderer for aiohttp.web.
* [aiohttp-jinja2](https://github.com/aio-libs/aiohttp-jinja2) Jinja2
  template renderer for aiohttp.web.
* [aiozipkin](https://github.com/aio-libs/aiozipkin) distributed
  tracing instrumentation for aiohttp client and server.

### Database drivers[¶](#database-drivers "Link to this heading")

* [aiopg](https://github.com/aio-libs/aiopg) PostgreSQL async driver.
* [aiomysql](https://github.com/aio-libs/aiomysql) MySQL async driver.
* [aioredis](https://github.com/aio-libs/aioredis) Redis async driver.

### Other tools[¶](#other-tools "Link to this heading")

* [aiodocker](https://github.com/aio-libs/aiodocker) Python Docker
  API client based on asyncio and aiohttp.
* [aiobotocore](https://github.com/aio-libs/aiobotocore) asyncio
  support for botocore library using aiohttp.

## Approved third-party libraries[¶](#approved-third-party-libraries "Link to this heading")

These libraries are not part of `aio-libs` but they have proven to be very
well written and highly recommended for usage.

* [uvloop](https://github.com/MagicStack/uvloop) Ultra fast
  implementation of asyncio event loop on top of `libuv`.

  We highly recommend to use this instead of standard `asyncio`.

### Database drivers[¶](#id1 "Link to this heading")

* [asyncpg](https://github.com/MagicStack/asyncpg) Another
  PostgreSQL async driver. It’s much faster than `aiopg` but is
  not a drop-in replacement – the API is different. But, please take
  a look at it – the driver is incredibly fast.

## OpenAPI / Swagger extensions[¶](#openapi-swagger-extensions "Link to this heading")

Extensions bringing [OpenAPI](https://swagger.io/docs/specification/about)
support to aiohttp web servers.

* [aiohttp-apispec](https://github.com/maximdanilchenko/aiohttp-apispec)
  Build and document REST APIs with `aiohttp` and `apispec`.
* [aiohttp\_apiset](https://github.com/aamalev/aiohttp_apiset)
  Package to build routes using swagger specification.
* [aiohttp-pydantic](https://github.com/Maillol/aiohttp-pydantic)
  An `aiohttp.View` to validate the HTTP request’s body, query-string, and
  headers regarding function annotations and generate OpenAPI doc.
* [aiohttp-swagger](https://github.com/cr0hn/aiohttp-swagger)
  Swagger API Documentation builder for aiohttp server.
* [aiohttp-swagger3](https://github.com/hh-h/aiohttp-swagger3)
  Library for Swagger documentation builder and validating aiohttp requests
  using swagger specification 3.0.
* [aiohttp-swaggerify](https://github.com/dchaplinsky/aiohttp_swaggerify)
  Library to automatically generate swagger2.0 definition for aiohttp endpoints.
* [aio-openapi](https://github.com/quantmind/aio-openapi)
  Asynchronous web middleware for aiohttp and serving Rest APIs with OpenAPI v3
  specification and with optional PostgreSQL database bindings.
* [rororo](https://github.com/playpauseandstop/rororo)
  Implement `aiohttp.web` OpenAPI 3 server applications with schema first
  approach.

## Others[¶](#others "Link to this heading")

Here is a list of other known libraries that do not belong in the former categories.

We cannot vouch for the quality of these libraries, use them at your own risk.

Please add your library reference here first and after some time
ask to raise the status.

* [pytest-aiohttp-client](https://github.com/sivakov512/pytest-aiohttp-client)
  Pytest fixture with simpler api, payload decoding and status code assertions.
* [octomachinery](https://octomachinery.dev) A framework for developing
  GitHub Apps and GitHub Actions.
* [aiomixcloud](https://github.com/amikrop/aiomixcloud)
  Mixcloud API wrapper for Python and Async IO.
* [aiohttp-cache](https://github.com/cr0hn/aiohttp-cache) A cache
  system for aiohttp server.
* [aiocache](https://github.com/argaen/aiocache) Caching for asyncio
  with multiple backends (framework agnostic)
* [gain](https://github.com/gaojiuli/gain) Web crawling framework
  based on asyncio for everyone.
* [aiohttp-validate](https://github.com/dchaplinsky/aiohttp_validate)
  Simple library that helps you validate your API endpoints requests/responses with json schema.
* [raven-aiohttp](https://github.com/getsentry/raven-aiohttp) An
  aiohttp transport for raven-python (Sentry client).
* [webargs](https://github.com/sloria/webargs) A friendly library
  for parsing HTTP request arguments, with built-in support for
  popular web frameworks, including Flask, Django, Bottle, Tornado,
  Pyramid, webapp2, Falcon, and aiohttp.
* [aioauth-client](https://github.com/klen/aioauth-client) OAuth
  client for aiohttp.
* [aiohttpretty](https://github.com/CenterForOpenScience/aiohttpretty) A simple
  asyncio compatible httpretty mock using aiohttp.
* [aioresponses](https://github.com/pnuckowski/aioresponses) a
  helper for mock/fake web requests in python aiohttp package.
* [aiohttp-transmute](https://github.com/toumorokoshi/aiohttp-transmute) A transmute
  implementation for aiohttp.
* [aiohttp-login](https://github.com/imbolc/aiohttp-login)
  Registration and authorization (including social) for aiohttp
  applications.
* [aiohttp\_utils](https://github.com/sloria/aiohttp_utils) Handy
  utilities for building aiohttp.web applications.
* [aiohttpproxy](https://github.com/jmehnle/aiohttpproxy) Simple
  aiohttp HTTP proxy.
* [aiohttp\_traversal](https://github.com/zzzsochi/aiohttp_traversal)
  Traversal based router for aiohttp.web.
* [aiohttp\_autoreload](https://github.com/anti1869/aiohttp_autoreload) Makes aiohttp
  server auto-reload on source code change.
* [gidgethub](https://github.com/brettcannon/gidgethub) An async
  GitHub API library for Python.
* [aiohttp\_jrpc](https://github.com/zloidemon/aiohttp_jrpc) aiohttp
  JSON-RPC service.
* [fbemissary](https://github.com/cdunklau/fbemissary) A bot
  framework for the Facebook Messenger platform, built on asyncio and
  aiohttp.
* [aioslacker](https://github.com/wikibusiness/aioslacker) slacker
  wrapper for asyncio.
* [aioreloader](https://github.com/and800/aioreloader) Port of
  tornado reloader to asyncio.
* [aiohttp\_babel](https://github.com/jie/aiohttp_babel) Babel
  localization support for aiohttp.
* [python-mocket](https://github.com/mindflayer/python-mocket) a
  socket mock framework - for all kinds of socket animals, web-clients
  included.
* [aioraft](https://github.com/lisael/aioraft) asyncio RAFT
  algorithm based on aiohttp.
* [home-assistant](https://github.com/home-assistant/home-assistant)
  Open-source home automation platform running on Python 3.
* [discord.py](https://github.com/Rapptz/discord.py) Discord client library.
* [aiogram](https://github.com/aiogram/aiogram)
  A fully asynchronous library for Telegram Bot API written with asyncio and aiohttp.
* [aiohttp-graphql](https://github.com/graphql-python/aiohttp-graphql)
  GraphQL and GraphIQL interface for aiohttp.
* [aiohttp-sentry](https://github.com/underyx/aiohttp-sentry)
  An aiohttp middleware for reporting errors to Sentry.
* [aiohttp-datadog](https://github.com/underyx/aiohttp-datadog)
  An aiohttp middleware for reporting metrics to DataDog.
* [async-v20](https://github.com/jamespeterschinner/async_v20)
  Asynchronous FOREX client for OANDA’s v20 API.
* [aiohttp-jwt](https://github.com/hzlmn/aiohttp-jwt)
  An aiohttp middleware for JWT(JSON Web Token) support.
* [AWS Xray Python SDK](https://github.com/aws/aws-xray-sdk-python)
  Native tracing support for Aiohttp applications.
* [GINO](https://github.com/fantix/gino)
  An asyncio ORM on top of SQLAlchemy core, delivered with an aiohttp extension.
* [New Relic](https://github.com/newrelic/newrelic-quickstarts/tree/main/quickstarts/python/aiohttp) An aiohttp middleware for reporting your [Python application performance](https://newrelic.com/instant-observability/aiohttp) metrics to New Relic.
* [eider-py](https://github.com/eider-rpc/eider-py) Python implementation of
  the [Eider RPC protocol](http://eider.readthedocs.io/).
* [asynapplicationinsights](https://github.com/RobertoPrevato/asynapplicationinsights)
  A client for [Azure Application Insights](https://azure.microsoft.com/en-us/services/application-insights/) implemented using
  `aiohttp` client, including a middleware for `aiohttp` servers to collect web apps
  telemetry.
* [aiogmaps](https://github.com/hzlmn/aiogmaps)
  Asynchronous client for Google Maps API Web Services.
* [DBGR](https://github.com/JakubTesarek/dbgr)
  Terminal based tool to test and debug HTTP APIs with `aiohttp`.
* [aiohttp-middlewares](https://github.com/playpauseandstop/aiohttp-middlewares)
  Collection of useful middlewares for `aiohttp.web` applications.
* [aiohttp-tus](https://github.com/pylotcode/aiohttp-tus)
  [tus.io](https://tus.io) protocol implementation for `aiohttp.web`
  applications.
* [aiohttp-sse-client](https://github.com/rtfol/aiohttp-sse-client)
  A Server-Sent Event python client base on aiohttp.
* [aiohttp-retry](https://github.com/inyutin/aiohttp_retry)
  Wrapper for aiohttp client for retrying requests.
* [aiohttp-socks](https://github.com/romis2012/aiohttp-socks)
  SOCKS proxy connector for aiohttp.
* [aiohttp-catcher](https://github.com/yuvalherziger/aiohttp-catcher)
  An aiohttp middleware library for centralized error handling in aiohttp servers.
* [rsocket](https://github.com/rsocket/rsocket-py)
  Python implementation of [RSocket protocol](https://rsocket.io).
* [nacl\_middleware](https://github.com/CosmicDNA/nacl_middleware)
  An aiohttp middleware library for asymmetric encryption of data transmitted via http and/or websocket connections.
* [aiohttp-asgi-connector](https://github.com/thearchitector/aiohttp-asgi-connector)
  An aiohttp connector for using a `ClientSession` to interface directly with separate ASGI applications.
* [aiohttp-openmetrics](https://github.com/jelmer/aiohttp-openmetrics)
  An aiohttp middleware for exposing Prometheus metrics.
* [wireup](https://github.com/maldoinc/wireup)
  Performant, concise, and easy-to-use dependency injection container.

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
* [Who uses aiohttp?](external.html)
  + [Third-Party libraries](#)
  + [Built with aiohttp](built_with.html)
  + [Powered by aiohttp](powered_by.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/third_party.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
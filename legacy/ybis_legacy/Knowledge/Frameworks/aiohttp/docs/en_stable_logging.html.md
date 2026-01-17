Logging — aiohttp 3.13.3 documentation

# Logging[¶](#logging "Link to this heading")

*aiohttp* uses standard [`logging`](https://docs.python.org/3/library/logging.html#module-logging "(in Python v3.14)") for tracking the
library activity.

We have the following loggers enumerated by names:

* `'aiohttp.access'`
* `'aiohttp.client'`
* `'aiohttp.internal'`
* `'aiohttp.server'`
* `'aiohttp.web'`
* `'aiohttp.websocket'`

You may subscribe to these loggers for getting logging messages. The
page does not provide instructions for logging subscribing while the
most friendly method is [`logging.config.dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "(in Python v3.14)") for
configuring whole loggers in your application.

Logging does not work out of the box. It requires at least minimal `'logging'`
configuration.
Example of minimal working logger setup:

```
import logging
from aiohttp import web

app = web.Application()
logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=5000)
```

Added in version 4.0.0.

## Access logs[¶](#access-logs "Link to this heading")

Access logs are enabled by default. If the debug flag is set, and the default
logger `'aiohttp.access'` is used, access logs will be output to
[`stderr`](https://docs.python.org/3/library/sys.html#sys.stderr "(in Python v3.14)") if no handlers are attached.
Furthermore, if the default logger has no log level set, the log level will be
set to [`logging.DEBUG`](https://docs.python.org/3/library/logging.html#logging.DEBUG "(in Python v3.14)").

This logging may be controlled by [`aiohttp.web.AppRunner()`](web_reference.html#aiohttp.web.AppRunner "aiohttp.web.AppRunner") and
[`aiohttp.web.run_app()`](web_reference.html#aiohttp.web.run_app "aiohttp.web.run_app").

To override the default logger, pass an instance of [`logging.Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "(in Python v3.14)") to
override the default logger.

Note

Use `web.run_app(app, access_log=None)` to disable access logs.

In addition, *access\_log\_format* may be used to specify the log format.

### Format specification[¶](#format-specification "Link to this heading")

The library provides custom micro-language to specifying info about
request and response:

| Option | Meaning |
| --- | --- |
| `%%` | The percent sign |
| `%a` | Remote IP-address (IP-address of proxy if using reverse proxy) |
| `%t` | Time when the request was started to process |
| `%P` | The process ID of the child that serviced the request |
| `%r` | First line of request |
| `%s` | Response status code |
| `%b` | Size of response in bytes, including HTTP headers |
| `%T` | The time taken to serve the request, in seconds |
| `%Tf` | The time taken to serve the request, in seconds with fraction in %.06f format |
| `%D` | The time taken to serve the request, in microseconds |
| `%{FOO}i` | `request.headers['FOO']` |
| `%{FOO}o` | `response.headers['FOO']` |

The default access log format is:

```
'%a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"'
```

Added in version 2.3.0.

*access\_log\_class* introduced.

Example of a drop-in replacement for the default access logger:

```
from aiohttp.abc import AbstractAccessLogger

class AccessLogger(AbstractAccessLogger):

    def log(self, request, response, time):
        self.logger.info(f'{request.remote} '
                         f'"{request.method} {request.path} '
                         f'done in {time}s: {response.status}')

    @property
    def enabled(self):
        """Return True if logger is enabled.

        Override this property if logging is disabled to avoid the
        overhead of calculating details to feed the logger.

        This property may be omitted if logging is always enabled.
        """
        return self.logger.isEnabledFor(logging.INFO)
```

### Gunicorn access logs[¶](#gunicorn-access-logs "Link to this heading")

When [Gunicorn](http://docs.gunicorn.org/en/latest/index.html) is used for
[deployment](deployment.html#aiohttp-deployment-gunicorn), its default access log format
will be automatically replaced with the default aiohttp’s access log format.

If Gunicorn’s option [access\_logformat](http://docs.gunicorn.org/en/stable/settings.html#access-log-format) is
specified explicitly, it should use aiohttp’s format specification.

Gunicorn’s access log works only if [accesslog](http://docs.gunicorn.org/en/stable/settings.html#accesslog) is specified explicitly in your
config or as a command line option.
This configuration can be either a path or `'-'`. If the application uses
a custom logging setup intercepting the `'gunicorn.access'` logger,
[accesslog](http://docs.gunicorn.org/en/stable/settings.html#accesslog) should be set to `'-'` to prevent Gunicorn to create an empty
access log file upon every startup.

## Error logs[¶](#error-logs "Link to this heading")

[`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") uses a logger named `'aiohttp.server'` to store errors
given on web requests handling.

This log is enabled by default.

To use a different logger name, pass *logger* ([`logging.Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "(in Python v3.14)")
instance) to the [`aiohttp.web.AppRunner()`](web_reference.html#aiohttp.web.AppRunner "aiohttp.web.AppRunner") constructor.

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
  + [Tutorial](https://demos.aiohttp.org)
  + [Quickstart](web_quickstart.html)
  + [Advanced Usage](web_advanced.html)
  + [Low Level](web_lowlevel.html)
  + [Reference](web_reference.html)
  + [Logging](#)
  + [Testing](testing.html)
  + [Deployment](deployment.html)
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
[Page source](_sources/logging.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
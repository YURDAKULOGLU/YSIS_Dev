Switching from Standard Logging to Loguru — loguru documentation



* [Help & Guides](../resources.html)
* Switching from Standard Logging to Loguru

---

# Switching from Standard Logging to Loguru[](#switching-from-standard-logging-to-loguru "Link to this heading")

## Introduction to logging in Python[](#introduction-to-logging-in-python "Link to this heading")

First and foremost, it is important to understand some basic concepts about logging in Python.

Logging is an essential part of any application, as it allows you to track the behavior of your code and diagnose issues. It associates messages with severity levels which are collected and dispatched to readable outputs called handlers.

For newcomers, take a look at the tutorial in the Python documentation: [Logging HOWTO](https://docs.python.org/3/howto/logging.html).

## Fundamental differences between `logging` and `loguru`[](#fundamental-differences-between-logging-and-loguru "Link to this heading")

Although `loguru` is written “from scratch” and does not rely on standard `logging` internally, both libraries serve the same purpose: provide functionalities to implement a flexible event logging system. The main difference is that standard `logging` requires the user to explicitly instantiate named `Logger` and configure them with `Handler`, `Formatter` and `Filter`, while `loguru` tries to narrow down the amount of configuration steps.

Apart from that, usage is globally the same, once the `logger` object is created or imported you can start using it to log messages with the appropriate severity (`logger.debug("Dev message")`, `logger.warning("Danger!")`, etc.), messages which are then sent to the configured handlers.

As for standard logging, default logs are sent to `sys.stderr` rather than `sys.stdout`. The POSIX standard specifies that `stderr` is the correct stream for “diagnostic output”. The main compelling case in favor or logging to `stderr` is that it avoids mixing the actual output of the application with debug information. Consider for example pipe-redirection like `python my_app.py | other_app` which would not be possible if logs were emitted to `stdout`. Another major benefit is that Python resolves encoding issues on `sys.stderr` by escaping faulty characters (`"backslashreplace"` policy) while it raises an `UnicodeEncodeError` (`"strict"` policy) on `sys.stdout`.

## Replacing `getLogger()` function[](#replacing-getlogger-function "Link to this heading")

It is usual to call [`getLogger()`](https://docs.python.org/3/library/logging.html#logging.getLogger "(in Python v3.13)") at the beginning of each file to retrieve and use a logger across your module, like this: `logger = logging.getLogger(__name__)`.

Using Loguru, there is no need to explicitly get and name a logger, `from loguru import logger` suffices. Each time this imported logger is used, a [record](../api/logger.html#record) is created and will automatically contain the contextual `__name__` value.

As for standard logging, the `name` attribute can then be used to format and filter your logs.

## Replacing `Logger` objects[](#replacing-logger-objects "Link to this heading")

Loguru replaces the standard [`Logger`](https://docs.python.org/3/library/logging.html#logging.Logger "(in Python v3.13)") configuration by a proper [sink](../api/logger.html#sink) definition. Instead of configuring a logger, you should [`add()`](../api/logger.html#loguru._logger.Logger.add "loguru._logger.Logger.add") and parametrize your handlers. The [`setLevel()`](https://docs.python.org/3/library/logging.html#logging.Logger.setLevel "(in Python v3.13)") and [`addFilter()`](https://docs.python.org/3/library/logging.html#logging.Logger.addFilter "(in Python v3.13)") are suppressed by the configured sink `level` and `filter` parameters. The [`propagate`](https://docs.python.org/3/library/logging.html#logging.Logger.propagate "(in Python v3.13)") attribute and [`disable()`](https://docs.python.org/3/library/logging.html#logging.disable "(in Python v3.13)") function can be replaced by the `filter` option too. The [`makeRecord()`](https://docs.python.org/3/library/logging.html#logging.Logger.makeRecord "(in Python v3.13)") method can be replaced using the `record["extra"]` dict.

Sometimes, more fine-grained control is required over a particular logger. In such case, Loguru provides the [`bind()`](../api/logger.html#loguru._logger.Logger.bind "loguru._logger.Logger.bind") method which can be in particular used to generate a specifically named logger.

For example, by calling `other_logger = logger.bind(name="other")`, each [message](../api/logger.html#message) logged using `other_logger` will populate the `record["extra"]` dict with the `name` value, while using `logger` won’t. This permits differentiating logs from `logger` or `other_logger` from within your sink or filter function.

Let suppose you want a sink to log only some very specific messages:

```
def specific_only(record):
    return "specific" in record["extra"]

logger.add("specific.log", filter=specific_only)

specific_logger = logger.bind(specific=True)

logger.info("General message")          # This is filtered-out by the specific sink
specific_logger.info("Module message")  # This is accepted by the specific sink (and others)
```

Another example, if you want to attach one sink to one named logger:

```
# Only write messages from "a" logger
logger.add("a.log", filter=lambda record: record["extra"].get("name") == "a")
# Only write messages from "b" logger
logger.add("b.log", filter=lambda record: record["extra"].get("name") == "b")

logger_a = logger.bind(name="a")
logger_b = logger.bind(name="b")

logger_a.info("Message A")
logger_b.info("Message B")
```

## Replacing `Handler`, `Filter` and `Formatter` objects[](#replacing-handler-filter-and-formatter-objects "Link to this heading")

Standard `logging` requires you to create an [`Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "(in Python v3.13)") object and then call [`addHandler()`](https://docs.python.org/3/library/logging.html#logging.Logger.addHandler "(in Python v3.13)"). Using Loguru, the handlers are started using [`add()`](../api/logger.html#loguru._logger.Logger.add "loguru._logger.Logger.add"). The sink defines how the handler should manage incoming logging messages, as would do [`handle()`](https://docs.python.org/3/library/logging.html#logging.Handler.handle "(in Python v3.13)") or [`emit()`](https://docs.python.org/3/library/logging.html#logging.Handler.emit "(in Python v3.13)"). To log from multiple modules, you just have to import the logger, all messages will be dispatched to the added handlers.

While calling [`add()`](../api/logger.html#loguru._logger.Logger.add "loguru._logger.Logger.add"), the `level` parameter replaces [`setLevel()`](https://docs.python.org/3/library/logging.html#logging.Handler.setLevel "(in Python v3.13)"), the `format` parameter replaces [`setFormatter()`](https://docs.python.org/3/library/logging.html#logging.Handler.setFormatter "(in Python v3.13)"), the `filter` parameter replaces [`addFilter()`](https://docs.python.org/3/library/logging.html#logging.Handler.addFilter "(in Python v3.13)"). The thread-safety is managed automatically by Loguru, so there is no need for [`createLock()`](https://docs.python.org/3/library/logging.html#logging.Handler.createLock "(in Python v3.13)"), [`acquire()`](https://docs.python.org/3/library/logging.html#logging.Handler.acquire "(in Python v3.13)") nor [`release()`](https://docs.python.org/3/library/logging.html#logging.Handler.release "(in Python v3.13)"). The equivalent method of [`removeHandler()`](https://docs.python.org/3/library/logging.html#logging.Logger.removeHandler "(in Python v3.13)") is [`remove()`](../api/logger.html#loguru._logger.Logger.remove "loguru._logger.Logger.remove") which should be used with the identifier returned by [`add()`](../api/logger.html#loguru._logger.Logger.add "loguru._logger.Logger.add").

Note that you don’t necessarily need to replace your [`Handler`](https://docs.python.org/3/library/logging.html#logging.Handler "(in Python v3.13)") objects because [`add()`](../api/logger.html#loguru._logger.Logger.add "loguru._logger.Logger.add") accepts them as valid sinks.

In short, you can replace:

```
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("spam.log")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
```

With:

```
fmt = "{time} - {name} - {level} - {message}"
logger.add("spam.log", level="DEBUG", format=fmt)
logger.add(sys.stderr, level="ERROR", format=fmt)
```

## Replacing `LogRecord` objects[](#replacing-logrecord-objects "Link to this heading")

In Loguru, the equivalence of a [`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "(in Python v3.13)") instance is a simple `dict` which stores the details of a logged message. To find the correspondence with [`LogRecord`](https://docs.python.org/3/library/logging.html#logging.LogRecord "(in Python v3.13)") attributes, please refer to [the “record dict” documentation](../api/logger.html#record) which lists all available keys.

This `dict` is attached to each [logged message](../api/logger.html#message) through a special `record` attribute of the `str`-like object received by sinks. For example:

```
def simple_sink(message):
    # A simple sink can use "message" as a basic string and ignore the "record" attribute.
    print(message, end="")

def advanced_sink(message):
    # An advanced sink can use the "record" attribute to access contextual information.
    record = message.record

    if record["level"].no >= 50:
        file_path = record["file"].path
        print(f"Critical error in {file_path}", end="", file=sys.stderr)
    else:
        print(message, end="")

logger.add(simple_sink)
logger.add(advanced_sink)
```

As explained in the previous sections, the record dict is also available during invocation of filtering and formatting functions.

If you need to extend the record dict with custom information similarly to what was possible with [`setLogRecordFactory()`](https://docs.python.org/3/library/logging.html#logging.setLogRecordFactory "(in Python v3.13)"), you can simply use the [`patch()`](../api/logger.html#loguru._logger.Logger.patch "loguru._logger.Logger.patch") method to add the desired keys to the `record["extra"]` dict.

## Replacing `%` style formatting of messages[](#replacing-style-formatting-of-messages "Link to this heading")

Loguru only supports `{}`-style formatting.

You have to replace `logger.debug("Some variable: %s", var)` with `logger.debug("Some variable: {}", var)`. All `*args` and `**kwargs` passed to a logging function are used to call `message.format(*args, **kwargs)`. Arguments which do not appear in the message string are simply ignored. Note that passing arguments to logging functions like this may be useful to (slightly) improve performances: it avoids formatting the message if the level is too low to pass any configured handler.

For converting the general format used by [`Formatter`](https://docs.python.org/3/library/logging.html#logging.Formatter "(in Python v3.13)"), refer to [list of available record tokens](../api/logger.html#record).

For converting the date format used by `datefmt`, refer to [list of available date tokens](../api/logger.html#time).

## Replacing `exc_info` argument[](#replacing-exc-info-argument "Link to this heading")

While calling standard logging function, you can pass `exc_info` as an argument to add stacktrace to the message. Instead of that, you should use the [`opt()`](../api/logger.html#loguru._logger.Logger.opt "loguru._logger.Logger.opt") method with `exception` parameter, replacing `logger.debug("Debug error:", exc_info=True)` with `logger.opt(exception=True).debug("Debug error:")`.

The formatted exception will include the whole stacktrace and variables. To prevent that, make sure to use `backtrace=False` and `diagnose=False` while adding your sink.

## Replacing `extra` argument and `LoggerAdapter` objects[](#replacing-extra-argument-and-loggeradapter-objects "Link to this heading")

To pass contextual information to log messages, replace `extra` by inlining [`bind()`](../api/logger.html#loguru._logger.Logger.bind "loguru._logger.Logger.bind") method:

```
context = {"clientip": "192.168.0.1", "user": "fbloggs"}

logger.info("Protocol problem", extra=context)   # Standard logging
logger.bind(**context).info("Protocol problem")  # Loguru
```

This will add context information to the `record["extra"]` dict of your logged message, so make sure to configure your handler format adequately:

```
fmt = "%(asctime)s %(clientip)s %(user)s %(message)s"     # Standard logging
fmt = "{time} {extra[clientip]} {extra[user]} {message}"  # Loguru
```

You can also replace [`LoggerAdapter`](https://docs.python.org/3/library/logging.html#logging.LoggerAdapter "(in Python v3.13)") by calling `logger = logger.bind(clientip="192.168.0.1")` before using it, or by assigning the bound logger to a class instance:

```
class MyClass:

    def __init__(self, clientip):
        self.logger = logger.bind(clientip=clientip)

    def func(self):
        self.logger.debug("Running func")
```

## Replacing `isEnabledFor()` method[](#replacing-isenabledfor-method "Link to this heading")

If you wish to log useful information for your debug logs, but don’t want to pay the performance penalty in release mode while no debug handler is configured, standard logging provides the [`isEnabledFor()`](https://docs.python.org/3/library/logging.html#logging.Logger.isEnabledFor "(in Python v3.13)") method:

```
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("Message data: %s", expensive_func())
```

You can replace this with the [`opt()`](../api/logger.html#loguru._logger.Logger.opt "loguru._logger.Logger.opt") method and `lazy` option:

```
# Arguments should be functions which will be called if needed
logger.opt(lazy=True).debug("Message data: {}", expensive_func)
```

## Replacing `addLevelName()` and `getLevelName()` functions[](#replacing-addlevelname-and-getlevelname-functions "Link to this heading")

To add a new custom level, you can replace [`addLevelName()`](https://docs.python.org/3/library/logging.html#logging.addLevelName "(in Python v3.13)") with the [`level()`](../api/logger.html#loguru._logger.Logger.level "loguru._logger.Logger.level") function:

```
logging.addLevelName(33, "CUSTOM")                       # Standard logging
logger.level("CUSTOM", no=45, color="<red>", icon="🚨")  # Loguru
```

The same function can be used to replace [`getLevelName()`](https://docs.python.org/3/library/logging.html#logging.getLevelName "(in Python v3.13)"):

```
logger.getLevelName(33)  # => "CUSTOM"
logger.level("CUSTOM")   # => (name='CUSTOM', no=33, color="<red>", icon="🚨")
```

Note that contrary to standard logging, Loguru doesn’t associate severity number to any level, levels are only identified by their name.

## Replacing `basicConfig()` and `dictConfig()` functions[](#replacing-basicconfig-and-dictconfig-functions "Link to this heading")

The [`basicConfig()`](https://docs.python.org/3/library/logging.html#logging.basicConfig "(in Python v3.13)") and [`dictConfig()`](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig "(in Python v3.13)") functions are replaced by the [`configure()`](../api/logger.html#loguru._logger.Logger.configure "loguru._logger.Logger.configure") method.

This does not accept `config.ini` files, though, so you have to handle that yourself using your favorite format.

## Replacing `captureWarnings()` function[](#replacing-capturewarnings-function "Link to this heading")

The [`captureWarnings()`](https://docs.python.org/3/library/logging.html#logging.captureWarnings "(in Python v3.13)") function which redirects alerts from the [`warnings`](https://docs.python.org/3/library/warnings.html#module-warnings "(in Python v3.13)") module to the logging system can be implemented by simply replacing [`warnings.showwarning()`](https://docs.python.org/3/library/warnings.html#warnings.showwarning "(in Python v3.13)") function as follow:

```
import warnings
from loguru import logger

showwarning_ = warnings.showwarning

def showwarning(message, *args, **kwargs):
    logger.warning(message)
    showwarning_(message, *args, **kwargs)

warnings.showwarning = showwarning
```

## Replacing `assertLogs()` method from `unittest` library[](#replacing-assertlogs-method-from-unittest-library "Link to this heading")

The [`assertLogs()`](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertLogs "(in Python v3.13)") method defined in the [`unittest`](https://docs.python.org/3/library/unittest.html#module-unittest "(in Python v3.13)") from standard library is used to capture and test logged messages. However, it can’t be made compatible with Loguru. It needs to be replaced with a custom context manager possibly implemented as follows:

```
from contextlib import contextmanager

@contextmanager
def capture_logs(level="INFO", format="{level}:{name}:{message}"):
    """Capture loguru-based logs."""
    output = []
    handler_id = logger.add(output.append, level=level, format=format)
    yield output
    logger.remove(handler_id)
```

It provides the list of [logged messages](../api/logger.html#message) for each of which you can access [the record attribute](../api/logger.html#record). Here is a usage example:

```
def do_something(val):
    if val < 0:
        logger.error("Invalid value")
        return 0
    return val * 2


class TestDoSomething(unittest.TestCase):
    def test_do_something_good(self):
        with capture_logs() as output:
            do_something(1)
        self.assertEqual(output, [])

    def test_do_something_bad(self):
        with capture_logs() as output:
            do_something(-1)
        self.assertEqual(len(output), 1)
        message = output[0]
        self.assertIn("Invalid value", message)
        self.assertEqual(message.record["level"].name, "ERROR")
```

See also

See [testing logging](recipes.html#recipes-testing) for more information.

## Replacing `caplog` fixture from `pytest` library[](#replacing-caplog-fixture-from-pytest-library "Link to this heading")

[`pytest`](https://docs.pytest.org/en/latest/) is a very common testing framework. The [`caplog`](https://docs.pytest.org/en/latest/logging.html?highlight=caplog#caplog-fixture) fixture captures logging output so that it can be tested against. For example:

```
from loguru import logger

def some_func(a, b):
    if a < 0:
        logger.warning("Oh no!")
    return a + b

def test_some_func(caplog):
    assert some_func(-1, 3) == 2
    assert "Oh no!" in caplog.text
```

If you’ve followed all the migration guidelines thus far, you’ll notice that this test will fail. This is because [`pytest`](https://docs.pytest.org/en/latest/) links to the standard library’s `logging` module.

So to fix things, we need to add a sink that propagates Loguru to the caplog handler.
This is done by overriding the [`caplog`](https://docs.pytest.org/en/latest/logging.html?highlight=caplog#caplog-fixture) fixture to capture its handler. In your `conftest.py` file, add the following:

```
import pytest
from loguru import logger
from _pytest.logging import LogCaptureFixture

@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)
```

Run your tests and things should all be working as expected. Additional information can be found in [GH#59](https://github.com/Delgan/loguru/issues/59) and [GH#474](https://github.com/Delgan/loguru/issues/474). You can also install and use the [`pytest-loguru`](https://github.com/mcarans/pytest-loguru) package created by [@mcarans](https://github.com/mcarans).

Note that if you want Loguru logs to be propagated to Pytest terminal reporter, you can do so by overriding the `reportlog` fixture as follows:

```
import pytest
from loguru import logger

@pytest.fixture
def reportlog(pytestconfig):
    logging_plugin = pytestconfig.pluginmanager.getplugin("logging-plugin")
    handler_id = logger.add(logging_plugin.report_handler, format="{message}")
    yield
    logger.remove(handler_id)
```

Finally, when dealing with the `--log-cli-level` command-line flag, remember that this option controls the standard `logging` logs, not `loguru` ones. For this reason, you must first install a `PropagateHandler` for compatibility:

```
@pytest.fixture(autouse=True)
def propagate_logs():

    class PropagateHandler(logging.Handler):
        def emit(self, record):
            if logging.getLogger(record.name).isEnabledFor(record.levelno):
                logging.getLogger(record.name).handle(record)

    logger.remove()
    logger.add(PropagateHandler(), format="{message}")
    yield
```

See also

See [testing logging](recipes.html#recipes-testing) for more information.

CLICK
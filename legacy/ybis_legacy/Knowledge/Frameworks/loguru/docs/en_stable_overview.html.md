Overview — loguru documentation



* Overview

---

# Overview[](#overview "Link to this heading")

## Installation[](#installation "Link to this heading")

```
pip install loguru
```

## Features[](#features "Link to this heading")

* [Ready to use out of the box without boilerplate](#ready-to-use-out-of-the-box-without-boilerplate)
* [No Handler, no Formatter, no Filter: one function to rule them all](#no-handler-no-formatter-no-filter-one-function-to-rule-them-all)
* [Easier file logging with rotation / retention / compression](#easier-file-logging-with-rotation-retention-compression)
* [Modern string formatting using braces style](#modern-string-formatting-using-braces-style)
* [Exceptions catching within threads or main](#exceptions-catching-within-threads-or-main)
* [Pretty logging with colors](#pretty-logging-with-colors)
* [Asynchronous, Thread-safe, Multiprocess-safe](#asynchronous-thread-safe-multiprocess-safe)
* [Fully descriptive exceptions](#fully-descriptive-exceptions)
* [Structured logging as needed](#structured-logging-as-needed)
* [Lazy evaluation of expensive functions](#lazy-evaluation-of-expensive-functions)
* [Customizable levels](#customizable-levels)
* [Better datetime handling](#better-datetime-handling)
* [Suitable for scripts and libraries](#suitable-for-scripts-and-libraries)
* [Entirely compatible with standard logging](#entirely-compatible-with-standard-logging)
* [Personalizable defaults through environment variables](#personalizable-defaults-through-environment-variables)
* [Convenient parser](#convenient-parser)
* [Exhaustive notifier](#exhaustive-notifier)
* ~~[10x faster than built-in logging](#x-faster-than-built-in-logging)~~

## Take the tour[](#take-the-tour "Link to this heading")

### Ready to use out of the box without boilerplate[](#ready-to-use-out-of-the-box-without-boilerplate "Link to this heading")

The main concept of Loguru is that **there is one and only one** [`logger`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger).

For convenience, it is pre-configured and outputs to `stderr` to begin with (but that’s entirely configurable).

```
from loguru import logger

logger.debug("That's it, beautiful and simple logging!")
```

The [`logger`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger) is just an interface which dispatches log messages to configured handlers. Simple, right?

### No Handler, no Formatter, no Filter: one function to rule them all[](#no-handler-no-formatter-no-filter-one-function-to-rule-them-all "Link to this heading")

How to add a handler? How to set up logs formatting? How to filter messages? How to set level?

One answer: the [`add()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add) function.

```
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
```

This function should be used to register [sinks](https://loguru.readthedocs.io/en/stable/api/logger.html#sink) which are responsible for managing [log messages](https://loguru.readthedocs.io/en/stable/api/logger.html#message) contextualized with a [record dict](https://loguru.readthedocs.io/en/stable/api/logger.html#record). A sink can take many forms: a simple function, a string path, a file-like object, a coroutine function or a built-in Handler.

Note that you may also a previously added handler by using the identifier returned while adding it. This is particularly useful if you want to supersede the default `stderr` handler: just call [`logger.remove()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.remove) to make a fresh start.

### Easier file logging with rotation / retention / compression[](#easier-file-logging-with-rotation-retention-compression "Link to this heading")

If you want to send logged messages to a file, you just have to use a string path as the sink. It can be automatically timed too for convenience:

```
logger.add("file_{time}.log")
```

It is also [easily configurable](https://loguru.readthedocs.io/en/stable/api/logger.html#file) if you need rotating logger, if you want to remove older logs, or if you wish to compress your files at closure.

```
logger.add("file_1.log", rotation="500 MB")    # Automatically rotate too big file
logger.add("file_2.log", rotation="12:00")     # New file is created each day at noon
logger.add("file_3.log", rotation="1 week")    # Once the file is too old, it's rotated

logger.add("file_X.log", retention="10 days")  # Cleanup after some time

logger.add("file_Y.log", compression="zip")    # Save some loved space
```

### Modern string formatting using braces style[](#modern-string-formatting-using-braces-style "Link to this heading")

Loguru favors the much more elegant and powerful `{}` formatting over `%`, logging functions are actually equivalent to `str.format()`.

```
logger.info("If you're using Python {}, prefer {feature} of course!", 3.6, feature="f-strings")
```

### Exceptions catching within threads or main[](#exceptions-catching-within-threads-or-main "Link to this heading")

Have you ever seen your program crashing unexpectedly without seeing anything in the log file? Did you ever notice that exceptions occurring in threads were not logged? This can be solved using the [`catch()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.catch) decorator / context manager which ensures that any error is correctly propagated to the [`logger`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger).

```
@logger.catch
def my_function(x, y, z):
    # An error? It's caught anyway!
    return 1 / (x + y + z)
```

### Pretty logging with colors[](#pretty-logging-with-colors "Link to this heading")

Loguru automatically adds colors to your logs if your terminal is compatible. You can define your favorite style by using [markup tags](https://loguru.readthedocs.io/en/stable/api/logger.html#color) in the sink format.

```
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")
```

### Asynchronous, Thread-safe, Multiprocess-safe[](#asynchronous-thread-safe-multiprocess-safe "Link to this heading")

All sinks added to the [`logger`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger) are thread-safe by default. They are not multiprocess-safe, but you can `enqueue` the messages to ensure logs integrity. This same argument can also be used if you want async logging.

```
logger.add("somefile.log", enqueue=True)
```

Coroutine functions used as sinks are also supported and should be awaited with [`complete()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.complete).

### Fully descriptive exceptions[](#fully-descriptive-exceptions "Link to this heading")

Logging exceptions that occur in your code is important to track bugs, but it’s quite useless if you don’t know why it failed. Loguru helps you identify problems by allowing the entire stack trace to be displayed, including values of variables (thanks [`better_exceptions`](https://github.com/Qix-/better-exceptions) for this!).

The code:

```
# Caution, "diagnose=True" is the default and may leak sensitive data in prod
logger.add("out.log", backtrace=True, diagnose=True)

def func(a, b):
    return a / b

def nested(c):
    try:
        func(5, c)
    except ZeroDivisionError:
        logger.exception("What?!")

nested(0)
```

Would result in:

```
2018-07-17 01:38:43.975 | ERROR    | __main__:nested:10 - What?!
Traceback (most recent call last):

  File "test.py", line 12, in <module>
    nested(0)
    └ <function nested at 0x7f5c755322f0>

> File "test.py", line 8, in nested
    func(5, c)
    │       └ 0
    └ <function func at 0x7f5c79fc2e18>

  File "test.py", line 4, in func
    return a / b
           │   └ 0
           └ 5

ZeroDivisionError: division by zero
```

Note that this feature won’t work on default Python REPL due to unavailable frame data.

See also: [Security considerations when using Loguru](https://loguru.readthedocs.io/en/stable/resources/recipes.html#security-considerations-when-using-loguru).

### Structured logging as needed[](#structured-logging-as-needed "Link to this heading")

Want your logs to be serialized for easier parsing or to pass them around? Using the `serialize` argument, each log message will be converted to a JSON string before being sent to the configured sink.

```
logger.add(custom_sink_function, serialize=True)
```

Using [`bind()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.bind) you can contextualize your logger messages by modifying the `extra` record attribute.

```
logger.add("file.log", format="{extra[ip]} {extra[user]} {message}")
context_logger = logger.bind(ip="192.168.0.1", user="someone")
context_logger.info("Contextualize your logger easily")
context_logger.bind(user="someone_else").info("Inline binding of extra attribute")
context_logger.info("Use kwargs to add context during formatting: {user}", user="anybody")
```

It is possible to modify a context-local state temporarily with [`contextualize()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.contextualize):

```
with logger.contextualize(task=task_id):
    do_something()
    logger.info("End of task")
```

You can also have more fine-grained control over your logs by combining [`bind()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.bind) and `filter`:

```
logger.add("special.log", filter=lambda record: "special" in record["extra"])
logger.debug("This message is not logged to the file")
logger.bind(special=True).info("This message, though, is logged to the file!")
```

Finally, the [`patch()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.patch) method allows dynamic values to be attached to the record dict of each new message:

```
logger.add(sys.stderr, format="{extra[utc]} {message}")
logger = logger.patch(lambda record: record["extra"].update(utc=datetime.utcnow()))
```

### Lazy evaluation of expensive functions[](#lazy-evaluation-of-expensive-functions "Link to this heading")

Sometime you would like to log verbose information without performance penalty in production, you can use the [`opt()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.opt) method to achieve this.

```
logger.opt(lazy=True).debug("If sink level <= DEBUG: {x}", x=lambda: expensive_function(2**64))

# By the way, "opt()" serves many usages
logger.opt(exception=True).info("Error stacktrace added to the log message (tuple accepted too)")
logger.opt(colors=True).info("Per message <blue>colors</blue>")
logger.opt(record=True).info("Display values from the record (eg. {record[thread]})")
logger.opt(raw=True).info("Bypass sink formatting\n")
logger.opt(depth=1).info("Use parent stack context (useful within wrapped functions)")
logger.opt(capture=False).info("Keyword arguments not added to {dest} dict", dest="extra")
```

### Customizable levels[](#customizable-levels "Link to this heading")

Loguru comes with all standard [logging levels](https://loguru.readthedocs.io/en/stable/api/logger.html#levels) to which [`trace()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.trace) and [`success()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.success) are added. Do you need more? Then, just create it by using the [`level()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.level) function.

```
new_level = logger.level("SNAKY", no=38, color="<yellow>", icon="🐍")

logger.log("SNAKY", "Here we go!")
```

### Better datetime handling[](#better-datetime-handling "Link to this heading")

The standard logging is bloated with arguments like `datefmt` or `msecs`, `%(asctime)s` and `%(created)s`, naive datetimes without timezone information, not intuitive formatting, etc. Loguru [fixes it](https://loguru.readthedocs.io/en/stable/api/logger.html#time):

```
logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
```

### Suitable for scripts and libraries[](#suitable-for-scripts-and-libraries "Link to this heading")

Using the logger in your scripts is easy, and you can [`configure()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.configure) it at start. To use Loguru from inside a library, remember to never call [`add()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add) but use [`disable()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.disable) instead so logging functions become no-op. If a developer wishes to see your library’s logs, they can [`enable()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.enable) it again.

```
# For scripts
config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": "file.log", "serialize": True},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)

# For libraries, should be your library's `__name__`
logger.disable("my_library")
logger.info("No matter added sinks, this message is not displayed")

# In your application, enable the logger in the library
logger.enable("my_library")
logger.info("This message however is propagated to the sinks")
```

For additional convenience, you can also use the [`loguru-config`](https://github.com/erezinman/loguru-config) library to setup the `logger` directly from a configuration file.

### Entirely compatible with standard logging[](#entirely-compatible-with-standard-logging "Link to this heading")

Wish to use built-in logging `Handler` as a Loguru sink?

```
handler = logging.handlers.SysLogHandler(address=('localhost', 514))
logger.add(handler)
```

Need to propagate Loguru messages to standard `logging`?

```
class PropagateHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        logging.getLogger(record.name).handle(record)

logger.add(PropagateHandler(), format="{message}")
```

Want to intercept standard `logging` messages toward your Loguru sinks?

```
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
```

### Personalizable defaults through environment variables[](#personalizable-defaults-through-environment-variables "Link to this heading")

Don’t like the default logger formatting? Would prefer another `DEBUG` color? [No problem](https://loguru.readthedocs.io/en/stable/api/logger.html#env):

```
# Linux / OSX
export LOGURU_FORMAT="{time} | <lvl>{message}</lvl>"

# Windows
setx LOGURU_DEBUG_COLOR "<green>"
```

### Convenient parser[](#convenient-parser "Link to this heading")

It is often useful to extract specific information from generated logs, this is why Loguru provides a [`parse()`](https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.parse) method which helps to deal with logs and regexes.

```
pattern = r"(?P<time>.*) - (?P<level>[0-9]+) - (?P<message>.*)"  # Regex with named groups
caster_dict = dict(time=dateutil.parser.parse, level=int)        # Transform matching groups

for groups in logger.parse("file.log", pattern, cast=caster_dict):
    print("Parsed:", groups)
    # {"level": 30, "message": "Log example", "time": datetime(2018, 12, 09, 11, 23, 55)}
```

### Exhaustive notifier[](#exhaustive-notifier "Link to this heading")

Loguru can easily be combined with the great [`apprise`](https://github.com/caronc/apprise) library (must be installed separately) to receive an e-mail when your program fail unexpectedly or to send many other kind of notifications.

```
import apprise

# Define the configuration constants.
WEBHOOK_ID = "123456790"
WEBHOOK_TOKEN = "abc123def456"

# Prepare the object to send Discord notifications.
notifier = apprise.Apprise()
notifier.add(f"discord://{WEBHOOK_ID}/{WEBHOOK_TOKEN}")

# Install a handler to be alerted on each error.
# You can filter out logs from "apprise" itself to avoid recursive calls.
logger.add(notifier.notify, level="ERROR", filter={"apprise": False})
```

### 10x faster than built-in logging[](#x-faster-than-built-in-logging "Link to this heading")

Although logging impact on performances is in most cases negligible, a zero-cost logger would allow to use it anywhere without much concern. In an upcoming release, Loguru’s critical functions will be implemented in C for maximum speed.

CLICK
celery.utils.log — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.text.html "celery.utils.text") |
* [previous](celery.utils.imports.html "celery.utils.imports") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.log`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.log.html).

# `celery.utils.log`[¶](#celery-utils-log "Link to this heading")

Logging utilities.

*class* celery.utils.log.ColorFormatter(*fmt=None*, *use\_color=True*)[[source]](../../_modules/celery/utils/log.html#ColorFormatter)[¶](#celery.utils.log.ColorFormatter "Link to this definition")
:   Logging formatter that adds colors based on severity.

    COLORS *= {'black': <bound method colored.black of ''>, 'blue': <bound method colored.blue of ''>, 'cyan': <bound method colored.cyan of ''>, 'green': <bound method colored.green of ''>, 'magenta': <bound method colored.magenta of ''>, 'red': <bound method colored.red of ''>, 'white': <bound method colored.white of ''>, 'yellow': <bound method colored.yellow of ''>}*[¶](#celery.utils.log.ColorFormatter.COLORS "Link to this definition")
    :   Loglevel -> Color mapping.

    colors *= {'CRITICAL': <bound method colored.magenta of ''>, 'DEBUG': <bound method colored.blue of ''>, 'ERROR': <bound method colored.red of ''>, 'WARNING': <bound method colored.yellow of ''>}*[¶](#celery.utils.log.ColorFormatter.colors "Link to this definition")

    format(*record*)[[source]](../../_modules/celery/utils/log.html#ColorFormatter.format)[¶](#celery.utils.log.ColorFormatter.format "Link to this definition")
    :   Format the specified record as text.

        The record’s attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.

    formatException(*ei*)[[source]](../../_modules/celery/utils/log.html#ColorFormatter.formatException)[¶](#celery.utils.log.ColorFormatter.formatException "Link to this definition")
    :   Format and return the specified exception information as a string.

        This default implementation just uses
        traceback.print\_exception()

*class* celery.utils.log.LoggingProxy(*logger*, *loglevel=None*)[[source]](../../_modules/celery/utils/log.html#LoggingProxy)[¶](#celery.utils.log.LoggingProxy "Link to this definition")
:   Forward file object to [`logging.Logger`](https://docs.python.org/dev/library/logging.html#logging.Logger "(in Python v3.15)") instance.

    Parameters:
    :   * **logger** ([*Logger*](https://docs.python.org/dev/library/logging.html#logging.Logger "(in Python v3.15)")) – Logger instance to forward to.
        * **loglevel** ([*int*](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")*,* [*str*](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")) – Log level to use when logging messages.

    close()[[source]](../../_modules/celery/utils/log.html#LoggingProxy.close)[¶](#celery.utils.log.LoggingProxy.close "Link to this definition")

    closed *= False*[¶](#celery.utils.log.LoggingProxy.closed "Link to this definition")

    flush()[[source]](../../_modules/celery/utils/log.html#LoggingProxy.flush)[¶](#celery.utils.log.LoggingProxy.flush "Link to this definition")

    isatty()[[source]](../../_modules/celery/utils/log.html#LoggingProxy.isatty)[¶](#celery.utils.log.LoggingProxy.isatty "Link to this definition")
    :   Here for file support.

    loglevel *= 40*[¶](#celery.utils.log.LoggingProxy.loglevel "Link to this definition")

    mode *= 'w'*[¶](#celery.utils.log.LoggingProxy.mode "Link to this definition")

    name *= None*[¶](#celery.utils.log.LoggingProxy.name "Link to this definition")

    write(*data: AnyStr*) → [int](https://docs.python.org/dev/library/functions.html#int "(in Python v3.15)")[[source]](../../_modules/celery/utils/log.html#LoggingProxy.write)[¶](#celery.utils.log.LoggingProxy.write "Link to this definition")
    :   Write message to logging object.

    writelines(*sequence: [Sequence](https://docs.python.org/dev/library/typing.html#typing.Sequence "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")]*) → [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")[[source]](../../_modules/celery/utils/log.html#LoggingProxy.writelines)[¶](#celery.utils.log.LoggingProxy.writelines "Link to this definition")
    :   Write list of strings to file.

        The sequence can be any iterable object producing strings.
        This is equivalent to calling [`write()`](#celery.utils.log.LoggingProxy.write "celery.utils.log.LoggingProxy.write") for each string.

celery.utils.log.get\_logger(*name*)[[source]](../../_modules/celery/utils/log.html#get_logger)[¶](#celery.utils.log.get_logger "Link to this definition")
:   Get logger by name.

celery.utils.log.get\_multiprocessing\_logger()[[source]](../../_modules/celery/utils/log.html#get_multiprocessing_logger)[¶](#celery.utils.log.get_multiprocessing_logger "Link to this definition")
:   Return the multiprocessing logger.

celery.utils.log.get\_task\_logger(*name*)[[source]](../../_modules/celery/utils/log.html#get_task_logger)[¶](#celery.utils.log.get_task_logger "Link to this definition")
:   Get logger for task module by name.

celery.utils.log.in\_sighandler()[[source]](../../_modules/celery/utils/log.html#in_sighandler)[¶](#celery.utils.log.in_sighandler "Link to this definition")
:   Context that records that we are in a signal handler.

celery.utils.log.mlevel(*level*)[[source]](../../_modules/celery/utils/log.html#mlevel)[¶](#celery.utils.log.mlevel "Link to this definition")
:   Convert level name/int to log level.

celery.utils.log.reset\_multiprocessing\_logger()[[source]](../../_modules/celery/utils/log.html#reset_multiprocessing_logger)[¶](#celery.utils.log.reset_multiprocessing_logger "Link to this definition")
:   Reset multiprocessing logging setup.

celery.utils.log.set\_in\_sighandler(*value*)[[source]](../../_modules/celery/utils/log.html#set_in_sighandler)[¶](#celery.utils.log.set_in_sighandler "Link to this definition")
:   Set flag signifying that we’re inside a signal handler.

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.utils.imports`](celery.utils.imports.html "previous chapter")

#### Next topic

[`celery.utils.text`](celery.utils.text.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.log.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.text.html "celery.utils.text") |
* [previous](celery.utils.imports.html "celery.utils.imports") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.log`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
celery.bin.base — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.bin.celery.html "celery.bin.celery") |
* [previous](celery.worker.worker.html "celery.worker.worker") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.bin.base`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.bin.base.html).

# `celery.bin.base`[¶](#celery-bin-base "Link to this heading")

Click customizations for Celery.

*class* celery.bin.base.CLIContext(*app*, *no\_color*, *workdir*, *quiet=False*)[[source]](../_modules/celery/bin/base.html#CLIContext)[¶](#celery.bin.base.CLIContext "Link to this definition")
:   Context Object for the CLI.

    *property* ERROR[¶](#celery.bin.base.CLIContext.ERROR "Link to this definition")

    *property* OK[¶](#celery.bin.base.CLIContext.OK "Link to this definition")

    echo(*message=None*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CLIContext.echo)[¶](#celery.bin.base.CLIContext.echo "Link to this definition")

    error(*message=None*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CLIContext.error)[¶](#celery.bin.base.CLIContext.error "Link to this definition")

    pretty(*n*)[[source]](../_modules/celery/bin/base.html#CLIContext.pretty)[¶](#celery.bin.base.CLIContext.pretty "Link to this definition")

    pretty\_dict\_ok\_error(*n*)[[source]](../_modules/celery/bin/base.html#CLIContext.pretty_dict_ok_error)[¶](#celery.bin.base.CLIContext.pretty_dict_ok_error "Link to this definition")

    pretty\_list(*n*)[[source]](../_modules/celery/bin/base.html#CLIContext.pretty_list)[¶](#celery.bin.base.CLIContext.pretty_list "Link to this definition")

    say\_chat(*direction*, *title*, *body=''*, *show\_body=False*)[[source]](../_modules/celery/bin/base.html#CLIContext.say_chat)[¶](#celery.bin.base.CLIContext.say_chat "Link to this definition")

    secho(*message=None*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CLIContext.secho)[¶](#celery.bin.base.CLIContext.secho "Link to this definition")

    style(*message=None*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CLIContext.style)[¶](#celery.bin.base.CLIContext.style "Link to this definition")

*class* celery.bin.base.CeleryCommand(*name: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)")*, *context\_settings: [MutableMapping](https://docs.python.org/dev/library/typing.html#typing.MutableMapping "(in Python v3.15)")[[str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)"), [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *callback: [Callable](https://docs.python.org/dev/library/typing.html#typing.Callable "(in Python v3.15)")[[...], [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *params: [List](https://docs.python.org/dev/library/typing.html#typing.List "(in Python v3.15)")[[Parameter](https://click.palletsprojects.com/en/stable/api/#click.Parameter "(in Click v8.3.x)")] | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *help: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *epilog: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *short\_help: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = None*, *options\_metavar: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)") | [None](https://docs.python.org/dev/library/constants.html#None "(in Python v3.15)") = '[OPTIONS]'*, *add\_help\_option: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = True*, *no\_args\_is\_help: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*, *hidden: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*, *deprecated: [bool](https://docs.python.org/dev/library/functions.html#bool "(in Python v3.15)") = False*)[[source]](../_modules/celery/bin/base.html#CeleryCommand)[¶](#celery.bin.base.CeleryCommand "Link to this definition")
:   Customized command for Celery.

    format\_options(*ctx*, *formatter*)[[source]](../_modules/celery/bin/base.html#CeleryCommand.format_options)[¶](#celery.bin.base.CeleryCommand.format_options "Link to this definition")
    :   Write all the options into the formatter if they exist.

*class* celery.bin.base.CeleryDaemonCommand(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CeleryDaemonCommand)[¶](#celery.bin.base.CeleryDaemonCommand "Link to this definition")
:   Daemon commands.

*class* celery.bin.base.CeleryOption(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CeleryOption)[¶](#celery.bin.base.CeleryOption "Link to this definition")
:   Customized option for Celery.

    get\_default(*ctx*, *\*args*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#CeleryOption.get_default)[¶](#celery.bin.base.CeleryOption.get_default "Link to this definition")
    :   Get the default for the parameter. Tries
        `Context.lookup_default()` first, then the local default.

        Parameters:
        :   * **ctx** – Current context.
            * **call** – If the default is a callable, call it. Disable to
              return the callable instead.

        Changed in version 8.0.2: Type casting is no longer performed when getting a default.

        Changed in version 8.0.1: Type casting can fail in resilient parsing mode. Invalid
        defaults will not prevent showing help text.

        Changed in version 8.0: Looks at `ctx.default_map` first.

        Changed in version 8.0: Added the `call` parameter.

*class* celery.bin.base.CommaSeparatedList[[source]](../_modules/celery/bin/base.html#CommaSeparatedList)[¶](#celery.bin.base.CommaSeparatedList "Link to this definition")
:   Comma separated list argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#CommaSeparatedList.convert)[¶](#celery.bin.base.CommaSeparatedList.convert "Link to this definition")
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   * **value** – The value to convert.
            * **param** – The parameter that is using this type to convert
              its value. May be `None`.
            * **ctx** – The current context that arrived at this value. May
              be `None`.

    name*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")* *= 'comma separated list'*[¶](#celery.bin.base.CommaSeparatedList.name "Link to this definition")
    :   the descriptive name of this type

*class* celery.bin.base.DaemonOption(*\*args*, *\*\*kwargs*)[[source]](../_modules/celery/bin/base.html#DaemonOption)[¶](#celery.bin.base.DaemonOption "Link to this definition")
:   Common daemonization option

    daemon\_setting(*ctx: [Context](https://click.palletsprojects.com/en/stable/api/#click.Context "(in Click v8.3.x)")*, *opt: [CeleryOption](#celery.bin.base.CeleryOption "celery.bin.base.CeleryOption")*, *value: [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")*) → [Any](https://docs.python.org/dev/library/typing.html#typing.Any "(in Python v3.15)")[[source]](../_modules/celery/bin/base.html#DaemonOption.daemon_setting)[¶](#celery.bin.base.DaemonOption.daemon_setting "Link to this definition")
    :   Try to fetch daemonization option from applications settings.
        Use the daemon command name as prefix (eg. worker -> worker\_pidfile)

*class* celery.bin.base.ISO8601DateTime[[source]](../_modules/celery/bin/base.html#ISO8601DateTime)[¶](#celery.bin.base.ISO8601DateTime "Link to this definition")
:   ISO 8601 Date Time argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#ISO8601DateTime.convert)[¶](#celery.bin.base.ISO8601DateTime.convert "Link to this definition")
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   * **value** – The value to convert.
            * **param** – The parameter that is using this type to convert
              its value. May be `None`.
            * **ctx** – The current context that arrived at this value. May
              be `None`.

    name*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")* *= 'iso-86091'*[¶](#celery.bin.base.ISO8601DateTime.name "Link to this definition")
    :   the descriptive name of this type

*class* celery.bin.base.ISO8601DateTimeOrFloat[[source]](../_modules/celery/bin/base.html#ISO8601DateTimeOrFloat)[¶](#celery.bin.base.ISO8601DateTimeOrFloat "Link to this definition")
:   ISO 8601 Date Time or float argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#ISO8601DateTimeOrFloat.convert)[¶](#celery.bin.base.ISO8601DateTimeOrFloat.convert "Link to this definition")
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   * **value** – The value to convert.
            * **param** – The parameter that is using this type to convert
              its value. May be `None`.
            * **ctx** – The current context that arrived at this value. May
              be `None`.

    name*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")* *= 'iso-86091 or float'*[¶](#celery.bin.base.ISO8601DateTimeOrFloat.name "Link to this definition")
    :   the descriptive name of this type

*class* celery.bin.base.JsonArray[[source]](../_modules/celery/bin/base.html#JsonArray)[¶](#celery.bin.base.JsonArray "Link to this definition")
:   JSON formatted array argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#JsonArray.convert)[¶](#celery.bin.base.JsonArray.convert "Link to this definition")
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   * **value** – The value to convert.
            * **param** – The parameter that is using this type to convert
              its value. May be `None`.
            * **ctx** – The current context that arrived at this value. May
              be `None`.

    name*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")* *= 'json array'*[¶](#celery.bin.base.JsonArray.name "Link to this definition")
    :   the descriptive name of this type

*class* celery.bin.base.JsonObject[[source]](../_modules/celery/bin/base.html#JsonObject)[¶](#celery.bin.base.JsonObject "Link to this definition")
:   JSON formatted object argument.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#JsonObject.convert)[¶](#celery.bin.base.JsonObject.convert "Link to this definition")
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   * **value** – The value to convert.
            * **param** – The parameter that is using this type to convert
              its value. May be `None`.
            * **ctx** – The current context that arrived at this value. May
              be `None`.

    name*: [str](https://docs.python.org/dev/library/stdtypes.html#str "(in Python v3.15)")* *= 'json object'*[¶](#celery.bin.base.JsonObject.name "Link to this definition")
    :   the descriptive name of this type

*class* celery.bin.base.LogLevel[[source]](../_modules/celery/bin/base.html#LogLevel)[¶](#celery.bin.base.LogLevel "Link to this definition")
:   Log level option.

    convert(*value*, *param*, *ctx*)[[source]](../_modules/celery/bin/base.html#LogLevel.convert)[¶](#celery.bin.base.LogLevel.convert "Link to this definition")
    :   Convert the value to the correct type. This is not called if
        the value is `None` (the missing value).

        This must accept string values from the command line, as well as
        values that are already the correct type. It may also convert
        other compatible types.

        The `param` and `ctx` arguments may be `None` in certain
        situations, such as when converting prompt input.

        If the value cannot be converted, call `fail()` with a
        descriptive message.

        Parameters:
        :   * **value** – The value to convert.
            * **param** – The parameter that is using this type to convert
              its value. May be `None`.
            * **ctx** – The current context that arrived at this value. May
              be `None`.

celery.bin.base.handle\_preload\_options(*f*)[[source]](../_modules/celery/bin/base.html#handle_preload_options)[¶](#celery.bin.base.handle_preload_options "Link to this definition")
:   Extract preload options and return a wrapped callable.

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.worker.worker`](celery.worker.worker.html "previous chapter")

#### Next topic

[`celery.bin.celery`](celery.bin.celery.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.bin.base.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.bin.celery.html "celery.bin.celery") |
* [previous](celery.worker.worker.html "celery.worker.worker") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.bin.base`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
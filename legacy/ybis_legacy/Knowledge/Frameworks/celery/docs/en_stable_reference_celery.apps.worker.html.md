celery.apps.worker — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.apps.beat.html "celery.apps.beat") |
* [previous](celery.beat.html "celery.beat") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.apps.worker`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/reference/celery.apps.worker.html).

# `celery.apps.worker`[¶](#celery-apps-worker "Link to this heading")

Worker command-line program.

This module is the ‘program-version’ of [`celery.worker`](celery.worker.html#module-celery.worker "celery.worker").

It does everything necessary to run that module
as an actual application, like installing signal handlers,
platform tweaks, and so on.

*class* celery.apps.worker.Worker(*app=None*, *hostname=None*, *\*\*kwargs*)[[source]](../_modules/celery/apps/worker.html#Worker)[¶](#celery.apps.worker.Worker "Link to this definition")
:   Worker as a program.

    emit\_banner()[[source]](../_modules/celery/apps/worker.html#Worker.emit_banner)[¶](#celery.apps.worker.Worker.emit_banner "Link to this definition")

    extra\_info()[[source]](../_modules/celery/apps/worker.html#Worker.extra_info)[¶](#celery.apps.worker.Worker.extra_info "Link to this definition")

    install\_platform\_tweaks(*worker*)[[source]](../_modules/celery/apps/worker.html#Worker.install_platform_tweaks)[¶](#celery.apps.worker.Worker.install_platform_tweaks "Link to this definition")
    :   Install platform specific tweaks and workarounds.

    macOS\_proxy\_detection\_workaround()[[source]](../_modules/celery/apps/worker.html#Worker.macOS_proxy_detection_workaround)[¶](#celery.apps.worker.Worker.macOS_proxy_detection_workaround "Link to this definition")
    :   See <https://github.com/celery/celery/issues#issue/161>.

    on\_after\_init(*purge=False*, *no\_color=None*, *redirect\_stdouts=None*, *redirect\_stdouts\_level=None*, *\*\*kwargs*)[[source]](../_modules/celery/apps/worker.html#Worker.on_after_init)[¶](#celery.apps.worker.Worker.on_after_init "Link to this definition")

    on\_before\_init(*quiet=False*, *\*\*kwargs*)[[source]](../_modules/celery/apps/worker.html#Worker.on_before_init)[¶](#celery.apps.worker.Worker.on_before_init "Link to this definition")

    on\_consumer\_ready(*consumer*)[[source]](../_modules/celery/apps/worker.html#Worker.on_consumer_ready)[¶](#celery.apps.worker.Worker.on_consumer_ready "Link to this definition")

    on\_init\_blueprint()[[source]](../_modules/celery/apps/worker.html#Worker.on_init_blueprint)[¶](#celery.apps.worker.Worker.on_init_blueprint "Link to this definition")

    on\_start()[[source]](../_modules/celery/apps/worker.html#Worker.on_start)[¶](#celery.apps.worker.Worker.on_start "Link to this definition")

    purge\_messages()[[source]](../_modules/celery/apps/worker.html#Worker.purge_messages)[¶](#celery.apps.worker.Worker.purge_messages "Link to this definition")

    set\_process\_status(*info*)[[source]](../_modules/celery/apps/worker.html#Worker.set_process_status)[¶](#celery.apps.worker.Worker.set_process_status "Link to this definition")

    setup\_logging(*colorize=None*)[[source]](../_modules/celery/apps/worker.html#Worker.setup_logging)[¶](#celery.apps.worker.Worker.setup_logging "Link to this definition")

    startup\_info(*artlines=True*)[[source]](../_modules/celery/apps/worker.html#Worker.startup_info)[¶](#celery.apps.worker.Worker.startup_info "Link to this definition")

    tasklist(*include\_builtins=True*, *sep='\n'*, *int\_='celery.'*)[[source]](../_modules/celery/apps/worker.html#Worker.tasklist)[¶](#celery.apps.worker.Worker.tasklist "Link to this definition")

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.beat`](celery.beat.html "previous chapter")

#### Next topic

[`celery.apps.beat`](celery.apps.beat.html "next chapter")

### This Page

* [Show Source](../_sources/reference/celery.apps.worker.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](celery.apps.beat.html "celery.apps.beat") |
* [previous](celery.beat.html "celery.beat") |
* [Celery 5.6.2 documentation](../index.html) »
* [API Reference](index.html) »
* `celery.apps.worker`

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.
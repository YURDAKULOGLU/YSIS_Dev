celery.utils.imports — Celery 5.6.2 documentation

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.log.html "celery.utils.log") |
* [previous](celery.utils.timer2.html "celery.utils.timer2") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.imports`

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/internals/reference/celery.utils.imports.html).

# `celery.utils.imports`[¶](#celery-utils-imports "Link to this heading")

Utilities related to importing modules and symbols by name.

*exception* celery.utils.imports.NotAPackage[[source]](../../_modules/celery/utils/imports.html#NotAPackage)[¶](#celery.utils.imports.NotAPackage "Link to this definition")
:   Raised when importing a package, but it’s not a package.

celery.utils.imports.cwd\_in\_path()[[source]](../../_modules/celery/utils/imports.html#cwd_in_path)[¶](#celery.utils.imports.cwd_in_path "Link to this definition")
:   Context adding the current working directory to sys.path.

celery.utils.imports.find\_module(*module*, *path=None*, *imp=None*)[[source]](../../_modules/celery/utils/imports.html#find_module)[¶](#celery.utils.imports.find_module "Link to this definition")
:   Version of `imp.find_module()` supporting dots.

celery.utils.imports.gen\_task\_name(*app*, *name*, *module\_name*)[[source]](../../_modules/celery/utils/imports.html#gen_task_name)[¶](#celery.utils.imports.gen_task_name "Link to this definition")
:   Generate task name from name/module pair.

celery.utils.imports.import\_from\_cwd(*module*, *imp=None*, *package=None*)[[source]](../../_modules/celery/utils/imports.html#import_from_cwd)[¶](#celery.utils.imports.import_from_cwd "Link to this definition")
:   Import module, temporarily including modules in the current directory.

    Modules located in the current directory has
    precedence over modules located in sys.path.

celery.utils.imports.instantiate(*name*, *\*args*, *\*\*kwargs*)[[source]](../../_modules/celery/utils/imports.html#instantiate)[¶](#celery.utils.imports.instantiate "Link to this definition")
:   Instantiate class by name.

    See also

    [`symbol_by_name()`](#celery.utils.imports.symbol_by_name "celery.utils.imports.symbol_by_name").

celery.utils.imports.module\_file(*module*)[[source]](../../_modules/celery/utils/imports.html#module_file)[¶](#celery.utils.imports.module_file "Link to this definition")
:   Return the correct original file name of a module.

celery.utils.imports.qualname(*obj*)[[source]](../../_modules/celery/utils/imports.html#qualname)[¶](#celery.utils.imports.qualname "Link to this definition")
:   Return object name.

celery.utils.imports.reload\_from\_cwd(*module*, *reloader=None*)[[source]](../../_modules/celery/utils/imports.html#reload_from_cwd)[¶](#celery.utils.imports.reload_from_cwd "Link to this definition")
:   Reload module (ensuring that CWD is in sys.path).

celery.utils.imports.symbol\_by\_name(*name*, *aliases=None*, *imp=None*, *package=None*, *sep='.'*, *default=None*, *\*\*kwargs*)[[source]](../../_modules/kombu/utils/imports.html#symbol_by_name)[¶](#celery.utils.imports.symbol_by_name "Link to this definition")
:   Get symbol by qualified name.

    The name should be the full dot-separated path to the class:

    ```
    modulename.ClassName
    ```

    Example:

    ```
    celery.concurrency.processes.TaskPool
                                ^- class name
    ```

    or using ‘:’ to separate module and symbol:

    ```
    celery.concurrency.processes:TaskPool
    ```

    If aliases is provided, a dict containing short name/long name
    mappings, the name is looked up in the aliases first.

    Examples

    ```
    >>> symbol_by_name('celery.concurrency.processes.TaskPool')
    <class 'celery.concurrency.processes.TaskPool'>
    ```

    ```
    >>> symbol_by_name('default', {
    ...     'default': 'celery.concurrency.processes.TaskPool'})
    <class 'celery.concurrency.processes.TaskPool'>
    ```

    # Does not try to look up non-string names.
    >>> from celery.concurrency.processes import TaskPool
    >>> symbol\_by\_name(TaskPool) is TaskPool
    True

[![Logo of Celery](../../_static/celery_512.png)](../../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[`celery.utils.timer2`](celery.utils.timer2.html "previous chapter")

#### Next topic

[`celery.utils.log`](celery.utils.log.html "next chapter")

### This Page

* [Show Source](../../_sources/internals/reference/celery.utils.imports.rst.txt)

### Quick search

### Navigation

* [index](../../genindex.html "General Index")
* [modules](../../py-modindex.html "Python Module Index") |
* [next](celery.utils.log.html "celery.utils.log") |
* [previous](celery.utils.timer2.html "celery.utils.timer2") |
* [Celery 5.6.2 documentation](../../index.html) »
* [Internals](../index.html) »
* [Internal Module Reference](index.html) »
* `celery.utils.imports`

© [Copyright](../../copyright.html) 2009-2023, Ask Solem & contributors.
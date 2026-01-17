Grimp — Grimp 3.14 documentation



* Grimp
* [View page source](_sources/readme.rst.txt)

---

# Grimp[](#grimp "Link to this heading")

[![https://img.shields.io/pypi/v/grimp.svg](https://img.shields.io/pypi/v/grimp.svg)](https://pypi.org/project/grimp)
[![Python versions](https://img.shields.io/pypi/pyversions/grimp.svg)](https://pypi.org/project/grimp/)
[![CI Status](https://github.com/python-grimp/grimp/actions/workflows/main.yml/badge.svg)](https://github.com/python-grimp/grimp/actions?workflow=CI)
[![Codspeed](https://img.shields.io/endpoint?url=https://codspeed.io/badge.json)](https://codspeed.io/python-grimp/grimp?utm_source=badge)
[![BSD license](https://img.shields.io/badge/License-BSD_2--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

Builds a queryable graph of the imports within one or more Python packages.

## Quick start[](#quick-start "Link to this heading")

Install grimp:

```
pip install grimp
```

Install the Python package you wish to analyse:

```
pip install somepackage
```

In Python, build the import graph for the package:

```
>>> import grimp
>>> graph = grimp.build_graph('somepackage')
```

You may now use the graph object to analyse the package. Some examples:

```
>>> graph.find_children('somepackage.foo')
{
    'somepackage.foo.one',
    'somepackage.foo.two',
}

>>> graph.find_descendants('somepackage.foo')
{
    'somepackage.foo.one',
    'somepackage.foo.two',
    'somepackage.foo.two.blue',
    'somepackage.foo.two.green',
}

>>> graph.find_modules_directly_imported_by('somepackage.foo')
{
    'somepackage.bar.one',
}

>>> graph.find_upstream_modules('somepackage.foo')
{
    'somepackage.bar.one',
    'somepackage.baz',
    'somepackage.foobar',
}

>>> graph.find_shortest_chain(importer='somepackage.foobar', imported='somepackage.foo')
(
    'somepackage.foobar',
    'somepackage.baz',
    'somepackage.foo',
)

>>> graph.get_import_details(importer='somepackage.foobar', imported='somepackage.baz'))
[
    {
        'importer': 'somepackage.foobar',
        'imported': 'somepackage.baz',
        'line_number': 5,
        'line_contents': 'from . import baz',
    },
]
```

## External packages[](#external-packages "Link to this heading")

By default, external dependencies will not be included. This can be overridden like so:

```
>>> graph = grimp.build_graph('somepackage', include_external_packages=True)
>>> graph.find_modules_directly_imported_by('somepackage.foo')
{
    'somepackage.bar.one',
    'os',
    'decimal',
    'sqlalchemy',
}
```

## Multiple packages[](#multiple-packages "Link to this heading")

You may analyse multiple root packages. To do this, pass each package name as a positional argument:

```
>>> graph = grimp.build_graph('somepackage', 'anotherpackage')
>>> graph.find_modules_directly_imported_by('somepackage.foo')
{
    'somepackage.bar.one',
    'anotherpackage.baz',
}
```

## Namespace packages[](#namespace-packages "Link to this heading")

Graphs can be built either from [namespace packages](https://docs.python.org/3/glossary.html#term-namespace-package) or from their [portions](https://docs.python.org/3/glossary.html#term-portion).

### What’s a namespace package?[](#what-s-a-namespace-package "Link to this heading")

Namespace packages are a Python feature allows subpackages to be distributed independently, while
still importable under a shared namespace.

This is used by
[the Python client for Google’s Cloud Logging API](https://pypi.org/project/google-cloud-logging/), for example. When installed, it is importable
in Python as `google.cloud.logging`. The parent packages `google` and `google.cloud` are both namespace
packages, while `google.cloud.logging` is known as the ‘portion’. Other portions in the same
namespace can be installed separately, for example `google.cloud.secretmanager`.

Examples:

```
# In this one, the portion is supplied. Neither "google" nor "google.cloud"
# will appear in the graph.
>>> graph = grimp.build_graph("google.cloud.logging")

# In this one, a namespace is supplied.
# Neither "google" nor "google.cloud" will appear in the graph,
# as will other installed packages under the "google" namespace such
# as "google.auth".
>>> graph = grimp.build_graph("google")

# This one supplies a subnamespace of "google" - it will include
# "google.cloud.logging" and "google.cloud.secretmanager" but not "google.auth".
>>> graph = grimp.build_graph("google.cloud")
```
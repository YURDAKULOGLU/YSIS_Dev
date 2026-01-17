openpyxl - A Python library to read/write Excel 2010 xlsx/xlsm files — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](tutorial.html "Tutorial") |
* [openpyxl 3.1.3 documentation](#) »
* openpyxl - A Python library to read/write Excel 2010 xlsx/xlsm files

# openpyxl - A Python library to read/write Excel 2010 xlsx/xlsm files[](#openpyxl-a-python-library-to-read-write-excel-2010-xlsx-xlsm-files "Link to this heading")

Author:
:   Eric Gazoni, Charlie Clark

Source code:
:   <https://foss.heptapod.net/openpyxl/openpyxl>

Issues:
:   <https://foss.heptapod.net/openpyxl/openpyxl/-/issues>

Generated:
:   May 29, 2024

License:
:   MIT/Expat

Version:
:   3.1.3

[![coverage status](https://coveralls.io/repos/bitbucket/openpyxl/openpyxl/badge.svg?branch=default)](https://coveralls.io/bitbucket/openpyxl/openpyxl?branch=default)

## Introduction[](#introduction "Link to this heading")

openpyxl is a Python library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.

It was born from lack of existing library to read/write natively from Python
the Office Open XML format.

All kudos to the PHPExcel team as openpyxl was initially based on PHPExcel.

## Security[](#security "Link to this heading")

By default openpyxl does not guard against quadratic blowup or billion laughs
xml attacks. To guard against these attacks install defusedxml.

## Mailing List[](#mailing-list "Link to this heading")

The user list can be found on <http://groups.google.com/group/openpyxl-users>

Sample code:

```
from openpyxl import Workbook
wb = Workbook()

# grab the active worksheet
ws = wb.active

# Data can be assigned directly to cells
ws['A1'] = 42

# Rows can also be appended
ws.append([1, 2, 3])

# Python types will automatically be converted
import datetime
ws['A2'] = datetime.datetime.now()

# Save the file
wb.save("sample.xlsx")
```

## Documentation[](#documentation "Link to this heading")

The documentation is at: <https://openpyxl.readthedocs.io>

* installation methods
* code examples
* instructions for contributing

Release notes: <https://openpyxl.readthedocs.io/en/stable/changes.html>

## Support[](#support "Link to this heading")

This is an open source project, maintained by volunteers in their spare time.
This may well mean that particular features or functions that you would like
are missing. But things don’t have to stay that way. You can contribute the
project [Development](development.html) yourself or contract a developer for particular
features.

Professional support for openpyxl is available from
[Clark Consulting & Research](http://www.clark-consulting.eu/) and
[Adimian](http://www.adimian.com). Donations to the project to support further
development and maintenance are welcome.

Bug reports and feature requests should be submitted using the [issue tracker](https://foss.heptapod.net/openpyxl/openpyxl/-/issues). Please provide a full
traceback of any error you see and if possible a sample file. If for reasons
of confidentiality you are unable to make a file publicly available then
contact of one the developers.

The repository is being provided by [Octobus](https://octobus.net/) and
[Clever Cloud](https://clever-cloud.com/).

## How to Contribute[](#how-to-contribute "Link to this heading")

Any help will be greatly appreciated, just follow those steps:

> 1.
> Please join the group and create a branch (<https://foss.heptapod.net/openpyxl/openpyxl/>) and
> follow the [Merge Request Start Guide](https://heptapod.net/pages/quick-start-guide.html).
> for each independent feature, don’t try to fix all problems at the same
> time, it’s easier for those who will review and merge your changes ;-)
>
> 2.
> Hack hack hack
>
> 3.
> Don’t forget to add unit tests for your changes! (YES, even if it’s a
> one-liner, changes without tests will **not** be accepted.) There are plenty
> of examples in the source if you lack know-how or inspiration.
>
> 4.
> If you added a whole new feature, or just improved something, you can
> be proud of it, so add yourself to the AUTHORS file :-)
>
> 5.
> Let people know about the shiny thing you just implemented, update the
> docs!
>
> 6.
> When it’s done, just issue a pull request (click on the large “pull
> request” button on *your* repository) and wait for your code to be
> reviewed, and, if you followed all theses steps, merged into the main
> repository.

For further information see [Development](development.html)

### Other ways to help[](#other-ways-to-help "Link to this heading")

There are several ways to contribute, even if you can’t code (or can’t code well):

> * triaging bugs on the bug tracker: closing bugs that have already been
>   closed, are not relevant, cannot be reproduced, …
> * updating documentation in virtually every area: many large features have
>   been added (mainly about charts and images at the moment) but without any
>   documentation, it’s pretty hard to do anything with it
> * proposing compatibility fixes for different versions of Python: we support
>   3.6, 3.7, 3.8 and 3.9.

## API Documentation[](#api-documentation "Link to this heading")

### Key Classes[](#key-classes "Link to this heading")

* [`openpyxl.workbook.workbook.Workbook`](api/openpyxl.workbook.workbook.html#openpyxl.workbook.workbook.Workbook "openpyxl.workbook.workbook.Workbook")
* [`openpyxl.worksheet.worksheet.Worksheet`](api/openpyxl.worksheet.worksheet.html#openpyxl.worksheet.worksheet.Worksheet "openpyxl.worksheet.worksheet.Worksheet")
* [`openpyxl.cell.cell.Cell`](api/openpyxl.cell.cell.html#openpyxl.cell.cell.Cell "openpyxl.cell.cell.Cell")

# Indices and tables[](#indices-and-tables "Link to this heading")

* [Index](genindex.html)
* [Module Index](py-modindex.html)
* [Search Page](search.html)

[![Logo](_static/logo.png)](#)

### [Table of Contents](#)

* [openpyxl - A Python library to read/write Excel 2010 xlsx/xlsm files](#)
  + [Introduction](#introduction)
  + [Security](#security)
  + [Mailing List](#mailing-list)
  + [Documentation](#documentation)
  + [Support](#support)
  + [How to Contribute](#how-to-contribute)
    - [Other ways to help](#other-ways-to-help)
  + [API Documentation](#api-documentation)
    - [Key Classes](#key-classes)
* [Indices and tables](#indices-and-tables)

#### Next topic

[Tutorial](tutorial.html "next chapter")

### This Page

* [Show Source](_sources/index.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](tutorial.html "Tutorial") |
* [openpyxl 3.1.3 documentation](#) »
* openpyxl - A Python library to read/write Excel 2010 xlsx/xlsm files

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.
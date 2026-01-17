Performance — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](development.html "Development") |
* [previous](optimized.html "Optimised Modes") |
* [openpyxl 3.1.3 documentation](index.html) »
* Performance

# Performance[](#performance "Link to this heading")

openpyxl attempts to balance functionality and performance. Where in doubt,
we have focused on functionality over optimisation: performance tweaks are
easier once an API has been established. Memory use is fairly high in
comparison with other libraries and applications and is approximately 50
times the original file size, e.g. 2.5 GB for a 50 MB Excel file. As many use
cases involve either only reading or writing files, the [Optimised Modes](optimized.html)
modes mean this is less of a problem.

## Benchmarks[](#benchmarks "Link to this heading")

All benchmarks are synthetic and extremely dependent upon the hardware but
they can nevertheless give an indication.

### Write Performance[](#write-performance "Link to this heading")

The [benchmark code](https://foss.heptapod.net/openpyxl/openpyxl/-/snippets/66)
can be adjusted to use more sheets and adjust the proportion of data that is
strings. Because the version of Python being used can also significantly
affect performance, a [driver script](https://foss.heptapod.net/openpyxl/openpyxl/-/snippets/67)
can also be used to test with different Python versions with a tox
environment.

Performance is compared with the excellent alternative library xlsxwriter

```
Versions:
python: 3.6.9
openpyxl: 3.0.1
xlsxwriter: 1.2.5

Dimensions:
    Rows = 1000
    Cols = 50
    Sheets = 1
    Proportion text = 0.10

Times:
    xlsxwriter            :   0.59
    xlsxwriter (optimised):   0.54
    openpyxl              :   0.73
    openpyxl (optimised)  :   0.61


Versions:
python: 3.7.5
openpyxl: 3.0.1
xlsxwriter: 1.2.5

Dimensions:
    Rows = 1000
    Cols = 50
    Sheets = 1
    Proportion text = 0.10

Times:
    xlsxwriter            :   0.65
    xlsxwriter (optimised):   0.53
    openpyxl              :   0.70
    openpyxl (optimised)  :   0.63


Versions:
python: 3.8.0
openpyxl: 3.0.1
xlsxwriter: 1.2.5

Dimensions:
    Rows = 1000
    Cols = 50
    Sheets = 1
    Proportion text = 0.10

Times:
    xlsxwriter            :   0.54
    xlsxwriter (optimised):   0.50
    openpyxl              :   1.10
    openpyxl (optimised)  :   0.57
```

### Read Performance[](#read-performance "Link to this heading")

Performance is measured using a file provided with a previous [bug report](https://bitbucket.org/openpyxl/openpyxl/issues/494/) and compared with the
older xlrd library. xlrd is primarily for the older BIFF file format of .XLS
files but it does have limited support for XLSX.

The code for the [benchmark](https://foss.heptapod.net/openpyxl/openpyxl/-/snippets/68) shows the importance of
choosing the right options when working with a file. In this case disabling
external links stops openpyxl opening cached copies of the linked worksheets.

One major difference between the libraries is that openpyxl’s read-only mode
opens a workbook almost immediately making it suitable for multiple
processes, this also reduces memory use significantly. xlrd does also not
automatically convert dates and times into Python datetimes, though it does
annotate cells accordingly but to do this in client code significantly
reduces performance.

```
Versions:
python: 3.6.9
xlread: 1.2.0
openpyxl: 3.0.1

openpyxl, read-only
    Workbook loaded 1.14s
    OptimizationData 23.17s
    Output Model 0.00s
    >>DATA>> 0.00s
    Store days 0% 23.92s
    Store days 100% 17.35s
    Total time 65.59s
    0 cells in total

Versions:
python: 3.7.5
xlread: 1.2.0
openpyxl: 3.0.1

openpyxl, read-only
    Workbook loaded 0.98s
    OptimizationData 21.35s
    Output Model 0.00s
    >>DATA>> 0.00s
    Store days 0% 20.70s
    Store days 100% 16.16s
    Total time 59.19s
    0 cells in total

Versions:
python: 3.8.0
xlread: 1.2.0
openpyxl: 3.0.1

openpyxl, read-only
    Workbook loaded 0.90s
    OptimizationData 19.58s
    Output Model 0.00s
    >>DATA>> 0.00s
    Store days 0% 19.35s
    Store days 100% 15.02s
    Total time 54.85s
    0 cells in total
```

### Parallelisation[](#parallelisation "Link to this heading")

Reading worksheets is fairly CPU-intensive which limits any benefits to be
gained by parallelisation. However, if you are mainly interested in dumping
the contents of a workbook then you can use openpyxl’s read-only mode and
open multiple instances of a workbook and take advantage of multiple CPUs.

[Sample code](https://foss.heptapod.net/openpyxl/openpyxl/-/snippets/69) using the
same source file as for read performance shows that performance scales
reasonably with only a slight overhead due to creating additional Python
processes.

```
Parallised Read
    Workbook loaded 1.12s
    >>DATA>> 2.27s
    Output Model 2.30s
    Store days 100% 37.18s
    OptimizationData 44.09s
    Store days 0% 45.60s
    Total time 46.76s
```

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Performance](#)
  + [Benchmarks](#benchmarks)
    - [Write Performance](#write-performance)
    - [Read Performance](#read-performance)
    - [Parallelisation](#parallelisation)

#### Previous topic

[Optimised Modes](optimized.html "previous chapter")

#### Next topic

[Development](development.html "next chapter")

### This Page

* [Show Source](_sources/performance.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](development.html "Development") |
* [previous](optimized.html "Optimised Modes") |
* [openpyxl 3.1.3 documentation](index.html) »
* Performance

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.
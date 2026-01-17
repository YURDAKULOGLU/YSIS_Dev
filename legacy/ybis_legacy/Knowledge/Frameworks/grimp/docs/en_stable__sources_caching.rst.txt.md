=======
Caching
=======
Grimp uses a file-based cache to speed up subsequent builds of the graph::
>>> build\_graph("somepackage", "anotherpackage") # Writes to a cache for the first time.
...
>>> build\_graph("somepackage", "anotherpackage") # Second time it's run, it's much quicker.
What is cached?
---------------
Grimp caches the imports discovered through static analysis of the packages when it builds a graph.
It does not cache the results of any methods called on a graph, e.g. ``find\_downstream\_modules``.
Separate caches of imports are created depending the arguments passed to ``build\_graph``. For example,
the following invocations will each have a separate cache and will not be able to make use of each
other's work:
- ``build\_graph("mypackage")``
- ``build\_graph("mypackage", "anotherpackage")``
- ``build\_graph("mypackage", "anotherpackage", include\_external\_packages=True)``
- ``build\_graph("mypackage", "anotherpackage", exclude\_type\_checking\_imports=True)``
Grimp can make use of cached results even if some of the modules change. For example,
if ``mypackage.foo`` is changed, but all the other modules within ``mypackage`` are left
untouched, Grimp will only need to rescan ``mypackage.foo``. This can have a significant
speed up effect when analysing large codebases in which only a small subset of files change
from run to run.
Grimp determines whether or not it needs to rescan a file based on its last modified time.
This makes it very effective for local development, but is less effective in environments
that reinstall the package under analysis between each build of the graph (e.g. on a
continuous integration server).
Location of the cache
---------------------
Cache files are written, by default, to a ``.grimp\_cache`` directory
in the current working directory. This directory can be changed by passing
``cache\_dir`` to the ``build\_graph`` function, e.g.::
graph = grimp.build\_graph("mypackage", cache\_dir="/path/to/cache")
Disabling caching
-----------------
To skip using (and writing to) the cache, pass ``cache\_dir=None`` to ``build\_graph``::
graph = grimp.build\_graph("mypackage", cache\_dir=None)
Concurrency
-----------
Caching isn't currently concurrency-safe. Specifically, if you have two concurrent processes writing to the same cache
files, you might experience incorrect behaviour.
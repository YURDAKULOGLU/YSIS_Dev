Changelog — Grimp 3.14 documentation



* Changelog
* [View page source](_sources/changelog.rst.txt)

---

# Changelog[](#changelog "Link to this heading")

## 3.14 (2025-12-10)[](#id1 "Link to this heading")

* Support building graph from namespace packages, not just their portions.
* Bugfix: support Python 3.14 syntax such as t-strings as syntax errors.
  (<https://github.com/python-grimp/grimp/issues/268>)
* Drop support for Python 3.9.

## 3.13 (2025-10-29)[](#id2 "Link to this heading")

* Add nominate\_cycle\_breakers method.

## 3.12 (2025-10-09)[](#id3 "Link to this heading")

* Officially support Python 3.14.
* Improve contribution / CI tooling using Just and UV.

## 3.11 (2025-09-01)[](#id4 "Link to this heading")

* Speed up graph building by switching from Python multiprocessing to Rust-based multithreading
  for import scanning.

## (yanked) 3.10 (2025-08-15)[](#yanked-3-10-2025-08-15 "Link to this heading")

This release was yanked due to poor performance when building very large graphs.

* Add closed layers to layer contract.
* Rename default repository branch to ‘main’.
* Optimise find\_shortest\_chains query.

## 3.9 (2025-05-05)[](#id5 "Link to this heading")

* Use Rust instead of Python’s built-in ast module for import parsing.

## 3.8.2 (2025-04-24)[](#id6 "Link to this heading")

* Provide more control of multiprocessing via `GRIMP_MIN_MULTIPROCESSING_MODULES`
  environment variable.

## 3.8.1 (2025-04-23)[](#id7 "Link to this heading")

* Use joblib instead of multiprocessing for CPU parallelism. Fixes <https://github.com/python-grimp/grimp/issues/208>.

## 3.8 (2025-04-11)[](#id8 "Link to this heading")

* Accelerate import scanning via CPU parallelism (multiprocessing).

## 3.7.1 (2025-03-12)[](#id9 "Link to this heading")

* Fixed handling of within-descendant-imports when squashing modules (see [Issue 195](https://github.com/python-grimp/grimp/issues/195)).

## 3.7 (2025-03-07)[](#id10 "Link to this heading")

* Added find\_matching\_modules and find\_matching\_direct\_imports methods.
* Added as\_packages option to the find\_shortest\_chain method.

## 3.6 (2025-02-07)[](#id11 "Link to this heading")

* Reimplement the graph in Rust. This is a substantial rewrite that, mostly, significantly
  improves performance, but there may be certain operations that are slower than before.

## 3.5 (2024-10-08)[](#id12 "Link to this heading")

* Added as\_packages option to the find\_shortest\_chains method.
* Include 3.13 wheel in release.
* Drop support for Python 3.8.

## 3.4.1 (2024-07-12)[](#id13 "Link to this heading")

* Officially support Python 3.13.

## 3.4 (2024-07-09)[](#id14 "Link to this heading")

* Speed up adding and removing modules.

## 3.3 (2024-06-13)[](#id15 "Link to this heading")

* Upgrade PyO3 to 0.21.
* Follow symbolic links while walking through module files.
* Speed up find\_illegal\_dependencies\_for\_layers by using thread concurrency.

## 3.2 (2024-1-8)[](#id16 "Link to this heading")

* Allow configuring sibling layer independence.
* Fix bug where a warning would be logged if a non-Python file with multiple dots
  in the filename was encountered.
* Formally add support for Python 3.12.

## 3.1 (2023-10-13)[](#id17 "Link to this heading")

* Add exclude\_type\_checking\_imports argument to build\_graph.

## 3.0 (2023-8-18)[](#id18 "Link to this heading")

* Stable release of functionality from 3.0b1-3.

## 3.0b3 (2023-8-17)[](#b3-2023-8-17 "Link to this heading")

* Support for independent layers in find\_illegal\_dependencies\_for\_layers.

## 3.0b1, 3.0b2 (2023-8-15)[](#b1-3-0b2-2023-8-15 "Link to this heading")

* Switch to pyproject.toml.
* Rename upstream/downstream in find\_illegal\_dependencies\_for\_layers to importer/imported.
  The original names were accidentally used in reverse; the new names have less potential for confusion.
* Use Rust extension module for find\_illegal\_dependencies\_for\_layers.

## 2.5 (2023-7-6)[](#id19 "Link to this heading")

* Log cache activity.
* Drop support for Python 3.7.
* Add find\_illegal\_dependencies\_for\_layers method.

## 2.4 (2023-5-5)[](#id20 "Link to this heading")

* Change cache filename scheme to use a hash.
* Ignore modules with dots in the filename.

## 2.3 (2023-3-3)[](#id21 "Link to this heading")

* Add caching.

## 2.2 (2023-1-5)[](#id22 "Link to this heading")

* Annotate get\_import\_details return value with a DetailedImport.

## 2.1 (2022-12-2)[](#id23 "Link to this heading")

* Officially support Python 3.11.

## 2.0 (2022-9-27)[](#id24 "Link to this heading")

* Significantly speed up graph copying.
* Remove find\_all\_simple\_chains method.
* No longer use a networkx graph internally.
* Fix bug where import details remained stored in the graph after removing modules or imports.

## 1.3 (2022-8-15)[](#id25 "Link to this heading")

* Officially support Python 3.9 and 3.10.
* Drop support for Python 3.6.
* Support namespaced packages.

## 1.2.3 (2021-1-19)[](#id26 "Link to this heading")

* Raise custom exception (NamespacePackageEncountered) if code under analysis appears to be a namespace package.

## 1.2.2 (2020-6-29)[](#id27 "Link to this heading")

* Raise custom exception (SourceSyntaxError) if code under analysis contains syntax error.

## 1.2.1 (2020-3-16)[](#id28 "Link to this heading")

* Better handling of source code containing non-ascii compatible characters

## 1.2 (2019-11-27)[](#id29 "Link to this heading")

* Significantly increase the speed of building the graph.

## 1.1 (2019-11-18)[](#id30 "Link to this heading")

* Clarify behaviour of get\_import\_details.
* Add module\_is\_squashed method.
* Add squash\_module method.
* Add find\_all\_simple\_chains method.

## 1.0 (2019-10-17)[](#id31 "Link to this heading")

* Officially support Python 3.8.

## 1.0b13 (2019-9-25)[](#b13-2019-9-25 "Link to this heading")

* Support multiple root packages.

## 1.0b12 (2019-6-12)[](#b12-2019-6-12 "Link to this heading")

* Add find\_shortest\_chains method.

## 1.0b11 (2019-5-18)[](#b11-2019-5-18 "Link to this heading")

* Add remove\_module method.

## 1.0b10 (2019-5-15)[](#b10-2019-5-15 "Link to this heading")

* Fix Windows incompatibility.

## 1.0b9 (2019-4-16)[](#b9-2019-4-16 "Link to this heading")

* Fix bug with calling importlib.util.find\_spec.

## 1.0b8 (2019-2-1)[](#b8-2019-2-1 "Link to this heading")

* Add as\_packages parameter to direct\_import\_exists.

## 1.0b7 (2019-1-21)[](#b7-2019-1-21 "Link to this heading")

* Add count\_imports method.

## 1.0b6 (2019-1-20)[](#b6-2019-1-20 "Link to this heading")

* Support building the graph with external packages.

## 1.0b5 (2019-1-12)[](#b5-2019-1-12 "Link to this heading")

* Rename get\_shortest\_path to get\_shortest\_chain.
* Rename path\_exists to chain\_exists.
* Rename and reorder the kwargs for get\_shortest\_chain and chain\_exists.
* Raise ValueError if modules with shared descendants are passed to chain\_exists if as\_packages=True.

## 1.0b4 (2019-1-7)[](#b4-2019-1-7 "Link to this heading")

* Improve repr of ImportGraph.
* Fix bug with find\_shortest\_path using upstream/downstream the wrong way around.

## 1.0b3 (2018-12-16)[](#b3-2018-12-16 "Link to this heading")

* Fix bug with analysing relative imports from within \_\_init\_\_.py files.
* Stop skipping analysing packages called `migrations`.
* Deal with invalid imports by warning instead of raising an exception.
* Rename NetworkXBackedImportGraph to ImportGraph.

## 1.0b2 (2018-12-12)[](#b2-2018-12-12 "Link to this heading")

* Fix PyPI readme rendering.

## 1.0b1 (2018-12-08)[](#b1-2018-12-08 "Link to this heading")

* Implement core functionality.

## 0.0.1 (2018-11-05)[](#id32 "Link to this heading")

* Release blank project on PyPI.
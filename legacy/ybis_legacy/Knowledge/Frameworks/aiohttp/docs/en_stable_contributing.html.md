Contributing — aiohttp 3.13.3 documentation

# Contributing[¶](#contributing "Link to this heading")

([Instructions for aiohttp admins](contributing-admins.html))

## Instructions for contributors[¶](#instructions-for-contributors "Link to this heading")

In order to make a clone of the [GitHub](https://github.com/aio-libs/aiohttp) repo: open the link and press the “Fork” button on the upper-right menu of the web page.

I hope everybody knows how to work with git and github nowadays :)

Workflow is pretty straightforward:

> 0. Make sure you are reading the latest version of this document.
>    It can be found in the [GitHub](https://github.com/aio-libs/aiohttp) repo in the `docs` subdirectory.
> 1. Clone the [GitHub](https://github.com/aio-libs/aiohttp) repo using the `--recurse-submodules` argument
> 2. Setup your machine with the required development environment
> 3. Make a change
> 4. Make sure all tests passed
> 5. Add a file into the `CHANGES` folder (see [Changelog update](#changelog-update) for how).
> 6. Commit changes to your own aiohttp clone
> 7. Make a pull request from the github page of your clone against the master branch
> 8. Optionally make backport Pull Request(s) for landing a bug fix into released aiohttp versions.

Note

The project uses *Squash-and-Merge* strategy for *GitHub Merge* button.

Basically it means that there is **no need to rebase** a Pull Request against
*master* branch. Just `git merge` *master* into your working copy (a fork) if
needed. The Pull Request is automatically squashed into the single commit
once the PR is accepted.

Note

GitHub issue and pull request threads are automatically locked when there has
not been any recent activity for one year. Please open a [new issue](https://github.com/aio-libs/aiohttp/issues/new) for related bugs.

If you feel like there are important points in the locked discussions,
please include those excerpts into that new issue.

## Preconditions for running aiohttp test suite[¶](#preconditions-for-running-aiohttp-test-suite "Link to this heading")

We expect you to use a python virtual environment to run our tests.

There are several ways to make a virtual environment.

If you like to use *virtualenv* please run:

```
$ cd aiohttp
$ virtualenv --python=`which python3` venv
$ . venv/bin/activate
```

For standard python *venv*:

```
$ cd aiohttp
$ python3 -m venv venv
$ . venv/bin/activate
```

For *virtualenvwrapper*:

```
$ cd aiohttp
$ mkvirtualenv --python=`which python3` aiohttp
```

There are other tools like *pyvenv* but you know the rule of thumb now: create a python3 virtual environment and activate it.

After that please install libraries required for development:

```
$ pip install -r requirements/dev.txt
```

Note

For now, the development tooling depends on `make` and assumes an Unix OS If you wish to contribute to aiohttp from a Windows machine, the easiest way is probably to [configure the WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) so you can use the same instructions. If it’s not possible for you or if it doesn’t work, please contact us so we can find a solution together.

Install pre-commit hooks:

```
$ pre-commit install
```

Warning

If you plan to use temporary `print()`, `pdb` or `ipdb` within the test suite, execute it with `-s`:

```
$ pytest tests -s
```

in order to run the tests without output capturing.

Congratulations, you are ready to run the test suite!

## LLHTTP[¶](#llhttp "Link to this heading")

When building aiohttp from source, there is a pure Python parser used by default.
For better performance, you may want to build the higher performance C parser.

To build this `llhttp` parser, first get/update the submodules (to update to a
newer release, add `--remote`):

```
git submodule update --init --recursive
```

Then build `llhttp`:

```
cd vendor/llhttp/
npm ci
make
```

Then build our parser:

```
cd -
make cythonize
```

Then you can build or install it with `python -m build` or `pip install -e .`

## Run autoformatter[¶](#run-autoformatter "Link to this heading")

The project uses [black](https://pypi.python.org/pypi/black) + [isort](https://pypi.python.org/pypi/isort) formatters to keep the source code style.
Please run make fmt after every change before starting tests.

> ```
> $ make fmt
> ```

## Run aiohttp test suite[¶](#run-aiohttp-test-suite "Link to this heading")

After all the preconditions are met you can run tests typing the next
command:

```
$ make test
```

The command at first will run the *linters* (sorry, we don’t accept
pull requests with pyflakes, black, isort, or mypy errors).

On *lint* success the tests will be run.

Please take a look on the produced output.

Any extra texts (print statements and so on) should be removed.

Note

If you see that CI build is failing on a specific Python version and
you don’t have this version on your computer, you can use the helper to
run it (only if you have docker):

```
make test-<python-version>[-no-extensions]
```

For example, if you want to run tests for python3.10
without extensions, you can run this command:

```
make test-3.10-no-extensions
```

## Code coverage[¶](#code-coverage "Link to this heading")

We use *codecov.io* as an indispensable tool for analyzing our coverage
results. Visit <https://codecov.io/gh/aio-libs/aiohttp> to see coverage
reports for the master branch, history, pull requests etc.

We’ll use an example from a real PR to demonstrate how we use this.
Once the tests run in a PR, you’ll see a comment posted by *codecov*.
The most important thing to check here is whether there are any new
missed or partial lines in the report:

![_images/contributing-cov-comment.svg](_images/contributing-cov-comment.svg)

Here, the PR has introduced 1 miss and 2 partials. Now we
click the link in the comment header to open the full report:

![Codecov report](_images/contributing-cov-header.svg)

Now, if we look through the diff under ‘Files changed’ we find one of
our partials:

![A while loop with partial coverage.](_images/contributing-cov-partial.svg)

In this case, the while loop is never skipped in our tests. This is
probably not worth writing a test for (and may be a situation that is
impossible to trigger anyway), so we leave this alone.

We’re still missing a partial and a miss, so we switch to the
‘Indirect changes’ tab and take a look through the diff there. This
time we find the remaining 2 lines:

![An if statement that isn't covered anymore.](_images/contributing-cov-miss.svg)

After reviewing the PR, we find that this code is no longer needed as
the changes mean that this method will never be called under those
conditions. Thanks to this report, we were able to remove some
redundant code from a performance-critical part of our codebase (this
check would have been run, probably multiple times, for every single
incoming request).

Tip

Sometimes the diff on *codecov.io* doesn’t make sense. This is usually
caused by the branch being out of sync with master. Try merging
master into the branch and it will likely fix the issue. Failing
that, try checking coverage locally as described in the next section.

## Other tools[¶](#other-tools "Link to this heading")

The browser extension <https://docs.codecov.io/docs/browser-extension>
is also a useful tool for analyzing the coverage directly from *Files
Changed* tab on the *GitHub Pull Request* review page.

You can also produce coverage reports locally with `make cov-dev`
or just adding `--cov-report=html` to `pytest`.

This will run the test suite and collect coverage information. Once
finished, coverage results can be view by opening:
`` `console
$ python -m webbrowser -n file://"$(pwd)"/htmlcov/index.html
` ``

## Documentation[¶](#documentation "Link to this heading")

We encourage documentation improvements.

Please before making a Pull Request about documentation changes run:

```
$ make doc
```

Once it finishes it will output the index html page
`open file:///.../aiohttp/docs/_build/html/index.html`.

Go to the link and make sure your doc changes looks good.

## Spell checking[¶](#spell-checking "Link to this heading")

We use `pyenchant` and `sphinxcontrib-spelling` for running spell
checker for documentation:

```
$ make doc-spelling
```

Unfortunately there are problems with running spell checker on MacOS X.

To run spell checker on Linux box you should install it first:

```
$ sudo apt-get install enchant
$ pip install sphinxcontrib-spelling
```

## Preparing a pull request[¶](#preparing-a-pull-request "Link to this heading")

When making a pull request, please include a short summary of the changes
and a reference to any issue tickets that the PR is intended to solve.
All PRs with code changes should include tests. All changes should
include a changelog entry.

## Changelog update[¶](#changelog-update "Link to this heading")

### Adding change notes with your PRs[¶](#adding-change-notes-with-your-prs "Link to this heading")

It is very important to maintain a log for news of how
updating to the new version of the software will affect
end-users. This is why we enforce collection of the change
fragment files in pull requests as per [Towncrier philosophy](https://towncrier.readthedocs.io/en/stable/#philosophy).

The idea is that when somebody makes a change, they must record
the bits that would affect end-users, only including information
that would be useful to them. Then, when the maintainers publish
a new release, they’ll automatically use these records to compose
a change log for the respective version. It is important to
understand that including unnecessary low-level implementation
related details generates noise that is not particularly useful
to the end-users most of the time. And so such details should be
recorded in the Git history rather than a changelog.

### Alright! So how to add a news fragment?[¶](#alright-so-how-to-add-a-news-fragment "Link to this heading")

`aiohttp` uses [towncrier](https://pypi.org/project/towncrier/)
for changelog management.
To submit a change note about your PR, add a text file into the
`CHANGES/` folder. It should contain an
explanation of what applying this PR will change in the way
end-users interact with the project. One sentence is usually
enough but feel free to add as many details as you feel necessary
for the users to understand what it means.

**Use the past tense** for the text in your fragment because,
combined with others, it will be a part of the “news digest”
telling the readers **what changed** in a specific version of
the library *since the previous version*. You should also use
*reStructuredText* syntax for highlighting code (inline or block),
linking parts of the docs or external sites.
However, you do not need to reference the issue or PR numbers here
as *towncrier* will automatically add a reference to all of the
affected issues when rendering the news file.
If you wish to sign your change, feel free to add `` -- by
:user:`github-username` `` at the end (replace `github-username`
with your own!).

Finally, name your file following the convention that Towncrier
understands: it should start with the number of an issue or a
PR followed by a dot, then add a patch type, like `feature`,
`doc`, `contrib` etc., and add `.rst` as a suffix. If you
need to add more than one fragment, you may add an optional
sequence number (delimited with another period) between the type
and the suffix.

In general the name will follow `<pr_number>.<category>.rst` pattern,
where the categories are:

* `bugfix`: A bug fix for something we deemed an improper undesired
  behavior that got corrected in the release to match pre-agreed
  expectations.
* `feature`: A new behavior, public APIs. That sort of stuff.
* `deprecation`: A declaration of future API removals and breaking
  changes in behavior.
* `breaking`: When something public gets removed in a breaking way.
  Could be deprecated in an earlier release.
* `doc`: Notable updates to the documentation structure or build
  process.
* `packaging`: Notes for downstreams about unobvious side effects
  and tooling. Changes in the test invocation considerations and
  runtime assumptions.
* `contrib`: Stuff that affects the contributor experience. e.g.
  Running tests, building the docs, setting up the development
  environment.
* `misc`: Changes that are hard to assign to any of the above
  categories.

A pull request may have more than one of these components, for example
a code change may introduce a new feature that deprecates an old
feature, in which case two fragments should be added. It is not
necessary to make a separate documentation fragment for documentation
changes accompanying the relevant code changes.

### Examples for adding changelog entries to your Pull Requests[¶](#examples-for-adding-changelog-entries-to-your-pull-requests "Link to this heading")

File `CHANGES/6045.doc.1.rst`:

```
Added a ``:user:`` role to Sphinx config -- by :user:`webknjaz`.
```

File `CHANGES/8074.bugfix.rst`:

```
Fixed an unhandled exception in the Python HTTP parser on header
lines starting with a colon -- by :user:`pajod`.

Invalid request lines with anything but a dot between the HTTP
major and minor version are now rejected. Invalid header field
names containing question mark or slash are now rejected. Such
requests are incompatible with :rfc:`9110#section-5.6.2` and are
not known to be of any legitimate use.
```

File `CHANGES/4594.feature.rst`:

```
Added support for ``ETag`` to :py:class:`~aiohttp.web.FileResponse`
-- by :user:`greshilov`, :user:`serhiy-storchaka` and
:user:`asvetlov`.
```

Tip

See `pyproject.toml` for all available categories
(`tool.towncrier.type`).

## Making a pull request[¶](#making-a-pull-request "Link to this heading")

After finishing all steps make a [GitHub](https://github.com/aio-libs/aiohttp) Pull Request with *master* base branch.

## Backporting[¶](#backporting "Link to this heading")

All Pull Requests are created against *master* git branch.

If the Pull Request is not a new functionality but bug fixing
*backport* to maintenance branch would be desirable.

*aiohttp* project committer may ask for making a *backport* of the PR
into maintained branch(es), in this case he or she adds a github label
like *needs backport to 3.1*.

*Backporting* is performed *after* main PR merging into master.
:   Please do the following steps:

1. Find *Pull Request’s commit* for cherry-picking.

   *aiohttp* does *squashing* PRs on merging, so open your PR page on
   github and scroll down to message like `asvetlov merged commit
   f7b8921 into master 9 days ago`. `f7b8921` is the required commit number.
2. Run [cherry\_picker](https://github.com/python/core-workflow/tree/master/cherry_picker)
   tool for making backport PR (the tool is already pre-installed from
   `./requirements/dev.txt`), e.g. `cherry_picker f7b8921 3.1`.
3. In case of conflicts fix them and continue cherry-picking by
   `cherry_picker --continue`.

   `cherry_picker --abort` stops the process.

   `cherry_picker --status` shows current cherry-picking status
   (like `git status`)
4. After all conflicts are done the tool opens a New Pull Request page
   in a browser with pre-filed information. Create a backport Pull
   Request and wait for review/merging.
5. *aiohttp* *committer* should remove *backport Git label* after
   merging the backport.

## How to become an aiohttp committer[¶](#how-to-become-an-aiohttp-committer "Link to this heading")

Contribute!

The easiest way is providing Pull Requests for issues in our bug
tracker. But if you have a great idea for the library improvement
– please make an issue and Pull Request.

The rules for committers are simple:

1. No wild commits! Everything should go through PRs.
2. Take a part in reviews. It’s very important part of maintainer’s activity.
3. Pickup issues created by others, especially if they are simple.
4. Keep test suite comprehensive. In practice it means leveling up
   coverage. 97% is not bad but we wish to have 100% someday. Well, 99%
   is good target too.
5. Don’t hesitate to improve our docs. Documentation is a very important
   thing, it’s the key for project success. The documentation should
   not only cover our public API but help newbies to start using the
   project and shed a light on non-obvious gotchas.

After positive answer aiohttp committer creates an issue on github
with the proposal for nomination. If the proposal will collect only
positive votes and no strong objection – you’ll be a new member in
our team.

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
* [Utilities](utilities.html)
* [FAQ](faq.html)
* [Miscellaneous](misc.html)
* [Who uses aiohttp?](external.html)
* [Contributing](#)
  + [Instructions for contributors](#instructions-for-contributors)
  + [Preconditions for running aiohttp test suite](#preconditions-for-running-aiohttp-test-suite)
  + [LLHTTP](#llhttp)
  + [Run autoformatter](#run-autoformatter)
  + [Run aiohttp test suite](#run-aiohttp-test-suite)
  + [Code coverage](#code-coverage)
  + [Other tools](#other-tools)
  + [Documentation](#documentation)
  + [Spell checking](#spell-checking)
  + [Preparing a pull request](#preparing-a-pull-request)
  + [Changelog update](#changelog-update)
  + [Making a pull request](#making-a-pull-request)
  + [Backporting](#backporting)
  + [How to become an aiohttp committer](#how-to-become-an-aiohttp-committer)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/contributing.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
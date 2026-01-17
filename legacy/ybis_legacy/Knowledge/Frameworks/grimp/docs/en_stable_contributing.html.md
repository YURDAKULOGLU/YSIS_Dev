Contributing — Grimp 3.14 documentation



* Contributing
* [View page source](_sources/contributing.rst.txt)

---

# Contributing[](#contributing "Link to this heading")

We welcome contributions to Grimp.

## Bug reports[](#bug-reports "Link to this heading")

When [reporting a bug](https://github.com/python-grimp/grimp/issues) please include:

> * Your operating system name and version.
> * Any details about your local setup that might be helpful in troubleshooting.
> * Detailed steps to reproduce the bug.

## Feature requests and feedback[](#feature-requests-and-feedback "Link to this heading")

The best way to send feedback is to file an issue at <https://github.com/python-grimp/grimp/issues>.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible.
* Remember that this is a volunteer-driven project.

## Submitting pull requests[](#submitting-pull-requests "Link to this heading")

Before spending time working on a pull request, we highly recommend filing a Github issue and engaging with the project maintainer (David Seddon) to align on the direction you’re planning to take. This can save a lot of your precious time!

This doesn’t apply to trivial pull requests such as spelling corrections.

We recommend installing precommit, which will perform basic linting and testing whenever you commit a file.
To set this up, run `just install-precommit`.

### Before requesting a review[](#before-requesting-a-review "Link to this heading")

* Ensure you have included tests that cover the change. In general, aim for full test coverage at the Python level.
  Rust tests are optional.
* Update documentation when there’s a new API, functionality etc.
* Add a note to `CHANGELOG.rst` about the changes.
* Add yourself to `AUTHORS.rst`.
* Run `just full-check` locally. (If you’re a new contributor, CI checks are not run automatically.)

## Development[](#development "Link to this heading")

### System prerequisites[](#system-prerequisites "Link to this heading")

Make sure these are installed first.

* [git](https://github.com/git-guides/install-git)
* [uv](https://docs.astral.sh/uv/#installation)
* [just](https://just.systems/man/en/packages.html)
* Cargo (via [rustup](https://rust-lang.org/tools/install/))

### Setup[](#setup "Link to this heading")

You don’t need to activate or manage a virtual environment - this is taken care in the background of by `uv`.

To set up Grimp for local development:

1. Fork [grimp](https://github.com/python-grimp/grimp)
   (look for the “Fork” button).
2. Clone your fork locally:

   ```
   git clone git@github.com:your_name_here/grimp.git
   ```
3. Change into the directory you just cloned:

   ```
   cd grimp
   ```
4. Set up pre-commit. (Optional, but recommended.):

   ```
   just install-precommit
   ```

You will now be able to run commands prefixed with `just`, providing you’re in the `grimp` directory.
To see available commands, run `just help`.

### Working with tests[](#working-with-tests "Link to this heading")

Grimp is a mixture of Python and Rust. The majority of the tests are in Python.

If you change the Rust code, you will need to recompile it before running the Python tests.

Typical workflow (Python changes only):

1. Make a change.
2. Run `just test-python`. This will run the Python tests using the default Python version (e.g. whatever is specified
   in a local `.python-version` file).

Typical workflow (changes that involve Rust):

1. Make a change to Rust code.
2. Run `just compile-and-test`. This will compile the Rust code, then run Rust and Python tests in the default version.

There are also version-specific test commands (e.g. `just test-3-14`) - run `just help` to see which ones.

### Working with documentation[](#working-with-documentation "Link to this heading")

You can preview any documentation changes locally by running:

```
just build-and-open-docs
```

It’s helpful to include a screenshot of the new docs in the pull request description.

### Before you push[](#before-you-push "Link to this heading")

It’s a good idea to run `just full-check` before getting a review.
This will run linters, docs build and tests under every supported Python version.

## Benchmarking[](#benchmarking "Link to this heading")

### Codspeed[](#codspeed "Link to this heading")

A few benchmarks are run automatically on pull requests, using [Codspeed](https://codspeed.io/).
Once the benchmarks have completed, a report will be included as a comment on the pull request.

Codspeed also shows flame graphs which can help track down why a change might have impacted performance.

### Local benchmarking[](#local-benchmarking "Link to this heading")

It’s also possible to run local benchmarks, which can be helpful if you want to quickly compare performance
across different versions of the code.

To benchmark a particular version of the code, run `just benchmark-local`. This command creates a report that will be
stored in a local file (ignored by Git).

This will display a list of all the benchmarks you’ve run locally, ordered from earlier to later.

## Profiling[](#profiling "Link to this heading")

### Codspeed[](#id2 "Link to this heading")

The easiest way to profile code is to look at the Codspeed flamegraph, automatically generated during benchmarking
(see above).

### Profiling Rust code locally[](#profiling-rust-code-locally "Link to this heading")

Rust integration tests can be profiled using [Cargo Flamegraph](https://github.com/flamegraph-rs/flamegraph)
(which will need to be installed first, e.g. using `cargo install flamegraph`).

Navigate to the `rust` directory in this package.

Run cargo flamegraph on the relevant test. E.g. to profile `rust/tests/large.rs`, run:

`sudo cargo flamegraph --root --test large`

This will create a file called `flamegraph.svg`, which you can open to view the flamegraph.

## Releasing to Pypi[](#releasing-to-pypi "Link to this heading")

This is only possible if you’re a maintainer.

1. Choose a new version number (based on [semver](https://semver.org/)).
2. `git pull origin main`
3. Update `CHANGELOG.rst` with the new version number.
4. Update the `release` variable in `docs/conf.py` with the new version number.
5. Update the `__version__` variable in `src/grimp/__init__.py` with the new version number.
6. Update `project.version` in `pyproject.toml` with the new version number.
7. `git commit -am "Release v{new version number"`
8. `git push`
9. Wait for tests to pass on CI.
10. `git tag v{new version number}`
11. `git push --tags`
12. This should kick start the Github `release` workflow, which builds wheels and releases the
    project to PyPI.
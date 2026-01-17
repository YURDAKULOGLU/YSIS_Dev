Instructions for aiohttp admins — aiohttp 3.13.3 documentation

# Instructions for aiohttp admins[¶](#instructions-for-aiohttp-admins "Link to this heading")

This page is intended to document certain processes for admins of the aiohttp repository.
For regular contributors, return to [Contributing](contributing.html).

## [Creating a new release](#id1)[¶](#creating-a-new-release "Link to this heading")

Note

The example commands assume that `origin` refers to the `aio-libs` repository.

To create a new release:

1. Start on the branch for the release you are planning (e.g. `3.8` for v3.8.6): `git checkout 3.8 && git pull`
2. Update the version number in `__init__.py`.
3. Run `towncrier`.
4. Check and cleanup the changes in `CHANGES.rst`.
5. Checkout a new branch: e.g. `git checkout -b release/v3.8.6`
6. Commit and create a PR. Verify the changelog and release notes look good on Read the Docs. Once PR is merged, continue.
7. Go back to the release branch: e.g. `git checkout 3.8 && git pull`
8. Add a tag: e.g. `git tag -a v3.8.6 -m 'Release 3.8.6' -s`
9. Push the tag: e.g. `git push origin v3.8.6`
10. Monitor CI to ensure release process completes without errors.

Once released, we need to complete some cleanup steps (no further steps are needed for
non-stable releases though). If doing a patch release, we need to do the below steps twice,
first merge into the newer release branch (e.g. 3.8 into 3.9) and then to master
(e.g. 3.9 into master). If a new minor release, then just merge to master.

1. Switch to target branch: e.g. `git checkout 3.9 && git pull`
2. Start a merge: e.g. `git merge 3.8 --no-commit --no-ff --gpg-sign`
3. Carefully review the changes and revert anything that should not be included (most
   things outside the changelog).
4. To ensure change fragments are cleaned up properly, run: `python tools/cleanup_changes.py`
5. Commit the merge (must be a normal merge commit, not squashed).
6. Push the branch directly to Github (because a PR would get squashed). When pushing,
   you may get a rejected message. Follow these steps to resolve:

> 1. Checkout to a new branch and push: e.g. `git checkout -b do-not-merge && git push`
> 2. Open a *draft* PR with a title of ‘DO NOT MERGE’.
> 3. Once the CI has completed on that branch, you should be able to switch back and push
>    the target branch (as tests have passed on the merge commit now).
> 4. This should automatically consider the PR merged and delete the temporary branch.

Back on the original release branch, bump the version number and append `.dev0` in `__init__.py`.

Post the release announcement to social media:
:   * BlueSky: <https://bsky.app/profile/aiohttp.org> and re-post to <https://bsky.app/profile/aio-libs.org>
    * Mastodon: <https://fosstodon.org/@aiohttp> and re-post to <https://fosstodon.org/@aio_libs>

If doing a minor release:

1. Create a new release branch for future features to go to: e.g. `git checkout -b 3.10 3.9 && git push`
2. Update both `target-branch` backports for Dependabot to reference the new branch name in `.github/dependabot.yml`.
3. Delete the older backport label (e.g. backport-3.8): <https://github.com/aio-libs/aiohttp/labels>
4. Add a new backport label (e.g. backport-3.10).

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
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/contributing-admins.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
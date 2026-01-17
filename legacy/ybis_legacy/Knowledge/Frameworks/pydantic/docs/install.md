Installation - Pydantic Validation






[Skip to content](#optional-dependencies)

What's new — we've launched
[Pydantic Logfire](https://pydantic.dev/articles/logfire-announcement)
![🔥](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f525.svg ":fire:")
to help you monitor and understand your
[Pydantic validations.](https://logfire.pydantic.dev/docs/integrations/pydantic/)

# Installation

Installation is as simple as:

pipuv

```
pip install pydantic
```

```
uv add pydantic
```

Pydantic has a few dependencies:

* [`pydantic-core`](https://pypi.org/project/pydantic-core/): Core validation logic for Pydantic written in Rust.
* [`typing-extensions`](https://pypi.org/project/typing-extensions/): Backport of the standard library [typing](https://docs.python.org/3/library/typing.html#module-typing) module.
* [`annotated-types`](https://pypi.org/project/annotated-types/): Reusable constraint types to use with [`typing.Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated).

If you've got Python 3.9+ and `pip` installed, you're good to go.

Pydantic is also available on [conda](https://www.anaconda.com) under the [conda-forge](https://conda-forge.org)
channel:

```
conda install pydantic -c conda-forge
```

## Optional dependencies[¶](#optional-dependencies "Permanent link")

Pydantic has the following optional dependencies:

* `email`: Email validation provided by the [email-validator](https://pypi.org/project/email-validator/) package.
* `timezone`: Fallback IANA time zone database provided by the [tzdata](https://pypi.org/project/tzdata/) package.

To install optional dependencies along with Pydantic:

pipuv

```
# with the `email` extra:
pip install 'pydantic[email]'
# or with `email` and `timezone` extras:
pip install 'pydantic[email,timezone]'
```

```
# with the `email` extra:
uv add 'pydantic[email]'
# or with `email` and `timezone` extras:
uv add 'pydantic[email,timezone]'
```

Of course, you can also install requirements manually with `pip install email-validator tzdata`.

## Install from repository[¶](#install-from-repository "Permanent link")

And if you prefer to install Pydantic directly from the repository:

pipuv

```
pip install 'git+https://github.com/pydantic/pydantic@main'
# or with `email` and `timezone` extras:
pip install 'git+https://github.com/pydantic/pydantic@main#egg=pydantic[email,timezone]'
```

```
uv add 'git+https://github.com/pydantic/pydantic@main'
# or with `email` and `timezone` extras:
uv add 'git+https://github.com/pydantic/pydantic@main#egg=pydantic[email,timezone]'
```

Was this page helpful?

Thanks for your feedback!

Thanks for your feedback!

Back to top
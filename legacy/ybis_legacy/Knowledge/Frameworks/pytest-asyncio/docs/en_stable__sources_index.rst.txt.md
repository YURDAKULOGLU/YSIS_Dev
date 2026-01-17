==========================
Welcome to pytest-asyncio!
==========================
.. toctree::
:maxdepth: 1
:hidden:
concepts
how-to-guides/index
reference/index
support
pytest-asyncio is a `pytest `\_ plugin. It facilitates testing of code that uses the `asyncio `\_ library.
Specifically, pytest-asyncio provides support for coroutines as test functions. This allows users to \*await\* code inside their tests. For example, the following code is executed as a test item by pytest:
.. code-block:: python
@pytest.mark.asyncio
async def test\_some\_asyncio\_code():
res = await library.do\_something()
assert b"expected result" == res
Note that test classes subclassing the standard `unittest `\_\_ library are not supported. Users
are advised to use `unittest.IsolatedAsyncioTestCase `\_\_
or an async framework such as `asynctest `\_\_.
pytest-asyncio is available under the `Apache License 2.0 `\_.
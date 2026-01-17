Welcome to pytest-asyncio! — pytest-asyncio 1.3.0 documentation



* Welcome to pytest-asyncio!
* [View page source](_sources/index.rst.txt)

---

# Welcome to pytest-asyncio![](#welcome-to-pytest-asyncio "Link to this heading")

pytest-asyncio is a [pytest](https://docs.pytest.org/en/latest/contents.html) plugin. It facilitates testing of code that uses the [asyncio](https://docs.python.org/3/library/asyncio.html) library.

Specifically, pytest-asyncio provides support for coroutines as test functions. This allows users to *await* code inside their tests. For example, the following code is executed as a test item by pytest:

```
@pytest.mark.asyncio
async def test_some_asyncio_code():
    res = await library.do_something()
    assert b"expected result" == res
```

Note that test classes subclassing the standard [unittest](https://docs.python.org/3/library/unittest.html) library are not supported. Users
are advised to use [unittest.IsolatedAsyncioTestCase](https://docs.python.org/3/library/unittest.html#unittest.IsolatedAsyncioTestCase)
or an async framework such as [asynctest](https://asynctest.readthedocs.io/en/latest).

pytest-asyncio is available under the [Apache License 2.0](https://github.com/pytest-dev/pytest-asyncio/blob/main/LICENSE).
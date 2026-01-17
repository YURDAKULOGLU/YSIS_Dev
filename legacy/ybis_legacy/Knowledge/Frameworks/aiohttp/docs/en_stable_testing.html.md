Testing — aiohttp 3.13.3 documentation

# Testing[¶](#testing "Link to this heading")

## Testing aiohttp web servers[¶](#testing-aiohttp-web-servers "Link to this heading")

aiohttp provides plugin for *pytest* making writing web server tests
extremely easy, it also provides [test framework agnostic
utilities](#aiohttp-testing-framework-agnostic-utilities) for testing
with other frameworks such as [unittest](#aiohttp-testing-unittest-example).

Before starting to write your tests, you may also be interested on
reading [how to write testable
services](#aiohttp-testing-writing-testable-services) that interact
with the loop.

For using pytest plugin please install [pytest-aiohttp](https://pypi.python.org/pypi/pytest-aiohttp) library:

```
$ pip install pytest-aiohttp
```

If you don’t want to install *pytest-aiohttp* for some reason you may
insert `pytest_plugins = 'aiohttp.pytest_plugin'` line into
`conftest.py` instead for the same functionality.

### The Test Client and Servers[¶](#the-test-client-and-servers "Link to this heading")

*aiohttp* test utils provides a scaffolding for testing aiohttp-based
web servers.

They are consist of two parts: running test server and making HTTP
requests to this server.

[`TestServer`](#aiohttp.test_utils.TestServer "aiohttp.test_utils.TestServer") runs [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application")
based server, [`RawTestServer`](#aiohttp.test_utils.RawTestServer "aiohttp.test_utils.RawTestServer") starts
[`aiohttp.web.Server`](web_reference.html#aiohttp.web.Server "aiohttp.web.Server") low level server.

For performing HTTP requests to these servers you have to create a
test client: [`TestClient`](#aiohttp.test_utils.TestClient "aiohttp.test_utils.TestClient") instance.

The client incapsulates [`aiohttp.ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") by providing
proxy methods to the client for common operations such as
*ws\_connect*, *get*, *post*, etc.

### Pytest[¶](#pytest "Link to this heading")

The [`aiohttp_client`](#pytest_aiohttp.aiohttp_client "pytest_aiohttp.aiohttp_client") fixture available from [pytest-aiohttp](https://pypi.python.org/pypi/pytest-aiohttp) plugin
allows you to create a client to make requests to test your app.

To run these examples, you need to use –asyncio-mode=auto or add to your
pytest config file:

```
asyncio_mode = auto
```

A simple test would be:

```
from aiohttp import web

async def hello(request):
    return web.Response(text='Hello, world')

async def test_hello(aiohttp_client):
    app = web.Application()
    app.router.add_get('/', hello)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text
```

It also provides access to the app instance allowing tests to check the state
of the app. Tests can be made even more succinct with a fixture to create an
app test client:

```
import pytest
from aiohttp import web

value = web.AppKey("value", str)


async def previous(request):
    if request.method == 'POST':
        request.app[value] = (await request.post())['value']
        return web.Response(body=b'thanks for the data')
    return web.Response(
        body='value: {}'.format(request.app[value]).encode('utf-8'))

@pytest.fixture
async def cli(aiohttp_client):
    app = web.Application()
    app.router.add_get('/', previous)
    app.router.add_post('/', previous)
    return await aiohttp_client(app)

async def test_set_value(cli):
    resp = await cli.post('/', data={'value': 'foo'})
    assert resp.status == 200
    assert await resp.text() == 'thanks for the data'
    assert cli.server.app[value] == 'foo'

async def test_get_value(cli):
    cli.server.app[value] = 'bar'
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.text() == 'value: bar'
```

Pytest tooling has the following fixtures:

pytest\_aiohttp.aiohttp\_server(*app*, *\**, *port=None*, *\*\*kwargs*)[¶](#pytest_aiohttp.aiohttp_server "Link to this definition")
:   A fixture factory that creates
    [`TestServer`](#aiohttp.test_utils.TestServer "aiohttp.test_utils.TestServer"):

    ```
    async def test_f(aiohttp_server):
        app = web.Application()
        # fill route table

        server = await aiohttp_server(app)
    ```

    The server will be destroyed on exit from test function.

    *app* is the [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") used
    :   to start server.

    *port* optional, port the server is run at, if
    not provided a random unused port is used.

    Added in version 3.0.

    *kwargs* are parameters passed to
    :   [`aiohttp.web.Application.make_handler()`](web_reference.html#aiohttp.web.Application.make_handler "aiohttp.web.Application.make_handler")

    Changed in version 3.0.

    Deprecated since version 3.2: The fixture was renamed from `test_server` to `aiohttp_server`.

pytest\_aiohttp.aiohttp\_client(*app*, *server\_kwargs=None*, *\*\*kwargs*)[¶](#pytest_aiohttp.aiohttp_client "Link to this definition")

pytest\_aiohttp.aiohttp\_client(*server*, *\*\*kwargs*)

pytest\_aiohttp.aiohttp\_client(*raw\_server*, *\*\*kwargs*)
:   A fixture factory that creates
    [`TestClient`](#aiohttp.test_utils.TestClient "aiohttp.test_utils.TestClient") for access to tested server:

    ```
    async def test_f(aiohttp_client):
        app = web.Application()
        # fill route table

        client = await aiohttp_client(app)
        resp = await client.get('/')
    ```

    *client* and responses are cleaned up after test function finishing.

    The fixture accepts [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application"),
    [`aiohttp.test_utils.TestServer`](#aiohttp.test_utils.TestServer "aiohttp.test_utils.TestServer") or
    [`aiohttp.test_utils.RawTestServer`](#aiohttp.test_utils.RawTestServer "aiohttp.test_utils.RawTestServer") instance.

    *server\_kwargs* are parameters passed to the test server if an app
    is passed, else ignored.

    *kwargs* are parameters passed to
    [`aiohttp.test_utils.TestClient`](#aiohttp.test_utils.TestClient "aiohttp.test_utils.TestClient") constructor.

    Changed in version 3.0: The fixture was renamed from `test_client` to `aiohttp_client`.

pytest\_aiohttp.aiohttp\_raw\_server(*handler*, *\**, *port=None*, *\*\*kwargs*)[¶](#pytest_aiohttp.aiohttp_raw_server "Link to this definition")
:   A fixture factory that creates
    [`RawTestServer`](#aiohttp.test_utils.RawTestServer "aiohttp.test_utils.RawTestServer") instance from given web
    handler.:

    ```
    async def test_f(aiohttp_raw_server, aiohttp_client):

        async def handler(request):
            return web.Response(text="OK")

        raw_server = await aiohttp_raw_server(handler)
        client = await aiohttp_client(raw_server)
        resp = await client.get('/')
    ```

    *handler* should be a coroutine which accepts a request and returns
    response, e.g.

    *port* optional, port the server is run at, if
    not provided a random unused port is used.

    Added in version 3.0.

pytest\_aiohttp.aiohttp\_unused\_port[¶](#pytest_aiohttp.aiohttp_unused_port "Link to this definition")
:   Function to return an unused port number for IPv4 TCP protocol:

    ```
    async def test_f(aiohttp_client, aiohttp_unused_port):
        port = aiohttp_unused_port()
        app = web.Application()
        # fill route table

        client = await aiohttp_client(app, server_kwargs={'port': port})
        ...
    ```

    Changed in version 3.0: The fixture was renamed from `unused_port` to `aiohttp_unused_port`.

### Unittest[¶](#unittest "Link to this heading")

To test applications with the standard library’s unittest or unittest-based
functionality, the AioHTTPTestCase is provided:

```
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web

class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        async def hello(request):
            return web.Response(text='Hello, world')

        app = web.Application()
        app.router.add_get('/', hello)
        return app

    async def test_example(self):
        async with self.client.request("GET", "/") as resp:
            self.assertEqual(resp.status, 200)
            text = await resp.text()
        self.assertIn("Hello, world", text)
```

class aiohttp.test\_utils.AioHTTPTestCase[[source]](_modules/aiohttp/test_utils.html#AioHTTPTestCase)[¶](#aiohttp.test_utils.AioHTTPTestCase "Link to this definition")
:   A base class to allow for unittest web applications using aiohttp.

    Derived from [`unittest.IsolatedAsyncioTestCase`](https://docs.python.org/3/library/unittest.html#unittest.IsolatedAsyncioTestCase "(in Python v3.14)")

    See [`unittest.TestCase`](https://docs.python.org/3/library/unittest.html#unittest.TestCase "(in Python v3.14)") and [`unittest.IsolatedAsyncioTestCase`](https://docs.python.org/3/library/unittest.html#unittest.IsolatedAsyncioTestCase "(in Python v3.14)")
    for inherited methods and behavior.

    This class additionally provides the following:

    client[¶](#aiohttp.test_utils.AioHTTPTestCase.client "Link to this definition")
    :   an aiohttp test client, [`TestClient`](#aiohttp.test_utils.TestClient "aiohttp.test_utils.TestClient") instance.

    server[¶](#aiohttp.test_utils.AioHTTPTestCase.server "Link to this definition")
    :   an aiohttp test server, [`TestServer`](#aiohttp.test_utils.TestServer "aiohttp.test_utils.TestServer") instance.

        Added in version 2.3.

    app[¶](#aiohttp.test_utils.AioHTTPTestCase.app "Link to this definition")
    :   The application returned by [`get_application()`](#aiohttp.test_utils.AioHTTPTestCase.get_application "aiohttp.test_utils.AioHTTPTestCase.get_application")
        ([`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") instance).

    async get\_client()[[source]](_modules/aiohttp/test_utils.html#AioHTTPTestCase.get_client)[¶](#aiohttp.test_utils.AioHTTPTestCase.get_client "Link to this definition")
    :   > This async method can be overridden to return the [`TestClient`](#aiohttp.test_utils.TestClient "aiohttp.test_utils.TestClient")
        > object used in the test.
        >
        > return:
        > :   [`TestClient`](#aiohttp.test_utils.TestClient "aiohttp.test_utils.TestClient") instance.
        >
        > Added in version 2.3.

    async get\_server()[[source]](_modules/aiohttp/test_utils.html#AioHTTPTestCase.get_server)[¶](#aiohttp.test_utils.AioHTTPTestCase.get_server "Link to this definition")
    :   > This async method can be overridden to return the [`TestServer`](#aiohttp.test_utils.TestServer "aiohttp.test_utils.TestServer")
        > object used in the test.
        >
        > return:
        > :   [`TestServer`](#aiohttp.test_utils.TestServer "aiohttp.test_utils.TestServer") instance.
        >
        > Added in version 2.3.

    async get\_application()[[source]](_modules/aiohttp/test_utils.html#AioHTTPTestCase.get_application)[¶](#aiohttp.test_utils.AioHTTPTestCase.get_application "Link to this definition")
    :   > This async method should be overridden
        > to return the [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application")
        > object to test.
        >
        > return:
        > :   [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") instance.

    async asyncSetUp()[[source]](_modules/aiohttp/test_utils.html#AioHTTPTestCase.asyncSetUp)[¶](#aiohttp.test_utils.AioHTTPTestCase.asyncSetUp "Link to this definition")
    :   > This async method can be overridden to execute asynchronous code during
        > the `setUp` stage of the `TestCase`:
        >
        > ```
        > async def asyncSetUp(self):
        >     await super().asyncSetUp()
        >     await foo()
        > ```
        >
        > Added in version 2.3.
        >
        > Changed in version 3.8: `await super().asyncSetUp()` call is required.

    async asyncTearDown()[[source]](_modules/aiohttp/test_utils.html#AioHTTPTestCase.asyncTearDown)[¶](#aiohttp.test_utils.AioHTTPTestCase.asyncTearDown "Link to this definition")
    :   > This async method can be overridden to execute asynchronous code during
        > the `tearDown` stage of the `TestCase`:
        >
        > ```
        > async def asyncTearDown(self):
        >     await super().asyncTearDown()
        >     await foo()
        > ```
        >
        > Added in version 2.3.
        >
        > Changed in version 3.8: `await super().asyncTearDown()` call is required.

#### Faking request object[¶](#faking-request-object "Link to this heading")

aiohttp provides test utility for creating fake
[`aiohttp.web.Request`](web_reference.html#aiohttp.web.Request "aiohttp.web.Request") objects:
[`aiohttp.test_utils.make_mocked_request()`](#aiohttp.test_utils.make_mocked_request "aiohttp.test_utils.make_mocked_request"), it could be useful in
case of simple unit tests, like handler tests, or simulate error
conditions that hard to reproduce on real server:

```
from aiohttp import web
from aiohttp.test_utils import make_mocked_request

def handler(request):
    assert request.headers.get('token') == 'x'
    return web.Response(body=b'data')

def test_handler():
    req = make_mocked_request('GET', '/', headers={'token': 'x'})
    resp = handler(req)
    assert resp.body == b'data'
```

Warning

We don’t recommend to apply
[`make_mocked_request()`](#aiohttp.test_utils.make_mocked_request "aiohttp.test_utils.make_mocked_request") everywhere for
testing web-handler’s business object – please use test client and
real networking via ‘localhost’ as shown in examples before.

[`make_mocked_request()`](#aiohttp.test_utils.make_mocked_request "aiohttp.test_utils.make_mocked_request") exists only for
testing complex cases (e.g. emulating network errors) which
are extremely hard or even impossible to test by conventional
way.

aiohttp.test\_utils.make\_mocked\_request(*method*, *path*, *headers=None*, *\**, *version=HttpVersion(1, 1)*, *closing=False*, *app=None*, *match\_info=sentinel*, *reader=sentinel*, *writer=sentinel*, *transport=sentinel*, *payload=sentinel*, *sslcontext=None*, *loop=...*)[[source]](_modules/aiohttp/test_utils.html#make_mocked_request)[¶](#aiohttp.test_utils.make_mocked_request "Link to this definition")
:   Creates mocked web.Request testing purposes.

    Useful in unit tests, when spinning full web server is overkill or
    specific conditions and errors are hard to trigger.

    Parameters:
    :   * **method** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – str, that represents HTTP method, like; GET, POST.
        * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – str, The URL including *PATH INFO* without the host or scheme
        * **headers** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")*,* [*multidict.CIMultiDict*](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)")*,* [*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.14)") *of* [*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")*(*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*,* [*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*)*) – mapping containing the headers. Can be anything accepted
          by the multidict.CIMultiDict constructor.
        * **match\_info** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)")) – mapping containing the info to match with url parameters.
        * **version** (*aiohttp.protocol.HttpVersion*) – namedtuple with encoded HTTP version
        * **closing** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")) – flag indicates that connection should be closed after
          response.
        * **app** ([*aiohttp.web.Application*](web_reference.html#aiohttp.web.Application "aiohttp.web.Application")) – the aiohttp.web application attached for fake request
        * **writer** (*aiohttp.StreamWriter*) – object for managing outcoming data
        * **transport** ([*asyncio.Transport*](https://docs.python.org/3/library/asyncio-protocol.html#asyncio.Transport "(in Python v3.14)")) – asyncio transport instance
        * **payload** ([*aiohttp.StreamReader*](streams.html#aiohttp.StreamReader "aiohttp.StreamReader")) – raw payload reader object
        * **sslcontext** ([*ssl.SSLContext*](https://docs.python.org/3/library/ssl.html#ssl.SSLContext "(in Python v3.14)")) – ssl.SSLContext object, for HTTPS connection
        * **loop** ([`asyncio.AbstractEventLoop`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop "(in Python v3.14)")) – An event loop instance, mocked loop by default.

    Returns:
    :   [`aiohttp.web.Request`](web_reference.html#aiohttp.web.Request "aiohttp.web.Request") object.

    Added in version 2.3: *match\_info* parameter.

## Framework Agnostic Utilities[¶](#framework-agnostic-utilities "Link to this heading")

High level test creation:

```
from aiohttp.test_utils import TestClient, TestServer
from aiohttp import request

async def test():
    app = _create_example_app()
    async with TestClient(TestServer(app)) as client:

        async def test_get_route():
            nonlocal client
            resp = await client.get("/")
            assert resp.status == 200
            text = await resp.text()
            assert "Hello, world" in text

        await test_get_route()
```

If it’s preferred to handle the creation / teardown on a more granular
basis, the TestClient object can be used directly:

```
from aiohttp.test_utils import TestClient, TestServer

async def test():
    app = _create_example_app()
    client = TestClient(TestServer(app))
    await client.start_server()
    root = "http://127.0.0.1:{}".format(port)

    async def test_get_route():
        resp = await client.get("/")
        assert resp.status == 200
        text = await resp.text()
        assert "Hello, world" in text

    await test_get_route()
    await client.close()
```

A full list of the utilities provided can be found at the
[`api reference`](#module-aiohttp.test_utils "aiohttp.test_utils")

## Testing API Reference[¶](#testing-api-reference "Link to this heading")

### Test server[¶](#test-server "Link to this heading")

Runs given [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") instance on random TCP port.

After creation the server is not started yet, use
[`start_server()`](#aiohttp.test_utils.BaseTestServer.start_server "aiohttp.test_utils.BaseTestServer.start_server") for actual server
starting and [`close()`](#aiohttp.test_utils.BaseTestServer.close "aiohttp.test_utils.BaseTestServer.close") for
stopping/cleanup.

Test server usually works in conjunction with
[`aiohttp.test_utils.TestClient`](#aiohttp.test_utils.TestClient "aiohttp.test_utils.TestClient") which provides handy client methods
for accessing to the server.

class aiohttp.test\_utils.BaseTestServer(*\**, *scheme='http'*, *host='127.0.0.1'*, *port=None*, *socket\_factory=get\_port\_socket*)[[source]](_modules/aiohttp/test_utils.html#BaseTestServer)[¶](#aiohttp.test_utils.BaseTestServer "Link to this definition")
:   Base class for test servers.

    Parameters:
    :   * **scheme** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – HTTP scheme, non-protected `"http"` by default.
        * **host** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – a host for TCP socket, IPv4 *local host*
          (`'127.0.0.1'`) by default.
        * **port** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          optional port for TCP socket, if not provided a
          random unused port is used.

          Added in version 3.0.
        * **socket\_factory** ([*collections.abc.Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable "(in Python v3.14)")*[**[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")*,*[*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")*,**socket.AddressFamily**]**,*[*socket.socket*](https://docs.python.org/3/library/socket.html#socket.socket "(in Python v3.14)")*]*) –

          optional
          :   Factory to create a socket for the server.
              By default creates a TCP socket and binds it
              to `host` and `port`.

          Added in version 3.8.

    scheme[¶](#aiohttp.test_utils.BaseTestServer.scheme "Link to this definition")
    :   A *scheme* for tested application, `'http'` for non-protected
        run and `'https'` for TLS encrypted server.

    host[¶](#aiohttp.test_utils.BaseTestServer.host "Link to this definition")
    :   *host* used to start a test server.

    port[¶](#aiohttp.test_utils.BaseTestServer.port "Link to this definition")
    :   *port* used to start the test server.

    handler[¶](#aiohttp.test_utils.BaseTestServer.handler "Link to this definition")
    :   [`aiohttp.web.Server`](web_reference.html#aiohttp.web.Server "aiohttp.web.Server") used for HTTP requests serving.

    server[¶](#aiohttp.test_utils.BaseTestServer.server "Link to this definition")
    :   `asyncio.AbstractServer` used for managing accepted connections.

    socket\_factory[¶](#aiohttp.test_utils.BaseTestServer.socket_factory "Link to this definition")
    :   *socket\_factory* used to create and bind a server socket.

        Added in version 3.8.

    async start\_server(*loop=None*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#BaseTestServer.start_server)[¶](#aiohttp.test_utils.BaseTestServer.start_server "Link to this definition")
    :   Parameters:
        :   **loop** ([*asyncio.AbstractEventLoop*](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop "(in Python v3.14)")) – the event\_loop to use

        Start a test server.

    async close()[[source]](_modules/aiohttp/test_utils.html#BaseTestServer.close)[¶](#aiohttp.test_utils.BaseTestServer.close "Link to this definition")
    :   Stop and finish executed test server.

    make\_url(*path*)[[source]](_modules/aiohttp/test_utils.html#BaseTestServer.make_url)[¶](#aiohttp.test_utils.BaseTestServer.make_url "Link to this definition")
    :   Return an *absolute* [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") for given *path*.

class aiohttp.test\_utils.RawTestServer(*handler*, *\**, *scheme='http'*, *host='127.0.0.1'*)[[source]](_modules/aiohttp/test_utils.html#RawTestServer)[¶](#aiohttp.test_utils.RawTestServer "Link to this definition")
:   Low-level test server (derived from [`BaseTestServer`](#aiohttp.test_utils.BaseTestServer "aiohttp.test_utils.BaseTestServer")).

    Parameters:
    :   * **handler** –

          a coroutine for handling web requests. The
          handler should accept
          [`aiohttp.web.BaseRequest`](web_reference.html#aiohttp.web.BaseRequest "aiohttp.web.BaseRequest") and return a
          response instance,
          e.g. [`StreamResponse`](web_reference.html#aiohttp.web.StreamResponse "aiohttp.web.StreamResponse") or
          [`Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response").

          The handler could raise
          [`HTTPException`](web_reference.html#aiohttp.web.HTTPException "aiohttp.web.HTTPException") as a signal for
          non-200 HTTP response.
        * **scheme** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – HTTP scheme, non-protected `"http"` by default.
        * **host** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – a host for TCP socket, IPv4 *local host*
          (`'127.0.0.1'`) by default.
        * **port** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          optional port for TCP socket, if not provided a
          random unused port is used.

          Added in version 3.0.

class aiohttp.test\_utils.TestServer(*app*, *\**, *scheme='http'*, *host='127.0.0.1'*)[[source]](_modules/aiohttp/test_utils.html#TestServer)[¶](#aiohttp.test_utils.TestServer "Link to this definition")
:   Test server (derived from [`BaseTestServer`](#aiohttp.test_utils.BaseTestServer "aiohttp.test_utils.BaseTestServer")) for starting
    [`Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application").

    Parameters:
    :   * **app** – [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") instance to run.
        * **scheme** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – HTTP scheme, non-protected `"http"` by default.
        * **host** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – a host for TCP socket, IPv4 *local host*
          (`'127.0.0.1'`) by default.
        * **port** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) –

          optional port for TCP socket, if not provided a
          random unused port is used.

          Added in version 3.0.

    app[¶](#aiohttp.test_utils.TestServer.app "Link to this definition")
    :   [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application") instance to run.

### Test Client[¶](#test-client "Link to this heading")

class aiohttp.test\_utils.TestClient(*app\_or\_server*, *\**, *loop=None*, *scheme='http'*, *host='127.0.0.1'*, *cookie\_jar=None*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient)[¶](#aiohttp.test_utils.TestClient "Link to this definition")
:   A test client used for making calls to tested server.

    Parameters:
    :   * **app\_or\_server** –

          [`BaseTestServer`](#aiohttp.test_utils.BaseTestServer "aiohttp.test_utils.BaseTestServer") instance for making
          client requests to it.

          In order to pass a [`aiohttp.web.Application`](web_reference.html#aiohttp.web.Application "aiohttp.web.Application")
          you need to convert it first to [`TestServer`](#aiohttp.test_utils.TestServer "aiohttp.test_utils.TestServer")
          first with `TestServer(app)`.
        * **cookie\_jar** – an optional [`aiohttp.CookieJar`](client_reference.html#aiohttp.CookieJar "aiohttp.CookieJar") instance,
          may be useful with
          `CookieJar(unsafe=True, treat_as_secure_origin="http://127.0.0.1")`
          option.
        * **scheme** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – HTTP scheme, non-protected `"http"` by default.
        * **loop** ([*asyncio.AbstractEventLoop*](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop "(in Python v3.14)")) – the event\_loop to use
        * **host** ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) – a host for TCP socket, IPv4 *local host*
          (`'127.0.0.1'`) by default.

    scheme[¶](#aiohttp.test_utils.TestClient.scheme "Link to this definition")
    :   A *scheme* for tested application, `'http'` for non-protected
        run and `'https'` for TLS encrypted server.

    host[¶](#aiohttp.test_utils.TestClient.host "Link to this definition")
    :   *host* used to start a test server.

    port[¶](#aiohttp.test_utils.TestClient.port "Link to this definition")
    :   *port* used to start the server

    server[¶](#aiohttp.test_utils.TestClient.server "Link to this definition")
    :   [`BaseTestServer`](#aiohttp.test_utils.BaseTestServer "aiohttp.test_utils.BaseTestServer") test server instance used in conjunction
        with client.

    app[¶](#aiohttp.test_utils.TestClient.app "Link to this definition")
    :   An alias for `self.server.app`. return `None` if
        `self.server` is not [`TestServer`](#aiohttp.test_utils.TestServer "aiohttp.test_utils.TestServer")
        instance(e.g. [`RawTestServer`](#aiohttp.test_utils.RawTestServer "aiohttp.test_utils.RawTestServer") instance for test low-level server).

    session[¶](#aiohttp.test_utils.TestClient.session "Link to this definition")
    :   An internal [`aiohttp.ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession").

        Unlike the methods on the [`TestClient`](#aiohttp.test_utils.TestClient "aiohttp.test_utils.TestClient"), client session
        requests do not automatically include the host in the url
        queried, and will require an absolute path to the resource.

    async start\_server(*\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.start_server)[¶](#aiohttp.test_utils.TestClient.start_server "Link to this definition")
    :   Start a test server.

    async close()[[source]](_modules/aiohttp/test_utils.html#TestClient.close)[¶](#aiohttp.test_utils.TestClient.close "Link to this definition")
    :   Stop and finish executed test server.

    make\_url(*path*)[[source]](_modules/aiohttp/test_utils.html#TestClient.make_url)[¶](#aiohttp.test_utils.TestClient.make_url "Link to this definition")
    :   Return an *absolute* [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") for given *path*.

    async request(*method*, *path*, *\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.request)[¶](#aiohttp.test_utils.TestClient.request "Link to this definition")
    :   Routes a request to tested http server.

        The interface is identical to
        [`aiohttp.ClientSession.request()`](client_reference.html#aiohttp.ClientSession.request "aiohttp.ClientSession.request"), except the loop kwarg is
        overridden by the instance used by the test server.

    async get(*path*, *\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.get)[¶](#aiohttp.test_utils.TestClient.get "Link to this definition")
    :   Perform an HTTP GET request.

    async post(*path*, *\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.post)[¶](#aiohttp.test_utils.TestClient.post "Link to this definition")
    :   Perform an HTTP POST request.

    async options(*path*, *\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.options)[¶](#aiohttp.test_utils.TestClient.options "Link to this definition")
    :   Perform an HTTP OPTIONS request.

    async head(*path*, *\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.head)[¶](#aiohttp.test_utils.TestClient.head "Link to this definition")
    :   Perform an HTTP HEAD request.

    async put(*path*, *\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.put)[¶](#aiohttp.test_utils.TestClient.put "Link to this definition")
    :   Perform an HTTP PUT request.

    async patch(*path*, *\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.patch)[¶](#aiohttp.test_utils.TestClient.patch "Link to this definition")
    :   Perform an HTTP PATCH request.

    async delete(*path*, *\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.delete)[¶](#aiohttp.test_utils.TestClient.delete "Link to this definition")
    :   Perform an HTTP DELETE request.

    async ws\_connect(*path*, *\*args*, *\*\*kwargs*)[[source]](_modules/aiohttp/test_utils.html#TestClient.ws_connect)[¶](#aiohttp.test_utils.TestClient.ws_connect "Link to this definition")
    :   Initiate websocket connection.

        The api corresponds to [`aiohttp.ClientSession.ws_connect()`](client_reference.html#aiohttp.ClientSession.ws_connect "aiohttp.ClientSession.ws_connect").

### Utilities[¶](#utilities "Link to this heading")

aiohttp.test\_utils.make\_mocked\_coro(*return\_value*)[[source]](_modules/aiohttp/test_utils.html#make_mocked_coro)[¶](#aiohttp.test_utils.make_mocked_coro "Link to this definition")
:   Creates a coroutine mock.

    Behaves like a coroutine which returns *return\_value*. But it is
    also a mock object, you might test it as usual
    [`Mock`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock "(in Python v3.14)"):

    ```
    mocked = make_mocked_coro(1)
    assert 1 == await mocked(1, 2)
    mocked.assert_called_with(1, 2)
    ```

    Parameters:
    :   **return\_value** – A value that the mock object will return when
        called.

    Returns:
    :   A mock object that behaves as a coroutine which returns
        *return\_value* when called.

aiohttp.test\_utils.unused\_port()[[source]](_modules/aiohttp/test_utils.html#unused_port)[¶](#aiohttp.test_utils.unused_port "Link to this definition")
:   Return an unused port number for IPv4 TCP protocol.

    Return int:
    :   ephemeral port number which could be reused by test server.

aiohttp.test\_utils.loop\_context(*loop\_factory=<function asyncio.new\_event\_loop>*)[[source]](_modules/aiohttp/test_utils.html#loop_context)[¶](#aiohttp.test_utils.loop_context "Link to this definition")
:   A contextmanager that creates an event\_loop, for test purposes.

    Handles the creation and cleanup of a test loop.

aiohttp.test\_utils.setup\_test\_loop(*loop\_factory=<function asyncio.new\_event\_loop>*)[[source]](_modules/aiohttp/test_utils.html#setup_test_loop)[¶](#aiohttp.test_utils.setup_test_loop "Link to this definition")
:   Create and return an [`asyncio.AbstractEventLoop`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop "(in Python v3.14)") instance.

    The caller should also call teardown\_test\_loop, once they are done
    with the loop.

    Note

    As side effect the function changes asyncio *default loop* by
    [`asyncio.set_event_loop()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.set_event_loop "(in Python v3.14)") call.

    Previous default loop is not restored.

    It should not be a problem for test suite: every test expects a
    new test loop instance anyway.

    Changed in version 3.1: The function installs a created event loop as *default*.

aiohttp.test\_utils.teardown\_test\_loop(*loop*)[[source]](_modules/aiohttp/test_utils.html#teardown_test_loop)[¶](#aiohttp.test_utils.teardown_test_loop "Link to this definition")
:   Teardown and cleanup an event\_loop created by setup\_test\_loop.

    Parameters:
    :   **loop** ([*asyncio.AbstractEventLoop*](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.AbstractEventLoop "(in Python v3.14)")) – the loop to teardown

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
* [Server](web.html)
  + [Tutorial](https://demos.aiohttp.org)
  + [Quickstart](web_quickstart.html)
  + [Advanced Usage](web_advanced.html)
  + [Low Level](web_lowlevel.html)
  + [Reference](web_reference.html)
  + [Logging](logging.html)
  + [Testing](#)
  + [Deployment](deployment.html)
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
[Page source](_sources/testing.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
.. module:: aiohttp.test\_utils
.. \_aiohttp-testing:
Testing
=======
Testing aiohttp web servers
---------------------------
aiohttp provides plugin for \*pytest\* making writing web server tests
extremely easy, it also provides :ref:`test framework agnostic
utilities ` for testing
with other frameworks such as :ref:`unittest
`.
Before starting to write your tests, you may also be interested on
reading :ref:`how to write testable
services` that interact
with the loop.
For using pytest plugin please install pytest-aiohttp\_ library:
.. code-block:: shell
$ pip install pytest-aiohttp
If you don't want to install \*pytest-aiohttp\* for some reason you may
insert ``pytest\_plugins = 'aiohttp.pytest\_plugin'`` line into
``conftest.py`` instead for the same functionality.
The Test Client and Servers
~~~~~~~~~~~~~~~~~~~~~~~~~~~
\*aiohttp\* test utils provides a scaffolding for testing aiohttp-based
web servers.
They are consist of two parts: running test server and making HTTP
requests to this server.
:class:`~aiohttp.test\_utils.TestServer` runs :class:`aiohttp.web.Application`
based server, :class:`~aiohttp.test\_utils.RawTestServer` starts
:class:`aiohttp.web.Server` low level server.
For performing HTTP requests to these servers you have to create a
test client: :class:`~aiohttp.test\_utils.TestClient` instance.
The client incapsulates :class:`aiohttp.ClientSession` by providing
proxy methods to the client for common operations such as
\*ws\_connect\*, \*get\*, \*post\*, etc.
Pytest
~~~~~~
.. currentmodule:: pytest\_aiohttp
The :data:`aiohttp\_client` fixture available from pytest-aiohttp\_ plugin
allows you to create a client to make requests to test your app.
To run these examples, you need to use `--asyncio-mode=auto` or add to your
pytest config file::
asyncio\_mode = auto
A simple test would be::
from aiohttp import web
async def hello(request):
return web.Response(text='Hello, world')
async def test\_hello(aiohttp\_client):
app = web.Application()
app.router.add\_get('/', hello)
client = await aiohttp\_client(app)
resp = await client.get('/')
assert resp.status == 200
text = await resp.text()
assert 'Hello, world' in text
It also provides access to the app instance allowing tests to check the state
of the app. Tests can be made even more succinct with a fixture to create an
app test client::
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
async def cli(aiohttp\_client):
app = web.Application()
app.router.add\_get('/', previous)
app.router.add\_post('/', previous)
return await aiohttp\_client(app)
async def test\_set\_value(cli):
resp = await cli.post('/', data={'value': 'foo'})
assert resp.status == 200
assert await resp.text() == 'thanks for the data'
assert cli.server.app[value] == 'foo'
async def test\_get\_value(cli):
cli.server.app[value] = 'bar'
resp = await cli.get('/')
assert resp.status == 200
assert await resp.text() == 'value: bar'
Pytest tooling has the following fixtures:
.. data:: aiohttp\_server(app, \*, port=None, \*\*kwargs)
A fixture factory that creates
:class:`~aiohttp.test\_utils.TestServer`::
async def test\_f(aiohttp\_server):
app = web.Application()
# fill route table
server = await aiohttp\_server(app)
The server will be destroyed on exit from test function.
\*app\* is the :class:`aiohttp.web.Application` used
to start server.
\*port\* optional, port the server is run at, if
not provided a random unused port is used.
.. versionadded:: 3.0
\*kwargs\* are parameters passed to
:meth:`aiohttp.web.Application.make\_handler`
.. versionchanged:: 3.0
.. deprecated:: 3.2
The fixture was renamed from ``test\_server`` to ``aiohttp\_server``.
.. data:: aiohttp\_client(app, server\_kwargs=None, \*\*kwargs)
aiohttp\_client(server, \*\*kwargs)
aiohttp\_client(raw\_server, \*\*kwargs)
A fixture factory that creates
:class:`~aiohttp.test\_utils.TestClient` for access to tested server::
async def test\_f(aiohttp\_client):
app = web.Application()
# fill route table
client = await aiohttp\_client(app)
resp = await client.get('/')
\*client\* and responses are cleaned up after test function finishing.
The fixture accepts :class:`aiohttp.web.Application`,
:class:`aiohttp.test\_utils.TestServer` or
:class:`aiohttp.test\_utils.RawTestServer` instance.
\*server\_kwargs\* are parameters passed to the test server if an app
is passed, else ignored.
\*kwargs\* are parameters passed to
:class:`aiohttp.test\_utils.TestClient` constructor.
.. versionchanged:: 3.0
The fixture was renamed from ``test\_client`` to ``aiohttp\_client``.
.. data:: aiohttp\_raw\_server(handler, \*, port=None, \*\*kwargs)
A fixture factory that creates
:class:`~aiohttp.test\_utils.RawTestServer` instance from given web
handler.::
async def test\_f(aiohttp\_raw\_server, aiohttp\_client):
async def handler(request):
return web.Response(text="OK")
raw\_server = await aiohttp\_raw\_server(handler)
client = await aiohttp\_client(raw\_server)
resp = await client.get('/')
\*handler\* should be a coroutine which accepts a request and returns
response, e.g.
\*port\* optional, port the server is run at, if
not provided a random unused port is used.
.. versionadded:: 3.0
.. data:: aiohttp\_unused\_port()
Function to return an unused port number for IPv4 TCP protocol::
async def test\_f(aiohttp\_client, aiohttp\_unused\_port):
port = aiohttp\_unused\_port()
app = web.Application()
# fill route table
client = await aiohttp\_client(app, server\_kwargs={'port': port})
...
.. versionchanged:: 3.0
The fixture was renamed from ``unused\_port`` to ``aiohttp\_unused\_port``.
.. \_aiohttp-testing-unittest-example:
.. \_aiohttp-testing-unittest-style:
Unittest
~~~~~~~~
.. currentmodule:: aiohttp.test\_utils
To test applications with the standard library's unittest or unittest-based
functionality, the AioHTTPTestCase is provided::
from aiohttp.test\_utils import AioHTTPTestCase
from aiohttp import web
class MyAppTestCase(AioHTTPTestCase):
async def get\_application(self):
"""
Override the get\_app method to return your application.
"""
async def hello(request):
return web.Response(text='Hello, world')
app = web.Application()
app.router.add\_get('/', hello)
return app
async def test\_example(self):
async with self.client.request("GET", "/") as resp:
self.assertEqual(resp.status, 200)
text = await resp.text()
self.assertIn("Hello, world", text)
.. class:: AioHTTPTestCase
A base class to allow for unittest web applications using aiohttp.
Derived from :class:`unittest.IsolatedAsyncioTestCase`
See :class:`unittest.TestCase` and :class:`unittest.IsolatedAsyncioTestCase`
for inherited methods and behavior.
This class additionally provides the following:
.. attribute:: client
an aiohttp test client, :class:`TestClient` instance.
.. attribute:: server
an aiohttp test server, :class:`TestServer` instance.
.. versionadded:: 2.3
.. attribute:: app
The application returned by :meth:`~aiohttp.test\_utils.AioHTTPTestCase.get\_application`
(:class:`aiohttp.web.Application` instance).
.. method:: get\_client()
:async:
This async method can be overridden to return the :class:`TestClient`
object used in the test.
:return: :class:`TestClient` instance.
.. versionadded:: 2.3
.. method:: get\_server()
:async:
This async method can be overridden to return the :class:`TestServer`
object used in the test.
:return: :class:`TestServer` instance.
.. versionadded:: 2.3
.. method:: get\_application()
:async:
This async method should be overridden
to return the :class:`aiohttp.web.Application`
object to test.
:return: :class:`aiohttp.web.Application` instance.
.. method:: asyncSetUp()
:async:
This async method can be overridden to execute asynchronous code during
the ``setUp`` stage of the ``TestCase``::
async def asyncSetUp(self):
await super().asyncSetUp()
await foo()
.. versionadded:: 2.3
.. versionchanged:: 3.8
``await super().asyncSetUp()`` call is required.
.. method:: asyncTearDown()
:async:
This async method can be overridden to execute asynchronous code during
the ``tearDown`` stage of the ``TestCase``::
async def asyncTearDown(self):
await super().asyncTearDown()
await foo()
.. versionadded:: 2.3
.. versionchanged:: 3.8
``await super().asyncTearDown()`` call is required.
Faking request object
^^^^^^^^^^^^^^^^^^^^^
aiohttp provides test utility for creating fake
:class:`aiohttp.web.Request` objects:
:func:`aiohttp.test\_utils.make\_mocked\_request`, it could be useful in
case of simple unit tests, like handler tests, or simulate error
conditions that hard to reproduce on real server::
from aiohttp import web
from aiohttp.test\_utils import make\_mocked\_request
def handler(request):
assert request.headers.get('token') == 'x'
return web.Response(body=b'data')
def test\_handler():
req = make\_mocked\_request('GET', '/', headers={'token': 'x'})
resp = handler(req)
assert resp.body == b'data'
.. warning::
We don't recommend to apply
:func:`~aiohttp.test\_utils.make\_mocked\_request` everywhere for
testing web-handler's business object -- please use test client and
real networking via 'localhost' as shown in examples before.
:func:`~aiohttp.test\_utils.make\_mocked\_request` exists only for
testing complex cases (e.g. emulating network errors) which
are extremely hard or even impossible to test by conventional
way.
.. function:: make\_mocked\_request(method, path, headers=None, \*, \
version=HttpVersion(1, 1), \
closing=False, \
app=None, \
match\_info=sentinel, \
reader=sentinel, \
writer=sentinel, \
transport=sentinel, \
payload=sentinel, \
sslcontext=None, \
loop=...)
Creates mocked web.Request testing purposes.
Useful in unit tests, when spinning full web server is overkill or
specific conditions and errors are hard to trigger.
:param method: str, that represents HTTP method, like; GET, POST.
:type method: str
:param path: str, The URL including \*PATH INFO\* without the host or scheme
:type path: str
:param headers: mapping containing the headers. Can be anything accepted
by the multidict.CIMultiDict constructor.
:type headers: dict, multidict.CIMultiDict, list of tuple(str, str)
:param match\_info: mapping containing the info to match with url parameters.
:type match\_info: dict
:param version: namedtuple with encoded HTTP version
:type version: aiohttp.protocol.HttpVersion
:param closing: flag indicates that connection should be closed after
response.
:type closing: bool
:param app: the aiohttp.web application attached for fake request
:type app: aiohttp.web.Application
:param writer: object for managing outcoming data
:type writer: aiohttp.StreamWriter
:param transport: asyncio transport instance
:type transport: asyncio.Transport
:param payload: raw payload reader object
:type payload: aiohttp.StreamReader
:param sslcontext: ssl.SSLContext object, for HTTPS connection
:type sslcontext: ssl.SSLContext
:param loop: An event loop instance, mocked loop by default.
:type loop: :class:`asyncio.AbstractEventLoop`
:return: :class:`aiohttp.web.Request` object.
.. versionadded:: 2.3
\*match\_info\* parameter.
.. \_aiohttp-testing-writing-testable-services:
.. \_aiohttp-testing-framework-agnostic-utilities:
Framework Agnostic Utilities
----------------------------
High level test creation::
from aiohttp.test\_utils import TestClient, TestServer
from aiohttp import request
async def test():
app = \_create\_example\_app()
async with TestClient(TestServer(app)) as client:
async def test\_get\_route():
nonlocal client
resp = await client.get("/")
assert resp.status == 200
text = await resp.text()
assert "Hello, world" in text
await test\_get\_route()
If it's preferred to handle the creation / teardown on a more granular
basis, the TestClient object can be used directly::
from aiohttp.test\_utils import TestClient, TestServer
async def test():
app = \_create\_example\_app()
client = TestClient(TestServer(app))
await client.start\_server()
root = "http://127.0.0.1:{}".format(port)
async def test\_get\_route():
resp = await client.get("/")
assert resp.status == 200
text = await resp.text()
assert "Hello, world" in text
await test\_get\_route()
await client.close()
A full list of the utilities provided can be found at the
:mod:`api reference `
Testing API Reference
---------------------
Test server
~~~~~~~~~~~
Runs given :class:`aiohttp.web.Application` instance on random TCP port.
After creation the server is not started yet, use
:meth:`~aiohttp.test\_utils.BaseTestServer.start\_server` for actual server
starting and :meth:`~aiohttp.test\_utils.BaseTestServer.close` for
stopping/cleanup.
Test server usually works in conjunction with
:class:`aiohttp.test\_utils.TestClient` which provides handy client methods
for accessing to the server.
.. class:: BaseTestServer(\*, scheme='http', host='127.0.0.1', port=None, socket\_factory=get\_port\_socket)
Base class for test servers.
:param str scheme: HTTP scheme, non-protected ``"http"`` by default.
:param str host: a host for TCP socket, IPv4 \*local host\*
(``'127.0.0.1'``) by default.
:param int port: optional port for TCP socket, if not provided a
random unused port is used.
.. versionadded:: 3.0
:param collections.abc.Callable[[str,int,socket.AddressFamily],socket.socket] socket\_factory: optional
Factory to create a socket for the server.
By default creates a TCP socket and binds it
to ``host`` and ``port``.
.. versionadded:: 3.8
.. attribute:: scheme
A \*scheme\* for tested application, ``'http'`` for non-protected
run and ``'https'`` for TLS encrypted server.
.. attribute:: host
\*host\* used to start a test server.
.. attribute:: port
\*port\* used to start the test server.
.. attribute:: handler
:class:`aiohttp.web.Server` used for HTTP requests serving.
.. attribute:: server
:class:`asyncio.AbstractServer` used for managing accepted connections.
.. attribute:: socket\_factory
\*socket\_factory\* used to create and bind a server socket.
.. versionadded:: 3.8
.. method:: start\_server(loop=None, \*\*kwargs)
:async:
:param loop: the event\_loop to use
:type loop: asyncio.AbstractEventLoop
Start a test server.
.. method:: close()
:async:
Stop and finish executed test server.
.. method:: make\_url(path)
Return an \*absolute\* :class:`~yarl.URL` for given \*path\*.
.. class:: RawTestServer(handler, \*, scheme="http", host='127.0.0.1')
Low-level test server (derived from :class:`BaseTestServer`).
:param handler: a coroutine for handling web requests. The
handler should accept
:class:`aiohttp.web.BaseRequest` and return a
response instance,
e.g. :class:`~aiohttp.web.StreamResponse` or
:class:`~aiohttp.web.Response`.
The handler could raise
:class:`~aiohttp.web.HTTPException` as a signal for
non-200 HTTP response.
:param str scheme: HTTP scheme, non-protected ``"http"`` by default.
:param str host: a host for TCP socket, IPv4 \*local host\*
(``'127.0.0.1'``) by default.
:param int port: optional port for TCP socket, if not provided a
random unused port is used.
.. versionadded:: 3.0
.. class:: TestServer(app, \*, scheme="http", host='127.0.0.1')
Test server (derived from :class:`BaseTestServer`) for starting
:class:`~aiohttp.web.Application`.
:param app: :class:`aiohttp.web.Application` instance to run.
:param str scheme: HTTP scheme, non-protected ``"http"`` by default.
:param str host: a host for TCP socket, IPv4 \*local host\*
(``'127.0.0.1'``) by default.
:param int port: optional port for TCP socket, if not provided a
random unused port is used.
.. versionadded:: 3.0
.. attribute:: app
:class:`aiohttp.web.Application` instance to run.
Test Client
~~~~~~~~~~~
.. class:: TestClient(app\_or\_server, \*, loop=None, \
scheme='http', host='127.0.0.1', \
cookie\_jar=None, \*\*kwargs)
A test client used for making calls to tested server.
:param app\_or\_server: :class:`BaseTestServer` instance for making
client requests to it.
In order to pass a :class:`aiohttp.web.Application`
you need to convert it first to :class:`TestServer`
first with ``TestServer(app)``.
:param cookie\_jar: an optional :class:`aiohttp.CookieJar` instance,
may be useful with
``CookieJar(unsafe=True, treat\_as\_secure\_origin="http://127.0.0.1")``
option.
:param str scheme: HTTP scheme, non-protected ``"http"`` by default.
:param asyncio.AbstractEventLoop loop: the event\_loop to use
:param str host: a host for TCP socket, IPv4 \*local host\*
(``'127.0.0.1'``) by default.
.. attribute:: scheme
A \*scheme\* for tested application, ``'http'`` for non-protected
run and ``'https'`` for TLS encrypted server.
.. attribute:: host
\*host\* used to start a test server.
.. attribute:: port
\*port\* used to start the server
.. attribute:: server
:class:`BaseTestServer` test server instance used in conjunction
with client.
.. attribute:: app
An alias for ``self.server.app``. return ``None`` if
``self.server`` is not :class:`TestServer`
instance(e.g. :class:`RawTestServer` instance for test low-level server).
.. attribute:: session
An internal :class:`aiohttp.ClientSession`.
Unlike the methods on the :class:`TestClient`, client session
requests do not automatically include the host in the url
queried, and will require an absolute path to the resource.
.. method:: start\_server(\*\*kwargs)
:async:
Start a test server.
.. method:: close()
:async:
Stop and finish executed test server.
.. method:: make\_url(path)
Return an \*absolute\* :class:`~yarl.URL` for given \*path\*.
.. method:: request(method, path, \*args, \*\*kwargs)
:async:
Routes a request to tested http server.
The interface is identical to
:meth:`aiohttp.ClientSession.request`, except the loop kwarg is
overridden by the instance used by the test server.
.. method:: get(path, \*args, \*\*kwargs)
:async:
Perform an HTTP GET request.
.. method:: post(path, \*args, \*\*kwargs)
:async:
Perform an HTTP POST request.
.. method:: options(path, \*args, \*\*kwargs)
:async:
Perform an HTTP OPTIONS request.
.. method:: head(path, \*args, \*\*kwargs)
:async:
Perform an HTTP HEAD request.
.. method:: put(path, \*args, \*\*kwargs)
:async:
Perform an HTTP PUT request.
.. method:: patch(path, \*args, \*\*kwargs)
:async:
Perform an HTTP PATCH request.
.. method:: delete(path, \*args, \*\*kwargs)
:async:
Perform an HTTP DELETE request.
.. method:: ws\_connect(path, \*args, \*\*kwargs)
:async:
Initiate websocket connection.
The api corresponds to :meth:`aiohttp.ClientSession.ws\_connect`.
Utilities
~~~~~~~~~
.. function:: make\_mocked\_coro(return\_value)
Creates a coroutine mock.
Behaves like a coroutine which returns \*return\_value\*. But it is
also a mock object, you might test it as usual
:class:`~unittest.mock.Mock`::
mocked = make\_mocked\_coro(1)
assert 1 == await mocked(1, 2)
mocked.assert\_called\_with(1, 2)
:param return\_value: A value that the mock object will return when
called.
:returns: A mock object that behaves as a coroutine which returns
\*return\_value\* when called.
.. function:: unused\_port()
Return an unused port number for IPv4 TCP protocol.
:return int: ephemeral port number which could be reused by test server.
.. function:: loop\_context(loop\_factory=)
A contextmanager that creates an event\_loop, for test purposes.
Handles the creation and cleanup of a test loop.
.. function:: setup\_test\_loop(loop\_factory=)
Create and return an :class:`asyncio.AbstractEventLoop` instance.
The caller should also call teardown\_test\_loop, once they are done
with the loop.
.. note::
As side effect the function changes asyncio \*default loop\* by
:func:`asyncio.set\_event\_loop` call.
Previous default loop is not restored.
It should not be a problem for test suite: every test expects a
new test loop instance anyway.
.. versionchanged:: 3.1
The function installs a created event loop as \*default\*.
.. function:: teardown\_test\_loop(loop)
Teardown and cleanup an event\_loop created by setup\_test\_loop.
:param loop: the loop to teardown
:type loop: asyncio.AbstractEventLoop
.. \_pytest: http://pytest.org/latest/
.. \_pytest-aiohttp: https://pypi.python.org/pypi/pytest-aiohttp
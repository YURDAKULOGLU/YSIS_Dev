Client Middleware Cookbook — aiohttp 3.13.3 documentation

# Client Middleware Cookbook[¶](#client-middleware-cookbook "Link to this heading")

This cookbook provides examples of how client middlewares can be used for common use cases.

## Simple Retry Middleware[¶](#simple-retry-middleware "Link to this heading")

It’s very easy to create middlewares that can retry a connection on a given condition:

```
async def retry_middleware(
    req: ClientRequest, handler: ClientHandlerType
) -> ClientResponse:
    for _ in range(3):  # Try up to 3 times
        resp = await handler(req)
        if resp.ok:
            return resp
    return resp
```

Warning

It is recommended to ensure loops are bounded (e.g. using a `for` loop) to avoid
creating an infinite loop.

## Logging to an external service[¶](#logging-to-an-external-service "Link to this heading")

If we needed to log our requests via an API call to an external server or similar, we could
create a simple middleware like this:

```
async def api_logging_middleware(
    req: ClientRequest, handler: ClientHandlerType
) -> ClientResponse:
    # We use middlewares=() to avoid infinite recursion.
    async with req.session.post("/log", data=req.url.host, middlewares=()) as resp:
        if not resp.ok:
            logging.warning("Log endpoint failed")

    return await handler(req)
```

Warning

Using the same session from within a middleware can cause infinite recursion if
that request gets processed again by the middleware.

To avoid such recursion a middleware should typically make requests with
`middlewares=()` or else contain some condition to stop the request triggering
the same logic when it is processed again by the middleware (e.g by whitelisting
the API domain of the request).

## Token Refresh Middleware[¶](#token-refresh-middleware "Link to this heading")

If you need to refresh access tokens to continue accessing an API, this is also a good
candidate for a middleware. For example, you could check for a 401 response, then
refresh the token and retry:

```
class TokenRefresh401Middleware:
    def __init__(self, refresh_token: str, access_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.lock = asyncio.Lock()

    async def __call__(
        self, req: ClientRequest, handler: ClientHandlerType
    ) -> ClientResponse:
        for _ in range(2):  # Retry at most one time
            token = self.access_token
            req.headers["Authorization"] = f"Bearer {token}"
            resp = await handler(req)
            if resp.status != 401:
                return resp
            async with self.lock:
                if token != self.access_token:  # Already refreshed
                    continue
                url = "https://api.example/refresh"
                async with req.session.post(url, data=self.refresh_token) as resp:
                    # Add error handling as needed
                    data = await resp.json()
                    self.access_token = data["access_token"]
        return resp
```

If you have an expiry time for the token, you could refresh at the expiry time, to avoid the
failed request:

```
class TokenRefreshExpiryMiddleware:
    def __init__(self, refresh_token: str):
        self.access_token = ""
        self.expires_at = 0
        self.refresh_token = refresh_token
        self.lock = asyncio.Lock()

    async def __call__(
        self, req: ClientRequest, handler: ClientHandlerType
    ) -> ClientResponse:
        if self.expires_at <= time.time():
            token = self.access_token
            async with self.lock:
                if token == self.access_token:  # Still not refreshed
                    url = "https://api.example/refresh"
                    async with req.session.post(url, data=self.refresh_token) as resp:
                        # Add error handling as needed
                        data = await resp.json()
                        self.access_token = data["access_token"]
                        self.expires_at = data["expires_at"]

        req.headers["Authorization"] = f"Bearer {self.access_token}"
        return await handler(req)
```

Or you could even refresh preemptively in a background task to avoid any API delays. This is probably more
efficient to implement without a middleware:

```
async def token_refresh_preemptively_example() -> None:
    async def set_token(session: ClientSession, event: asyncio.Event) -> None:
        while True:
            async with session.post("/refresh") as resp:
                token = await resp.json()
                session.headers["Authorization"] = f"Bearer {token['auth']}"
                event.set()
                await asyncio.sleep(token["valid_duration"])

    @asynccontextmanager
    async def auto_refresh_client() -> AsyncIterator[ClientSession]:
        async with ClientSession() as session:
            ready = asyncio.Event()
            t = asyncio.create_task(set_token(session, ready))
            await ready.wait()
            yield session
            t.cancel()
            with suppress(asyncio.CancelledError):
                await t

    async with auto_refresh_client() as sess:
        ...
```

Or combine the above approaches to create a more robust solution.

Note

These can also be adjusted to handle proxy auth by modifying
[`ClientRequest.proxy_headers`](client_reference.html#aiohttp.ClientRequest.proxy_headers "aiohttp.ClientRequest.proxy_headers").

## Server-side Request Forgery Protection[¶](#server-side-request-forgery-protection "Link to this heading")

To provide protection against server-side request forgery, we could blacklist any internal
IPs or domains. We could create a middleware that rejects requests made to a blacklist:

```
async def ssrf_middleware(
    req: ClientRequest, handler: ClientHandlerType
) -> ClientResponse:
    # WARNING: This is a simplified example for demonstration purposes only.
    # A complete implementation should also check:
    # - IPv6 loopback (::1)
    # - Private IP ranges (10.x.x.x, 192.168.x.x, 172.16-31.x.x)
    # - Link-local addresses (169.254.x.x, fe80::/10)
    # - Other internal hostnames and aliases
    if req.url.host in {"127.0.0.1", "localhost"}:
        raise SSRFError(req.url.host)
    return await handler(req)
```

Warning

The above example is simplified for demonstration purposes. A production-ready
implementation should also check IPv6 addresses (`::1`), private IP ranges,
link-local addresses, and other internal hostnames. Consider using a well-tested
library for SSRF protection in production environments.

If you know that your services correctly reject requests with an incorrect Host header, then
that may provide sufficient protection. Otherwise, we still have a concern with an attacker’s
own domain resolving to a blacklisted IP. To provide complete protection, we can also
create a custom resolver:

```
class SSRFConnector(TCPConnector):
    async def _resolve_host(
        self, host: str, port: int, traces: Sequence[Trace] | None = None
    ) -> list[ResolveResult]:
        res = await super()._resolve_host(host, port, traces)
        # WARNING: This is a simplified example - should also check ::1, private ranges, etc.
        if any(r["host"] in {"127.0.0.1"} for r in res):
            raise SSRFError()
        return res
```

Using both of these together in a session should provide full SSRF protection.

## Best Practices[¶](#best-practices "Link to this heading")

Important

**Request-level middlewares replace session middlewares**: When you pass `middlewares`
to `request()` or its convenience methods (`get()`, `post()`, etc.), it completely
replaces the session-level middlewares, rather than extending them. This differs from
other parameters like `headers`, which are merged.

```
session = ClientSession(middlewares=[middleware_session])

# Session middleware is used
await session.get("http://example.com")

# Session middleware is NOT used, only request middleware
await session.get("http://example.com", middlewares=[middleware_request])

# To use both, explicitly pass both
await session.get(
    "http://example.com",
    middlewares=[middleware_session, middleware_request]
)
```

1. **Keep middleware focused**: Each middleware should have a single responsibility.
2. **Order matters**: Middlewares execute in the order they’re listed. Place logging first,
   authentication before retry, etc.
3. **Avoid infinite recursion**: When making HTTP requests inside middleware, either:

   * Use `middlewares=()` to disable middleware for internal requests
   * Check the request URL/host to skip middleware for specific endpoints
   * Use a separate session for internal requests
4. **Handle errors gracefully**: Don’t let middleware errors break the request flow unless
   absolutely necessary.
5. **Use bounded loops**: Always use `for` loops with a maximum iteration count instead
   of unbounded `while` loops to prevent infinite retries.
6. **Consider performance**: Each middleware adds overhead. For simple cases like adding
   static headers, consider using session or request parameters instead.
7. **Test thoroughly**: Middleware can affect all requests in subtle ways. Test edge cases
   like network errors, timeouts, and concurrent requests.

## See Also[¶](#see-also "Link to this heading")

* [Client Middleware](client_advanced.html#aiohttp-client-middleware) - Core middleware documentation
* [Advanced Client Usage](client_advanced.html#aiohttp-client-advanced) - Advanced client usage
* [`DigestAuthMiddleware`](client_reference.html#aiohttp.DigestAuthMiddleware "aiohttp.DigestAuthMiddleware") - Built-in digest authentication middleware

[![Logo of aiohttp](_static/aiohttp-plain.svg)](index.html)

# [aiohttp](index.html)

Async HTTP client/server for asyncio and Python

* [![Azure Pipelines CI status](https://github.com/aio-libs/aiohttp/workflows/CI/badge.svg)](https://github.com/aio-libs/aiohttp/actions?query=workflow%3ACI)* [![Code coverage status](https://codecov.io/github/aio-libs/aiohttp/coverage.svg?branch=master)](https://codecov.io/github/aio-libs/aiohttp)* [![Latest PyPI package version](https://badge.fury.io/py/aiohttp.svg)](https://badge.fury.io/py/aiohttp)* [![Chat on Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/aio-libs/Lobby)

### Navigation

* [Client](client.html)
  + [Quickstart](client_quickstart.html)
  + [Advanced Usage](client_advanced.html)
  + [Client Middleware Cookbook](#)
  + [Reference](client_reference.html)
  + [Tracing Reference](tracing_reference.html)
  + [The aiohttp Request Lifecycle](http_request_lifecycle.html)
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
[Page source](_sources/client_middleware_cookbook.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
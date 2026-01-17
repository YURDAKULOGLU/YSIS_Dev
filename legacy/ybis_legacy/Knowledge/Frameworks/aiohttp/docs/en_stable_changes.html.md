Changelog — aiohttp 3.13.3 documentation

# Changelog[¶](#changelog "Link to this heading")

## 3.13.3 (2026-01-03)[¶](#id1 "Link to this heading")

This release contains fixes for several vulnerabilities. It is advised to
upgrade as soon as possible.

### Bug fixes[¶](#bug-fixes "Link to this heading")

* Fixed proxy authorization headers not being passed when reusing a connection, which caused 407 (Proxy authentication required) errors
  – by [@GLeurquin](https://github.com/sponsors/GLeurquin).

  *Related issues and pull requests on GitHub:*
  [#2596](https://github.com/aio-libs/aiohttp/issues/2596).
* Fixed multipart reading failing when encountering an empty body part – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#11857](https://github.com/aio-libs/aiohttp/issues/11857).
* Fixed a case where the parser wasn’t raising an exception for a websocket continuation frame when there was no initial frame in context.

  *Related issues and pull requests on GitHub:*
  [#11862](https://github.com/aio-libs/aiohttp/issues/11862).

### Removals and backward incompatible breaking changes[¶](#removals-and-backward-incompatible-breaking-changes "Link to this heading")

* `Brotli` and `brotlicffi` minimum version is now 1.2.
  Decompression now has a default maximum output size of 32MiB per decompress call – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#11898](https://github.com/aio-libs/aiohttp/issues/11898).

### Packaging updates and notes for downstreams[¶](#packaging-updates-and-notes-for-downstreams "Link to this heading")

* Moved dependency metadata from `setup.cfg` to `pyproject.toml` per [**PEP 621**](https://peps.python.org/pep-0621/)
  – by [@cdce8p](https://github.com/sponsors/cdce8p).

  *Related issues and pull requests on GitHub:*
  [#11643](https://github.com/aio-libs/aiohttp/issues/11643).

### Contributor-facing changes[¶](#contributor-facing-changes "Link to this heading")

* Removed unused `update-pre-commit` github action workflow – by [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#11689](https://github.com/aio-libs/aiohttp/issues/11689).

### Miscellaneous internal changes[¶](#miscellaneous-internal-changes "Link to this heading")

* Optimized web server performance when access logging is disabled by reducing time syscalls – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10713](https://github.com/aio-libs/aiohttp/issues/10713).
* Added regression test for cached logging status – by [@meehand](https://github.com/sponsors/meehand).

  *Related issues and pull requests on GitHub:*
  [#11778](https://github.com/aio-libs/aiohttp/issues/11778).

---

## 3.13.2 (2025-10-28)[¶](#id2 "Link to this heading")

### Bug fixes[¶](#id3 "Link to this heading")

* Fixed cookie parser to continue parsing subsequent cookies when encountering a malformed cookie that fails regex validation, such as Google’s `g_state` cookie with unescaped quotes – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11632](https://github.com/aio-libs/aiohttp/issues/11632).
* Fixed loading netrc credentials from the default `~/.netrc` (`~/_netrc` on Windows) location when the [`NETRC`](glossary.html#envvar-NETRC) environment variable is not set – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11713](https://github.com/aio-libs/aiohttp/issues/11713), [#11714](https://github.com/aio-libs/aiohttp/issues/11714).
* Fixed WebSocket compressed sends to be cancellation safe. Tasks are now shielded during compression to prevent compressor state corruption. This ensures that the stateful compressor remains consistent even when send operations are cancelled – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11725](https://github.com/aio-libs/aiohttp/issues/11725).

---

## 3.13.1 (2025-10-17)[¶](#id4 "Link to this heading")

### Features[¶](#features "Link to this heading")

* Make configuration options in `AppRunner` also available in `run_app()`
  – by [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#11633](https://github.com/aio-libs/aiohttp/issues/11633).

### Bug fixes[¶](#id5 "Link to this heading")

* Switched to backports.zstd for Python <3.14 and fixed zstd decompression for chunked zstd streams – by [@ZhaoMJ](https://github.com/sponsors/ZhaoMJ).

  Note: Users who installed `zstandard` for support on Python <3.14 will now need to install
  `backports.zstd` instead (installing `aiohttp[speedups]` will do this automatically).

  *Related issues and pull requests on GitHub:*
  [#11623](https://github.com/aio-libs/aiohttp/issues/11623).
* Updated `Content-Type` header parsing to return `application/octet-stream` when header contains invalid syntax.
  See [**RFC 9110 Section 8.3-5**](https://datatracker.ietf.org/doc/html/rfc9110.html#section-8.3-5).

  – by [@sgaist](https://github.com/sponsors/sgaist).

  *Related issues and pull requests on GitHub:*
  [#10889](https://github.com/aio-libs/aiohttp/issues/10889).
* Fixed Python 3.14 support when built without `zstd` support – by [@JacobHenner](https://github.com/sponsors/JacobHenner).

  *Related issues and pull requests on GitHub:*
  [#11603](https://github.com/aio-libs/aiohttp/issues/11603).
* Fixed blocking I/O in the event loop when using netrc authentication by moving netrc file lookup to an executor – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11634](https://github.com/aio-libs/aiohttp/issues/11634).
* Fixed routing to a sub-application added via `.add_domain()` not working
  if the same path exists on the parent app. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#11673](https://github.com/aio-libs/aiohttp/issues/11673).

### Packaging updates and notes for downstreams[¶](#id6 "Link to this heading")

* Moved core packaging metadata from `setup.cfg` to `pyproject.toml` per [**PEP 621**](https://peps.python.org/pep-0621/)
  – by [@cdce8p](https://github.com/sponsors/cdce8p).

  *Related issues and pull requests on GitHub:*
  [#9951](https://github.com/aio-libs/aiohttp/issues/9951).

---

## 3.13.0 (2025-10-06)[¶](#id7 "Link to this heading")

### Features[¶](#id8 "Link to this heading")

* Added support for Python 3.14.

  *Related issues and pull requests on GitHub:*
  [#10851](https://github.com/aio-libs/aiohttp/issues/10851), [#10872](https://github.com/aio-libs/aiohttp/issues/10872).
* Added support for free-threading in Python 3.14+ – by [@kumaraditya303](https://github.com/sponsors/kumaraditya303).

  *Related issues and pull requests on GitHub:*
  [#11466](https://github.com/aio-libs/aiohttp/issues/11466), [#11464](https://github.com/aio-libs/aiohttp/issues/11464).
* Added support for Zstandard (aka Zstd) compression
  – by [@KGuillaume-chaps](https://github.com/sponsors/KGuillaume-chaps).

  *Related issues and pull requests on GitHub:*
  [#11161](https://github.com/aio-libs/aiohttp/issues/11161).
* Added `StreamReader.total_raw_bytes` to check the number of bytes downloaded
  – by [@robpats](https://github.com/sponsors/robpats).

  *Related issues and pull requests on GitHub:*
  [#11483](https://github.com/aio-libs/aiohttp/issues/11483).

### Bug fixes[¶](#id9 "Link to this heading")

* Fixed pytest plugin to not use deprecated [`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio "(in Python v3.14)") policy APIs.

  *Related issues and pull requests on GitHub:*
  [#10851](https://github.com/aio-libs/aiohttp/issues/10851).
* Updated Content-Disposition header parsing to handle trailing semicolons and empty parts
  – by [@PLPeeters](https://github.com/sponsors/PLPeeters).

  *Related issues and pull requests on GitHub:*
  [#11243](https://github.com/aio-libs/aiohttp/issues/11243).
* Fixed saved `CookieJar` failing to be loaded if cookies have `partitioned` flag when
  `http.cookie` does not have partitioned cookies supports. – by [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#11523](https://github.com/aio-libs/aiohttp/issues/11523).

### Improved documentation[¶](#improved-documentation "Link to this heading")

* Added `Wireup` to third-party libraries – by [@maldoinc](https://github.com/sponsors/maldoinc).

  *Related issues and pull requests on GitHub:*
  [#11233](https://github.com/aio-libs/aiohttp/issues/11233).

### Packaging updates and notes for downstreams[¶](#id10 "Link to this heading")

* The blockbuster test dependency is now optional; the corresponding test fixture is disabled when it is unavailable
  – by [@musicinybrain](https://github.com/sponsors/musicinybrain).

  *Related issues and pull requests on GitHub:*
  [#11363](https://github.com/aio-libs/aiohttp/issues/11363).
* Added `riscv64` build to releases – by [@eshattow](https://github.com/sponsors/eshattow).

  *Related issues and pull requests on GitHub:*
  [#11425](https://github.com/aio-libs/aiohttp/issues/11425).

### Contributor-facing changes[¶](#id11 "Link to this heading")

* Fixed `test_send_compress_text` failing when alternative zlib implementation
  is used. (`zlib-ng` in python 3.14 windows build) – by [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#11546](https://github.com/aio-libs/aiohttp/issues/11546).

---

## 3.12.15 (2025-07-28)[¶](#id12 "Link to this heading")

### Bug fixes[¶](#id13 "Link to this heading")

* Fixed [`DigestAuthMiddleware`](client_reference.html#aiohttp.DigestAuthMiddleware "aiohttp.DigestAuthMiddleware") to preserve the algorithm case from the server’s challenge in the authorization response. This improves compatibility with servers that perform case-sensitive algorithm matching (e.g., servers expecting `algorithm=MD5-sess` instead of `algorithm=MD5-SESS`)
  – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11352](https://github.com/aio-libs/aiohttp/issues/11352).

### Improved documentation[¶](#id14 "Link to this heading")

* Remove outdated contents of `aiohttp-devtools` and `aiohttp-swagger`
  from Web\_advanced docs.
  – by [@Cycloctane](https://github.com/sponsors/Cycloctane)

  *Related issues and pull requests on GitHub:*
  [#11347](https://github.com/aio-libs/aiohttp/issues/11347).

### Packaging updates and notes for downstreams[¶](#id15 "Link to this heading")

* Started including the `llhttp` `LICENSE` file in wheels by adding `vendor/llhttp/LICENSE` to `license-files` in `setup.cfg` – by [@threexc](https://github.com/sponsors/threexc).

  *Related issues and pull requests on GitHub:*
  [#11226](https://github.com/aio-libs/aiohttp/issues/11226).

### Contributor-facing changes[¶](#id16 "Link to this heading")

* Updated a regex in test\_aiohttp\_request\_coroutine for Python 3.14.

  *Related issues and pull requests on GitHub:*
  [#11271](https://github.com/aio-libs/aiohttp/issues/11271).

---

## 3.12.14 (2025-07-10)[¶](#id17 "Link to this heading")

### Bug fixes[¶](#id18 "Link to this heading")

* Fixed file uploads failing with HTTP 422 errors when encountering 307/308 redirects, and 301/302 redirects for non-POST methods, by preserving the request body when appropriate per [**RFC 9110 Section 15.4.3-3.1**](https://datatracker.ietf.org/doc/html/rfc9110.html#section-15.4.3-3.1) – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11270](https://github.com/aio-libs/aiohttp/issues/11270).
* Fixed [`ClientSession.close()`](client_reference.html#aiohttp.ClientSession.close "aiohttp.ClientSession.close") hanging indefinitely when using HTTPS requests through HTTP proxies – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11273](https://github.com/aio-libs/aiohttp/issues/11273).
* Bumped minimum version of aiosignal to 1.4+ to resolve typing issues – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#11280](https://github.com/aio-libs/aiohttp/issues/11280).

### Features[¶](#id19 "Link to this heading")

* Added initial trailer parsing logic to Python HTTP parser – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#11269](https://github.com/aio-libs/aiohttp/issues/11269).

### Improved documentation[¶](#id20 "Link to this heading")

* Clarified exceptions raised by `WebSocketResponse.send_frame` et al.
  – by [@DoctorJohn](https://github.com/sponsors/DoctorJohn).

  *Related issues and pull requests on GitHub:*
  [#11234](https://github.com/aio-libs/aiohttp/issues/11234).

---

## 3.12.13 (2025-06-14)[¶](#id21 "Link to this heading")

### Bug fixes[¶](#id22 "Link to this heading")

* Fixed auto-created [`TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") not using the session’s event loop when [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") is created without an explicit connector – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11147](https://github.com/aio-libs/aiohttp/issues/11147).

---

## 3.12.12 (2025-06-09)[¶](#id23 "Link to this heading")

### Bug fixes[¶](#id24 "Link to this heading")

* Fixed cookie unquoting to properly handle octal escape sequences in cookie values (e.g., `\012` for newline) by vendoring the correct `_unquote` implementation from Python’s `http.cookies` module – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11173](https://github.com/aio-libs/aiohttp/issues/11173).
* Fixed `Cookie` header parsing to treat attribute names as regular cookies per [**RFC 6265 Section 5.4**](https://datatracker.ietf.org/doc/html/rfc6265.html#section-5.4) – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11178](https://github.com/aio-libs/aiohttp/issues/11178).

---

## 3.12.11 (2025-06-07)[¶](#id25 "Link to this heading")

### Features[¶](#id26 "Link to this heading")

* Improved SSL connection handling by changing the default `ssl_shutdown_timeout`
  from `0.1` to `0` seconds. SSL connections now use Python’s default graceful
  shutdown during normal operation but are aborted immediately when the connector
  is closed, providing optimal behavior for both cases. Also added support for
  `ssl_shutdown_timeout=0` on all Python versions. Previously, this value was
  rejected on Python 3.11+ and ignored on earlier versions. Non-zero values on
  Python < 3.11 now trigger a `RuntimeWarning` – by [@bdraco](https://github.com/sponsors/bdraco).

  The `ssl_shutdown_timeout` parameter is now deprecated and will be removed in
  aiohttp 4.0 as there is no clear use case for changing the default.

  *Related issues and pull requests on GitHub:*
  [#11148](https://github.com/aio-libs/aiohttp/issues/11148).

### Deprecations (removal in next major release)[¶](#deprecations-removal-in-next-major-release "Link to this heading")

* Improved SSL connection handling by changing the default `ssl_shutdown_timeout`
  from `0.1` to `0` seconds. SSL connections now use Python’s default graceful
  shutdown during normal operation but are aborted immediately when the connector
  is closed, providing optimal behavior for both cases. Also added support for
  `ssl_shutdown_timeout=0` on all Python versions. Previously, this value was
  rejected on Python 3.11+ and ignored on earlier versions. Non-zero values on
  Python < 3.11 now trigger a `RuntimeWarning` – by [@bdraco](https://github.com/sponsors/bdraco).

  The `ssl_shutdown_timeout` parameter is now deprecated and will be removed in
  aiohttp 4.0 as there is no clear use case for changing the default.

  *Related issues and pull requests on GitHub:*
  [#11148](https://github.com/aio-libs/aiohttp/issues/11148).

---

## 3.12.10 (2025-06-07)[¶](#id27 "Link to this heading")

### Bug fixes[¶](#id28 "Link to this heading")

* Fixed leak of `aiodns.DNSResolver` when [`TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") is closed and no resolver was passed when creating the connector – by [@Tasssadar](https://github.com/sponsors/Tasssadar).

  This was a regression introduced in version 3.12.0 ([PR #10897](https://github.com/aio-libs/aiohttp/pull/10897)).

  *Related issues and pull requests on GitHub:*
  [#11150](https://github.com/aio-libs/aiohttp/issues/11150).

---

## 3.12.9 (2025-06-04)[¶](#id29 "Link to this heading")

### Bug fixes[¶](#id30 "Link to this heading")

* Fixed `IOBasePayload` and `TextIOPayload` reading entire files into memory when streaming large files – by [@bdraco](https://github.com/sponsors/bdraco).

  When using file-like objects with the aiohttp client, the entire file would be read into memory if the file size was provided in the `Content-Length` header. This could cause out-of-memory errors when uploading large files. The payload classes now correctly read data in chunks of `READ_SIZE` (64KB) regardless of the total content length.

  *Related issues and pull requests on GitHub:*
  [#11138](https://github.com/aio-libs/aiohttp/issues/11138).

---

## 3.12.8 (2025-06-04)[¶](#id31 "Link to this heading")

### Features[¶](#id32 "Link to this heading")

* Added preemptive digest authentication to [`DigestAuthMiddleware`](client_reference.html#aiohttp.DigestAuthMiddleware "aiohttp.DigestAuthMiddleware") – by [@bdraco](https://github.com/sponsors/bdraco).

  The middleware now reuses authentication credentials for subsequent requests to the same
  protection space, improving efficiency by avoiding extra authentication round trips.
  This behavior matches how web browsers handle digest authentication and follows
  [**RFC 7616 Section 3.6**](https://datatracker.ietf.org/doc/html/rfc7616.html#section-3.6).

  Preemptive authentication is enabled by default but can be disabled by passing
  `preemptive=False` to the middleware constructor.

  *Related issues and pull requests on GitHub:*
  [#11128](https://github.com/aio-libs/aiohttp/issues/11128), [#11129](https://github.com/aio-libs/aiohttp/issues/11129).

---

## 3.12.7 (2025-06-02)[¶](#id33 "Link to this heading")

Warning

This release fixes an issue where the `quote_cookie` parameter was not being properly
respected for shared cookies (domain=””, path=””). If your server does not handle quoted
cookies correctly, you may need to disable cookie quoting by setting `quote_cookie=False`
when creating your [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") or [`CookieJar`](client_reference.html#aiohttp.CookieJar "aiohttp.CookieJar").
See [Cookie Quoting Routine](client_advanced.html#aiohttp-client-cookie-quoting-routine) for details.

### Bug fixes[¶](#id34 "Link to this heading")

* Fixed cookie parsing to be more lenient when handling cookies with special characters
  in names or values. Cookies with characters like `{`, `}`, and `/` in names are now
  accepted instead of causing a [`CookieError`](https://docs.python.org/3/library/http.cookies.html#http.cookies.CookieError "(in Python v3.14)") and 500 errors. Additionally,
  cookies with mismatched quotes in values are now parsed correctly, and quoted cookie
  values are now handled consistently whether or not they include special attributes
  like `Domain`. Also fixed [`CookieJar`](client_reference.html#aiohttp.CookieJar "aiohttp.CookieJar") to ensure shared cookies (domain=””, path=””)
  respect the `quote_cookie` parameter, making cookie quoting behavior consistent for
  all cookies – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#2683](https://github.com/aio-libs/aiohttp/issues/2683), [#5397](https://github.com/aio-libs/aiohttp/issues/5397), [#7993](https://github.com/aio-libs/aiohttp/issues/7993), [#11112](https://github.com/aio-libs/aiohttp/issues/11112).
* Fixed an issue where cookies with duplicate names but different domains or paths
  were lost when updating the cookie jar. The [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession")
  cookie jar now correctly stores all cookies even if they have the same name but
  different domain or path, following the [**RFC 6265 Section 5.3**](https://datatracker.ietf.org/doc/html/rfc6265.html#section-5.3) storage model – by [@bdraco](https://github.com/sponsors/bdraco).

  Note that [`ClientResponse.cookies`](client_reference.html#aiohttp.ClientResponse.cookies "aiohttp.ClientResponse.cookies") returns
  a [`SimpleCookie`](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie "(in Python v3.14)") which uses the cookie name as a key, so
  only the last cookie with each name is accessible via this interface. All cookies
  can be accessed via [`ClientResponse.headers.getall('Set-Cookie')`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.MultiDictProxy.getall "(in multidict v6.7)") if needed.

  *Related issues and pull requests on GitHub:*
  [#4486](https://github.com/aio-libs/aiohttp/issues/4486), [#11105](https://github.com/aio-libs/aiohttp/issues/11105), [#11106](https://github.com/aio-libs/aiohttp/issues/11106).

### Miscellaneous internal changes[¶](#id35 "Link to this heading")

* Avoided creating closed futures in `ResponseHandler` that will never be awaited – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11107](https://github.com/aio-libs/aiohttp/issues/11107).
* Downgraded the logging level for connector close errors from ERROR to DEBUG, as these are expected behavior with TLS 1.3 connections – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11114](https://github.com/aio-libs/aiohttp/issues/11114).

---

## 3.12.6 (2025-05-31)[¶](#id36 "Link to this heading")

### Bug fixes[¶](#id37 "Link to this heading")

* Fixed spurious “Future exception was never retrieved” warnings for connection lost errors when the connector is not closed – by [@bdraco](https://github.com/sponsors/bdraco).

  When connections are lost, the exception is now marked as retrieved since it is always propagated through other means, preventing unnecessary warnings in logs.

  *Related issues and pull requests on GitHub:*
  [#11100](https://github.com/aio-libs/aiohttp/issues/11100).

---

## 3.12.5 (2025-05-30)[¶](#id38 "Link to this heading")

### Features[¶](#id39 "Link to this heading")

* Added `ssl_shutdown_timeout` parameter to [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") and [`TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") to control the grace period for SSL shutdown handshake on TLS connections. This helps prevent “connection reset” errors on the server side while avoiding excessive delays during connector cleanup. Note: This parameter only takes effect on Python 3.11+ – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11091](https://github.com/aio-libs/aiohttp/issues/11091), [#11094](https://github.com/aio-libs/aiohttp/issues/11094).

### Miscellaneous internal changes[¶](#id40 "Link to this heading")

* Improved performance of isinstance checks by using collections.abc types instead of typing module equivalents – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#11085](https://github.com/aio-libs/aiohttp/issues/11085), [#11088](https://github.com/aio-libs/aiohttp/issues/11088).

---

## 3.12.4 (2025-05-28)[¶](#id41 "Link to this heading")

### Bug fixes[¶](#id42 "Link to this heading")

* Fixed connector not waiting for connections to close before returning from [`close()`](client_reference.html#aiohttp.BaseConnector.close "aiohttp.BaseConnector.close") (partial backport of [PR #3733](https://github.com/aio-libs/aiohttp/pull/3733)) – by [@atemate](https://github.com/sponsors/atemate) and [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#1925](https://github.com/aio-libs/aiohttp/issues/1925), [#11074](https://github.com/aio-libs/aiohttp/issues/11074).

---

## 3.12.3 (2025-05-28)[¶](#id43 "Link to this heading")

### Bug fixes[¶](#id44 "Link to this heading")

* Fixed memory leak in [`filter_cookies()`](client_reference.html#aiohttp.CookieJar.filter_cookies "aiohttp.CookieJar.filter_cookies") that caused unbounded memory growth
  when making requests to different URL paths – by [@bdraco](https://github.com/sponsors/bdraco) and [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#11052](https://github.com/aio-libs/aiohttp/issues/11052), [#11054](https://github.com/aio-libs/aiohttp/issues/11054).

---

## 3.12.2 (2025-05-26)[¶](#id45 "Link to this heading")

### Bug fixes[¶](#id46 "Link to this heading")

* Fixed `Content-Length` header not being set to `0` for non-GET requests with `None` body – by [@bdraco](https://github.com/sponsors/bdraco).

  Non-GET requests (`POST`, `PUT`, `PATCH`, `DELETE`) with `None` as the body now correctly set the `Content-Length` header to `0`, matching the behavior of requests with empty bytes (`b""`). This regression was introduced in aiohttp 3.12.1.

  *Related issues and pull requests on GitHub:*
  [#11035](https://github.com/aio-libs/aiohttp/issues/11035).

---

## 3.12.1 (2025-05-26)[¶](#id47 "Link to this heading")

### Features[¶](#id48 "Link to this heading")

* Added support for reusable request bodies to enable retries, redirects, and digest authentication – by [@bdraco](https://github.com/sponsors/bdraco) and [@GLGDLY](https://github.com/sponsors/GLGDLY).

  Most payloads can now be safely reused multiple times, fixing long-standing issues where POST requests with form data or file uploads would fail on redirects with errors like “Form data has been processed already” or “I/O operation on closed file”. This also enables digest authentication to work with request bodies and allows retry mechanisms to resend requests without consuming the payload. Note that payloads derived from async iterables may still not be reusable in some cases.

  *Related issues and pull requests on GitHub:*
  [#5530](https://github.com/aio-libs/aiohttp/issues/5530), [#5577](https://github.com/aio-libs/aiohttp/issues/5577), [#9201](https://github.com/aio-libs/aiohttp/issues/9201), [#11017](https://github.com/aio-libs/aiohttp/issues/11017).

---

## 3.12.0 (2025-05-24)[¶](#id49 "Link to this heading")

### Bug fixes[¶](#id50 "Link to this heading")

* Fixed [`prepared`](web_reference.html#aiohttp.web.WebSocketResponse.prepared "aiohttp.web.WebSocketResponse.prepared") property to correctly reflect the prepared state, especially during timeout scenarios – by [@bdraco](https://github.com/sponsors/bdraco)

  *Related issues and pull requests on GitHub:*
  [#6009](https://github.com/aio-libs/aiohttp/issues/6009), [#10988](https://github.com/aio-libs/aiohttp/issues/10988).
* Response is now always True, instead of using MutableMapping behaviour (False when map is empty)

  *Related issues and pull requests on GitHub:*
  [#10119](https://github.com/aio-libs/aiohttp/issues/10119).
* Fixed connection reuse for file-like data payloads by ensuring buffer
  truncation respects content-length boundaries and preventing premature
  connection closure race – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10325](https://github.com/aio-libs/aiohttp/issues/10325), [#10915](https://github.com/aio-libs/aiohttp/issues/10915), [#10941](https://github.com/aio-libs/aiohttp/issues/10941), [#10943](https://github.com/aio-libs/aiohttp/issues/10943).
* Fixed pytest plugin to not use deprecated [`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio "(in Python v3.14)") policy APIs.

  *Related issues and pull requests on GitHub:*
  [#10851](https://github.com/aio-libs/aiohttp/issues/10851).
* Fixed `AsyncResolver` not using the `loop` argument in versions 3.x where it should still be supported – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10951](https://github.com/aio-libs/aiohttp/issues/10951).

### Features[¶](#id51 "Link to this heading")

* Added a comprehensive HTTP Digest Authentication client middleware (DigestAuthMiddleware)
  that implements RFC 7616. The middleware supports all standard hash algorithms
  (MD5, SHA, SHA-256, SHA-512) with session variants, handles both ‘auth’ and
  ‘auth-int’ quality of protection options, and automatically manages the
  authentication flow by intercepting 401 responses and retrying with proper
  credentials – by [@feus4177](https://github.com/sponsors/feus4177), [@TimMenninger](https://github.com/sponsors/TimMenninger), and [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#2213](https://github.com/aio-libs/aiohttp/issues/2213), [#10725](https://github.com/aio-libs/aiohttp/issues/10725).
* Added client middleware support – by [@bdraco](https://github.com/sponsors/bdraco) and [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  This change allows users to add middleware to the client session and requests, enabling features like
  authentication, logging, and request/response modification without modifying the core
  request logic. Additionally, the `session` attribute was added to `ClientRequest`,
  allowing middleware to access the session for making additional requests.

  *Related issues and pull requests on GitHub:*
  [#9732](https://github.com/aio-libs/aiohttp/issues/9732), [#10902](https://github.com/aio-libs/aiohttp/issues/10902), [#10945](https://github.com/aio-libs/aiohttp/issues/10945), [#10952](https://github.com/aio-libs/aiohttp/issues/10952), [#10959](https://github.com/aio-libs/aiohttp/issues/10959), [#10968](https://github.com/aio-libs/aiohttp/issues/10968).
* Allow user setting zlib compression backend – by [@TimMenninger](https://github.com/sponsors/TimMenninger)

  This change allows the user to call [`aiohttp.set_zlib_backend()`](client_reference.html#aiohttp.set_zlib_backend "aiohttp.set_zlib_backend") with the
  zlib compression module of their choice. Default behavior continues to use
  the builtin `zlib` library.

  *Related issues and pull requests on GitHub:*
  [#9798](https://github.com/aio-libs/aiohttp/issues/9798).
* Added support for overriding the base URL with an absolute one in client sessions
  – by [@vivodi](https://github.com/sponsors/vivodi).

  *Related issues and pull requests on GitHub:*
  [#10074](https://github.com/aio-libs/aiohttp/issues/10074).
* Added `host` parameter to `aiohttp_server` fixture – by [@christianwbrock](https://github.com/sponsors/christianwbrock).

  *Related issues and pull requests on GitHub:*
  [#10120](https://github.com/aio-libs/aiohttp/issues/10120).
* Detect blocking calls in coroutines using BlockBuster – by [@cbornet](https://github.com/sponsors/cbornet).

  *Related issues and pull requests on GitHub:*
  [#10433](https://github.com/aio-libs/aiohttp/issues/10433).
* Added `socket_factory` to [`aiohttp.TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") to allow specifying custom socket options
  – by [@TimMenninger](https://github.com/sponsors/TimMenninger).

  *Related issues and pull requests on GitHub:*
  [#10474](https://github.com/aio-libs/aiohttp/issues/10474), [#10520](https://github.com/aio-libs/aiohttp/issues/10520), [#10961](https://github.com/aio-libs/aiohttp/issues/10961), [#10962](https://github.com/aio-libs/aiohttp/issues/10962).
* Started building armv7l manylinux wheels – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10797](https://github.com/aio-libs/aiohttp/issues/10797).
* Implemented shared DNS resolver management to fix excessive resolver object creation
  when using multiple client sessions. The new `_DNSResolverManager` singleton ensures
  only one `DNSResolver` object is created for default configurations, significantly
  reducing resource usage and improving performance for applications using multiple
  client sessions simultaneously – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10847](https://github.com/aio-libs/aiohttp/issues/10847), [#10923](https://github.com/aio-libs/aiohttp/issues/10923), [#10946](https://github.com/aio-libs/aiohttp/issues/10946).
* Upgraded to LLHTTP 9.3.0 – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#10972](https://github.com/aio-libs/aiohttp/issues/10972).
* Optimized small HTTP requests/responses by coalescing headers and body into a single TCP packet – by [@bdraco](https://github.com/sponsors/bdraco).

  This change enhances network efficiency by reducing the number of packets sent for small HTTP payloads, improving latency and reducing overhead. Most importantly, this fixes compatibility with memory-constrained IoT devices that can only perform a single read operation and expect HTTP requests in one packet. The optimization uses zero-copy `writelines` when coalescing data and works with both regular and chunked transfer encoding.

  When `aiohttp` uses client middleware to communicate with an `aiohttp` server, connection reuse is more likely to occur since complete responses arrive in a single packet for small payloads.

  This aligns `aiohttp` with other popular HTTP clients that already coalesce small requests.

  *Related issues and pull requests on GitHub:*
  [#10991](https://github.com/aio-libs/aiohttp/issues/10991).

### Improved documentation[¶](#id52 "Link to this heading")

* Improved documentation for middleware by adding warnings and examples about
  request body stream consumption. The documentation now clearly explains that
  request body streams can only be read once and provides best practices for
  sharing parsed request data between middleware and handlers – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#2914](https://github.com/aio-libs/aiohttp/issues/2914).

### Packaging updates and notes for downstreams[¶](#id53 "Link to this heading")

* Removed non SPDX-license description from `setup.cfg` – by [@devanshu-ziphq](https://github.com/sponsors/devanshu-ziphq).

  *Related issues and pull requests on GitHub:*
  [#10662](https://github.com/aio-libs/aiohttp/issues/10662).
* Added support for building against system `llhttp` library – by [@mgorny](https://github.com/sponsors/mgorny).

  This change adds support for [`AIOHTTP_USE_SYSTEM_DEPS`](glossary.html#envvar-AIOHTTP_USE_SYSTEM_DEPS) environment variable that
  can be used to build aiohttp against the system install of the `llhttp` library rather
  than the vendored one.

  *Related issues and pull requests on GitHub:*
  [#10759](https://github.com/aio-libs/aiohttp/issues/10759).
* `aiodns` is now installed on Windows with speedups extra – by [@bdraco](https://github.com/sponsors/bdraco).

  As of `aiodns` 3.3.0, `SelectorEventLoop` is no longer required when using `pycares` 4.7.0 or later.

  *Related issues and pull requests on GitHub:*
  [#10823](https://github.com/aio-libs/aiohttp/issues/10823).
* Fixed compatibility issue with Cython 3.1.1 – by [@bdraco](https://github.com/sponsors/bdraco)

  *Related issues and pull requests on GitHub:*
  [#10877](https://github.com/aio-libs/aiohttp/issues/10877).

### Contributor-facing changes[¶](#id54 "Link to this heading")

* Sped up tests by disabling `blockbuster` fixture for `test_static_file_huge` and `test_static_file_huge_cancel` tests – by [@dikos1337](https://github.com/sponsors/dikos1337).

  *Related issues and pull requests on GitHub:*
  [#9705](https://github.com/aio-libs/aiohttp/issues/9705), [#10761](https://github.com/aio-libs/aiohttp/issues/10761).
* Updated tests to avoid using deprecated [`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio "(in Python v3.14)") policy APIs and
  make it compatible with Python 3.14.

  *Related issues and pull requests on GitHub:*
  [#10851](https://github.com/aio-libs/aiohttp/issues/10851).
* Added Winloop to test suite to support in the future – by [@Vizonex](https://github.com/sponsors/Vizonex).

  *Related issues and pull requests on GitHub:*
  [#10922](https://github.com/aio-libs/aiohttp/issues/10922).

### Miscellaneous internal changes[¶](#id55 "Link to this heading")

* Added support for the `partitioned` attribute in the `set_cookie` method.

  *Related issues and pull requests on GitHub:*
  [#9870](https://github.com/aio-libs/aiohttp/issues/9870).
* Setting [`aiohttp.web.StreamResponse.last_modified`](web_reference.html#aiohttp.web.StreamResponse.last_modified "aiohttp.web.StreamResponse.last_modified") to an unsupported type will now raise [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") instead of silently failing – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10146](https://github.com/aio-libs/aiohttp/issues/10146).

---

## 3.11.18 (2025-04-20)[¶](#id56 "Link to this heading")

### Bug fixes[¶](#id57 "Link to this heading")

* Disabled TLS in TLS warning (when using HTTPS proxies) for uvloop and newer Python versions – by [@lezgomatt](https://github.com/sponsors/lezgomatt).

  *Related issues and pull requests on GitHub:*
  [#7686](https://github.com/aio-libs/aiohttp/issues/7686).
* Fixed reading fragmented WebSocket messages when the payload was masked – by [@bdraco](https://github.com/sponsors/bdraco).

  The problem first appeared in 3.11.17

  *Related issues and pull requests on GitHub:*
  [#10764](https://github.com/aio-libs/aiohttp/issues/10764).

---

## 3.11.17 (2025-04-19)[¶](#id58 "Link to this heading")

### Miscellaneous internal changes[¶](#id59 "Link to this heading")

* Optimized web server performance when access logging is disabled by reducing time syscalls – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10713](https://github.com/aio-libs/aiohttp/issues/10713).
* Improved web server performance when connection can be reused – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10714](https://github.com/aio-libs/aiohttp/issues/10714).
* Improved performance of the WebSocket reader – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10740](https://github.com/aio-libs/aiohttp/issues/10740).
* Improved performance of the WebSocket reader with large messages – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10744](https://github.com/aio-libs/aiohttp/issues/10744).

---

## 3.11.16 (2025-04-01)[¶](#id60 "Link to this heading")

### Bug fixes[¶](#id61 "Link to this heading")

* Replaced deprecated `asyncio.iscoroutinefunction` with its counterpart from `inspect`
  – by [@layday](https://github.com/sponsors/layday).

  *Related issues and pull requests on GitHub:*
  [#10634](https://github.com/aio-libs/aiohttp/issues/10634).
* Fixed [`multidict.CIMultiDict`](https://multidict.aio-libs.org/en/stable/multidict/#multidict.CIMultiDict "(in multidict v6.7)") being mutated when passed to [`aiohttp.web.Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response") – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10672](https://github.com/aio-libs/aiohttp/issues/10672).

---

## 3.11.15 (2025-03-31)[¶](#id62 "Link to this heading")

### Bug fixes[¶](#id63 "Link to this heading")

* Reverted explicitly closing sockets if an exception is raised during `create_connection` – by [@bdraco](https://github.com/sponsors/bdraco).

  This change originally appeared in aiohttp 3.11.13

  *Related issues and pull requests on GitHub:*
  [#10464](https://github.com/aio-libs/aiohttp/issues/10464), [#10617](https://github.com/aio-libs/aiohttp/issues/10617), [#10656](https://github.com/aio-libs/aiohttp/issues/10656).

### Miscellaneous internal changes[¶](#id64 "Link to this heading")

* Improved performance of WebSocket buffer handling – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10601](https://github.com/aio-libs/aiohttp/issues/10601).
* Improved performance of serializing headers – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10625](https://github.com/aio-libs/aiohttp/issues/10625).

---

## 3.11.14 (2025-03-16)[¶](#id65 "Link to this heading")

### Bug fixes[¶](#id66 "Link to this heading")

* Fixed an issue where dns queries were delayed indefinitely when an exception occurred in a `trace.send_dns_cache_miss`
  – by [@logioniz](https://github.com/sponsors/logioniz).

  *Related issues and pull requests on GitHub:*
  [#10529](https://github.com/aio-libs/aiohttp/issues/10529).
* Fixed DNS resolution on platforms that don’t support `socket.AI_ADDRCONFIG` – by [@maxbachmann](https://github.com/sponsors/maxbachmann).

  *Related issues and pull requests on GitHub:*
  [#10542](https://github.com/aio-libs/aiohttp/issues/10542).
* The connector now raises [`aiohttp.ClientConnectionError`](client_reference.html#aiohttp.ClientConnectionError "aiohttp.ClientConnectionError") instead of [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError "(in Python v3.14)") when failing to explicitly close the socket after [`asyncio.loop.create_connection()`](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.create_connection "(in Python v3.14)") fails – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10551](https://github.com/aio-libs/aiohttp/issues/10551).
* Break cyclic references at connection close when there was a traceback – by [@bdraco](https://github.com/sponsors/bdraco).

  Special thanks to [@availov](https://github.com/sponsors/availov) for reporting the issue.

  *Related issues and pull requests on GitHub:*
  [#10556](https://github.com/aio-libs/aiohttp/issues/10556).
* Break cyclic references when there is an exception handling a request – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10569](https://github.com/aio-libs/aiohttp/issues/10569).

### Features[¶](#id67 "Link to this heading")

* Improved logging on non-overlapping WebSocket client protocols to include the remote address – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10564](https://github.com/aio-libs/aiohttp/issues/10564).

### Miscellaneous internal changes[¶](#id68 "Link to this heading")

* Improved performance of parsing content types by adding a cache in the same manner currently done with mime types – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10552](https://github.com/aio-libs/aiohttp/issues/10552).

---

## 3.11.13 (2025-02-24)[¶](#id69 "Link to this heading")

### Bug fixes[¶](#id70 "Link to this heading")

* Removed a break statement inside the finally block in `RequestHandler`
  – by [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#10434](https://github.com/aio-libs/aiohttp/issues/10434).
* Changed connection creation to explicitly close sockets if an exception is raised in the event loop’s `create_connection` method – by [@top-oai](https://github.com/sponsors/top-oai).

  *Related issues and pull requests on GitHub:*
  [#10464](https://github.com/aio-libs/aiohttp/issues/10464).

### Packaging updates and notes for downstreams[¶](#id71 "Link to this heading")

* Fixed test `test_write_large_payload_deflate_compression_data_in_eof_writelines` failing with Python 3.12.9+ or 3.13.2+ – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10423](https://github.com/aio-libs/aiohttp/issues/10423).

### Miscellaneous internal changes[¶](#id72 "Link to this heading")

* Added human-readable error messages to the exceptions for WebSocket disconnects due to PONG not being received – by [@bdraco](https://github.com/sponsors/bdraco).

  Previously, the error messages were empty strings, which made it hard to determine what went wrong.

  *Related issues and pull requests on GitHub:*
  [#10422](https://github.com/aio-libs/aiohttp/issues/10422).

---

## 3.11.12 (2025-02-05)[¶](#id73 "Link to this heading")

### Bug fixes[¶](#id74 "Link to this heading")

* `MultipartForm.decode()` now follows RFC1341 7.2.1 with a `CRLF` after the boundary
  – by [@imnotjames](https://github.com/sponsors/imnotjames).

  *Related issues and pull requests on GitHub:*
  [#10270](https://github.com/aio-libs/aiohttp/issues/10270).
* Restored the missing `total_bytes` attribute to `EmptyStreamReader` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10387](https://github.com/aio-libs/aiohttp/issues/10387).

### Features[¶](#id75 "Link to this heading")

* Updated [`request()`](client_reference.html#aiohttp.request "aiohttp.request") to make it accept `_RequestOptions` kwargs.
  – by [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#10300](https://github.com/aio-libs/aiohttp/issues/10300).
* Improved logging of HTTP protocol errors to include the remote address – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10332](https://github.com/aio-libs/aiohttp/issues/10332).

### Improved documentation[¶](#id76 "Link to this heading")

* Added `aiohttp-openmetrics` to list of third-party libraries – by [@jelmer](https://github.com/sponsors/jelmer).

  *Related issues and pull requests on GitHub:*
  [#10304](https://github.com/aio-libs/aiohttp/issues/10304).

### Packaging updates and notes for downstreams[¶](#id77 "Link to this heading")

* Added missing files to the source distribution to fix `Makefile` targets.
  Added a `cythonize-nodeps` target to run Cython without invoking pip to install dependencies.

  *Related issues and pull requests on GitHub:*
  [#10366](https://github.com/aio-libs/aiohttp/issues/10366).
* Started building armv7l musllinux wheels – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10404](https://github.com/aio-libs/aiohttp/issues/10404).

### Contributor-facing changes[¶](#id78 "Link to this heading")

* The CI/CD workflow has been updated to use upload-artifact v4 and download-artifact v4 GitHub Actions – by [@silamon](https://github.com/sponsors/silamon).

  *Related issues and pull requests on GitHub:*
  [#10281](https://github.com/aio-libs/aiohttp/issues/10281).

### Miscellaneous internal changes[¶](#id79 "Link to this heading")

* Restored support for zero copy writes when using Python 3.12 versions 3.12.9 and later or Python 3.13.2+ – by [@bdraco](https://github.com/sponsors/bdraco).

  Zero copy writes were previously disabled due to [**CVE 2024-12254**](https://www.cve.org/CVERecord?id=CVE-2024-12254) which is resolved in these Python versions.

  *Related issues and pull requests on GitHub:*
  [#10137](https://github.com/aio-libs/aiohttp/issues/10137).

---

## 3.11.11 (2024-12-18)[¶](#id80 "Link to this heading")

### Bug fixes[¶](#id81 "Link to this heading")

* Updated [`request()`](client_reference.html#aiohttp.ClientSession.request "aiohttp.ClientSession.request") to reuse the `quote_cookie` setting from `ClientSession._cookie_jar` when processing cookies parameter.
  – by [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#10093](https://github.com/aio-libs/aiohttp/issues/10093).
* Fixed type of `SSLContext` for some static type checkers (e.g. pyright).

  *Related issues and pull requests on GitHub:*
  [#10099](https://github.com/aio-libs/aiohttp/issues/10099).
* Updated [`aiohttp.web.StreamResponse.write()`](web_reference.html#aiohttp.web.StreamResponse.write "aiohttp.web.StreamResponse.write") annotation to also allow [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)") and [`memoryview`](https://docs.python.org/3/library/stdtypes.html#memoryview "(in Python v3.14)") as inputs – by [@cdce8p](https://github.com/sponsors/cdce8p).

  *Related issues and pull requests on GitHub:*
  [#10154](https://github.com/aio-libs/aiohttp/issues/10154).
* Fixed a hang where a connection previously used for a streaming
  download could be returned to the pool in a paused state.
  – by [@javitonino](https://github.com/sponsors/javitonino).

  *Related issues and pull requests on GitHub:*
  [#10169](https://github.com/aio-libs/aiohttp/issues/10169).

### Features[¶](#id82 "Link to this heading")

* Enabled ALPN on default SSL contexts. This improves compatibility with some
  proxies which don’t work without this extension.
  – by [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#10156](https://github.com/aio-libs/aiohttp/issues/10156).

### Miscellaneous internal changes[¶](#id83 "Link to this heading")

* Fixed an infinite loop that can occur when using aiohttp in combination
  with [async-solipsism](https://github.com/bmerry/async-solipsism) – by [@bmerry](https://github.com/sponsors/bmerry).

  *Related issues and pull requests on GitHub:*
  [#10149](https://github.com/aio-libs/aiohttp/issues/10149).

---

## 3.11.10 (2024-12-05)[¶](#id84 "Link to this heading")

### Bug fixes[¶](#id85 "Link to this heading")

* Fixed race condition in [`aiohttp.web.FileResponse`](web_reference.html#aiohttp.web.FileResponse "aiohttp.web.FileResponse") that could have resulted in an incorrect response if the file was replaced on the file system during `prepare` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10101](https://github.com/aio-libs/aiohttp/issues/10101), [#10113](https://github.com/aio-libs/aiohttp/issues/10113).
* Replaced deprecated call to [`mimetypes.guess_type()`](https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type "(in Python v3.14)") with [`mimetypes.guess_file_type()`](https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_file_type "(in Python v3.14)") when using Python 3.13+ – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10102](https://github.com/aio-libs/aiohttp/issues/10102).
* Disabled zero copy writes in the `StreamWriter` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10125](https://github.com/aio-libs/aiohttp/issues/10125).

---

## 3.11.9 (2024-12-01)[¶](#id86 "Link to this heading")

### Bug fixes[¶](#id87 "Link to this heading")

* Fixed invalid method logging unexpected being logged at exception level on subsequent connections – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10055](https://github.com/aio-libs/aiohttp/issues/10055), [#10076](https://github.com/aio-libs/aiohttp/issues/10076).

### Miscellaneous internal changes[¶](#id88 "Link to this heading")

* Improved performance of parsing headers when using the C parser – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10073](https://github.com/aio-libs/aiohttp/issues/10073).

---

## 3.11.8 (2024-11-27)[¶](#id89 "Link to this heading")

### Miscellaneous internal changes[¶](#id90 "Link to this heading")

* Improved performance of creating [`aiohttp.ClientResponse`](client_reference.html#aiohttp.ClientResponse "aiohttp.ClientResponse") objects when there are no cookies – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10029](https://github.com/aio-libs/aiohttp/issues/10029).
* Improved performance of creating [`aiohttp.ClientResponse`](client_reference.html#aiohttp.ClientResponse "aiohttp.ClientResponse") objects – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10030](https://github.com/aio-libs/aiohttp/issues/10030).
* Improved performances of creating objects during the HTTP request lifecycle – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10037](https://github.com/aio-libs/aiohttp/issues/10037).
* Improved performance of constructing [`aiohttp.web.Response`](web_reference.html#aiohttp.web.Response "aiohttp.web.Response") with headers – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10043](https://github.com/aio-libs/aiohttp/issues/10043).
* Improved performance of making requests when there are no auto headers to skip – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10049](https://github.com/aio-libs/aiohttp/issues/10049).
* Downgraded logging of invalid HTTP method exceptions on the first request to debug level – by [@bdraco](https://github.com/sponsors/bdraco).

  HTTP requests starting with an invalid method are relatively common, especially when connected to the public internet, because browsers or other clients may try to speak SSL to a plain-text server or vice-versa. These exceptions can quickly fill the log with noise when nothing is wrong.

  *Related issues and pull requests on GitHub:*
  [#10055](https://github.com/aio-libs/aiohttp/issues/10055).

---

## 3.11.7 (2024-11-21)[¶](#id91 "Link to this heading")

### Bug fixes[¶](#id92 "Link to this heading")

* Fixed the HTTP client not considering the connector’s `force_close` value when setting the `Connection` header – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10003](https://github.com/aio-libs/aiohttp/issues/10003).

### Miscellaneous internal changes[¶](#id93 "Link to this heading")

* Improved performance of serializing HTTP headers – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#10014](https://github.com/aio-libs/aiohttp/issues/10014).

---

## 3.11.6 (2024-11-19)[¶](#id94 "Link to this heading")

### Bug fixes[¶](#id95 "Link to this heading")

* Restored the `force_close` method to the `ResponseHandler` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9997](https://github.com/aio-libs/aiohttp/issues/9997).

---

## 3.11.5 (2024-11-19)[¶](#id96 "Link to this heading")

### Bug fixes[¶](#id97 "Link to this heading")

* Fixed the `ANY` method not appearing in [`routes()`](web_reference.html#aiohttp.web.UrlDispatcher.routes "aiohttp.web.UrlDispatcher.routes") – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9899](https://github.com/aio-libs/aiohttp/issues/9899), [#9987](https://github.com/aio-libs/aiohttp/issues/9987).

---

## 3.11.4 (2024-11-18)[¶](#id98 "Link to this heading")

### Bug fixes[¶](#id99 "Link to this heading")

* Fixed `StaticResource` not allowing the `OPTIONS` method after calling `set_options_route` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9972](https://github.com/aio-libs/aiohttp/issues/9972), [#9975](https://github.com/aio-libs/aiohttp/issues/9975), [#9976](https://github.com/aio-libs/aiohttp/issues/9976).

### Miscellaneous internal changes[¶](#id100 "Link to this heading")

* Improved performance of creating web responses when there are no cookies – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9895](https://github.com/aio-libs/aiohttp/issues/9895).

---

## 3.11.3 (2024-11-18)[¶](#id101 "Link to this heading")

### Bug fixes[¶](#id102 "Link to this heading")

* Removed non-existing `__author__` from `dir(aiohttp)` – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9918](https://github.com/aio-libs/aiohttp/issues/9918).
* Restored the `FlowControlDataQueue` class – by [@bdraco](https://github.com/sponsors/bdraco).

  This class is no longer used internally, and will be permanently removed in the next major version.

  *Related issues and pull requests on GitHub:*
  [#9963](https://github.com/aio-libs/aiohttp/issues/9963).

### Miscellaneous internal changes[¶](#id103 "Link to this heading")

* Improved performance of resolving resources when multiple methods are registered for the same route – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9899](https://github.com/aio-libs/aiohttp/issues/9899).

---

## 3.11.2 (2024-11-14)[¶](#id104 "Link to this heading")

### Bug fixes[¶](#id105 "Link to this heading")

* Fixed improperly closed WebSocket connections generating an unhandled exception – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9883](https://github.com/aio-libs/aiohttp/issues/9883).

---

## 3.11.1 (2024-11-14)[¶](#id106 "Link to this heading")

### Bug fixes[¶](#id107 "Link to this heading")

* Added a backward compatibility layer to [`aiohttp.RequestInfo`](client_reference.html#aiohttp.RequestInfo "aiohttp.RequestInfo") to allow creating these objects without a `real_url` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9873](https://github.com/aio-libs/aiohttp/issues/9873).

---

## 3.11.0 (2024-11-13)[¶](#id108 "Link to this heading")

### Bug fixes[¶](#id109 "Link to this heading")

* Raise [`aiohttp.ServerFingerprintMismatch`](client_reference.html#aiohttp.ServerFingerprintMismatch "aiohttp.ServerFingerprintMismatch") exception on client-side if request through http proxy with mismatching server fingerprint digest: aiohttp.ClientSession(headers=headers, connector=TCPConnector(ssl=aiohttp.Fingerprint(mismatch\_digest), trust\_env=True).request(…) – by [@gangj](https://github.com/sponsors/gangj).

  *Related issues and pull requests on GitHub:*
  [#6652](https://github.com/aio-libs/aiohttp/issues/6652).
* Modified websocket [`aiohttp.ClientWebSocketResponse.receive_str()`](client_reference.html#aiohttp.ClientWebSocketResponse.receive_str "aiohttp.ClientWebSocketResponse.receive_str"), [`aiohttp.ClientWebSocketResponse.receive_bytes()`](client_reference.html#aiohttp.ClientWebSocketResponse.receive_bytes "aiohttp.ClientWebSocketResponse.receive_bytes"), [`aiohttp.web.WebSocketResponse.receive_str()`](web_reference.html#aiohttp.web.WebSocketResponse.receive_str "aiohttp.web.WebSocketResponse.receive_str") & [`aiohttp.web.WebSocketResponse.receive_bytes()`](web_reference.html#aiohttp.web.WebSocketResponse.receive_bytes "aiohttp.web.WebSocketResponse.receive_bytes") methods to raise new [`aiohttp.WSMessageTypeError`](client_reference.html#aiohttp.WSMessageTypeError "aiohttp.WSMessageTypeError") exception, instead of generic [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)"), when websocket messages of incorrect types are received – by [@ara-25](https://github.com/sponsors/ara-25).

  *Related issues and pull requests on GitHub:*
  [#6800](https://github.com/aio-libs/aiohttp/issues/6800).
* Made `TestClient.app` a `Generic` so type checkers will know the correct type (avoiding unneeded `client.app is not None` checks) – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8977](https://github.com/aio-libs/aiohttp/issues/8977).
* Fixed the keep-alive connection pool to be FIFO instead of LIFO – by [@bdraco](https://github.com/sponsors/bdraco).

  Keep-alive connections are more likely to be reused before they disconnect.

  *Related issues and pull requests on GitHub:*
  [#9672](https://github.com/aio-libs/aiohttp/issues/9672).

### Features[¶](#id110 "Link to this heading")

* Added `strategy` parameter to [`aiohttp.web.StreamResponse.enable_compression()`](web_reference.html#aiohttp.web.StreamResponse.enable_compression "aiohttp.web.StreamResponse.enable_compression")
  The value of this parameter is passed to the [`zlib.compressobj()`](https://docs.python.org/3/library/zlib.html#zlib.compressobj "(in Python v3.14)") function, allowing people
  to use a more sufficient compression algorithm for their data served by [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web")
  – by [@shootkin](https://github.com/sponsors/shootkin)

  *Related issues and pull requests on GitHub:*
  [#6257](https://github.com/aio-libs/aiohttp/issues/6257).
* Added `server_hostname` parameter to `ws_connect`.

  *Related issues and pull requests on GitHub:*
  [#7941](https://github.com/aio-libs/aiohttp/issues/7941).
* Exported [`ClientWSTimeout`](client_reference.html#aiohttp.ClientWSTimeout "aiohttp.ClientWSTimeout") to top-level namespace – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8612](https://github.com/aio-libs/aiohttp/issues/8612).
* Added `secure`/`httponly`/`samesite` parameters to `.del_cookie()` – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8956](https://github.com/aio-libs/aiohttp/issues/8956).
* Updated [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession")’s auth logic to include default auth only if the request URL’s origin matches \_base\_url; otherwise, the auth will not be included – by [@MaximZemskov](https://github.com/sponsors/MaximZemskov)

  *Related issues and pull requests on GitHub:*
  [#8966](https://github.com/aio-libs/aiohttp/issues/8966), [#9466](https://github.com/aio-libs/aiohttp/issues/9466).
* Added `proxy` and `proxy_auth` parameters to [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") – by [@meshya](https://github.com/sponsors/meshya).

  *Related issues and pull requests on GitHub:*
  [#9207](https://github.com/aio-libs/aiohttp/issues/9207).
* Added `default_to_multipart` parameter to `FormData`.

  *Related issues and pull requests on GitHub:*
  [#9335](https://github.com/aio-libs/aiohttp/issues/9335).
* Added [`send_frame()`](client_reference.html#aiohttp.ClientWebSocketResponse.send_frame "aiohttp.ClientWebSocketResponse.send_frame") and [`send_frame()`](web_reference.html#aiohttp.web.WebSocketResponse.send_frame "aiohttp.web.WebSocketResponse.send_frame") for WebSockets – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9348](https://github.com/aio-libs/aiohttp/issues/9348).
* Updated [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") to support paths in `base_url` parameter.
  `base_url` paths must end with a `/` – by [@Cycloctane](https://github.com/sponsors/Cycloctane).

  *Related issues and pull requests on GitHub:*
  [#9530](https://github.com/aio-libs/aiohttp/issues/9530).
* Improved performance of reading WebSocket messages with a Cython implementation – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9543](https://github.com/aio-libs/aiohttp/issues/9543), [#9554](https://github.com/aio-libs/aiohttp/issues/9554), [#9556](https://github.com/aio-libs/aiohttp/issues/9556), [#9558](https://github.com/aio-libs/aiohttp/issues/9558), [#9636](https://github.com/aio-libs/aiohttp/issues/9636), [#9649](https://github.com/aio-libs/aiohttp/issues/9649), [#9781](https://github.com/aio-libs/aiohttp/issues/9781).
* Added `writer_limit` to the [`WebSocketResponse`](web_reference.html#aiohttp.web.WebSocketResponse "aiohttp.web.WebSocketResponse") to be able to adjust the limit before the writer forces the buffer to be drained – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9572](https://github.com/aio-libs/aiohttp/issues/9572).
* Added an [`enabled`](abc.html#aiohttp.abc.AbstractAccessLogger.enabled "aiohttp.abc.AbstractAccessLogger.enabled") property to [`aiohttp.abc.AbstractAccessLogger`](abc.html#aiohttp.abc.AbstractAccessLogger "aiohttp.abc.AbstractAccessLogger") to dynamically check if logging is enabled – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9822](https://github.com/aio-libs/aiohttp/issues/9822).

### Deprecations (removal in next major release)[¶](#id111 "Link to this heading")

* Deprecate obsolete timeout: float and receive\_timeout: Optional[float] in [`ws_connect()`](client_reference.html#aiohttp.ClientSession.ws_connect "aiohttp.ClientSession.ws_connect"). Change default websocket receive timeout from None to 10.0.

  *Related issues and pull requests on GitHub:*
  [#3945](https://github.com/aio-libs/aiohttp/issues/3945).

### Removals and backward incompatible breaking changes[¶](#id112 "Link to this heading")

* Dropped support for Python 3.8 – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8797](https://github.com/aio-libs/aiohttp/issues/8797).
* Increased minimum yarl version to 1.17.0 – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8909](https://github.com/aio-libs/aiohttp/issues/8909), [#9079](https://github.com/aio-libs/aiohttp/issues/9079), [#9305](https://github.com/aio-libs/aiohttp/issues/9305), [#9574](https://github.com/aio-libs/aiohttp/issues/9574).
* Removed the `is_ipv6_address` and `is_ip4_address` helpers are they are no longer used – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9344](https://github.com/aio-libs/aiohttp/issues/9344).
* Changed `ClientRequest.connection_key` to be a NamedTuple to improve client performance – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9365](https://github.com/aio-libs/aiohttp/issues/9365).
* `FlowControlDataQueue` has been replaced with the `WebSocketDataQueue` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9685](https://github.com/aio-libs/aiohttp/issues/9685).
* Changed `ClientRequest.request_info` to be a NamedTuple to improve client performance – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9692](https://github.com/aio-libs/aiohttp/issues/9692).

### Packaging updates and notes for downstreams[¶](#id113 "Link to this heading")

* Switched to using the [`propcache`](https://propcache.aio-libs.org/en/stable/api/#module-propcache.api "(in propcache v0.4)") package for property caching
  – by [@bdraco](https://github.com/sponsors/bdraco).

  The [`propcache`](https://propcache.aio-libs.org/en/stable/api/#module-propcache.api "(in propcache v0.4)") package is derived from the property caching
  code in [`yarl`](https://yarl.aio-libs.org/en/stable/api/#module-yarl "(in yarl v1.23)") and has been broken out to avoid maintaining it for multiple
  projects.

  *Related issues and pull requests on GitHub:*
  [#9394](https://github.com/aio-libs/aiohttp/issues/9394).
* Separated `aiohttp.http_websocket` into multiple files to make it easier to maintain – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9542](https://github.com/aio-libs/aiohttp/issues/9542), [#9552](https://github.com/aio-libs/aiohttp/issues/9552).

### Contributor-facing changes[¶](#id114 "Link to this heading")

* Changed diagram images generator from `blockdiag` to `GraphViz`.
  Generating documentation now requires the GraphViz executable to be included in $PATH or sphinx build configuration.

  *Related issues and pull requests on GitHub:*
  [#9359](https://github.com/aio-libs/aiohttp/issues/9359).

### Miscellaneous internal changes[¶](#id115 "Link to this heading")

* Added flake8 settings to avoid some forms of implicit concatenation. – by [@booniepepper](https://github.com/sponsors/booniepepper).

  *Related issues and pull requests on GitHub:*
  [#7731](https://github.com/aio-libs/aiohttp/issues/7731).
* Enabled keep-alive support on proxies (which was originally disabled several years ago) – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8920](https://github.com/aio-libs/aiohttp/issues/8920).
* Changed web entry point to not listen on TCP when only a Unix path is passed – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9033](https://github.com/aio-libs/aiohttp/issues/9033).
* Disabled automatic retries of failed requests in [`aiohttp.test_utils.TestClient`](testing.html#aiohttp.test_utils.TestClient "aiohttp.test_utils.TestClient")’s client session
  (which could potentially hide errors in tests) – by [@ShubhAgarwal-dev](https://github.com/sponsors/ShubhAgarwal-dev).

  *Related issues and pull requests on GitHub:*
  [#9141](https://github.com/aio-libs/aiohttp/issues/9141).
* Changed web `keepalive_timeout` default to around an hour in order to reduce race conditions on reverse proxies – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9285](https://github.com/aio-libs/aiohttp/issues/9285).
* Reduced memory required for stream objects created during the client request lifecycle – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9407](https://github.com/aio-libs/aiohttp/issues/9407).
* Improved performance of the internal `DataQueue` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9659](https://github.com/aio-libs/aiohttp/issues/9659).
* Improved performance of calling `receive` for WebSockets for the most common message types – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9679](https://github.com/aio-libs/aiohttp/issues/9679).
* Replace internal helper methods `method_must_be_empty_body` and `status_code_must_be_empty_body` with simple set lookups – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9722](https://github.com/aio-libs/aiohttp/issues/9722).
* Improved performance of [`aiohttp.BaseConnector`](client_reference.html#aiohttp.BaseConnector "aiohttp.BaseConnector") when there is no `limit_per_host` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9756](https://github.com/aio-libs/aiohttp/issues/9756).
* Improved performance of sending HTTP requests when there is no body – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9757](https://github.com/aio-libs/aiohttp/issues/9757).
* Improved performance of the `WebsocketWriter` when the protocol is not paused – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9796](https://github.com/aio-libs/aiohttp/issues/9796).
* Implemented zero copy writes for `StreamWriter` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9839](https://github.com/aio-libs/aiohttp/issues/9839).

---

## 3.10.11 (2024-11-13)[¶](#id116 "Link to this heading")

### Bug fixes[¶](#id117 "Link to this heading")

* Authentication provided by a redirect now takes precedence over provided `auth` when making requests with the client – by [@PLPeeters](https://github.com/sponsors/PLPeeters).

  *Related issues and pull requests on GitHub:*
  [#9436](https://github.com/aio-libs/aiohttp/issues/9436).
* Fixed [`WebSocketResponse.close()`](web_reference.html#aiohttp.web.WebSocketResponse.close "aiohttp.web.WebSocketResponse.close") to discard non-close messages within its timeout window after sending close – by [@lenard-mosys](https://github.com/sponsors/lenard-mosys).

  *Related issues and pull requests on GitHub:*
  [#9506](https://github.com/aio-libs/aiohttp/issues/9506).
* Fixed a deadlock that could occur while attempting to get a new connection slot after a timeout – by [@bdraco](https://github.com/sponsors/bdraco).

  The connector was not cancellation-safe.

  *Related issues and pull requests on GitHub:*
  [#9670](https://github.com/aio-libs/aiohttp/issues/9670), [#9671](https://github.com/aio-libs/aiohttp/issues/9671).
* Fixed the WebSocket flow control calculation undercounting with multi-byte data – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9686](https://github.com/aio-libs/aiohttp/issues/9686).
* Fixed incorrect parsing of chunk extensions with the pure Python parser – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9851](https://github.com/aio-libs/aiohttp/issues/9851).
* Fixed system routes polluting the middleware cache – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9852](https://github.com/aio-libs/aiohttp/issues/9852).

### Removals and backward incompatible breaking changes[¶](#id118 "Link to this heading")

* Improved performance of the connector when a connection can be reused – by [@bdraco](https://github.com/sponsors/bdraco).

  If `BaseConnector.connect` has been subclassed and replaced with custom logic, the `ceil_timeout` must be added.

  *Related issues and pull requests on GitHub:*
  [#9600](https://github.com/aio-libs/aiohttp/issues/9600).

### Miscellaneous internal changes[¶](#id119 "Link to this heading")

* Improved performance of the client request lifecycle when there are no cookies – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9470](https://github.com/aio-libs/aiohttp/issues/9470).
* Improved performance of sending client requests when the writer can finish synchronously – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9485](https://github.com/aio-libs/aiohttp/issues/9485).
* Improved performance of serializing HTTP headers – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9603](https://github.com/aio-libs/aiohttp/issues/9603).
* Passing `enable_cleanup_closed` to [`aiohttp.TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") is now ignored on Python 3.12.7+ and 3.13.1+ since the underlying bug that caused asyncio to leak SSL connections has been fixed upstream – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9726](https://github.com/aio-libs/aiohttp/issues/9726), [#9736](https://github.com/aio-libs/aiohttp/issues/9736).

---

## 3.10.10 (2024-10-10)[¶](#id120 "Link to this heading")

### Bug fixes[¶](#id121 "Link to this heading")

* Fixed error messages from `AsyncResolver` being swallowed – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9451](https://github.com/aio-libs/aiohttp/issues/9451), [#9455](https://github.com/aio-libs/aiohttp/issues/9455).

### Features[¶](#id122 "Link to this heading")

* Added [`aiohttp.ClientConnectorDNSError`](client_reference.html#aiohttp.ClientConnectorDNSError "aiohttp.ClientConnectorDNSError") for differentiating DNS resolution errors from other connector errors – by [@mstojcevich](https://github.com/sponsors/mstojcevich).

  *Related issues and pull requests on GitHub:*
  [#8455](https://github.com/aio-libs/aiohttp/issues/8455).

### Miscellaneous internal changes[¶](#id123 "Link to this heading")

* Simplified DNS resolution throttling code to reduce chance of race conditions – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9454](https://github.com/aio-libs/aiohttp/issues/9454).

---

## 3.10.9 (2024-10-04)[¶](#id124 "Link to this heading")

### Bug fixes[¶](#id125 "Link to this heading")

* Fixed proxy headers being used in the `ConnectionKey` hash when a proxy was not being used – by [@bdraco](https://github.com/sponsors/bdraco).

  If default headers are used, they are also used for proxy headers. This could have led to creating connections that were not needed when one was already available.

  *Related issues and pull requests on GitHub:*
  [#9368](https://github.com/aio-libs/aiohttp/issues/9368).
* Widened the type of the `trace_request_ctx` parameter of
  [`ClientSession.request()`](client_reference.html#aiohttp.ClientSession.request "aiohttp.ClientSession.request") and friends
  – by [@layday](https://github.com/sponsors/layday).

  *Related issues and pull requests on GitHub:*
  [#9397](https://github.com/aio-libs/aiohttp/issues/9397).

### Removals and backward incompatible breaking changes[¶](#id126 "Link to this heading")

* Fixed failure to try next host after single-host connection timeout – by [@brettdh](https://github.com/sponsors/brettdh).

  The default client [`aiohttp.ClientTimeout`](client_reference.html#aiohttp.ClientTimeout "aiohttp.ClientTimeout") params has changed to include a `sock_connect` timeout of 30 seconds so that this correct behavior happens by default.

  *Related issues and pull requests on GitHub:*
  [#7342](https://github.com/aio-libs/aiohttp/issues/7342).

### Miscellaneous internal changes[¶](#id127 "Link to this heading")

* Improved performance of resolving hosts with Python 3.12+ – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9342](https://github.com/aio-libs/aiohttp/issues/9342).
* Reduced memory required for timer objects created during the client request lifecycle – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9406](https://github.com/aio-libs/aiohttp/issues/9406).

---

## 3.10.8 (2024-09-28)[¶](#id128 "Link to this heading")

### Bug fixes[¶](#id129 "Link to this heading")

* Fixed cancellation leaking upwards on timeout – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9326](https://github.com/aio-libs/aiohttp/issues/9326).

---

## 3.10.7 (2024-09-27)[¶](#id130 "Link to this heading")

### Bug fixes[¶](#id131 "Link to this heading")

* Fixed assembling the [`URL`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL "(in yarl v1.23)") for web requests when the host contains a non-default port or IPv6 address – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9309](https://github.com/aio-libs/aiohttp/issues/9309).

### Miscellaneous internal changes[¶](#id132 "Link to this heading")

* Improved performance of determining if a URL is absolute – by [@bdraco](https://github.com/sponsors/bdraco).

  The property [`absolute`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL.absolute "(in yarl v1.23)") is more performant than the method `URL.is_absolute()` and preferred when newer versions of yarl are used.

  *Related issues and pull requests on GitHub:*
  [#9171](https://github.com/aio-libs/aiohttp/issues/9171).
* Replaced code that can now be handled by `yarl` – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9301](https://github.com/aio-libs/aiohttp/issues/9301).

---

## 3.10.6 (2024-09-24)[¶](#id133 "Link to this heading")

### Bug fixes[¶](#id134 "Link to this heading")

* Added [`aiohttp.ClientConnectionResetError`](client_reference.html#aiohttp.ClientConnectionResetError "aiohttp.ClientConnectionResetError"). Client code that previously threw [`ConnectionResetError`](https://docs.python.org/3/library/exceptions.html#ConnectionResetError "(in Python v3.14)")
  will now throw this – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9137](https://github.com/aio-libs/aiohttp/issues/9137).
* Fixed an unclosed transport `ResourceWarning` on web handlers – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8875](https://github.com/aio-libs/aiohttp/issues/8875).
* Fixed resolve\_host() ‘Task was destroyed but is pending’ errors – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8967](https://github.com/aio-libs/aiohttp/issues/8967).
* Fixed handling of some file-like objects (e.g. `tarfile.extractfile()`) which raise `AttributeError` instead of `OSError` when `fileno` fails for streaming payload data – by [@ReallyReivax](https://github.com/sponsors/ReallyReivax).

  *Related issues and pull requests on GitHub:*
  [#6732](https://github.com/aio-libs/aiohttp/issues/6732).
* Fixed web router not matching pre-encoded URLs (requires yarl 1.9.6+) – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8898](https://github.com/aio-libs/aiohttp/issues/8898), [#9267](https://github.com/aio-libs/aiohttp/issues/9267).
* Fixed an error when trying to add a route for multiple methods with a path containing a regex pattern – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8998](https://github.com/aio-libs/aiohttp/issues/8998).
* Fixed `Response.text` when body is a `Payload` – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#6485](https://github.com/aio-libs/aiohttp/issues/6485).
* Fixed compressed requests failing when no body was provided – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9108](https://github.com/aio-libs/aiohttp/issues/9108).
* Fixed client incorrectly reusing a connection when the previous message had not been fully sent – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8992](https://github.com/aio-libs/aiohttp/issues/8992).
* Fixed race condition that could cause server to close connection incorrectly at keepalive timeout – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9140](https://github.com/aio-libs/aiohttp/issues/9140).
* Fixed Python parser chunked handling with multiple Transfer-Encoding values – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8823](https://github.com/aio-libs/aiohttp/issues/8823).
* Fixed error handling after 100-continue so server sends 500 response instead of disconnecting – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8876](https://github.com/aio-libs/aiohttp/issues/8876).
* Stopped adding a default Content-Type header when response has no content – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8858](https://github.com/aio-libs/aiohttp/issues/8858).
* Added support for URL credentials with empty (zero-length) username, e.g. `https://:password@host` – by [@shuckc](https://github.com/sponsors/shuckc)

  *Related issues and pull requests on GitHub:*
  [#6494](https://github.com/aio-libs/aiohttp/issues/6494).
* Stopped logging exceptions from `web.run_app()` that would be raised regardless – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#6807](https://github.com/aio-libs/aiohttp/issues/6807).
* Implemented binding to IPv6 addresses in the pytest server fixture.

  *Related issues and pull requests on GitHub:*
  [#4650](https://github.com/aio-libs/aiohttp/issues/4650).
* Fixed the incorrect use of flags for `getnameinfo()` in the Resolver –by [@GitNMLee](https://github.com/sponsors/GitNMLee)

  Link-Local IPv6 addresses can now be handled by the Resolver correctly.

  *Related issues and pull requests on GitHub:*
  [#9032](https://github.com/aio-libs/aiohttp/issues/9032).
* Fixed StreamResponse.prepared to return True after EOF is sent – by [@arthurdarcet](https://github.com/sponsors/arthurdarcet).

  *Related issues and pull requests on GitHub:*
  [#5343](https://github.com/aio-libs/aiohttp/issues/5343).
* Changed `make_mocked_request()` to use empty payload by default – by [@rahulnht](https://github.com/sponsors/rahulnht).

  *Related issues and pull requests on GitHub:*
  [#7167](https://github.com/aio-libs/aiohttp/issues/7167).
* Used more precise type for `ClientResponseError.headers`, fixing some type errors when using them – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8768](https://github.com/aio-libs/aiohttp/issues/8768).
* Changed behavior when returning an invalid response to send a 500 response – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8845](https://github.com/aio-libs/aiohttp/issues/8845).
* Fixed response reading from closed session to throw an error immediately instead of timing out – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8878](https://github.com/aio-libs/aiohttp/issues/8878).
* Fixed `CancelledError` from one cleanup context stopping other contexts from completing – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8908](https://github.com/aio-libs/aiohttp/issues/8908).
* Fixed changing scheme/host in `Response.clone()` for absolute URLs – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8990](https://github.com/aio-libs/aiohttp/issues/8990).
* Fixed `Site.name` when host is an empty string – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8929](https://github.com/aio-libs/aiohttp/issues/8929).
* Updated Python parser to reject messages after a close message, matching C parser behaviour – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9018](https://github.com/aio-libs/aiohttp/issues/9018).
* Fixed creation of `SSLContext` inside of [`aiohttp.TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") with multiple event loops in different threads – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9029](https://github.com/aio-libs/aiohttp/issues/9029).
* Fixed (on Python 3.11+) some edge cases where a task cancellation may get incorrectly suppressed – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9030](https://github.com/aio-libs/aiohttp/issues/9030).
* Fixed exception information getting lost on `HttpProcessingError` – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9052](https://github.com/aio-libs/aiohttp/issues/9052).
* Fixed `If-None-Match` not using weak comparison – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9063](https://github.com/aio-libs/aiohttp/issues/9063).
* Fixed badly encoded charset crashing when getting response text instead of falling back to charset detector.

  *Related issues and pull requests on GitHub:*
  [#9160](https://github.com/aio-libs/aiohttp/issues/9160).
* Rejected n in reason values to avoid sending broken HTTP messages – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9167](https://github.com/aio-libs/aiohttp/issues/9167).
* Changed [`ClientResponse.raise_for_status()`](client_reference.html#aiohttp.ClientResponse.raise_for_status "aiohttp.ClientResponse.raise_for_status") to only release the connection when invoked outside an `async with` context – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9239](https://github.com/aio-libs/aiohttp/issues/9239).

### Features[¶](#id135 "Link to this heading")

* Improved type on `params` to match the underlying type allowed by `yarl` – by [@lpetre](https://github.com/sponsors/lpetre).

  *Related issues and pull requests on GitHub:*
  [#8564](https://github.com/aio-libs/aiohttp/issues/8564).
* Declared Python 3.13 supported – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8748](https://github.com/aio-libs/aiohttp/issues/8748).

### Removals and backward incompatible breaking changes[¶](#id136 "Link to this heading")

* Improved middleware performance – by [@bdraco](https://github.com/sponsors/bdraco).

  The `set_current_app` method was removed from `UrlMappingMatchInfo` because it is no longer used, and it was unlikely external caller would ever use it.

  *Related issues and pull requests on GitHub:*
  [#9200](https://github.com/aio-libs/aiohttp/issues/9200).
* Increased minimum yarl version to 1.12.0 – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9267](https://github.com/aio-libs/aiohttp/issues/9267).

### Improved documentation[¶](#id137 "Link to this heading")

* Clarified that `GracefulExit` needs to be handled in `AppRunner` and `ServerRunner` when using `handle_signals=True`. – by [@Daste745](https://github.com/sponsors/Daste745)

  *Related issues and pull requests on GitHub:*
  [#4414](https://github.com/aio-libs/aiohttp/issues/4414).
* Clarified that auth parameter in ClientSession will persist and be included with any request to any origin, even during redirects to different origins. – by [@MaximZemskov](https://github.com/sponsors/MaximZemskov).

  *Related issues and pull requests on GitHub:*
  [#6764](https://github.com/aio-libs/aiohttp/issues/6764).
* Clarified which timeout exceptions happen on which timeouts – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8968](https://github.com/aio-libs/aiohttp/issues/8968).
* Updated `ClientSession` parameters to match current code – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8991](https://github.com/aio-libs/aiohttp/issues/8991).

### Packaging updates and notes for downstreams[¶](#id138 "Link to this heading")

* Fixed `test_client_session_timeout_zero` to not require internet access – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#9004](https://github.com/aio-libs/aiohttp/issues/9004).

### Miscellaneous internal changes[¶](#id139 "Link to this heading")

* Improved performance of making requests when there are no auto headers to skip – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8847](https://github.com/aio-libs/aiohttp/issues/8847).
* Exported `aiohttp.TraceRequestHeadersSentParams` – by [@Hadock-is-ok](https://github.com/sponsors/Hadock-is-ok).

  *Related issues and pull requests on GitHub:*
  [#8947](https://github.com/aio-libs/aiohttp/issues/8947).
* Avoided tracing overhead in the http writer when there are no active traces – by user:bdraco.

  *Related issues and pull requests on GitHub:*
  [#9031](https://github.com/aio-libs/aiohttp/issues/9031).
* Improved performance of reify Cython implementation – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9054](https://github.com/aio-libs/aiohttp/issues/9054).
* Use [`URL.extend_query()`](https://yarl.aio-libs.org/en/stable/api/#yarl.URL.extend_query "(in yarl v1.23)") to extend query params (requires yarl 1.11.0+) – by [@bdraco](https://github.com/sponsors/bdraco).

  If yarl is older than 1.11.0, the previous slower hand rolled version will be used.

  *Related issues and pull requests on GitHub:*
  [#9068](https://github.com/aio-libs/aiohttp/issues/9068).
* Improved performance of checking if a host is an IP Address – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9095](https://github.com/aio-libs/aiohttp/issues/9095).
* Significantly improved performance of middlewares – by [@bdraco](https://github.com/sponsors/bdraco).

  The construction of the middleware wrappers is now cached and is built once per handler instead of on every request.

  *Related issues and pull requests on GitHub:*
  [#9158](https://github.com/aio-libs/aiohttp/issues/9158), [#9170](https://github.com/aio-libs/aiohttp/issues/9170).
* Improved performance of web requests – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9168](https://github.com/aio-libs/aiohttp/issues/9168), [#9169](https://github.com/aio-libs/aiohttp/issues/9169), [#9172](https://github.com/aio-libs/aiohttp/issues/9172), [#9174](https://github.com/aio-libs/aiohttp/issues/9174), [#9175](https://github.com/aio-libs/aiohttp/issues/9175), [#9241](https://github.com/aio-libs/aiohttp/issues/9241).
* Improved performance of starting web requests when there is no response prepare hook – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9173](https://github.com/aio-libs/aiohttp/issues/9173).
* Significantly improved performance of expiring cookies – by [@bdraco](https://github.com/sponsors/bdraco).

  Expiring cookies has been redesigned to use [`heapq`](https://docs.python.org/3/library/heapq.html#module-heapq "(in Python v3.14)") instead of a linear search, to better scale.

  *Related issues and pull requests on GitHub:*
  [#9203](https://github.com/aio-libs/aiohttp/issues/9203).
* Significantly sped up filtering cookies – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#9204](https://github.com/aio-libs/aiohttp/issues/9204).

---

## 3.10.5 (2024-08-19)[¶](#id140 "Link to this heading")

### Bug fixes[¶](#id141 "Link to this heading")

* Fixed [`aiohttp.ClientResponse.json()`](client_reference.html#aiohttp.ClientResponse.json "aiohttp.ClientResponse.json") not setting `status` when [`aiohttp.ContentTypeError`](client_reference.html#aiohttp.ContentTypeError "aiohttp.ContentTypeError") is raised – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8742](https://github.com/aio-libs/aiohttp/issues/8742).

### Miscellaneous internal changes[¶](#id142 "Link to this heading")

* Improved performance of the WebSocket reader – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8736](https://github.com/aio-libs/aiohttp/issues/8736), [#8747](https://github.com/aio-libs/aiohttp/issues/8747).

---

## 3.10.4 (2024-08-17)[¶](#id143 "Link to this heading")

### Bug fixes[¶](#id144 "Link to this heading")

* Fixed decoding base64 chunk in BodyPartReader – by [@hyzyla](https://github.com/sponsors/hyzyla).

  *Related issues and pull requests on GitHub:*
  [#3867](https://github.com/aio-libs/aiohttp/issues/3867).
* Fixed a race closing the server-side WebSocket where the close code would not reach the client – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8680](https://github.com/aio-libs/aiohttp/issues/8680).
* Fixed unconsumed exceptions raised by the WebSocket heartbeat – by [@bdraco](https://github.com/sponsors/bdraco).

  If the heartbeat ping raised an exception, it would not be consumed and would be logged as an warning.

  *Related issues and pull requests on GitHub:*
  [#8685](https://github.com/aio-libs/aiohttp/issues/8685).
* Fixed an edge case in the Python parser when chunk separators happen to align with network chunks – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8720](https://github.com/aio-libs/aiohttp/issues/8720).

### Improved documentation[¶](#id145 "Link to this heading")

* Added `aiohttp-apischema` to supported libraries – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8700](https://github.com/aio-libs/aiohttp/issues/8700).

### Miscellaneous internal changes[¶](#id146 "Link to this heading")

* Improved performance of starting request handlers with Python 3.12+ – by [@bdraco](https://github.com/sponsors/bdraco).

  This change is a followup to [#8661](https://github.com/aio-libs/aiohttp/issues/8661) to make the same optimization for Python 3.12+ where the request is connected.

  *Related issues and pull requests on GitHub:*
  [#8681](https://github.com/aio-libs/aiohttp/issues/8681).

---

## 3.10.3 (2024-08-10)[¶](#id147 "Link to this heading")

### Bug fixes[¶](#id148 "Link to this heading")

* Fixed multipart reading when stream buffer splits the boundary over several read() calls – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8653](https://github.com/aio-libs/aiohttp/issues/8653).
* Fixed [`aiohttp.TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector") doing blocking I/O in the event loop to create the `SSLContext` – by [@bdraco](https://github.com/sponsors/bdraco).

  The blocking I/O would only happen once per verify mode. However, it could cause the event loop to block for a long time if the `SSLContext` creation is slow, which is more likely during startup when the disk cache is not yet present.

  *Related issues and pull requests on GitHub:*
  [#8672](https://github.com/aio-libs/aiohttp/issues/8672).

### Miscellaneous internal changes[¶](#id149 "Link to this heading")

* Improved performance of [`receive()`](client_reference.html#aiohttp.ClientWebSocketResponse.receive "aiohttp.ClientWebSocketResponse.receive") and [`receive()`](web_reference.html#aiohttp.web.WebSocketResponse.receive "aiohttp.web.WebSocketResponse.receive") when there is no timeout. – by [@bdraco](https://github.com/sponsors/bdraco).

  The timeout context manager is now avoided when there is no timeout as it accounted for up to 50% of the time spent in the [`receive()`](client_reference.html#aiohttp.ClientWebSocketResponse.receive "aiohttp.ClientWebSocketResponse.receive") and [`receive()`](web_reference.html#aiohttp.web.WebSocketResponse.receive "aiohttp.web.WebSocketResponse.receive") methods.

  *Related issues and pull requests on GitHub:*
  [#8660](https://github.com/aio-libs/aiohttp/issues/8660).
* Improved performance of starting request handlers with Python 3.12+ – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8661](https://github.com/aio-libs/aiohttp/issues/8661).
* Improved performance of HTTP keep-alive checks – by [@bdraco](https://github.com/sponsors/bdraco).

  Previously, when processing a request for a keep-alive connection, the keep-alive check would happen every second; the check is now rescheduled if it fires too early instead.

  *Related issues and pull requests on GitHub:*
  [#8662](https://github.com/aio-libs/aiohttp/issues/8662).
* Improved performance of generating random WebSocket mask – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8667](https://github.com/aio-libs/aiohttp/issues/8667).

---

## 3.10.2 (2024-08-08)[¶](#id150 "Link to this heading")

### Bug fixes[¶](#id151 "Link to this heading")

* Fixed server checks for circular symbolic links to be compatible with Python 3.13 – by [@steverep](https://github.com/sponsors/steverep).

  *Related issues and pull requests on GitHub:*
  [#8565](https://github.com/aio-libs/aiohttp/issues/8565).
* Fixed request body not being read when ignoring an Upgrade request – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8597](https://github.com/aio-libs/aiohttp/issues/8597).
* Fixed an edge case where shutdown would wait for timeout when the handler was already completed – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8611](https://github.com/aio-libs/aiohttp/issues/8611).
* Fixed connecting to `npipe://`, `tcp://`, and `unix://` urls – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8632](https://github.com/aio-libs/aiohttp/issues/8632).
* Fixed WebSocket ping tasks being prematurely garbage collected – by [@bdraco](https://github.com/sponsors/bdraco).

  There was a small risk that WebSocket ping tasks would be prematurely garbage collected because the event loop only holds a weak reference to the task. The garbage collection risk has been fixed by holding a strong reference to the task. Additionally, the task is now scheduled eagerly with Python 3.12+ to increase the chance it can be completed immediately and avoid having to hold any references to the task.

  *Related issues and pull requests on GitHub:*
  [#8641](https://github.com/aio-libs/aiohttp/issues/8641).
* Fixed incorrectly following symlinks for compressed file variants – by [@steverep](https://github.com/sponsors/steverep).

  *Related issues and pull requests on GitHub:*
  [#8652](https://github.com/aio-libs/aiohttp/issues/8652).

### Removals and backward incompatible breaking changes[¶](#id152 "Link to this heading")

* Removed `Request.wait_for_disconnection()`, which was mistakenly added briefly in 3.10.0 – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8636](https://github.com/aio-libs/aiohttp/issues/8636).

### Contributor-facing changes[¶](#id153 "Link to this heading")

* Fixed monkey patches for `Path.stat()` and `Path.is_dir()` for Python 3.13 compatibility – by [@steverep](https://github.com/sponsors/steverep).

  *Related issues and pull requests on GitHub:*
  [#8551](https://github.com/aio-libs/aiohttp/issues/8551).

### Miscellaneous internal changes[¶](#id154 "Link to this heading")

* Improved WebSocket performance when messages are sent or received frequently – by [@bdraco](https://github.com/sponsors/bdraco).

  The WebSocket heartbeat scheduling algorithm was improved to reduce the `asyncio` scheduling overhead by decreasing the number of `asyncio.TimerHandle` creations and cancellations.

  *Related issues and pull requests on GitHub:*
  [#8608](https://github.com/aio-libs/aiohttp/issues/8608).
* Minor improvements to various type annotations – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8634](https://github.com/aio-libs/aiohttp/issues/8634).

---

## 3.10.1 (2024-08-03)[¶](#id155 "Link to this heading")

### Bug fixes[¶](#id156 "Link to this heading")

* Fixed WebSocket server heartbeat timeout logic to terminate [`receive()`](client_reference.html#aiohttp.ClientWebSocketResponse.receive "aiohttp.ClientWebSocketResponse.receive") and return [`ServerTimeoutError`](client_reference.html#aiohttp.ServerTimeoutError "aiohttp.ServerTimeoutError") – by [@arcivanov](https://github.com/sponsors/arcivanov).

  When a WebSocket pong message was not received, the [`receive()`](client_reference.html#aiohttp.ClientWebSocketResponse.receive "aiohttp.ClientWebSocketResponse.receive") operation did not terminate. This change causes `_pong_not_received` to feed the `reader` an error message, causing pending [`receive()`](client_reference.html#aiohttp.ClientWebSocketResponse.receive "aiohttp.ClientWebSocketResponse.receive") to terminate and return the error message. The error message contains the exception [`ServerTimeoutError`](client_reference.html#aiohttp.ServerTimeoutError "aiohttp.ServerTimeoutError").

  *Related issues and pull requests on GitHub:*
  [#8540](https://github.com/aio-libs/aiohttp/issues/8540).
* Fixed url dispatcher index not matching when a variable is preceded by a fixed string after a slash – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8566](https://github.com/aio-libs/aiohttp/issues/8566).

### Removals and backward incompatible breaking changes[¶](#id157 "Link to this heading")

* Creating [`aiohttp.TCPConnector`](client_reference.html#aiohttp.TCPConnector "aiohttp.TCPConnector"), [`aiohttp.ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession"), `ThreadedResolver` [`aiohttp.web.Server`](web_reference.html#aiohttp.web.Server "aiohttp.web.Server"), or [`aiohttp.CookieJar`](client_reference.html#aiohttp.CookieJar "aiohttp.CookieJar") instances without a running event loop now raises a [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – by [@asvetlov](https://github.com/sponsors/asvetlov).

  Creating these objects without a running event loop was deprecated in [#3372](https://github.com/aio-libs/aiohttp/issues/3372) which was released in version 3.5.0.

  This change first appeared in version 3.10.0 as [#6378](https://github.com/aio-libs/aiohttp/issues/6378).

  *Related issues and pull requests on GitHub:*
  [#8555](https://github.com/aio-libs/aiohttp/issues/8555), [#8583](https://github.com/aio-libs/aiohttp/issues/8583).

---

## 3.10.0 (2024-07-30)[¶](#id158 "Link to this heading")

### Bug fixes[¶](#id159 "Link to this heading")

* Fixed server response headers for `Content-Type` and `Content-Encoding` for
  static compressed files – by [@steverep](https://github.com/sponsors/steverep).

  Server will now respond with a `Content-Type` appropriate for the compressed
  file (e.g. `"application/gzip"`), and omit the `Content-Encoding` header.
  Users should expect that most clients will no longer decompress such responses
  by default.

  *Related issues and pull requests on GitHub:*
  [#4462](https://github.com/aio-libs/aiohttp/issues/4462).
* Fixed duplicate cookie expiration calls in the CookieJar implementation

  *Related issues and pull requests on GitHub:*
  [#7784](https://github.com/aio-libs/aiohttp/issues/7784).
* Adjusted `FileResponse` to check file existence and access when preparing the response – by [@steverep](https://github.com/sponsors/steverep).

  The [`FileResponse`](web_reference.html#aiohttp.web.FileResponse "aiohttp.web.FileResponse") class was modified to respond with
  :   403 Forbidden or 404 Not Found as appropriate. Previously, it would cause a
      server error if the path did not exist or could not be accessed. Checks for
      existence, non-regular files, and permissions were expected to be done in the
      route handler. For static routes, this now permits a compressed file to exist
      without its uncompressed variant and still be served. In addition, this
      changes the response status for files without read permission to 403, and for
      non-regular files from 404 to 403 for consistency.

  *Related issues and pull requests on GitHub:*
  [#8182](https://github.com/aio-libs/aiohttp/issues/8182).
* Fixed `AsyncResolver` to match `ThreadedResolver` behavior
  – by [@bdraco](https://github.com/sponsors/bdraco).

  On system with IPv6 support, the `AsyncResolver` would not fallback
  to providing A records when AAAA records were not available.
  Additionally, unlike the `ThreadedResolver`, the `AsyncResolver`
  did not handle link-local addresses correctly.

  This change makes the behavior consistent with the `ThreadedResolver`.

  *Related issues and pull requests on GitHub:*
  [#8270](https://github.com/aio-libs/aiohttp/issues/8270).
* Fixed `ws_connect` not respecting receive\_timeout` on WS(S) connection.
  – by [@arcivanov](https://github.com/sponsors/arcivanov).

  *Related issues and pull requests on GitHub:*
  [#8444](https://github.com/aio-libs/aiohttp/issues/8444).
* Removed blocking I/O in the event loop for static resources and refactored
  exception handling – by [@steverep](https://github.com/sponsors/steverep).

  File system calls when handling requests for static routes were moved to a
  separate thread to potentially improve performance. Exception handling
  was tightened in order to only return 403 Forbidden or 404 Not Found responses
  for expected scenarios; 500 Internal Server Error would be returned for any
  unknown errors.

  *Related issues and pull requests on GitHub:*
  [#8507](https://github.com/aio-libs/aiohttp/issues/8507).

### Features[¶](#id160 "Link to this heading")

* Added a Request.wait\_for\_disconnection() method, as means of allowing request handlers to be notified of premature client disconnections.

  *Related issues and pull requests on GitHub:*
  [#2492](https://github.com/aio-libs/aiohttp/issues/2492).
* Added 5 new exceptions: [`InvalidUrlClientError`](client_reference.html#aiohttp.InvalidUrlClientError "aiohttp.InvalidUrlClientError"), [`RedirectClientError`](client_reference.html#aiohttp.RedirectClientError "aiohttp.RedirectClientError"),
  [`NonHttpUrlClientError`](client_reference.html#aiohttp.NonHttpUrlClientError "aiohttp.NonHttpUrlClientError"), [`InvalidUrlRedirectClientError`](client_reference.html#aiohttp.InvalidUrlRedirectClientError "aiohttp.InvalidUrlRedirectClientError"),
  [`NonHttpUrlRedirectClientError`](client_reference.html#aiohttp.NonHttpUrlRedirectClientError "aiohttp.NonHttpUrlRedirectClientError")

  [`InvalidUrlRedirectClientError`](client_reference.html#aiohttp.InvalidUrlRedirectClientError "aiohttp.InvalidUrlRedirectClientError"), [`NonHttpUrlRedirectClientError`](client_reference.html#aiohttp.NonHttpUrlRedirectClientError "aiohttp.NonHttpUrlRedirectClientError")
  are raised instead of [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)") or [`InvalidURL`](client_reference.html#aiohttp.InvalidURL "aiohttp.InvalidURL") when the redirect URL is invalid. Classes
  [`InvalidUrlClientError`](client_reference.html#aiohttp.InvalidUrlClientError "aiohttp.InvalidUrlClientError"), [`RedirectClientError`](client_reference.html#aiohttp.RedirectClientError "aiohttp.RedirectClientError"),
  [`NonHttpUrlClientError`](client_reference.html#aiohttp.NonHttpUrlClientError "aiohttp.NonHttpUrlClientError") are base for them.

  The [`InvalidURL`](client_reference.html#aiohttp.InvalidURL "aiohttp.InvalidURL") now exposes a `description` property with the text explanation of the error details.

  – by [@setla](https://github.com/sponsors/setla), [@AraHaan](https://github.com/sponsors/AraHaan), and [@bdraco](https://github.com/sponsors/bdraco)

  *Related issues and pull requests on GitHub:*
  [#2507](https://github.com/aio-libs/aiohttp/issues/2507), [#3315](https://github.com/aio-libs/aiohttp/issues/3315), [#6722](https://github.com/aio-libs/aiohttp/issues/6722), [#8481](https://github.com/aio-libs/aiohttp/issues/8481), [#8482](https://github.com/aio-libs/aiohttp/issues/8482).
* Added a feature to retry closed connections automatically for idempotent methods. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  *Related issues and pull requests on GitHub:*
  [#7297](https://github.com/aio-libs/aiohttp/issues/7297).
* Implemented filter\_cookies() with domain-matching and path-matching on the keys, instead of testing every single cookie.
  This may break existing cookies that have been saved with CookieJar.save(). Cookies can be migrated with this script:

  ```
  import pickle
  with file_path.open("rb") as f:
      cookies = pickle.load(f)

  morsels = [(name, m) for c in cookies.values() for name, m in c.items()]
  cookies.clear()
  for name, m in morsels:
      cookies[(m["domain"], m["path"].rstrip("/"))][name] = m

  with file_path.open("wb") as f:
      pickle.dump(cookies, f, pickle.HIGHEST_PROTOCOL)
  ```

  *Related issues and pull requests on GitHub:*
  [#7583](https://github.com/aio-libs/aiohttp/issues/7583), [#8535](https://github.com/aio-libs/aiohttp/issues/8535).
* Separated connection and socket timeout errors, from ServerTimeoutError.

  *Related issues and pull requests on GitHub:*
  [#7801](https://github.com/aio-libs/aiohttp/issues/7801).
* Implemented happy eyeballs

  *Related issues and pull requests on GitHub:*
  [#7954](https://github.com/aio-libs/aiohttp/issues/7954).
* Added server capability to check for static files with Brotli compression via a `.br` extension – by [@steverep](https://github.com/sponsors/steverep).

  *Related issues and pull requests on GitHub:*
  [#8062](https://github.com/aio-libs/aiohttp/issues/8062).

### Removals and backward incompatible breaking changes[¶](#id161 "Link to this heading")

* The shutdown logic in 3.9 waited on all tasks, which caused issues with some libraries.
  In 3.10 we’ve changed this logic to only wait on request handlers. This means that it’s
  important for developers to correctly handle the lifecycle of background tasks using a
  library such as `aiojobs`. If an application is using `handler_cancellation=True` then
  it is also a good idea to ensure that any [`asyncio.shield()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.shield "(in Python v3.14)") calls are replaced with
  [`aiojobs.aiohttp.shield()`](https://aiojobs.readthedocs.io/en/stable/api.html#aiojobs.aiohttp.shield "(in aiojobs v1.4)").

  Please read the updated documentation on these points: <https://docs.aiohttp.org/en/stable/web_advanced.html#graceful-shutdown> <https://docs.aiohttp.org/en/stable/web_advanced.html#web-handler-cancellation>

  – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  *Related issues and pull requests on GitHub:*
  [#8495](https://github.com/aio-libs/aiohttp/issues/8495).

### Improved documentation[¶](#id162 "Link to this heading")

* Added documentation for `aiohttp.web.FileResponse`.

  *Related issues and pull requests on GitHub:*
  [#3958](https://github.com/aio-libs/aiohttp/issues/3958).
* Improved the docs for the ssl params.

  *Related issues and pull requests on GitHub:*
  [#8403](https://github.com/aio-libs/aiohttp/issues/8403).

### Contributor-facing changes[¶](#id163 "Link to this heading")

* Enabled HTTP parser tests originally intended for 3.9.2 release – by [@pajod](https://github.com/sponsors/pajod).

  *Related issues and pull requests on GitHub:*
  [#8088](https://github.com/aio-libs/aiohttp/issues/8088).

### Miscellaneous internal changes[¶](#id164 "Link to this heading")

* Improved URL handler resolution time by indexing resources in the UrlDispatcher.
  For applications with a large number of handlers, this should increase performance significantly.
  – by [@bdraco](https://github.com/sponsors/bdraco)

  *Related issues and pull requests on GitHub:*
  [#7829](https://github.com/aio-libs/aiohttp/issues/7829).
* Added [nacl\_middleware](https://github.com/CosmicDNA/nacl_middleware) to the list of middlewares in the third party section of the documentation.

  *Related issues and pull requests on GitHub:*
  [#8346](https://github.com/aio-libs/aiohttp/issues/8346).
* Minor improvements to static typing – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8364](https://github.com/aio-libs/aiohttp/issues/8364).
* Added a 3.11-specific overloads to `ClientSession` – by [@max-muoto](https://github.com/sponsors/max-muoto).

  *Related issues and pull requests on GitHub:*
  [#8463](https://github.com/aio-libs/aiohttp/issues/8463).
* Simplified path checks for `UrlDispatcher.add_static()` method – by [@steverep](https://github.com/sponsors/steverep).

  *Related issues and pull requests on GitHub:*
  [#8491](https://github.com/aio-libs/aiohttp/issues/8491).
* Avoided creating a future on every websocket receive – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8498](https://github.com/aio-libs/aiohttp/issues/8498).
* Updated identity checks for all `WSMsgType` type compares – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8501](https://github.com/aio-libs/aiohttp/issues/8501).
* When using Python 3.12 or later, the writer is no longer scheduled on the event loop if it can finish synchronously. Avoiding event loop scheduling reduces latency and improves performance. – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8510](https://github.com/aio-libs/aiohttp/issues/8510).
* Restored `AsyncResolver` to be the default resolver. – by [@bdraco](https://github.com/sponsors/bdraco).

  `AsyncResolver` was disabled by default because
  of IPv6 compatibility issues. These issues have been resolved and
  `AsyncResolver` is again now the default resolver.

  *Related issues and pull requests on GitHub:*
  [#8522](https://github.com/aio-libs/aiohttp/issues/8522).

---

## 3.9.5 (2024-04-16)[¶](#id165 "Link to this heading")

### Bug fixes[¶](#id166 "Link to this heading")

* Fixed “Unclosed client session” when initialization of
  [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") fails – by [@NewGlad](https://github.com/sponsors/NewGlad).

  *Related issues and pull requests on GitHub:*
  [#8253](https://github.com/aio-libs/aiohttp/issues/8253).
* Fixed regression (from [PR #8280](https://github.com/aio-libs/aiohttp/pull/8280)) with adding `Content-Disposition` to the `form-data`
  part after appending to writer – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)/[@Olegt0rr](https://github.com/sponsors/Olegt0rr).

  *Related issues and pull requests on GitHub:*
  [#8332](https://github.com/aio-libs/aiohttp/issues/8332).
* Added default `Content-Disposition` in `multipart/form-data` responses to avoid broken
  form-data responses – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8335](https://github.com/aio-libs/aiohttp/issues/8335).

---

## 3.9.4 (2024-04-11)[¶](#id167 "Link to this heading")

### Bug fixes[¶](#id168 "Link to this heading")

* The asynchronous internals now set the underlying causes
  when assigning exceptions to the future objects
  – by [@webknjaz](https://github.com/sponsors/webknjaz).

  *Related issues and pull requests on GitHub:*
  [#8089](https://github.com/aio-libs/aiohttp/issues/8089).
* Treated values of `Accept-Encoding` header as case-insensitive when checking
  for gzip files – by [@steverep](https://github.com/sponsors/steverep).

  *Related issues and pull requests on GitHub:*
  [#8104](https://github.com/aio-libs/aiohttp/issues/8104).
* Improved the DNS resolution performance on cache hit – by [@bdraco](https://github.com/sponsors/bdraco).

  This is achieved by avoiding an [`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio "(in Python v3.14)") task creation in this case.

  *Related issues and pull requests on GitHub:*
  [#8163](https://github.com/aio-libs/aiohttp/issues/8163).
* Changed the type annotations to allow `dict` on [`aiohttp.MultipartWriter.append()`](multipart_reference.html#aiohttp.MultipartWriter.append "aiohttp.MultipartWriter.append"),
  [`aiohttp.MultipartWriter.append_json()`](multipart_reference.html#aiohttp.MultipartWriter.append_json "aiohttp.MultipartWriter.append_json") and
  [`aiohttp.MultipartWriter.append_form()`](multipart_reference.html#aiohttp.MultipartWriter.append_form "aiohttp.MultipartWriter.append_form") – by [@cakemanny](https://github.com/sponsors/cakemanny)

  *Related issues and pull requests on GitHub:*
  [#7741](https://github.com/aio-libs/aiohttp/issues/7741).
* Ensure websocket transport is closed when client does not close it
  – by [@bdraco](https://github.com/sponsors/bdraco).

  The transport could remain open if the client did not close it. This
  change ensures the transport is closed when the client does not close
  it.

  *Related issues and pull requests on GitHub:*
  [#8200](https://github.com/aio-libs/aiohttp/issues/8200).
* Leave websocket transport open if receive times out or is cancelled
  – by [@bdraco](https://github.com/sponsors/bdraco).

  This restores the behavior prior to the change in #7978.

  *Related issues and pull requests on GitHub:*
  [#8251](https://github.com/aio-libs/aiohttp/issues/8251).
* Fixed content not being read when an upgrade request was not supported with the pure Python implementation.
  – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8252](https://github.com/aio-libs/aiohttp/issues/8252).
* Fixed a race condition with incoming connections during server shutdown – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8271](https://github.com/aio-libs/aiohttp/issues/8271).
* Fixed `multipart/form-data` compliance with [**RFC 7578**](https://datatracker.ietf.org/doc/html/rfc7578.html) – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8280](https://github.com/aio-libs/aiohttp/issues/8280).
* Fixed blocking I/O in the event loop while processing files in a POST request
  – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8283](https://github.com/aio-libs/aiohttp/issues/8283).
* Escaped filenames in static view – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8317](https://github.com/aio-libs/aiohttp/issues/8317).
* Fixed the pure python parser to mark a connection as closing when a
  response has no length – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8320](https://github.com/aio-libs/aiohttp/issues/8320).

### Features[¶](#id169 "Link to this heading")

* Upgraded *llhttp* to 9.2.1, and started rejecting obsolete line folding
  in Python parser to match – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8146](https://github.com/aio-libs/aiohttp/issues/8146), [#8292](https://github.com/aio-libs/aiohttp/issues/8292).

### Deprecations (removal in next major release)[¶](#id170 "Link to this heading")

* Deprecated `content_transfer_encoding` parameter in [`FormData.add_field()`](client_reference.html#aiohttp.FormData.add_field "aiohttp.FormData.add_field") – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8280](https://github.com/aio-libs/aiohttp/issues/8280).

### Improved documentation[¶](#id171 "Link to this heading")

* Added a note about canceling tasks to avoid delaying server shutdown – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8267](https://github.com/aio-libs/aiohttp/issues/8267).

### Contributor-facing changes[¶](#id172 "Link to this heading")

* The pull request template is now asking the contributors to
  answer a question about the long-term maintenance challenges
  they envision as a result of merging their patches
  – by [@webknjaz](https://github.com/sponsors/webknjaz).

  *Related issues and pull requests on GitHub:*
  [#8099](https://github.com/aio-libs/aiohttp/issues/8099).
* Updated CI and documentation to use NPM clean install and upgrade
  node to version 18 – by [@steverep](https://github.com/sponsors/steverep).

  *Related issues and pull requests on GitHub:*
  [#8116](https://github.com/aio-libs/aiohttp/issues/8116).
* A pytest fixture `hello_txt` was introduced to aid
  static file serving tests in
  `test_web_sendfile_functional.py`. It dynamically
  provisions `hello.txt` file variants shared across the
  tests in the module.

  – by [@steverep](https://github.com/sponsors/steverep)

  *Related issues and pull requests on GitHub:*
  [#8136](https://github.com/aio-libs/aiohttp/issues/8136).

### Packaging updates and notes for downstreams[¶](#id173 "Link to this heading")

* Added an `internal` pytest marker for tests which should be skipped
  by packagers (use `-m 'not internal'` to disable them) – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8299](https://github.com/aio-libs/aiohttp/issues/8299).

---

## 3.9.3 (2024-01-29)[¶](#id174 "Link to this heading")

### Bug fixes[¶](#id175 "Link to this heading")

* Fixed backwards compatibility breakage (in 3.9.2) of `ssl` parameter when set outside
  of `ClientSession` (e.g. directly in `TCPConnector`) – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#8097](https://github.com/aio-libs/aiohttp/issues/8097), [#8098](https://github.com/aio-libs/aiohttp/issues/8098).

### Miscellaneous internal changes[¶](#id176 "Link to this heading")

* Improved test suite handling of paths and temp files to consistently use pathlib and pytest fixtures.

  *Related issues and pull requests on GitHub:*
  [#3957](https://github.com/aio-libs/aiohttp/issues/3957).

---

## 3.9.2 (2024-01-28)[¶](#id177 "Link to this heading")

### Bug fixes[¶](#id178 "Link to this heading")

* Fixed server-side websocket connection leak.

  *Related issues and pull requests on GitHub:*
  [#7978](https://github.com/aio-libs/aiohttp/issues/7978).
* Fixed `web.FileResponse` doing blocking I/O in the event loop.

  *Related issues and pull requests on GitHub:*
  [#8012](https://github.com/aio-libs/aiohttp/issues/8012).
* Fixed double compress when compression enabled and compressed file exists in server file responses.

  *Related issues and pull requests on GitHub:*
  [#8014](https://github.com/aio-libs/aiohttp/issues/8014).
* Added runtime type check for `ClientSession` `timeout` parameter.

  *Related issues and pull requests on GitHub:*
  [#8021](https://github.com/aio-libs/aiohttp/issues/8021).
* Fixed an unhandled exception in the Python HTTP parser on header lines starting with a colon – by [@pajod](https://github.com/sponsors/pajod).

  Invalid request lines with anything but a dot between the HTTP major and minor version are now rejected.
  Invalid header field names containing question mark or slash are now rejected.
  Such requests are incompatible with [**RFC 9110 Section 5.6.2**](https://datatracker.ietf.org/doc/html/rfc9110.html#section-5.6.2) and are not known to be of any legitimate use.

  *Related issues and pull requests on GitHub:*
  [#8074](https://github.com/aio-libs/aiohttp/issues/8074).
* Improved validation of paths for static resources requests to the server – by [@bdraco](https://github.com/sponsors/bdraco).

  *Related issues and pull requests on GitHub:*
  [#8079](https://github.com/aio-libs/aiohttp/issues/8079).

### Features[¶](#id179 "Link to this heading")

* Added support for passing [`True`](https://docs.python.org/3/library/constants.html#True "(in Python v3.14)") to `ssl` parameter in `ClientSession` while
  deprecating [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") – by [@xiangyan99](https://github.com/sponsors/xiangyan99).

  *Related issues and pull requests on GitHub:*
  [#7698](https://github.com/aio-libs/aiohttp/issues/7698).

### Breaking changes[¶](#breaking-changes "Link to this heading")

* Fixed an unhandled exception in the Python HTTP parser on header lines starting with a colon – by [@pajod](https://github.com/sponsors/pajod).

  Invalid request lines with anything but a dot between the HTTP major and minor version are now rejected.
  Invalid header field names containing question mark or slash are now rejected.
  Such requests are incompatible with [**RFC 9110 Section 5.6.2**](https://datatracker.ietf.org/doc/html/rfc9110.html#section-5.6.2) and are not known to be of any legitimate use.

  *Related issues and pull requests on GitHub:*
  [#8074](https://github.com/aio-libs/aiohttp/issues/8074).

### Improved documentation[¶](#id180 "Link to this heading")

* Fixed examples of `fallback_charset_resolver` function in the [Advanced Client Usage](client_advanced.html) document. – by [@henry0312](https://github.com/sponsors/henry0312).

  *Related issues and pull requests on GitHub:*
  [#7995](https://github.com/aio-libs/aiohttp/issues/7995).
* The Sphinx setup was updated to avoid showing the empty
  changelog draft section in the tagged release documentation
  builds on Read The Docs – by [@webknjaz](https://github.com/sponsors/webknjaz).

  *Related issues and pull requests on GitHub:*
  [#8067](https://github.com/aio-libs/aiohttp/issues/8067).

### Packaging updates and notes for downstreams[¶](#id181 "Link to this heading")

* The changelog categorization was made clearer. The
  contributors can now mark their fragment files more
  accurately – by [@webknjaz](https://github.com/sponsors/webknjaz).

  The new category tags are:

  > + `bugfix`
  > + `feature`
  > + `deprecation`
  > + `breaking` (previously, `removal`)
  > + `doc`
  > + `packaging`
  > + `contrib`
  > + `misc`

  *Related issues and pull requests on GitHub:*
  [#8066](https://github.com/aio-libs/aiohttp/issues/8066).

### Contributor-facing changes[¶](#id182 "Link to this heading")

* Updated [contributing/Tests coverage](contributing.html#aiohttp-contributing) section to show how we use `codecov` – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  *Related issues and pull requests on GitHub:*
  [#7916](https://github.com/aio-libs/aiohttp/issues/7916).
* The changelog categorization was made clearer. The
  contributors can now mark their fragment files more
  accurately – by [@webknjaz](https://github.com/sponsors/webknjaz).

  The new category tags are:

  > + `bugfix`
  > + `feature`
  > + `deprecation`
  > + `breaking` (previously, `removal`)
  > + `doc`
  > + `packaging`
  > + `contrib`
  > + `misc`

  *Related issues and pull requests on GitHub:*
  [#8066](https://github.com/aio-libs/aiohttp/issues/8066).

### Miscellaneous internal changes[¶](#id183 "Link to this heading")

* Replaced all `tmpdir` fixtures with `tmp_path` in test suite.

  *Related issues and pull requests on GitHub:*
  [#3551](https://github.com/aio-libs/aiohttp/issues/3551).

---

## 3.9.1 (2023-11-26)[¶](#id184 "Link to this heading")

### Bugfixes[¶](#bugfixes "Link to this heading")

* Fixed importing aiohttp under PyPy on Windows.

  [#7848](https://github.com/aio-libs/aiohttp/issues/7848)
* Fixed async concurrency safety in websocket compressor.

  [#7865](https://github.com/aio-libs/aiohttp/issues/7865)
* Fixed `ClientResponse.close()` releasing the connection instead of closing.

  [#7869](https://github.com/aio-libs/aiohttp/issues/7869)
* Fixed a regression where connection may get closed during upgrade. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7879](https://github.com/aio-libs/aiohttp/issues/7879)
* Fixed messages being reported as upgraded without an Upgrade header in Python parser. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7895](https://github.com/aio-libs/aiohttp/issues/7895)

---

## 3.9.0 (2023-11-18)[¶](#id190 "Link to this heading")

### Features[¶](#id191 "Link to this heading")

* Introduced `AppKey` for static typing support of `Application` storage.
  See <https://docs.aiohttp.org/en/stable/web_advanced.html#application-s-config>

  [#5864](https://github.com/aio-libs/aiohttp/issues/5864)
* Added a graceful shutdown period which allows pending tasks to complete before the application’s cleanup is called.
  The period can be adjusted with the `shutdown_timeout` parameter. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).
  See <https://docs.aiohttp.org/en/latest/web_advanced.html#graceful-shutdown>

  [#7188](https://github.com/aio-libs/aiohttp/issues/7188)
* Added [handler\_cancellation](https://docs.aiohttp.org/en/stable/web_advanced.html#web-handler-cancellation) parameter to cancel web handler on client disconnection. – by [@mosquito](https://github.com/sponsors/mosquito)
  This (optionally) reintroduces a feature removed in a previous release.
  Recommended for those looking for an extra level of protection against denial-of-service attacks.

  [#7056](https://github.com/aio-libs/aiohttp/issues/7056)
* Added support for setting response header parameters `max_line_size` and `max_field_size`.

  [#2304](https://github.com/aio-libs/aiohttp/issues/2304)
* Added `auto_decompress` parameter to `ClientSession.request` to override `ClientSession._auto_decompress`. – by [@Daste745](https://github.com/sponsors/Daste745)

  [#3751](https://github.com/aio-libs/aiohttp/issues/3751)
* Changed `raise_for_status` to allow a coroutine.

  [#3892](https://github.com/aio-libs/aiohttp/issues/3892)
* Added client brotli compression support (optional with runtime check).

  [#5219](https://github.com/aio-libs/aiohttp/issues/5219)
* Added `client_max_size` to `BaseRequest.clone()` to allow overriding the request body size. – [@anesabml](https://github.com/sponsors/anesabml).

  [#5704](https://github.com/aio-libs/aiohttp/issues/5704)
* Added a middleware type alias `aiohttp.typedefs.Middleware`.

  [#5898](https://github.com/aio-libs/aiohttp/issues/5898)
* Exported `HTTPMove` which can be used to catch any redirection request
  that has a location – [@dreamsorcerer](https://github.com/sponsors/dreamsorcerer).

  [#6594](https://github.com/aio-libs/aiohttp/issues/6594)
* Changed the `path` parameter in `web.run_app()` to accept a `pathlib.Path` object.

  [#6839](https://github.com/aio-libs/aiohttp/issues/6839)
* Performance: Skipped filtering `CookieJar` when the jar is empty or all cookies have expired.

  [#7819](https://github.com/aio-libs/aiohttp/issues/7819)
* Performance: Only check origin if insecure scheme and there are origins to treat as secure, in `CookieJar.filter_cookies()`.

  [#7821](https://github.com/aio-libs/aiohttp/issues/7821)
* Performance: Used timestamp instead of `datetime` to achieve faster cookie expiration in `CookieJar`.

  [#7824](https://github.com/aio-libs/aiohttp/issues/7824)
* Added support for passing a custom server name parameter to HTTPS connection.

  [#7114](https://github.com/aio-libs/aiohttp/issues/7114)
* Added support for using Basic Auth credentials from `.netrc` file when making HTTP requests with the
  [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession") `trust_env` argument is set to `True`. – by [@yuvipanda](https://github.com/sponsors/yuvipanda).

  [#7131](https://github.com/aio-libs/aiohttp/issues/7131)
* Turned access log into no-op when the logger is disabled.

  [#7240](https://github.com/aio-libs/aiohttp/issues/7240)
* Added typing information to `RawResponseMessage`. – by [@Gobot1234](https://github.com/sponsors/Gobot1234)

  [#7365](https://github.com/aio-libs/aiohttp/issues/7365)
* Removed `async-timeout` for Python 3.11+ (replaced with `asyncio.timeout()` on newer releases).

  [#7502](https://github.com/aio-libs/aiohttp/issues/7502)
* Added support for `brotlicffi` as an alternative to `brotli` (fixing Brotli support on PyPy).

  [#7611](https://github.com/aio-libs/aiohttp/issues/7611)
* Added `WebSocketResponse.get_extra_info()` to access a protocol transport’s extra info.

  [#7078](https://github.com/aio-libs/aiohttp/issues/7078)
* Allow `link` argument to be set to None/empty in HTTP 451 exception.

  [#7689](https://github.com/aio-libs/aiohttp/issues/7689)

### Bugfixes[¶](#id214 "Link to this heading")

* Implemented stripping the trailing dots from fully-qualified domain names in `Host` headers and TLS context when acting as an HTTP client.
  This allows the client to connect to URLs with FQDN host name like `https://example.com./`.
  – by [@martin-sucha](https://github.com/sponsors/martin-sucha).

  [#3636](https://github.com/aio-libs/aiohttp/issues/3636)
* Fixed client timeout not working when incoming data is always available without waiting. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  [#5854](https://github.com/aio-libs/aiohttp/issues/5854)
* Fixed `readuntil` to work with a delimiter of more than one character.

  [#6701](https://github.com/aio-libs/aiohttp/issues/6701)
* Added `__repr__` to `EmptyStreamReader` to avoid `AttributeError`.

  [#6916](https://github.com/aio-libs/aiohttp/issues/6916)
* Fixed bug when using `TCPConnector` with `ttl_dns_cache=0`.

  [#7014](https://github.com/aio-libs/aiohttp/issues/7014)
* Fixed response returned from expect handler being thrown away. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7025](https://github.com/aio-libs/aiohttp/issues/7025)
* Avoided raising `UnicodeDecodeError` in multipart and in HTTP headers parsing.

  [#7044](https://github.com/aio-libs/aiohttp/issues/7044)
* Changed `sock_read` timeout to start after writing has finished, avoiding read timeouts caused by an unfinished write. – by [@dtrifiro](https://github.com/sponsors/dtrifiro)

  [#7149](https://github.com/aio-libs/aiohttp/issues/7149)
* Fixed missing query in tracing method URLs when using `yarl` 1.9+.

  [#7259](https://github.com/aio-libs/aiohttp/issues/7259)
* Changed max 32-bit timestamp to an aware datetime object, for consistency with the non-32-bit one, and to avoid a `DeprecationWarning` on Python 3.12.

  [#7302](https://github.com/aio-libs/aiohttp/issues/7302)
* Fixed `EmptyStreamReader.iter_chunks()` never ending. – by [@mind1m](https://github.com/sponsors/mind1m)

  [#7616](https://github.com/aio-libs/aiohttp/issues/7616)
* Fixed a rare `RuntimeError: await wasn't used with future` exception. – by [@stalkerg](https://github.com/sponsors/stalkerg)

  [#7785](https://github.com/aio-libs/aiohttp/issues/7785)
* Fixed issue with insufficient HTTP method and version validation.

  [#7700](https://github.com/aio-libs/aiohttp/issues/7700)
* Added check to validate that absolute URIs have schemes.

  [#7712](https://github.com/aio-libs/aiohttp/issues/7712)
* Fixed unhandled exception when Python HTTP parser encounters unpaired Unicode surrogates.

  [#7715](https://github.com/aio-libs/aiohttp/issues/7715)
* Updated parser to disallow invalid characters in header field names and stop accepting LF as a request line separator.

  [#7719](https://github.com/aio-libs/aiohttp/issues/7719)
* Fixed Python HTTP parser not treating 204/304/1xx as an empty body.

  [#7755](https://github.com/aio-libs/aiohttp/issues/7755)
* Ensure empty body response for 1xx/204/304 per RFC 9112 sec 6.3.

  [#7756](https://github.com/aio-libs/aiohttp/issues/7756)
* Fixed an issue when a client request is closed before completing a chunked payload. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7764](https://github.com/aio-libs/aiohttp/issues/7764)
* Edge Case Handling for ResponseParser for missing reason value.

  [#7776](https://github.com/aio-libs/aiohttp/issues/7776)
* Fixed `ClientWebSocketResponse.close_code` being erroneously set to `None` when there are concurrent async tasks receiving data and closing the connection.

  [#7306](https://github.com/aio-libs/aiohttp/issues/7306)
* Added HTTP method validation.

  [#6533](https://github.com/aio-libs/aiohttp/issues/6533)
* Fixed arbitrary sequence types being allowed to inject values via version parameter. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7835](https://github.com/aio-libs/aiohttp/issues/7835)
* Performance: Fixed increase in latency with small messages from websocket compression changes.

  [#7797](https://github.com/aio-libs/aiohttp/issues/7797)

### Improved Documentation[¶](#id239 "Link to this heading")

* Fixed the ClientResponse.release’s type in the doc. Changed from comethod to method.

  [#5836](https://github.com/aio-libs/aiohttp/issues/5836)
* Added information on behavior of base\_url parameter in ClientSession.

  [#6647](https://github.com/aio-libs/aiohttp/issues/6647)
* Fixed ClientResponseError docs.

  [#6700](https://github.com/aio-libs/aiohttp/issues/6700)
* Updated Redis code examples to follow the latest API.

  [#6907](https://github.com/aio-libs/aiohttp/issues/6907)
* Added a note about possibly needing to update headers when using `on_response_prepare`. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7283](https://github.com/aio-libs/aiohttp/issues/7283)
* Completed `trust_env` parameter description to honor `wss_proxy`, `ws_proxy` or `no_proxy` env.

  [#7325](https://github.com/aio-libs/aiohttp/issues/7325)
* Expanded SSL documentation with more examples (e.g. how to use certifi). – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7334](https://github.com/aio-libs/aiohttp/issues/7334)
* Fix, update, and improve client exceptions documentation.

  [#7733](https://github.com/aio-libs/aiohttp/issues/7733)

### Deprecations and Removals[¶](#deprecations-and-removals "Link to this heading")

* Added `shutdown_timeout` parameter to `BaseRunner`, while
  deprecating `shutdown_timeout` parameter from `BaseSite`. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7718](https://github.com/aio-libs/aiohttp/issues/7718)
* Dropped Python 3.6 support.

  [#6378](https://github.com/aio-libs/aiohttp/issues/6378)
* Dropped Python 3.7 support. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7336](https://github.com/aio-libs/aiohttp/issues/7336)
* Removed support for abandoned `tokio` event loop. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7281](https://github.com/aio-libs/aiohttp/issues/7281)

### Misc[¶](#misc "Link to this heading")

* Made `print` argument in `run_app()` optional.

  [#3690](https://github.com/aio-libs/aiohttp/issues/3690)
* Improved performance of `ceil_timeout` in some cases.

  [#6316](https://github.com/aio-libs/aiohttp/issues/6316)
* Changed importing Gunicorn to happen on-demand, decreasing import time by ~53%. – [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#6591](https://github.com/aio-libs/aiohttp/issues/6591)
* Improved import time by replacing `http.server` with `http.HTTPStatus`.

  [#6903](https://github.com/aio-libs/aiohttp/issues/6903)
* Fixed annotation of `ssl` parameter to disallow `True`. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  [#7335](https://github.com/aio-libs/aiohttp/issues/7335)

---

## 3.8.6 (2023-10-07)[¶](#id257 "Link to this heading")

### Security bugfixes[¶](#security-bugfixes "Link to this heading")

* Upgraded the vendored copy of [llhttp](https://llhttp.org) to v9.1.3 – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  Thanks to [@kenballus](https://github.com/sponsors/kenballus) for reporting this, see
  <https://github.com/aio-libs/aiohttp/security/advisories/GHSA-pjjw-qhg8-p2p9>.

  [#7647](https://github.com/aio-libs/aiohttp/issues/7647)
* Updated Python parser to comply with RFCs 9110/9112 – by [@Dreamorcerer](https://github.com/sponsors/Dreamorcerer)

  Thanks to [@kenballus](https://github.com/sponsors/kenballus) for reporting this, see
  <https://github.com/aio-libs/aiohttp/security/advisories/GHSA-gfw2-4jvh-wgfg>.

  [#7663](https://github.com/aio-libs/aiohttp/issues/7663)

### Deprecation[¶](#deprecation "Link to this heading")

* Added `fallback_charset_resolver` parameter in `ClientSession` to allow a user-supplied
  character set detection function.

  Character set detection will no longer be included in 3.9 as a default. If this feature is needed,
  please use [fallback\_charset\_resolver](https://docs.aiohttp.org/en/stable/client_advanced.html#character-set-detection).

  [#7561](https://github.com/aio-libs/aiohttp/issues/7561)

### Features[¶](#id261 "Link to this heading")

* Enabled lenient response parsing for more flexible parsing in the client
  (this should resolve some regressions when dealing with badly formatted HTTP responses). – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7490](https://github.com/aio-libs/aiohttp/issues/7490)

### Bugfixes[¶](#id263 "Link to this heading")

* Fixed `PermissionError` when `.netrc` is unreadable due to permissions.

  [#7237](https://github.com/aio-libs/aiohttp/issues/7237)
* Fixed output of parsing errors pointing to a `\n`. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7468](https://github.com/aio-libs/aiohttp/issues/7468)
* Fixed `GunicornWebWorker` max\_requests\_jitter not working.

  [#7518](https://github.com/aio-libs/aiohttp/issues/7518)
* Fixed sorting in `filter_cookies` to use cookie with longest path. – by [@marq24](https://github.com/sponsors/marq24).

  [#7577](https://github.com/aio-libs/aiohttp/issues/7577)
* Fixed display of `BadStatusLine` messages from [llhttp](https://llhttp.org). – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7651](https://github.com/aio-libs/aiohttp/issues/7651)

---

## 3.8.5 (2023-07-19)[¶](#id269 "Link to this heading")

### Security bugfixes[¶](#id270 "Link to this heading")

* Upgraded the vendored copy of [llhttp](https://llhttp.org) to v8.1.1 – by [@webknjaz](https://github.com/sponsors/webknjaz)
  and [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  Thanks to [@sethmlarson](https://github.com/sponsors/sethmlarson) for reporting this and providing us with
  comprehensive reproducer, workarounds and fixing details! For more
  information, see
  <https://github.com/aio-libs/aiohttp/security/advisories/GHSA-45c4-8wx5-qw6w>.

  [#7346](https://github.com/aio-libs/aiohttp/issues/7346)

### Features[¶](#id273 "Link to this heading")

* Added information to C parser exceptions to show which character caused the error. – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer)

  [#7366](https://github.com/aio-libs/aiohttp/issues/7366)

### Bugfixes[¶](#id275 "Link to this heading")

* Fixed a transport is [`None`](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") error – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  [#3355](https://github.com/aio-libs/aiohttp/issues/3355)

---

## 3.8.4 (2023-02-12)[¶](#id277 "Link to this heading")

### Bugfixes[¶](#id278 "Link to this heading")

* Fixed incorrectly overwriting cookies with the same name and domain, but different path.
  [#6638](https://github.com/aio-libs/aiohttp/issues/6638)
* Fixed `ConnectionResetError` not being raised after client disconnection in SSL environments.
  [#7180](https://github.com/aio-libs/aiohttp/issues/7180)

---

## 3.8.3 (2022-09-21)[¶](#id281 "Link to this heading")

Attention

This is the last [aiohttp](index.html) release tested under
Python 3.6. The 3.9 stream is dropping it from the CI and the
distribution package metadata.

### Bugfixes[¶](#id282 "Link to this heading")

* Increased the upper boundary of the [multidict](https://multidict.aio-libs.org/en/stable/ "(in multidict v6.7)") dependency
  to allow for the version 6 – by [@hugovk](https://github.com/sponsors/hugovk).

  It used to be limited below version 7 in [aiohttp](index.html) v3.8.1 but
  was lowered in v3.8.2 via [PR #6550](https://github.com/aio-libs/aiohttp/pull/6550) and never brought back, causing
  problems with dependency pins when upgrading. [aiohttp](index.html) v3.8.3
  fixes that by recovering the original boundary of `< 7`.
  [#6950](https://github.com/aio-libs/aiohttp/issues/6950)

---

## 3.8.2 (2022-09-20, subsequently yanked on 2022-09-21)[¶](#subsequently-yanked-on-2022-09-21 "Link to this heading")

### Bugfixes[¶](#id284 "Link to this heading")

* Support registering OPTIONS HTTP method handlers via RouteTableDef.
  [#4663](https://github.com/aio-libs/aiohttp/issues/4663)
* Started supporting `authority-form` and `absolute-form` URLs on the server-side.
  [#6227](https://github.com/aio-libs/aiohttp/issues/6227)
* Fix Python 3.11 alpha incompatibilities by using Cython 0.29.25
  [#6396](https://github.com/aio-libs/aiohttp/issues/6396)
* Remove a deprecated usage of pytest.warns(None)
  [#6663](https://github.com/aio-libs/aiohttp/issues/6663)
* Fix regression where `asyncio.CancelledError` occurs on client disconnection.
  [#6719](https://github.com/aio-libs/aiohttp/issues/6719)
* Export [`PrefixedSubAppResource`](web_reference.html#aiohttp.web.PrefixedSubAppResource "aiohttp.web.PrefixedSubAppResource") under
  [`aiohttp.web`](web.html#module-aiohttp.web "aiohttp.web") – by [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).

  This fixes a regression introduced by [PR #3469](https://github.com/aio-libs/aiohttp/pull/3469).
  [#6889](https://github.com/aio-libs/aiohttp/issues/6889)
* Dropped the [`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") type possibility from
  the [`aiohttp.ClientSession.timeout`](client_reference.html#aiohttp.ClientSession.timeout "aiohttp.ClientSession.timeout")
  property return type declaration.
  [#6917](https://github.com/aio-libs/aiohttp/issues/6917),
  [#6923](https://github.com/aio-libs/aiohttp/issues/6923)

### Improved Documentation[¶](#id293 "Link to this heading")

* Added clarification on configuring the app object with settings such as a db connection.
  [#4137](https://github.com/aio-libs/aiohttp/issues/4137)
* Edited the web.run\_app declaration.
  [#6401](https://github.com/aio-libs/aiohttp/issues/6401)
* Dropped the [`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") type possibility from
  the [`aiohttp.ClientSession.timeout`](client_reference.html#aiohttp.ClientSession.timeout "aiohttp.ClientSession.timeout")
  property return type declaration.
  [#6917](https://github.com/aio-libs/aiohttp/issues/6917),
  [#6923](https://github.com/aio-libs/aiohttp/issues/6923)

### Deprecations and Removals[¶](#id298 "Link to this heading")

* Drop Python 3.5 support, aiohttp works on 3.6+ now.
  [#4046](https://github.com/aio-libs/aiohttp/issues/4046)

### Misc[¶](#id300 "Link to this heading")

* [#6369](https://github.com/aio-libs/aiohttp/issues/6369), [#6399](https://github.com/aio-libs/aiohttp/issues/6399), [#6550](https://github.com/aio-libs/aiohttp/issues/6550), [#6708](https://github.com/aio-libs/aiohttp/issues/6708), [#6757](https://github.com/aio-libs/aiohttp/issues/6757), [#6857](https://github.com/aio-libs/aiohttp/issues/6857), [#6872](https://github.com/aio-libs/aiohttp/issues/6872)

---

## 3.8.1 (2021-11-14)[¶](#id308 "Link to this heading")

### Bugfixes[¶](#id309 "Link to this heading")

* Fix the error in handling the return value of getaddrinfo.
  getaddrinfo will return an (int, bytes) tuple, if CPython could not handle the address family.
  It will cause a index out of range error in aiohttp. For example, if user compile CPython with
  –disable-ipv6 option but his system enable the ipv6.
  [#5901](https://github.com/aio-libs/aiohttp/issues/5901)
* Do not install “examples” as a top-level package.
  [#6189](https://github.com/aio-libs/aiohttp/issues/6189)
* Restored ability to connect IPv6-only host.
  [#6195](https://github.com/aio-libs/aiohttp/issues/6195)
* Remove `Signal` from `__all__`, replace `aiohttp.Signal` with `aiosignal.Signal` in docs
  [#6201](https://github.com/aio-libs/aiohttp/issues/6201)
* Made chunked encoding HTTP header check stricter.
  [#6305](https://github.com/aio-libs/aiohttp/issues/6305)

### Improved Documentation[¶](#id315 "Link to this heading")

* update quick starter demo codes.
  [#6240](https://github.com/aio-libs/aiohttp/issues/6240)
* Added an explanation of how tiny timeouts affect performance to the client reference document.
  [#6274](https://github.com/aio-libs/aiohttp/issues/6274)
* Add flake8-docstrings to flake8 configuration, enable subset of checks.
  [#6276](https://github.com/aio-libs/aiohttp/issues/6276)
* Added information on running complex applications with additional tasks/processes – [@Dreamsorcerer](https://github.com/sponsors/Dreamsorcerer).
  [#6278](https://github.com/aio-libs/aiohttp/issues/6278)

### Misc[¶](#id320 "Link to this heading")

* [#6205](https://github.com/aio-libs/aiohttp/issues/6205)

---

## 3.8.0 (2021-10-31)[¶](#id322 "Link to this heading")

### Features[¶](#id323 "Link to this heading")

* Added a `GunicornWebWorker` feature for extending the aiohttp server configuration by allowing the ‘wsgi’ coroutine to return `web.AppRunner` object.
  [#2988](https://github.com/aio-libs/aiohttp/issues/2988)
* Switch from `http-parser` to `llhttp`
  [#3561](https://github.com/aio-libs/aiohttp/issues/3561)
* Use Brotli instead of brotlipy
  [#3803](https://github.com/aio-libs/aiohttp/issues/3803)
* Disable implicit switch-back to pure python mode. The build fails loudly if aiohttp
  cannot be compiled with C Accelerators. Use AIOHTTP\_NO\_EXTENSIONS=1 to explicitly
  disable C Extensions complication and switch to Pure-Python mode. Note that Pure-Python
  mode is significantly slower than compiled one.
  [#3828](https://github.com/aio-libs/aiohttp/issues/3828)
* Make access log use local time with timezone
  [#3853](https://github.com/aio-libs/aiohttp/issues/3853)
* Implemented `readuntil` in `StreamResponse`
  [#4054](https://github.com/aio-libs/aiohttp/issues/4054)
* FileResponse now supports ETag.
  [#4594](https://github.com/aio-libs/aiohttp/issues/4594)
* Add a request handler type alias `aiohttp.typedefs.Handler`.
  [#4686](https://github.com/aio-libs/aiohttp/issues/4686)
* `AioHTTPTestCase` is more async friendly now.

  For people who use unittest and are used to use [`TestCase`](https://docs.python.org/3/library/unittest.html#unittest.TestCase "(in Python v3.14)")
  it will be easier to write new test cases like the sync version of the [`TestCase`](https://docs.python.org/3/library/unittest.html#unittest.TestCase "(in Python v3.14)") class,
  without using the decorator @unittest\_run\_loop, just async def test\_\*.
  The only difference is that for the people using python3.7 and below a new dependency is needed, it is `asynctestcase`.
  [#4700](https://github.com/aio-libs/aiohttp/issues/4700)
* Add validation of HTTP header keys and values to prevent header injection.
  [#4818](https://github.com/aio-libs/aiohttp/issues/4818)
* Add predicate to `AbstractCookieJar.clear`.
  Add `AbstractCookieJar.clear_domain` to clean all domain and subdomains cookies only.
  [#4942](https://github.com/aio-libs/aiohttp/issues/4942)
* Add keepalive\_timeout parameter to web.run\_app.
  [#5094](https://github.com/aio-libs/aiohttp/issues/5094)
* Tracing for client sent headers
  [#5105](https://github.com/aio-libs/aiohttp/issues/5105)
* Make type hints for http parser stricter
  [#5267](https://github.com/aio-libs/aiohttp/issues/5267)
* Add final declarations for constants.
  [#5275](https://github.com/aio-libs/aiohttp/issues/5275)
* Switch to external frozenlist and aiosignal libraries.
  [#5293](https://github.com/aio-libs/aiohttp/issues/5293)
* Don’t send secure cookies by insecure transports.

  By default, the transport is secure if https or wss scheme is used.
  Use CookieJar(treat\_as\_secure\_origin=”http://127.0.0.1”) to override the default security checker.
  [#5571](https://github.com/aio-libs/aiohttp/issues/5571)
* Always create a new event loop in `aiohttp.web.run_app()`.
  This adds better compatibility with `asyncio.run()` or if trying to run multiple apps in sequence.
  [#5572](https://github.com/aio-libs/aiohttp/issues/5572)
* Add `aiohttp.pytest_plugin.AiohttpClient` for static typing of pytest plugin.
  [#5585](https://github.com/aio-libs/aiohttp/issues/5585)
* Added a `socket_factory` argument to `BaseTestServer`.
  [#5844](https://github.com/aio-libs/aiohttp/issues/5844)
* Add compression strategy parameter to enable\_compression method.
  [#5909](https://github.com/aio-libs/aiohttp/issues/5909)
* Added support for Python 3.10 to Github Actions CI/CD workflows and fix the related deprecation warnings – [@Hanaasagi](https://github.com/sponsors/Hanaasagi).
  [#5927](https://github.com/aio-libs/aiohttp/issues/5927)
* Switched `chardet` to `charset-normalizer` for guessing the HTTP payload body encoding – [@Ousret](https://github.com/sponsors/Ousret).
  [#5930](https://github.com/aio-libs/aiohttp/issues/5930)
* Added optional auto\_decompress argument for HttpRequestParser
  [#5957](https://github.com/aio-libs/aiohttp/issues/5957)
* Added support for HTTPS proxies to the extent CPython’s
  [`asyncio`](https://docs.python.org/3/library/asyncio.html#module-asyncio "(in Python v3.14)") supports it – by [@bmbouter](https://github.com/sponsors/bmbouter),
  [@jborean93](https://github.com/sponsors/jborean93) and [@webknjaz](https://github.com/sponsors/webknjaz).
  [#5992](https://github.com/aio-libs/aiohttp/issues/5992)
* Added `base_url` parameter to the initializer of [`ClientSession`](client_reference.html#aiohttp.ClientSession "aiohttp.ClientSession").
  [#6013](https://github.com/aio-libs/aiohttp/issues/6013)
* Add Trove classifier and create binary wheels for 3.10. – [@hugovk](https://github.com/sponsors/hugovk).
  [#6079](https://github.com/aio-libs/aiohttp/issues/6079)
* Started shipping platform-specific wheels with the `musl` tag targeting typical Alpine Linux runtimes — [@asvetlov](https://github.com/sponsors/asvetlov).
  [#6139](https://github.com/aio-libs/aiohttp/issues/6139)
* Started shipping platform-specific arm64 wheels for Apple Silicon — [@asvetlov](https://github.com/sponsors/asvetlov).
  [#6139](https://github.com/aio-libs/aiohttp/issues/6139)

### Bugfixes[¶](#id353 "Link to this heading")

* Modify \_drain\_helper() to handle concurrent await resp.write(…) or ws.send\_json(…) calls without race-condition.
  [#2934](https://github.com/aio-libs/aiohttp/issues/2934)
* Started using MultiLoopChildWatcher when it’s available under POSIX while setting up the test I/O loop.
  [#3450](https://github.com/aio-libs/aiohttp/issues/3450)
* Only encode content-disposition filename parameter using percent-encoding.
  Other parameters are encoded to quoted-string or RFC2231 extended parameter
  value.
  [#4012](https://github.com/aio-libs/aiohttp/issues/4012)
* Fixed HTTP client requests to honor `no_proxy` environment variables.
  [#4431](https://github.com/aio-libs/aiohttp/issues/4431)
* Fix supporting WebSockets proxies configured via environment variables.
  [#4648](https://github.com/aio-libs/aiohttp/issues/4648)
* Change return type on URLDispatcher to UrlMappingMatchInfo to improve type annotations.
  [#4748](https://github.com/aio-libs/aiohttp/issues/4748)
* Ensure a cleanup context is cleaned up even when an exception occurs during startup.
  [#4799](https://github.com/aio-libs/aiohttp/issues/4799)
* Added a new exception type for Unix socket client errors which provides a more useful error message.
  [#4984](https://github.com/aio-libs/aiohttp/issues/4984)
* Remove Transfer-Encoding and Content-Type headers for 204 in StreamResponse
  [#5106](https://github.com/aio-libs/aiohttp/issues/5106)
* Only depend on typing\_extensions for Python <3.8
  [#5107](https://github.com/aio-libs/aiohttp/issues/5107)
* Add ABNORMAL\_CLOSURE and BAD\_GATEWAY to WSCloseCode
  [#5192](https://github.com/aio-libs/aiohttp/issues/5192)
* Fix cookies disappearing from HTTPExceptions.
  [#5233](https://github.com/aio-libs/aiohttp/issues/5233)
* StaticResource prefixes no longer match URLs with a non-folder prefix. For example `routes.static('/foo', '/foo')` no longer matches the URL `/foobar`. Previously, this would attempt to load the file `/foo/ar`.
  [#5250](https://github.com/aio-libs/aiohttp/issues/5250)
* Acquire the connection before running traces to prevent race condition.
  [#5259](https://github.com/aio-libs/aiohttp/issues/5259)
* Add missing slots to `` `_RequestContextManager `` and `_WSRequestContextManager`
  [#5329](https://github.com/aio-libs/aiohttp/issues/5329)
* Ensure sending a zero byte file does not throw an exception (round 2)
  [#5380](https://github.com/aio-libs/aiohttp/issues/5380)
* Set “text/plain” when data is an empty string in client requests.
  [#5392](https://github.com/aio-libs/aiohttp/issues/5392)
* Stop automatically releasing the `ClientResponse` object on calls to the `ok` property for the failed requests.
  [#5403](https://github.com/aio-libs/aiohttp/issues/5403)
* Include query parameters from params keyword argument in tracing URL.
  [#5432](https://github.com/aio-libs/aiohttp/issues/5432)
* Fix annotations
  [#5466](https://github.com/aio-libs/aiohttp/issues/5466)
* Fixed the multipart POST requests processing to always release file
  descriptors for the `tempfile.Temporaryfile`-created
  `_io.BufferedRandom` instances of files sent within multipart request
  bodies via HTTP POST requests – by [@webknjaz](https://github.com/sponsors/webknjaz).
  [#5494](https://github.com/aio-libs/aiohttp/issues/5494)
* Fix 0 being incorrectly treated as an immediate timeout.
  [#5527](https://github.com/aio-libs/aiohttp/issues/5527)
* Fixes failing tests when an environment variable <scheme>\_proxy is set.
  [#5554](https://github.com/aio-libs/aiohttp/issues/5554)
* Replace deprecated app handler design in `tests/autobahn/server.py` with call to `web.run_app`; replace deprecated `aiohttp.ws_connect` calls in `tests/autobahn/client.py` with `aiohttp.ClienSession.ws_connect`.
  [#5606](https://github.com/aio-libs/aiohttp/issues/5606)
* Fixed test for `HTTPUnauthorized` that access the `text` argument. This is not used in any part of the code, so it’s removed now.
  [#5657](https://github.com/aio-libs/aiohttp/issues/5657)
* Remove incorrect default from docs
  [#5727](https://github.com/aio-libs/aiohttp/issues/5727)
* Remove external test dependency to <http://httpbin.org>
  [#5840](https://github.com/aio-libs/aiohttp/issues/5840)
* Don’t cancel current task when entering a cancelled timer.
  [#5853](https://github.com/aio-libs/aiohttp/issues/5853)
* Added `params` keyword argument to `ClientSession.ws_connect`. – [@hoh](https://github.com/sponsors/hoh).
  [#5868](https://github.com/aio-libs/aiohttp/issues/5868)
* Uses `asyncio.ThreadedChildWatcher` under POSIX to allow setting up test loop in non-main thread.
  [#5877](https://github.com/aio-libs/aiohttp/issues/5877)
* Fix the error in handling the return value of getaddrinfo.
  getaddrinfo will return an (int, bytes) tuple, if CPython could not handle the address family.
  It will cause a index out of range error in aiohttp. For example, if user compile CPython with
  –disable-ipv6 option but his system enable the ipv6.
  [#5901](https://github.com/aio-libs/aiohttp/issues/5901)
* Removed the deprecated `loop` argument from the `asyncio.sleep`/`gather` calls
  [#5905](https://github.com/aio-libs/aiohttp/issues/5905)
* Return `None` from `request.if_modified_since`, `request.if_unmodified_since`, `request.if_range` and `response.last_modified` when corresponding http date headers are invalid.
  [#5925](https://github.com/aio-libs/aiohttp/issues/5925)
* Fix resetting SIGCHLD signals in Gunicorn aiohttp Worker to fix subprocesses that capture output having an incorrect returncode.
  [#6130](https://github.com/aio-libs/aiohttp/issues/6130)
* Raise `400: Content-Length can't be present with Transfer-Encoding` if both `Content-Length` and `Transfer-Encoding` are sent by peer by both C and Python implementations
  [#6182](https://github.com/aio-libs/aiohttp/issues/6182)

### Improved Documentation[¶](#id389 "Link to this heading")

* Refactored OpenAPI/Swagger aiohttp addons, added `aio-openapi`
  [#5326](https://github.com/aio-libs/aiohttp/issues/5326)
* Fixed docs on request cookies type, so it matches what is actually used in the code (a
  read-only dictionary-like object).
  [#5725](https://github.com/aio-libs/aiohttp/issues/5725)
* Documented that the HTTP client `Authorization` header is removed
  on redirects to a different host or protocol.
  [#5850](https://github.com/aio-libs/aiohttp/issues/5850)

### Misc[¶](#id393 "Link to this heading")

* [#3927](https://github.com/aio-libs/aiohttp/issues/3927), [#4247](https://github.com/aio-libs/aiohttp/issues/4247), [#4247](https://github.com/aio-libs/aiohttp/issues/4247), [#5389](https://github.com/aio-libs/aiohttp/issues/5389), [#5457](https://github.com/aio-libs/aiohttp/issues/5457), [#5486](https://github.com/aio-libs/aiohttp/issues/5486), [#5494](https://github.com/aio-libs/aiohttp/issues/5494), [#5515](https://github.com/aio-libs/aiohttp/issues/5515), [#5625](https://github.com/aio-libs/aiohttp/issues/5625), [#5635](https://github.com/aio-libs/aiohttp/issues/5635), [#5648](https://github.com/aio-libs/aiohttp/issues/5648), [#5657](https://github.com/aio-libs/aiohttp/issues/5657), [#5890](https://github.com/aio-libs/aiohttp/issues/5890), [#5914](https://github.com/aio-libs/aiohttp/issues/5914), [#5932](https://github.com/aio-libs/aiohttp/issues/5932), [#6002](https://github.com/aio-libs/aiohttp/issues/6002), [#6045](https://github.com/aio-libs/aiohttp/issues/6045), [#6131](https://github.com/aio-libs/aiohttp/issues/6131), [#6156](https://github.com/aio-libs/aiohttp/issues/6156), [#6165](https://github.com/aio-libs/aiohttp/issues/6165), [#6166](https://github.com/aio-libs/aiohttp/issues/6166)

---

## 3.7.4.post0 (2021-03-06)[¶](#post0-2021-03-06 "Link to this heading")

### Misc[¶](#id415 "Link to this heading")

* Bumped upper bound of the `chardet` runtime dependency
  to allow their v4.0 version stream.
  [#5366](https://github.com/aio-libs/aiohttp/issues/5366)

---

## 3.7.4 (2021-02-25)[¶](#id417 "Link to this heading")

### Bugfixes[¶](#id418 "Link to this heading")

* **(SECURITY BUG)** Started preventing open redirects in the
  `aiohttp.web.normalize_path_middleware` middleware. For
  more details, see
  <https://github.com/aio-libs/aiohttp/security/advisories/GHSA-v6wp-4m6f-gcjg>.

  Thanks to [Beast Glatisant](https://github.com/g147) for
  finding the first instance of this issue and [Jelmer Vernooĳ](https://jelmer.uk/) for reporting and tracking it down
  in aiohttp.
  [#5497](https://github.com/aio-libs/aiohttp/issues/5497)
* Fix interpretation difference of the pure-Python and the Cython-based
  HTTP parsers construct a `yarl.URL` object for HTTP request-target.

  Before this fix, the Python parser would turn the URI’s absolute-path
  for `//some-path` into `/` while the Cython code preserved it as
  `//some-path`. Now, both do the latter.
  [#5498](https://github.com/aio-libs/aiohttp/issues/5498)

---

## 3.7.3 (2020-11-18)[¶](#id421 "Link to this heading")

### Features[¶](#id422 "Link to this heading")

* Use Brotli instead of brotlipy
  [#3803](https://github.com/aio-libs/aiohttp/issues/3803)
* Made exceptions pickleable. Also changed the repr of some exceptions.
  [#4077](https://github.com/aio-libs/aiohttp/issues/4077)

### Bugfixes[¶](#id425 "Link to this heading")

* Raise a ClientResponseError instead of an AssertionError for a blank
  HTTP Reason Phrase.
  [#3532](https://github.com/aio-libs/aiohttp/issues/3532)
* Fix `web_middlewares.normalize_path_middleware` behavior for patch without slash.
  [#3669](https://github.com/aio-libs/aiohttp/issues/3669)
* Fix overshadowing of overlapped sub-applications prefixes.
  [#3701](https://github.com/aio-libs/aiohttp/issues/3701)
* Make BaseConnector.close() a coroutine and wait until the client closes all connections. Drop deprecated “with Connector():” syntax.
  [#3736](https://github.com/aio-libs/aiohttp/issues/3736)
* Reset the `sock_read` timeout each time data is received for a `aiohttp.client` response.
  [#3808](https://github.com/aio-libs/aiohttp/issues/3808)
* Fixed type annotation for add\_view method of UrlDispatcher to accept any subclass of View
  [#3880](https://github.com/aio-libs/aiohttp/issues/3880)
* Fixed querying the address families from DNS that the current host supports.
  [#5156](https://github.com/aio-libs/aiohttp/issues/5156)
* Change return type of MultipartReader.\_\_aiter\_\_() and BodyPartReader.\_\_aiter\_\_() to AsyncIterator.
  [#5163](https://github.com/aio-libs/aiohttp/issues/5163)
* Provide x86 Windows wheels.
  [#5230](https://github.com/aio-libs/aiohttp/issues/5230)

### Improved Documentation[¶](#id435 "Link to this heading")

* Add documentation for `aiohttp.web.FileResponse`.
  [#3958](https://github.com/aio-libs/aiohttp/issues/3958)
* Removed deprecation warning in tracing example docs
  [#3964](https://github.com/aio-libs/aiohttp/issues/3964)
* Fixed wrong “Usage” docstring of `aiohttp.client.request`.
  [#4603](https://github.com/aio-libs/aiohttp/issues/4603)
* Add aiohttp-pydantic to third party libraries
  [#5228](https://github.com/aio-libs/aiohttp/issues/5228)

### Misc[¶](#id440 "Link to this heading")

* [#4102](https://github.com/aio-libs/aiohttp/issues/4102)

---

## 3.7.2 (2020-10-27)[¶](#id442 "Link to this heading")

### Bugfixes[¶](#id443 "Link to this heading")

* Fixed static files handling for loops without `.sendfile()` support
  [#5149](https://github.com/aio-libs/aiohttp/issues/5149)

---

## 3.7.1 (2020-10-25)[¶](#id445 "Link to this heading")

### Bugfixes[¶](#id446 "Link to this heading")

* Fixed a type error caused by the conditional import of Protocol.
  [#5111](https://github.com/aio-libs/aiohttp/issues/5111)
* Server doesn’t send Content-Length for 1xx or 204
  [#4901](https://github.com/aio-libs/aiohttp/issues/4901)
* Fix run\_app typing
  [#4957](https://github.com/aio-libs/aiohttp/issues/4957)
* Always require `typing_extensions` library.
  [#5107](https://github.com/aio-libs/aiohttp/issues/5107)
* Fix a variable-shadowing bug causing ThreadedResolver.resolve to
  return the resolved IP as the `hostname` in each record, which prevented
  validation of HTTPS connections.
  [#5110](https://github.com/aio-libs/aiohttp/issues/5110)
* Added annotations to all public attributes.
  [#5115](https://github.com/aio-libs/aiohttp/issues/5115)
* Fix flaky test\_when\_timeout\_smaller\_second
  [#5116](https://github.com/aio-libs/aiohttp/issues/5116)
* Ensure sending a zero byte file does not throw an exception
  [#5124](https://github.com/aio-libs/aiohttp/issues/5124)
* Fix a bug in `web.run_app()` about Python version checking on Windows
  [#5127](https://github.com/aio-libs/aiohttp/issues/5127)

---

## 3.7.0 (2020-10-24)[¶](#id456 "Link to this heading")

### Features[¶](#id457 "Link to this heading")

* Response headers are now prepared prior to running `on_response_prepare` hooks, directly before headers are sent to the client.
  [#1958](https://github.com/aio-libs/aiohttp/issues/1958)
* Add a `quote_cookie` option to `CookieJar`, a way to skip quotation wrapping of cookies containing special characters.
  [#2571](https://github.com/aio-libs/aiohttp/issues/2571)
* Call `AccessLogger.log` with the current exception available from `sys.exc_info()`.
  [#3557](https://github.com/aio-libs/aiohttp/issues/3557)
* web.UrlDispatcher.add\_routes and web.Application.add\_routes return a list
  of registered AbstractRoute instances. AbstractRouteDef.register (and all
  subclasses) return a list of registered resources registered resource.
  [#3866](https://github.com/aio-libs/aiohttp/issues/3866)
* Added properties of default ClientSession params to ClientSession class so it is available for introspection
  [#3882](https://github.com/aio-libs/aiohttp/issues/3882)
* Don’t cancel web handler on peer disconnection, raise OSError on reading/writing instead.
  [#4080](https://github.com/aio-libs/aiohttp/issues/4080)
* Implement BaseRequest.get\_extra\_info() to access a protocol transports’ extra info.
  [#4189](https://github.com/aio-libs/aiohttp/issues/4189)
* Added ClientSession.timeout property.
  [#4191](https://github.com/aio-libs/aiohttp/issues/4191)
* allow use of SameSite in cookies.
  [#4224](https://github.com/aio-libs/aiohttp/issues/4224)
* Use `loop.sendfile()` instead of custom implementation if available.
  [#4269](https://github.com/aio-libs/aiohttp/issues/4269)
* Apply SO\_REUSEADDR to test server’s socket.
  [#4393](https://github.com/aio-libs/aiohttp/issues/4393)
* Use .raw\_host instead of slower .host in client API
  [#4402](https://github.com/aio-libs/aiohttp/issues/4402)
* Allow configuring the buffer size of input stream by passing `read_bufsize` argument.
  [#4453](https://github.com/aio-libs/aiohttp/issues/4453)
* Pass tests on Python 3.8 for Windows.
  [#4513](https://github.com/aio-libs/aiohttp/issues/4513)
* Add method and url attributes to TraceRequestChunkSentParams and TraceResponseChunkReceivedParams.
  [#4674](https://github.com/aio-libs/aiohttp/issues/4674)
* Add ClientResponse.ok property for checking status code under 400.
  [#4711](https://github.com/aio-libs/aiohttp/issues/4711)
* Don’t ceil timeouts that are smaller than 5 seconds.
  [#4850](https://github.com/aio-libs/aiohttp/issues/4850)
* TCPSite now listens by default on all interfaces instead of just IPv4 when None is passed in as the host.
  [#4894](https://github.com/aio-libs/aiohttp/issues/4894)
* Bump `http_parser` to 2.9.4
  [#5070](https://github.com/aio-libs/aiohttp/issues/5070)

### Bugfixes[¶](#id477 "Link to this heading")

* Fix keepalive connections not being closed in time
  [#3296](https://github.com/aio-libs/aiohttp/issues/3296)
* Fix failed websocket handshake leaving connection hanging.
  [#3380](https://github.com/aio-libs/aiohttp/issues/3380)
* Fix tasks cancellation order on exit. The run\_app task needs to be cancelled first for cleanup hooks to run with all tasks intact.
  [#3805](https://github.com/aio-libs/aiohttp/issues/3805)
* Don’t start heartbeat until \_writer is set
  [#4062](https://github.com/aio-libs/aiohttp/issues/4062)
* Fix handling of multipart file uploads without a content type.
  [#4089](https://github.com/aio-libs/aiohttp/issues/4089)
* Preserve view handler function attributes across middlewares
  [#4174](https://github.com/aio-libs/aiohttp/issues/4174)
* Fix the string representation of `ServerDisconnectedError`.
  [#4175](https://github.com/aio-libs/aiohttp/issues/4175)
* Raising RuntimeError when trying to get encoding from not read body
  [#4214](https://github.com/aio-libs/aiohttp/issues/4214)
* Remove warning messages from noop.
  [#4282](https://github.com/aio-libs/aiohttp/issues/4282)
* Raise ClientPayloadError if FormData re-processed.
  [#4345](https://github.com/aio-libs/aiohttp/issues/4345)
* Fix a warning about unfinished task in `web_protocol.py`
  [#4408](https://github.com/aio-libs/aiohttp/issues/4408)
* Fixed ‘deflate’ compression. According to RFC 2616 now.
  [#4506](https://github.com/aio-libs/aiohttp/issues/4506)
* Fixed OverflowError on platforms with 32-bit time\_t
  [#4515](https://github.com/aio-libs/aiohttp/issues/4515)
* Fixed request.body\_exists returns wrong value for methods without body.
  [#4528](https://github.com/aio-libs/aiohttp/issues/4528)
* Fix connecting to link-local IPv6 addresses.
  [#4554](https://github.com/aio-libs/aiohttp/issues/4554)
* Fix a problem with connection waiters that are never awaited.
  [#4562](https://github.com/aio-libs/aiohttp/issues/4562)
* Always make sure transport is not closing before reuse a connection.

  Reuse a protocol based on keepalive in headers is unreliable.
  For example, uWSGI will not support keepalive even it serves a
  HTTP 1.1 request, except explicitly configure uWSGI with a
  `--http-keepalive` option.

  Servers designed like uWSGI could cause aiohttp intermittently
  raise a ConnectionResetException when the protocol poll runs
  out and some protocol is reused.
  [#4587](https://github.com/aio-libs/aiohttp/issues/4587)
* Handle the last CRLF correctly even if it is received via separate TCP segment.
  [#4630](https://github.com/aio-libs/aiohttp/issues/4630)
* Fix the register\_resource function to validate route name before splitting it so that route name can include python keywords.
  [#4691](https://github.com/aio-libs/aiohttp/issues/4691)
* Improve typing annotations for `web.Request`, `aiohttp.ClientResponse` and
  `multipart` module.
  [#4736](https://github.com/aio-libs/aiohttp/issues/4736)
* Fix resolver task is not awaited when connector is cancelled
  [#4795](https://github.com/aio-libs/aiohttp/issues/4795)
* Fix a bug “Aiohttp doesn’t return any error on invalid request methods”
  [#4798](https://github.com/aio-libs/aiohttp/issues/4798)
* Fix HEAD requests for static content.
  [#4809](https://github.com/aio-libs/aiohttp/issues/4809)
* Fix incorrect size calculation for memoryview
  [#4890](https://github.com/aio-libs/aiohttp/issues/4890)
* Add HTTPMove to \_all\_\_.
  [#4897](https://github.com/aio-libs/aiohttp/issues/4897)
* Fixed the type annotations in the `tracing` module.
  [#4912](https://github.com/aio-libs/aiohttp/issues/4912)
* Fix typing for multipart `__aiter__`.
  [#4931](https://github.com/aio-libs/aiohttp/issues/4931)
* Fix for race condition on connections in BaseConnector that leads to exceeding the connection limit.
  [#4936](https://github.com/aio-libs/aiohttp/issues/4936)
* Add forced UTF-8 encoding for `application/rdap+json` responses.
  [#4938](https://github.com/aio-libs/aiohttp/issues/4938)
* Fix inconsistency between Python and C http request parsers in parsing pct-encoded URL.
  [#4972](https://github.com/aio-libs/aiohttp/issues/4972)
* Fix connection closing issue in HEAD request.
  [#5012](https://github.com/aio-libs/aiohttp/issues/5012)
* Fix type hint on BaseRunner.addresses (from `List[str]` to `List[Any]`)
  [#5086](https://github.com/aio-libs/aiohttp/issues/5086)
* Make web.run\_app() more responsive to Ctrl+C on Windows for Python < 3.8. It slightly
  increases CPU load as a side effect.
  [#5098](https://github.com/aio-libs/aiohttp/issues/5098)

### Improved Documentation[¶](#id511 "Link to this heading")

* Fix example code in client quick-start
  [#3376](https://github.com/aio-libs/aiohttp/issues/3376)
* Updated the docs so there is no contradiction in `ttl_dns_cache` default value
  [#3512](https://github.com/aio-libs/aiohttp/issues/3512)
* Add ‘Deploy with SSL’ to docs.
  [#4201](https://github.com/aio-libs/aiohttp/issues/4201)
* Change typing of the secure argument on StreamResponse.set\_cookie from `Optional[str]` to `Optional[bool]`
  [#4204](https://github.com/aio-libs/aiohttp/issues/4204)
* Changes `ttl_dns_cache` type from int to Optional[int].
  [#4270](https://github.com/aio-libs/aiohttp/issues/4270)
* Simplify README hello word example and add a documentation page for people coming from requests.
  [#4272](https://github.com/aio-libs/aiohttp/issues/4272)
* Improve some code examples in the documentation involving websockets and starting a simple HTTP site with an AppRunner.
  [#4285](https://github.com/aio-libs/aiohttp/issues/4285)
* Fix typo in code example in Multipart docs
  [#4312](https://github.com/aio-libs/aiohttp/issues/4312)
* Fix code example in Multipart section.
  [#4314](https://github.com/aio-libs/aiohttp/issues/4314)
* Update contributing guide so new contributors read the most recent version of that guide. Update command used to create test coverage reporting.
  [#4810](https://github.com/aio-libs/aiohttp/issues/4810)
* Spelling: Change “canonize” to “canonicalize”.
  [#4986](https://github.com/aio-libs/aiohttp/issues/4986)
* Add `aiohttp-sse-client` library to third party usage list.
  [#5084](https://github.com/aio-libs/aiohttp/issues/5084)

### Misc[¶](#id524 "Link to this heading")

* [#2856](https://github.com/aio-libs/aiohttp/issues/2856), [#4218](https://github.com/aio-libs/aiohttp/issues/4218), [#4250](https://github.com/aio-libs/aiohttp/issues/4250)

---

## 3.6.3 (2020-10-12)[¶](#id528 "Link to this heading")

### Bugfixes[¶](#id529 "Link to this heading")

* Pin yarl to `<1.6.0` to avoid buggy behavior that will be fixed by the next aiohttp
  release.

## 3.6.2 (2019-10-09)[¶](#id530 "Link to this heading")

### Features[¶](#id531 "Link to this heading")

* Made exceptions pickleable. Also changed the repr of some exceptions.
  [#4077](https://github.com/aio-libs/aiohttp/issues/4077)
* Use `Iterable` type hint instead of `Sequence` for `Application` *middleware*
  parameter. [#4125](https://github.com/aio-libs/aiohttp/issues/4125)

### Bugfixes[¶](#id534 "Link to this heading")

* Reset the `sock_read` timeout each time data is received for a
  `aiohttp.ClientResponse`. [#3808](https://github.com/aio-libs/aiohttp/issues/3808)
* Fix handling of expired cookies so they are not stored in CookieJar.
  [#4063](https://github.com/aio-libs/aiohttp/issues/4063)
* Fix misleading message in the string representation of `ClientConnectorError`;
  `self.ssl == None` means default SSL context, not SSL disabled [#4097](https://github.com/aio-libs/aiohttp/issues/4097)
* Don’t clobber HTTP status when using FileResponse.
  [#4106](https://github.com/aio-libs/aiohttp/issues/4106)

### Improved Documentation[¶](#id539 "Link to this heading")

* Added minimal required logging configuration to logging documentation.
  [#2469](https://github.com/aio-libs/aiohttp/issues/2469)
* Update docs to reflect proxy support.
  [#4100](https://github.com/aio-libs/aiohttp/issues/4100)
* Fix typo in code example in testing docs.
  [#4108](https://github.com/aio-libs/aiohttp/issues/4108)

### Misc[¶](#id543 "Link to this heading")

* [#4102](https://github.com/aio-libs/aiohttp/issues/4102)

---

## 3.6.1 (2019-09-19)[¶](#id545 "Link to this heading")

### Features[¶](#id546 "Link to this heading")

* Compatibility with Python 3.8.
  [#4056](https://github.com/aio-libs/aiohttp/issues/4056)

### Bugfixes[¶](#id548 "Link to this heading")

* correct some exception string format
  [#4068](https://github.com/aio-libs/aiohttp/issues/4068)
* Emit a warning when `ssl.OP_NO_COMPRESSION` is
  unavailable because the runtime is built against
  an outdated OpenSSL.
  [#4052](https://github.com/aio-libs/aiohttp/issues/4052)
* Update multidict requirement to >= 4.5
  [#4057](https://github.com/aio-libs/aiohttp/issues/4057)

### Improved Documentation[¶](#id552 "Link to this heading")

* Provide pytest-aiohttp namespace for pytest fixtures in docs.
  [#3723](https://github.com/aio-libs/aiohttp/issues/3723)

---

## 3.6.0 (2019-09-06)[¶](#id554 "Link to this heading")

### Features[¶](#id555 "Link to this heading")

* Add support for Named Pipes (Site and Connector) under Windows. This feature requires
  Proactor event loop to work. [#3629](https://github.com/aio-libs/aiohttp/issues/3629)
* Removed `Transfer-Encoding: chunked` header from websocket responses to be
  compatible with more http proxy servers. [#3798](https://github.com/aio-libs/aiohttp/issues/3798)
* Accept non-GET request for starting websocket handshake on server side.
  [#3980](https://github.com/aio-libs/aiohttp/issues/3980)

### Bugfixes[¶](#id559 "Link to this heading")

* Raise a ClientResponseError instead of an AssertionError for a blank
  HTTP Reason Phrase.
  [#3532](https://github.com/aio-libs/aiohttp/issues/3532)
* Fix an issue where cookies would sometimes not be set during a redirect.
  [#3576](https://github.com/aio-libs/aiohttp/issues/3576)
* Change normalize\_path\_middleware to use 308 redirect instead of 301.

  This behavior should prevent clients from being unable to use PUT/POST
  methods on endpoints that are redirected because of a trailing slash.
  [#3579](https://github.com/aio-libs/aiohttp/issues/3579)
* Drop the processed task from `all_tasks()` list early. It prevents logging about a
  task with unhandled exception when the server is used in conjunction with
  `asyncio.run()`. [#3587](https://github.com/aio-libs/aiohttp/issues/3587)
* `Signal` type annotation changed from `Signal[Callable[['TraceConfig'],
  Awaitable[None]]]` to `Signal[Callable[ClientSession, SimpleNamespace, ...]`.
  [#3595](https://github.com/aio-libs/aiohttp/issues/3595)
* Use sanitized URL as Location header in redirects
  [#3614](https://github.com/aio-libs/aiohttp/issues/3614)
* Improve typing annotations for multipart.py along with changes required
  by mypy in files that references multipart.py.
  [#3621](https://github.com/aio-libs/aiohttp/issues/3621)
* Close session created inside `aiohttp.request` when unhandled exception occurs
  [#3628](https://github.com/aio-libs/aiohttp/issues/3628)
* Cleanup per-chunk data in generic data read. Memory leak fixed.
  [#3631](https://github.com/aio-libs/aiohttp/issues/3631)
* Use correct type for add\_view and family
  [#3633](https://github.com/aio-libs/aiohttp/issues/3633)
* Fix \_keepalive field in \_\_slots\_\_ of `RequestHandler`.
  [#3644](https://github.com/aio-libs/aiohttp/issues/3644)
* Properly handle ConnectionResetError, to silence the “Cannot write to closing
  transport” exception when clients disconnect uncleanly.
  [#3648](https://github.com/aio-libs/aiohttp/issues/3648)
* Suppress pytest warnings due to `test_utils` classes
  [#3660](https://github.com/aio-libs/aiohttp/issues/3660)
* Fix overshadowing of overlapped sub-application prefixes.
  [#3701](https://github.com/aio-libs/aiohttp/issues/3701)
* Fixed return type annotation for WSMessage.json()
  [#3720](https://github.com/aio-libs/aiohttp/issues/3720)
* Properly expose TooManyRedirects publicly as documented.
  [#3818](https://github.com/aio-libs/aiohttp/issues/3818)
* Fix missing brackets for IPv6 in proxy CONNECT request
  [#3841](https://github.com/aio-libs/aiohttp/issues/3841)
* Make the signature of `aiohttp.test_utils.TestClient.request` match
  `asyncio.ClientSession.request` according to the docs [#3852](https://github.com/aio-libs/aiohttp/issues/3852)
* Use correct style for re-exported imports, makes mypy `--strict` mode happy.
  [#3868](https://github.com/aio-libs/aiohttp/issues/3868)
* Fixed type annotation for add\_view method of UrlDispatcher to accept any subclass of
  View [#3880](https://github.com/aio-libs/aiohttp/issues/3880)
* Made cython HTTP parser set Reason-Phrase of the response to an empty string if it is
  missing. [#3906](https://github.com/aio-libs/aiohttp/issues/3906)
* Add URL to the string representation of ClientResponseError.
  [#3959](https://github.com/aio-libs/aiohttp/issues/3959)
* Accept `istr` keys in `LooseHeaders` type hints.
  [#3976](https://github.com/aio-libs/aiohttp/issues/3976)
* Fixed race conditions in \_resolve\_host caching and throttling when tracing is enabled.
  [#4013](https://github.com/aio-libs/aiohttp/issues/4013)
* For URLs like “unix://localhost/…” set Host HTTP header to “localhost” instead of
  “localhost:None”. [#4039](https://github.com/aio-libs/aiohttp/issues/4039)

### Improved Documentation[¶](#id585 "Link to this heading")

* Modify documentation for Background Tasks to remove deprecated usage of event loop.
  [#3526](https://github.com/aio-libs/aiohttp/issues/3526)
* use `if __name__ == '__main__':` in server examples.
  [#3775](https://github.com/aio-libs/aiohttp/issues/3775)
* Update documentation reference to the default access logger.
  [#3783](https://github.com/aio-libs/aiohttp/issues/3783)
* Improve documentation for `web.BaseRequest.path` and `web.BaseRequest.raw_path`.
  [#3791](https://github.com/aio-libs/aiohttp/issues/3791)
* Removed deprecation warning in tracing example docs
  [#3964](https://github.com/aio-libs/aiohttp/issues/3964)

---

## 3.5.4 (2019-01-12)[¶](#id591 "Link to this heading")

### Bugfixes[¶](#id592 "Link to this heading")

* Fix stream `.read()` / `.readany()` / `.iter_any()` which used to return a
  partial content only in case of compressed content
  [#3525](https://github.com/aio-libs/aiohttp/issues/3525)

## 3.5.3 (2019-01-10)[¶](#id594 "Link to this heading")

### Bugfixes[¶](#id595 "Link to this heading")

* Fix type stubs for `aiohttp.web.run_app(access_log=True)` and fix edge case of
  `access_log=True` and the event loop being in debug mode. [#3504](https://github.com/aio-libs/aiohttp/issues/3504)
* Fix `aiohttp.ClientTimeout` type annotations to accept `None` for fields
  [#3511](https://github.com/aio-libs/aiohttp/issues/3511)
* Send custom per-request cookies even if session jar is empty
  [#3515](https://github.com/aio-libs/aiohttp/issues/3515)
* Restore Linux binary wheels publishing on PyPI

---

## 3.5.2 (2019-01-08)[¶](#id599 "Link to this heading")

### Features[¶](#id600 "Link to this heading")

* `FileResponse` from `web_fileresponse.py` uses a `ThreadPoolExecutor` to work
  with files asynchronously. I/O based payloads from `payload.py` uses a
  `ThreadPoolExecutor` to work with I/O objects asynchronously. [#3313](https://github.com/aio-libs/aiohttp/issues/3313)
* Internal Server Errors in plain text if the browser does not support HTML.
  [#3483](https://github.com/aio-libs/aiohttp/issues/3483)

### Bugfixes[¶](#id603 "Link to this heading")

* Preserve MultipartWriter parts headers on write. Refactor the way how
  `Payload.headers` are handled. Payload instances now always have headers and
  Content-Type defined. Fix Payload Content-Disposition header reset after initial
  creation. [#3035](https://github.com/aio-libs/aiohttp/issues/3035)
* Log suppressed exceptions in `GunicornWebWorker`.
  [#3464](https://github.com/aio-libs/aiohttp/issues/3464)
* Remove wildcard imports.
  [#3468](https://github.com/aio-libs/aiohttp/issues/3468)
* Use the same task for app initialization and web server handling in gunicorn workers.
  It allows to use Python3.7 context vars smoothly.
  [#3471](https://github.com/aio-libs/aiohttp/issues/3471)
* Fix handling of chunked+gzipped response when first chunk does not give uncompressed
  data [#3477](https://github.com/aio-libs/aiohttp/issues/3477)
* Replace `collections.MutableMapping` with `collections.abc.MutableMapping` to
  avoid a deprecation warning. [#3480](https://github.com/aio-libs/aiohttp/issues/3480)
* `Payload.size` type annotation changed from `Optional[float]` to
  `Optional[int]`. [#3484](https://github.com/aio-libs/aiohttp/issues/3484)
* Ignore done tasks when cancels pending activities on `web.run_app` finalization.
  [#3497](https://github.com/aio-libs/aiohttp/issues/3497)

### Improved Documentation[¶](#id612 "Link to this heading")

* Add documentation for `aiohttp.web.HTTPException`.
  [#3490](https://github.com/aio-libs/aiohttp/issues/3490)

### Misc[¶](#id614 "Link to this heading")

* [#3487](https://github.com/aio-libs/aiohttp/issues/3487)

---

## 3.5.1 (2018-12-24)[¶](#id616 "Link to this heading")

* Fix a regression about `ClientSession._requote_redirect_url` modification in debug
  mode.

## 3.5.0 (2018-12-22)[¶](#id617 "Link to this heading")

### Features[¶](#id618 "Link to this heading")

* The library type annotations are checked in strict mode now.
* Add support for setting cookies for individual request ([#2387](https://github.com/aio-libs/aiohttp/pull/2387))
* Application.add\_domain implementation ([#2809](https://github.com/aio-libs/aiohttp/pull/2809))
* The default `app` in the request returned by `test_utils.make_mocked_request` can
  now have objects assigned to it and retrieved using the `[]` operator. ([#3174](https://github.com/aio-libs/aiohttp/pull/3174))
* Make `request.url` accessible when transport is closed. ([#3177](https://github.com/aio-libs/aiohttp/pull/3177))
* Add `zlib_executor_size` argument to `Response` constructor to allow compression
  to run in a background executor to avoid blocking the main thread and potentially
  triggering health check failures. ([#3205](https://github.com/aio-libs/aiohttp/pull/3205))
* Enable users to set `ClientTimeout` in `aiohttp.request` ([#3213](https://github.com/aio-libs/aiohttp/pull/3213))
* Don’t raise a warning if `NETRC` environment variable is not set and `~/.netrc`
  file doesn’t exist. ([#3267](https://github.com/aio-libs/aiohttp/pull/3267))
* Add default logging handler to web.run\_app If the `` Application.debug` `` flag is set
  and the default logger `aiohttp.access` is used, access logs will now be output
  using a *stderr* `StreamHandler` if no handlers are attached. Furthermore, if the
  default logger has no log level set, the log level will be set to `DEBUG`. ([#3324](https://github.com/aio-libs/aiohttp/pull/3324))
* Add method argument to `session.ws_connect()`. Sometimes server API requires a
  different HTTP method for WebSocket connection establishment. For example, `Docker
  exec` needs POST. ([#3378](https://github.com/aio-libs/aiohttp/pull/3378))
* Create a task per request handling. ([#3406](https://github.com/aio-libs/aiohttp/pull/3406))

### Bugfixes[¶](#id629 "Link to this heading")

* Enable passing `access_log_class` via `handler_args` ([#3158](https://github.com/aio-libs/aiohttp/pull/3158))
* Return empty bytes with end-of-chunk marker in empty stream reader. ([#3186](https://github.com/aio-libs/aiohttp/pull/3186))
* Accept `CIMultiDictProxy` instances for `headers` argument in `web.Response`
  constructor. ([#3207](https://github.com/aio-libs/aiohttp/pull/3207))
* Don’t uppercase HTTP method in parser ([#3233](https://github.com/aio-libs/aiohttp/pull/3233))
* Make method match regexp RFC-7230 compliant ([#3235](https://github.com/aio-libs/aiohttp/pull/3235))
* Add `app.pre_frozen` state to properly handle startup signals in
  sub-applications. ([#3237](https://github.com/aio-libs/aiohttp/pull/3237))
* Enhanced parsing and validation of helpers.BasicAuth.decode. ([#3239](https://github.com/aio-libs/aiohttp/pull/3239))
* Change imports from collections module in preparation for 3.8. ([#3258](https://github.com/aio-libs/aiohttp/pull/3258))
* Ensure Host header is added first to ClientRequest to better replicate browser ([#3265](https://github.com/aio-libs/aiohttp/pull/3265))
* Fix forward compatibility with Python 3.8: importing ABCs directly from the
  collections module will not be supported anymore. ([#3273](https://github.com/aio-libs/aiohttp/pull/3273))
* Keep the query string by `normalize_path_middleware`. ([#3278](https://github.com/aio-libs/aiohttp/pull/3278))
* Fix missing parameter `raise_for_status` for aiohttp.request() ([#3290](https://github.com/aio-libs/aiohttp/pull/3290))
* Bracket IPv6 addresses in the HOST header ([#3304](https://github.com/aio-libs/aiohttp/pull/3304))
* Fix default message for server ping and pong frames. ([#3308](https://github.com/aio-libs/aiohttp/pull/3308))
* Fix tests/test\_connector.py typo and tests/autobahn/server.py duplicate loop
  def. ([#3337](https://github.com/aio-libs/aiohttp/pull/3337))
* Fix false-negative indicator end\_of\_HTTP\_chunk in StreamReader.readchunk function
  ([#3361](https://github.com/aio-libs/aiohttp/pull/3361))
* Release HTTP response before raising status exception ([#3364](https://github.com/aio-libs/aiohttp/pull/3364))
* Fix task cancellation when `sendfile()` syscall is used by static file
  handling. ([#3383](https://github.com/aio-libs/aiohttp/pull/3383))
* Fix stack trace for `asyncio.TimeoutError` which was not logged, when it is caught
  in the handler. ([#3414](https://github.com/aio-libs/aiohttp/pull/3414))

### Improved Documentation[¶](#id649 "Link to this heading")

* Improve documentation of `Application.make_handler` parameters. ([#3152](https://github.com/aio-libs/aiohttp/pull/3152))
* Fix BaseRequest.raw\_headers doc. ([#3215](https://github.com/aio-libs/aiohttp/pull/3215))
* Fix typo in TypeError exception reason in `web.Application._handle` ([#3229](https://github.com/aio-libs/aiohttp/pull/3229))
* Make server access log format placeholder %b documentation reflect
  behavior and docstring. ([#3307](https://github.com/aio-libs/aiohttp/pull/3307))

### Deprecations and Removals[¶](#id654 "Link to this heading")

* Deprecate modification of `session.requote_redirect_url` ([#2278](https://github.com/aio-libs/aiohttp/pull/2278))
* Deprecate `stream.unread_data()` ([#3260](https://github.com/aio-libs/aiohttp/pull/3260))
* Deprecated use of boolean in `resp.enable_compression()` ([#3318](https://github.com/aio-libs/aiohttp/pull/3318))
* Encourage creation of aiohttp public objects inside a coroutine ([#3331](https://github.com/aio-libs/aiohttp/pull/3331))
* Drop dead `Connection.detach()` and `Connection.writer`. Both methods were broken
  for more than 2 years. ([#3358](https://github.com/aio-libs/aiohttp/pull/3358))
* Deprecate `app.loop`, `request.loop`, `client.loop` and `connector.loop`
  properties. ([#3374](https://github.com/aio-libs/aiohttp/pull/3374))
* Deprecate explicit debug argument. Use asyncio debug mode instead. ([#3381](https://github.com/aio-libs/aiohttp/pull/3381))
* Deprecate body parameter in HTTPException (and derived classes) constructor. ([#3385](https://github.com/aio-libs/aiohttp/pull/3385))
* Deprecate bare connector close, use `async with connector:` and `await
  connector.close()` instead. ([#3417](https://github.com/aio-libs/aiohttp/pull/3417))
* Deprecate obsolete `read_timeout` and `conn_timeout` in `ClientSession`
  constructor. ([#3438](https://github.com/aio-libs/aiohttp/pull/3438))

### Misc[¶](#id665 "Link to this heading")

* #3341, #3351

---

## 3.4.4 (2018-09-05)[¶](#id666 "Link to this heading")

* Fix installation from sources when compiling toolkit is not available ([#3241](https://github.com/aio-libs/aiohttp/pull/3241))

---

## 3.4.3 (2018-09-04)[¶](#id668 "Link to this heading")

* Add `app.pre_frozen` state to properly handle startup signals in sub-applications. ([#3237](https://github.com/aio-libs/aiohttp/pull/3237))

---

## 3.4.2 (2018-09-01)[¶](#id670 "Link to this heading")

* Fix `iter_chunks` type annotation ([#3230](https://github.com/aio-libs/aiohttp/pull/3230))

---

## 3.4.1 (2018-08-28)[¶](#id672 "Link to this heading")

* Fix empty header parsing regression. ([#3218](https://github.com/aio-libs/aiohttp/pull/3218))
* Fix BaseRequest.raw\_headers doc. ([#3215](https://github.com/aio-libs/aiohttp/pull/3215))
* Fix documentation building on ReadTheDocs ([#3221](https://github.com/aio-libs/aiohttp/pull/3221))

---

## 3.4.0 (2018-08-25)[¶](#id676 "Link to this heading")

### Features[¶](#id677 "Link to this heading")

* Add type hints ([#3049](https://github.com/aio-libs/aiohttp/pull/3049))
* Add `raise_for_status` request parameter ([#3073](https://github.com/aio-libs/aiohttp/pull/3073))
* Add type hints to HTTP client ([#3092](https://github.com/aio-libs/aiohttp/pull/3092))
* Minor server optimizations ([#3095](https://github.com/aio-libs/aiohttp/pull/3095))
* Preserve the cause when HTTPException is raised from another exception. ([#3096](https://github.com/aio-libs/aiohttp/pull/3096))
* Add close\_boundary option in MultipartWriter.write method. Support streaming ([#3104](https://github.com/aio-libs/aiohttp/pull/3104))
* Added a `remove_slash` option to the `normalize_path_middleware` factory. ([#3173](https://github.com/aio-libs/aiohttp/pull/3173))
* The class AbstractRouteDef is importable from aiohttp.web. ([#3183](https://github.com/aio-libs/aiohttp/pull/3183))

### Bugfixes[¶](#id686 "Link to this heading")

* Prevent double closing when client connection is released before the
  last `data_received()` callback. ([#3031](https://github.com/aio-libs/aiohttp/pull/3031))
* Make redirect with normalize\_path\_middleware work when using url encoded paths. ([#3051](https://github.com/aio-libs/aiohttp/pull/3051))
* Postpone web task creation to connection establishment. ([#3052](https://github.com/aio-libs/aiohttp/pull/3052))
* Fix `sock_read` timeout. ([#3053](https://github.com/aio-libs/aiohttp/pull/3053))
* When using a server-request body as the data= argument of a client request, iterate over the content with readany instead of readline to avoid Line too long errors. ([#3054](https://github.com/aio-libs/aiohttp/pull/3054))
* fix UrlDispatcher has no attribute add\_options, add web.options ([#3062](https://github.com/aio-libs/aiohttp/pull/3062))
* correct filename in content-disposition with multipart body ([#3064](https://github.com/aio-libs/aiohttp/pull/3064))
* Many HTTP proxies has buggy keepalive support.
  Let’s not reuse connection but close it after processing every response. ([#3070](https://github.com/aio-libs/aiohttp/pull/3070))
* raise 413 “Payload Too Large” rather than raising ValueError in request.post()
  Add helpful debug message to 413 responses ([#3087](https://github.com/aio-libs/aiohttp/pull/3087))
* Fix StreamResponse equality, now that they are MutableMapping objects. ([#3100](https://github.com/aio-libs/aiohttp/pull/3100))
* Fix server request objects comparison ([#3116](https://github.com/aio-libs/aiohttp/pull/3116))
* Do not hang on 206 Partial Content response with Content-Encoding: gzip ([#3123](https://github.com/aio-libs/aiohttp/pull/3123))
* Fix timeout precondition checkers ([#3145](https://github.com/aio-libs/aiohttp/pull/3145))

### Improved Documentation[¶](#id700 "Link to this heading")

* Add a new FAQ entry that clarifies that you should not reuse response
  objects in middleware functions. ([#3020](https://github.com/aio-libs/aiohttp/pull/3020))
* Add FAQ section “Why is creating a ClientSession outside of an event loop dangerous?” ([#3072](https://github.com/aio-libs/aiohttp/pull/3072))
* Fix link to Rambler ([#3115](https://github.com/aio-libs/aiohttp/pull/3115))
* Fix TCPSite documentation on the Server Reference page. ([#3146](https://github.com/aio-libs/aiohttp/pull/3146))
* Fix documentation build configuration file for Windows. ([#3147](https://github.com/aio-libs/aiohttp/pull/3147))
* Remove no longer existing lingering\_timeout parameter of Application.make\_handler from documentation. ([#3151](https://github.com/aio-libs/aiohttp/pull/3151))
* Mention that `app.make_handler` is deprecated, recommend to use runners
  API instead. ([#3157](https://github.com/aio-libs/aiohttp/pull/3157))

### Deprecations and Removals[¶](#id708 "Link to this heading")

* Drop `loop.current_task()` from `helpers.current_task()` ([#2826](https://github.com/aio-libs/aiohttp/pull/2826))
* Drop `reader` parameter from `request.multipart()`. ([#3090](https://github.com/aio-libs/aiohttp/pull/3090))

---

## 3.3.2 (2018-06-12)[¶](#id711 "Link to this heading")

* Many HTTP proxies has buggy keepalive support. Let’s not reuse connection but
  close it after processing every response. ([#3070](https://github.com/aio-libs/aiohttp/pull/3070))
* Provide vendor source files in tarball ([#3076](https://github.com/aio-libs/aiohttp/pull/3076))

---

## 3.3.1 (2018-06-05)[¶](#id714 "Link to this heading")

* Fix `sock_read` timeout. ([#3053](https://github.com/aio-libs/aiohttp/pull/3053))
* When using a server-request body as the `data=` argument of a client request,
  iterate over the content with `readany` instead of `readline` to avoid `Line
  too long` errors. ([#3054](https://github.com/aio-libs/aiohttp/pull/3054))

---

## 3.3.0 (2018-06-01)[¶](#id717 "Link to this heading")

### Features[¶](#id718 "Link to this heading")

* Raise `ConnectionResetError` instead of `CancelledError` on trying to
  write to a closed stream. ([#2499](https://github.com/aio-libs/aiohttp/pull/2499))
* Implement `ClientTimeout` class and support socket read timeout. ([#2768](https://github.com/aio-libs/aiohttp/pull/2768))
* Enable logging when `aiohttp.web` is used as a program ([#2956](https://github.com/aio-libs/aiohttp/pull/2956))
* Add canonical property to resources ([#2968](https://github.com/aio-libs/aiohttp/pull/2968))
* Forbid reading response BODY after release ([#2983](https://github.com/aio-libs/aiohttp/pull/2983))
* Implement base protocol class to avoid a dependency from internal
  `asyncio.streams.FlowControlMixin` ([#2986](https://github.com/aio-libs/aiohttp/pull/2986))
* Cythonize `@helpers.reify`, 5% boost on macro benchmark ([#2995](https://github.com/aio-libs/aiohttp/pull/2995))
* Optimize HTTP parser ([#3015](https://github.com/aio-libs/aiohttp/pull/3015))
* Implement `runner.addresses` property. ([#3036](https://github.com/aio-libs/aiohttp/pull/3036))
* Use `bytearray` instead of a list of `bytes` in websocket reader. It
  improves websocket message reading a little. ([#3039](https://github.com/aio-libs/aiohttp/pull/3039))
* Remove heartbeat on closing connection on keepalive timeout. The used hack
  violates HTTP protocol. ([#3041](https://github.com/aio-libs/aiohttp/pull/3041))
* Limit websocket message size on reading to 4 MB by default. ([#3045](https://github.com/aio-libs/aiohttp/pull/3045))

### Bugfixes[¶](#id731 "Link to this heading")

* Don’t reuse a connection with the same URL but different proxy/TLS settings
  ([#2981](https://github.com/aio-libs/aiohttp/pull/2981))
* When parsing the Forwarded header, the optional port number is now preserved.
  ([#3009](https://github.com/aio-libs/aiohttp/pull/3009))

### Improved Documentation[¶](#id734 "Link to this heading")

* Make Change Log more visible in docs ([#3029](https://github.com/aio-libs/aiohttp/pull/3029))
* Make style and grammar improvements on the FAQ page. ([#3030](https://github.com/aio-libs/aiohttp/pull/3030))
* Document that signal handlers should be async functions since aiohttp 3.0
  ([#3032](https://github.com/aio-libs/aiohttp/pull/3032))

### Deprecations and Removals[¶](#id738 "Link to this heading")

* Deprecate custom application’s router. ([#3021](https://github.com/aio-libs/aiohttp/pull/3021))

### Misc[¶](#id740 "Link to this heading")

* #3008, #3011

---

## 3.2.1 (2018-05-10)[¶](#id741 "Link to this heading")

* Don’t reuse a connection with the same URL but different proxy/TLS settings
  ([#2981](https://github.com/aio-libs/aiohttp/pull/2981))

---

## 3.2.0 (2018-05-06)[¶](#id743 "Link to this heading")

### Features[¶](#id744 "Link to this heading")

* Raise `TooManyRedirects` exception when client gets redirected too many
  times instead of returning last response. ([#2631](https://github.com/aio-libs/aiohttp/pull/2631))
* Extract route definitions into separate `web_routedef.py` file ([#2876](https://github.com/aio-libs/aiohttp/pull/2876))
* Raise an exception on request body reading after sending response. ([#2895](https://github.com/aio-libs/aiohttp/pull/2895))
* ClientResponse and RequestInfo now have real\_url property, which is request
  url without fragment part being stripped ([#2925](https://github.com/aio-libs/aiohttp/pull/2925))
* Speed up connector limiting ([#2937](https://github.com/aio-libs/aiohttp/pull/2937))
* Added and links property for ClientResponse object ([#2948](https://github.com/aio-libs/aiohttp/pull/2948))
* Add `request.config_dict` for exposing nested applications data. ([#2949](https://github.com/aio-libs/aiohttp/pull/2949))
* Speed up HTTP headers serialization, server micro-benchmark runs 5% faster
  now. ([#2957](https://github.com/aio-libs/aiohttp/pull/2957))
* Apply assertions in debug mode only ([#2966](https://github.com/aio-libs/aiohttp/pull/2966))

### Bugfixes[¶](#id754 "Link to this heading")

* expose property app for TestClient ([#2891](https://github.com/aio-libs/aiohttp/pull/2891))
* Call on\_chunk\_sent when write\_eof takes as a param the last chunk ([#2909](https://github.com/aio-libs/aiohttp/pull/2909))
* A closing bracket was added to \_\_repr\_\_ of resources ([#2935](https://github.com/aio-libs/aiohttp/pull/2935))
* Fix compression of FileResponse ([#2942](https://github.com/aio-libs/aiohttp/pull/2942))
* Fixes some bugs in the limit connection feature ([#2964](https://github.com/aio-libs/aiohttp/pull/2964))

### Improved Documentation[¶](#id760 "Link to this heading")

* Drop `async_timeout` usage from documentation for client API in favor of
  `timeout` parameter. ([#2865](https://github.com/aio-libs/aiohttp/pull/2865))
* Improve Gunicorn logging documentation ([#2921](https://github.com/aio-libs/aiohttp/pull/2921))
* Replace multipart writer .serialize() method with .write() in
  documentation. ([#2965](https://github.com/aio-libs/aiohttp/pull/2965))

### Deprecations and Removals[¶](#id764 "Link to this heading")

* Deprecate Application.make\_handler() ([#2938](https://github.com/aio-libs/aiohttp/pull/2938))

### Misc[¶](#id766 "Link to this heading")

* #2958

---

## 3.1.3 (2018-04-12)[¶](#id767 "Link to this heading")

* Fix cancellation broadcast during DNS resolve ([#2910](https://github.com/aio-libs/aiohttp/pull/2910))

---

## 3.1.2 (2018-04-05)[¶](#id769 "Link to this heading")

* Make `LineTooLong` exception more detailed about actual data size ([#2863](https://github.com/aio-libs/aiohttp/pull/2863))
* Call `on_chunk_sent` when write\_eof takes as a param the last chunk ([#2909](https://github.com/aio-libs/aiohttp/pull/2909))

---

## 3.1.1 (2018-03-27)[¶](#id772 "Link to this heading")

* Support *asynchronous iterators* (and *asynchronous generators* as
  well) in both client and server API as request / response BODY
  payloads. ([#2802](https://github.com/aio-libs/aiohttp/pull/2802))

---

## 3.1.0 (2018-03-21)[¶](#id774 "Link to this heading")

Welcome to aiohttp 3.1 release.

This is an *incremental* release, fully backward compatible with *aiohttp 3.0*.

But we have added several new features.

The most visible one is `app.add_routes()` (an alias for existing
`app.router.add_routes()`. The addition is very important because
all *aiohttp* docs now uses `app.add_routes()` call in code
snippets. All your existing code still do register routes / resource
without any warning but you’ve got the idea for a favorite way: noisy
`app.router.add_get()` is replaced by `app.add_routes()`.

The library does not make a preference between decorators:

```
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")

app.add_routes(routes)
```

and route tables as a list:

```
async def hello(request):
    return web.Response(text="Hello, world")

app.add_routes([web.get('/', hello)])
```

Both ways are equal, user may decide basing on own code taste.

Also we have a lot of minor features, bug fixes and documentation
updates, see below.

### Features[¶](#id775 "Link to this heading")

* Relax JSON content-type checking in the `ClientResponse.json()` to allow
  “application/xxx+json” instead of strict “application/json”. ([#2206](https://github.com/aio-libs/aiohttp/pull/2206))
* Bump C HTTP parser to version 2.8 ([#2730](https://github.com/aio-libs/aiohttp/pull/2730))
* Accept a coroutine as an application factory in `web.run_app` and gunicorn
  worker. ([#2739](https://github.com/aio-libs/aiohttp/pull/2739))
* Implement application cleanup context (`app.cleanup_ctx` property). ([#2747](https://github.com/aio-libs/aiohttp/pull/2747))
* Make `writer.write_headers` a coroutine. ([#2762](https://github.com/aio-libs/aiohttp/pull/2762))
* Add tracking signals for getting request/response bodies. ([#2767](https://github.com/aio-libs/aiohttp/pull/2767))
* Deprecate ClientResponseError.code in favor of .status to keep similarity
  with response classes. ([#2781](https://github.com/aio-libs/aiohttp/pull/2781))
* Implement `app.add_routes()` method. ([#2787](https://github.com/aio-libs/aiohttp/pull/2787))
* Implement `web.static()` and `RouteTableDef.static()` API. ([#2795](https://github.com/aio-libs/aiohttp/pull/2795))
* Install a test event loop as default by `asyncio.set_event_loop()`. The
  change affects aiohttp test utils but backward compatibility is not broken
  for 99.99% of use cases. ([#2804](https://github.com/aio-libs/aiohttp/pull/2804))
* Refactor `ClientResponse` constructor: make logically required constructor
  arguments mandatory, drop `_post_init()` method. ([#2820](https://github.com/aio-libs/aiohttp/pull/2820))
* Use `app.add_routes()` in server docs everywhere ([#2830](https://github.com/aio-libs/aiohttp/pull/2830))
* Websockets refactoring, all websocket writer methods are converted into
  coroutines. ([#2836](https://github.com/aio-libs/aiohttp/pull/2836))
* Provide `Content-Range` header for `Range` requests ([#2844](https://github.com/aio-libs/aiohttp/pull/2844))

### Bugfixes[¶](#id790 "Link to this heading")

* Fix websocket client return EofStream. ([#2784](https://github.com/aio-libs/aiohttp/pull/2784))
* Fix websocket demo. ([#2789](https://github.com/aio-libs/aiohttp/pull/2789))
* Property `BaseRequest.http_range` now returns a python-like slice when
  requesting the tail of the range. It’s now indicated by a negative value in
  `range.start` rather then in `range.stop` ([#2805](https://github.com/aio-libs/aiohttp/pull/2805))
* Close a connection if an unexpected exception occurs while sending a request
  ([#2827](https://github.com/aio-libs/aiohttp/pull/2827))
* Fix firing DNS tracing events. ([#2841](https://github.com/aio-libs/aiohttp/pull/2841))

### Improved Documentation[¶](#id796 "Link to this heading")

* Document behavior when cchardet detects encodings that are unknown to Python.
  ([#2732](https://github.com/aio-libs/aiohttp/pull/2732))
* Add diagrams for tracing request life style. ([#2748](https://github.com/aio-libs/aiohttp/pull/2748))
* Drop removed functionality for passing `StreamReader` as data at client
  side. ([#2793](https://github.com/aio-libs/aiohttp/pull/2793))

---

## 3.0.9 (2018-03-14)[¶](#id800 "Link to this heading")

* Close a connection if an unexpected exception occurs while sending a request
  ([#2827](https://github.com/aio-libs/aiohttp/pull/2827))

---

## 3.0.8 (2018-03-12)[¶](#id802 "Link to this heading")

* Use `asyncio.current_task()` on Python 3.7 ([#2825](https://github.com/aio-libs/aiohttp/pull/2825))

---

## 3.0.7 (2018-03-08)[¶](#id804 "Link to this heading")

* Fix SSL proxy support by client. ([#2810](https://github.com/aio-libs/aiohttp/pull/2810))
* Restore an imperative check in `setup.py` for python version. The check
  works in parallel to environment marker. As effect an error about unsupported
  Python versions is raised even on outdated systems with very old
  `setuptools` version installed. ([#2813](https://github.com/aio-libs/aiohttp/pull/2813))

---

## 3.0.6 (2018-03-05)[¶](#id807 "Link to this heading")

* Add `_reuse_address` and `_reuse_port` to
  `web_runner.TCPSite.__slots__`. ([#2792](https://github.com/aio-libs/aiohttp/pull/2792))

---

## 3.0.5 (2018-02-27)[¶](#id809 "Link to this heading")

* Fix `InvalidStateError` on processing a sequence of two
  `RequestHandler.data_received` calls on web server. ([#2773](https://github.com/aio-libs/aiohttp/pull/2773))

---

## 3.0.4 (2018-02-26)[¶](#id811 "Link to this heading")

* Fix `IndexError` in HTTP request handling by server. ([#2752](https://github.com/aio-libs/aiohttp/pull/2752))
* Fix MultipartWriter.append\* no longer returning part/payload. ([#2759](https://github.com/aio-libs/aiohttp/pull/2759))

---

## 3.0.3 (2018-02-25)[¶](#id814 "Link to this heading")

* Relax `attrs` dependency to minimal actually supported version
  17.0.3 The change allows to avoid version conflicts with currently
  existing test tools.

---

## 3.0.2 (2018-02-23)[¶](#id815 "Link to this heading")

### Security Fix[¶](#security-fix "Link to this heading")

* Prevent Windows absolute URLs in static files. Paths like
  `/static/D:\path` and `/static/\\hostname\drive\path` are
  forbidden.

---

## 3.0.1[¶](#id816 "Link to this heading")

* Technical release for fixing distribution problems.

---

## 3.0.0 (2018-02-12)[¶](#id817 "Link to this heading")

### Features[¶](#id818 "Link to this heading")

* Speed up the PayloadWriter.write method for large request bodies. ([#2126](https://github.com/aio-libs/aiohttp/pull/2126))
* StreamResponse and Response are now MutableMappings. ([#2246](https://github.com/aio-libs/aiohttp/pull/2246))
* ClientSession publishes a set of signals to track the HTTP request execution.
  ([#2313](https://github.com/aio-libs/aiohttp/pull/2313))
* Content-Disposition fast access in ClientResponse ([#2455](https://github.com/aio-libs/aiohttp/pull/2455))
* Added support to Flask-style decorators with class-based Views. ([#2472](https://github.com/aio-libs/aiohttp/pull/2472))
* Signal handlers (registered callbacks) should be coroutines. ([#2480](https://github.com/aio-libs/aiohttp/pull/2480))
* Support `async with test_client.ws_connect(...)` ([#2525](https://github.com/aio-libs/aiohttp/pull/2525))
* Introduce *site* and *application runner* as underlying API for web.run\_app
  implementation. ([#2530](https://github.com/aio-libs/aiohttp/pull/2530))
* Only quote multipart boundary when necessary and sanitize input ([#2544](https://github.com/aio-libs/aiohttp/pull/2544))
* Make the aiohttp.ClientResponse.get\_encoding method public with the
  processing of invalid charset while detecting content encoding. ([#2549](https://github.com/aio-libs/aiohttp/pull/2549))
* Add optional configurable per message compression for
  ClientWebSocketResponse and WebSocketResponse. ([#2551](https://github.com/aio-libs/aiohttp/pull/2551))
* Add hysteresis to StreamReader to prevent flipping between paused and
  resumed states too often. ([#2555](https://github.com/aio-libs/aiohttp/pull/2555))
* Support .netrc by trust\_env ([#2581](https://github.com/aio-libs/aiohttp/pull/2581))
* Avoid to create a new resource when adding a route with the same name and
  path of the last added resource ([#2586](https://github.com/aio-libs/aiohttp/pull/2586))
* MultipartWriter.boundary is str now. ([#2589](https://github.com/aio-libs/aiohttp/pull/2589))
* Allow a custom port to be used by TestServer (and associated pytest
  fixtures) ([#2613](https://github.com/aio-libs/aiohttp/pull/2613))
* Add param access\_log\_class to web.run\_app function ([#2615](https://github.com/aio-libs/aiohttp/pull/2615))
* Add `ssl` parameter to client API ([#2626](https://github.com/aio-libs/aiohttp/pull/2626))
* Fixes performance issue introduced by #2577. When there are no middlewares
  installed by the user, no additional and useless code is executed. ([#2629](https://github.com/aio-libs/aiohttp/pull/2629))
* Rename PayloadWriter to StreamWriter ([#2654](https://github.com/aio-libs/aiohttp/pull/2654))
* New options *reuse\_port*, *reuse\_address* are added to run\_app and
  TCPSite. ([#2679](https://github.com/aio-libs/aiohttp/pull/2679))
* Use custom classes to pass client signals parameters ([#2686](https://github.com/aio-libs/aiohttp/pull/2686))
* Use `attrs` library for data classes, replace namedtuple. ([#2690](https://github.com/aio-libs/aiohttp/pull/2690))
* Pytest fixtures renaming, add `aiohttp_` prefix ([#2578](https://github.com/aio-libs/aiohttp/pull/2578))
* Add `aiohttp-` prefix for `pytest-aiohttp` command line
  parameters ([#2578](https://github.com/aio-libs/aiohttp/pull/2578))

### Bugfixes[¶](#id844 "Link to this heading")

* Correctly process upgrade request from server to HTTP2. `aiohttp` does not
  support HTTP2 yet, the protocol is not upgraded but response is handled
  correctly. ([#2277](https://github.com/aio-libs/aiohttp/pull/2277))
* Fix ClientConnectorSSLError and ClientProxyConnectionError for proxy
  connector ([#2408](https://github.com/aio-libs/aiohttp/pull/2408))
* Fix connector convert OSError to ClientConnectorError ([#2423](https://github.com/aio-libs/aiohttp/pull/2423))
* Fix connection attempts for multiple dns hosts ([#2424](https://github.com/aio-libs/aiohttp/pull/2424))
* Fix writing to closed transport by raising asyncio.CancelledError ([#2499](https://github.com/aio-libs/aiohttp/pull/2499))
* Fix warning in ClientSession.\_\_del\_\_ by stopping to try to close it.
  ([#2523](https://github.com/aio-libs/aiohttp/pull/2523))
* Fixed race-condition for iterating addresses from the DNSCache. ([#2620](https://github.com/aio-libs/aiohttp/pull/2620))
* Fix default value of access\_log\_format argument in web.run\_app ([#2649](https://github.com/aio-libs/aiohttp/pull/2649))
* Freeze sub-application on adding to parent app ([#2656](https://github.com/aio-libs/aiohttp/pull/2656))
* Do percent encoding for .url\_for() parameters ([#2668](https://github.com/aio-libs/aiohttp/pull/2668))
* Correctly process request start time and multiple request/response
  headers in access log extra ([#2641](https://github.com/aio-libs/aiohttp/pull/2641))

### Improved Documentation[¶](#id856 "Link to this heading")

* Improve tutorial docs, using literalinclude to link to the actual files.
  ([#2396](https://github.com/aio-libs/aiohttp/pull/2396))
* Small improvement docs: better example for file uploads. ([#2401](https://github.com/aio-libs/aiohttp/pull/2401))
* Rename from\_env to trust\_env in client reference. ([#2451](https://github.com/aio-libs/aiohttp/pull/2451))
* ﻿Fixed mistype in Proxy Support section where trust\_env parameter was
  used in session.get(“http://python.org”, trust\_env=True) method instead of
  aiohttp.ClientSession constructor as follows:
  aiohttp.ClientSession(trust\_env=True). ([#2688](https://github.com/aio-libs/aiohttp/pull/2688))
* Fix issue with unittest example not compiling in testing docs. ([#2717](https://github.com/aio-libs/aiohttp/pull/2717))

### Deprecations and Removals[¶](#id862 "Link to this heading")

* Simplify HTTP pipelining implementation ([#2109](https://github.com/aio-libs/aiohttp/pull/2109))
* Drop StreamReaderPayload and DataQueuePayload. ([#2257](https://github.com/aio-libs/aiohttp/pull/2257))
* Drop md5 and sha1 finger-prints ([#2267](https://github.com/aio-libs/aiohttp/pull/2267))
* Drop WSMessage.tp ([#2321](https://github.com/aio-libs/aiohttp/pull/2321))
* Drop Python 3.4 and Python 3.5.0, 3.5.1, 3.5.2. Minimal supported Python
  versions are 3.5.3 and 3.6.0. yield from is gone, use async/await syntax.
  ([#2343](https://github.com/aio-libs/aiohttp/pull/2343))
* Drop aiohttp.Timeout and use async\_timeout.timeout instead. ([#2348](https://github.com/aio-libs/aiohttp/pull/2348))
* Drop resolve param from TCPConnector. ([#2377](https://github.com/aio-libs/aiohttp/pull/2377))
* Add DeprecationWarning for returning HTTPException ([#2415](https://github.com/aio-libs/aiohttp/pull/2415))
* send\_str(), send\_bytes(), send\_json(), ping() and pong() are
  genuine async functions now. ([#2475](https://github.com/aio-libs/aiohttp/pull/2475))
* Drop undocumented app.on\_pre\_signal and app.on\_post\_signal. Signal
  handlers should be coroutines, support for regular functions is dropped.
  ([#2480](https://github.com/aio-libs/aiohttp/pull/2480))
* StreamResponse.drain() is not a part of public API anymore, just use await
  StreamResponse.write(). StreamResponse.write is converted to async
  function. ([#2483](https://github.com/aio-libs/aiohttp/pull/2483))
* Drop deprecated slow\_request\_timeout param and \*\*kwargs` from
  RequestHandler. ([#2500](https://github.com/aio-libs/aiohttp/pull/2500))
* Drop deprecated resource.url(). ([#2501](https://github.com/aio-libs/aiohttp/pull/2501))
* Remove %u and %l format specifiers from access log format. ([#2506](https://github.com/aio-libs/aiohttp/pull/2506))
* Drop deprecated request.GET property. ([#2547](https://github.com/aio-libs/aiohttp/pull/2547))
* Simplify stream classes: drop ChunksQueue and FlowControlChunksQueue,
  merge FlowControlStreamReader functionality into StreamReader, drop
  FlowControlStreamReader name. ([#2555](https://github.com/aio-libs/aiohttp/pull/2555))
* Do not create a new resource on router.add\_get(…, allow\_head=True)
  ([#2585](https://github.com/aio-libs/aiohttp/pull/2585))
* Drop access to TCP tuning options from PayloadWriter and Response classes
  ([#2604](https://github.com/aio-libs/aiohttp/pull/2604))
* Drop deprecated encoding parameter from client API ([#2606](https://github.com/aio-libs/aiohttp/pull/2606))
* Deprecate `verify_ssl`, `ssl_context` and `fingerprint` parameters in
  client API ([#2626](https://github.com/aio-libs/aiohttp/pull/2626))
* Get rid of the legacy class StreamWriter. ([#2651](https://github.com/aio-libs/aiohttp/pull/2651))
* Forbid non-strings in resource.url\_for() parameters. ([#2668](https://github.com/aio-libs/aiohttp/pull/2668))
* Deprecate inheritance from `ClientSession` and `web.Application` and
  custom user attributes for `ClientSession`, `web.Request` and
  `web.Application` ([#2691](https://github.com/aio-libs/aiohttp/pull/2691))
* Drop resp = await aiohttp.request(…) syntax for sake of async with
  aiohttp.request(…) as resp:. ([#2540](https://github.com/aio-libs/aiohttp/pull/2540))
* Forbid synchronous context managers for ClientSession and test
  server/client. ([#2362](https://github.com/aio-libs/aiohttp/pull/2362))

### Misc[¶](#id888 "Link to this heading")

* #2552

---

## 2.3.10 (2018-02-02)[¶](#id889 "Link to this heading")

* Fix 100% CPU usage on HTTP GET and websocket connection just after it ([#1955](https://github.com/aio-libs/aiohttp/pull/1955))
* Patch broken ssl.match\_hostname() on Python<3.7 ([#2674](https://github.com/aio-libs/aiohttp/pull/2674))

---

## 2.3.9 (2018-01-16)[¶](#id892 "Link to this heading")

* Fix colon handing in path for dynamic resources ([#2670](https://github.com/aio-libs/aiohttp/pull/2670))

---

## 2.3.8 (2018-01-15)[¶](#id894 "Link to this heading")

* Do not use yarl.unquote internal function in aiohttp. Fix
  incorrectly unquoted path part in URL dispatcher ([#2662](https://github.com/aio-libs/aiohttp/pull/2662))
* Fix compatibility with yarl==1.0.0 ([#2662](https://github.com/aio-libs/aiohttp/pull/2662))

---

## 2.3.7 (2017-12-27)[¶](#id897 "Link to this heading")

* Fixed race-condition for iterating addresses from the DNSCache. ([#2620](https://github.com/aio-libs/aiohttp/pull/2620))
* Fix docstring for request.host ([#2591](https://github.com/aio-libs/aiohttp/pull/2591))
* Fix docstring for request.remote ([#2592](https://github.com/aio-libs/aiohttp/pull/2592))

---

## 2.3.6 (2017-12-04)[¶](#id901 "Link to this heading")

* Correct request.app context (for handlers not just middlewares). ([#2577](https://github.com/aio-libs/aiohttp/pull/2577))

---

## 2.3.5 (2017-11-30)[¶](#id903 "Link to this heading")

* Fix compatibility with pytest 3.3+ ([#2565](https://github.com/aio-libs/aiohttp/pull/2565))

---

## 2.3.4 (2017-11-29)[¶](#id905 "Link to this heading")

* Make request.app point to proper application instance when using nested
  applications (with middlewares). ([#2550](https://github.com/aio-libs/aiohttp/pull/2550))
* Change base class of ClientConnectorSSLError to ClientSSLError from
  ClientConnectorError. ([#2563](https://github.com/aio-libs/aiohttp/pull/2563))
* Return client connection back to free pool on error in connector.connect().
  ([#2567](https://github.com/aio-libs/aiohttp/pull/2567))

---

## 2.3.3 (2017-11-17)[¶](#id909 "Link to this heading")

* Having a ; in Response content type does not assume it contains a charset
  anymore. ([#2197](https://github.com/aio-libs/aiohttp/pull/2197))
* Use getattr(asyncio, ‘async’) for keeping compatibility with Python 3.7.
  ([#2476](https://github.com/aio-libs/aiohttp/pull/2476))
* Ignore NotImplementedError raised by set\_child\_watcher from uvloop.
  ([#2491](https://github.com/aio-libs/aiohttp/pull/2491))
* Fix warning in ClientSession.\_\_del\_\_ by stopping to try to close it.
  ([#2523](https://github.com/aio-libs/aiohttp/pull/2523))
* Fixed typo’s in Third-party libraries page. And added async-v20 to the list
  ([#2510](https://github.com/aio-libs/aiohttp/pull/2510))

---

## 2.3.2 (2017-11-01)[¶](#id915 "Link to this heading")

* Fix passing client max size on cloning request obj. ([#2385](https://github.com/aio-libs/aiohttp/pull/2385))
* Fix ClientConnectorSSLError and ClientProxyConnectionError for proxy
  connector. ([#2408](https://github.com/aio-libs/aiohttp/pull/2408))
* Drop generated \_http\_parser shared object from tarball distribution. ([#2414](https://github.com/aio-libs/aiohttp/pull/2414))
* Fix connector convert OSError to ClientConnectorError. ([#2423](https://github.com/aio-libs/aiohttp/pull/2423))
* Fix connection attempts for multiple dns hosts. ([#2424](https://github.com/aio-libs/aiohttp/pull/2424))
* Fix ValueError for AF\_INET6 sockets if a preexisting INET6 socket to the
  aiohttp.web.run\_app function. ([#2431](https://github.com/aio-libs/aiohttp/pull/2431))
* \_SessionRequestContextManager closes the session properly now. ([#2441](https://github.com/aio-libs/aiohttp/pull/2441))
* Rename from\_env to trust\_env in client reference. ([#2451](https://github.com/aio-libs/aiohttp/pull/2451))

---

## 2.3.1 (2017-10-18)[¶](#id924 "Link to this heading")

* Relax attribute lookup in warning about old-styled middleware ([#2340](https://github.com/aio-libs/aiohttp/pull/2340))

---

## 2.3.0 (2017-10-18)[¶](#id926 "Link to this heading")

### Features[¶](#id927 "Link to this heading")

* Add SSL related params to ClientSession.request ([#1128](https://github.com/aio-libs/aiohttp/pull/1128))
* Make enable\_compression work on HTTP/1.0 ([#1828](https://github.com/aio-libs/aiohttp/pull/1828))
* Deprecate registering synchronous web handlers ([#1993](https://github.com/aio-libs/aiohttp/pull/1993))
* Switch to multidict 3.0. All HTTP headers preserve casing now but compared
  in case-insensitive way. ([#1994](https://github.com/aio-libs/aiohttp/pull/1994))
* Improvement for normalize\_path\_middleware. Added possibility to handle URLs
  with query string. ([#1995](https://github.com/aio-libs/aiohttp/pull/1995))
* Use towncrier for CHANGES.txt build ([#1997](https://github.com/aio-libs/aiohttp/pull/1997))
* Implement trust\_env=True param in ClientSession. ([#1998](https://github.com/aio-libs/aiohttp/pull/1998))
* Added variable to customize proxy headers ([#2001](https://github.com/aio-libs/aiohttp/pull/2001))
* Implement router.add\_routes and router decorators. ([#2004](https://github.com/aio-libs/aiohttp/pull/2004))
* Deprecated BaseRequest.has\_body in favor of
  BaseRequest.can\_read\_body Added BaseRequest.body\_exists
  attribute that stays static for the lifetime of the request ([#2005](https://github.com/aio-libs/aiohttp/pull/2005))
* Provide BaseRequest.loop attribute ([#2024](https://github.com/aio-libs/aiohttp/pull/2024))
* Make \_CoroGuard awaitable and fix ClientSession.close warning message
  ([#2026](https://github.com/aio-libs/aiohttp/pull/2026))
* Responses to redirects without Location header are returned instead of
  raising a RuntimeError ([#2030](https://github.com/aio-libs/aiohttp/pull/2030))
* Added get\_client, get\_server, setUpAsync and tearDownAsync methods to
  AioHTTPTestCase ([#2032](https://github.com/aio-libs/aiohttp/pull/2032))
* Add automatically a SafeChildWatcher to the test loop ([#2058](https://github.com/aio-libs/aiohttp/pull/2058))
* add ability to disable automatic response decompression ([#2110](https://github.com/aio-libs/aiohttp/pull/2110))
* Add support for throttling DNS request, avoiding the requests saturation when
  there is a miss in the DNS cache and many requests getting into the connector
  at the same time. ([#2111](https://github.com/aio-libs/aiohttp/pull/2111))
* Use request for getting access log information instead of message/transport
  pair. Add RequestBase.remote property for accessing to IP of client
  initiated HTTP request. ([#2123](https://github.com/aio-libs/aiohttp/pull/2123))
* json() raises a ContentTypeError exception if the content-type does not meet
  the requirements instead of raising a generic ClientResponseError. ([#2136](https://github.com/aio-libs/aiohttp/pull/2136))
* Make the HTTP client able to return HTTP chunks when chunked transfer
  encoding is used. ([#2150](https://github.com/aio-libs/aiohttp/pull/2150))
* add append\_version arg into StaticResource.url and
  StaticResource.url\_for methods for getting an url with hash (version) of
  the file. ([#2157](https://github.com/aio-libs/aiohttp/pull/2157))
* Fix parsing the Forwarded header. \* commas and semicolons are allowed inside
  quoted-strings; \* empty forwarded-pairs (as in for=\_1;;by=\_2) are allowed; \*
  non-standard parameters are allowed (although this alone could be easily done
  in the previous parser). ([#2173](https://github.com/aio-libs/aiohttp/pull/2173))
* Don’t require ssl module to run. aiohttp does not require SSL to function.
  The code paths involved with SSL will only be hit upon SSL usage. Raise
  RuntimeError if HTTPS protocol is required but ssl module is not present.
  ([#2221](https://github.com/aio-libs/aiohttp/pull/2221))
* Accept coroutine fixtures in pytest plugin ([#2223](https://github.com/aio-libs/aiohttp/pull/2223))
* Call shutdown\_asyncgens before event loop closing on Python 3.6. ([#2227](https://github.com/aio-libs/aiohttp/pull/2227))
* Speed up Signals when there are no receivers ([#2229](https://github.com/aio-libs/aiohttp/pull/2229))
* Raise InvalidURL instead of ValueError on fetches with invalid URL.
  ([#2241](https://github.com/aio-libs/aiohttp/pull/2241))
* Move DummyCookieJar into cookiejar.py ([#2242](https://github.com/aio-libs/aiohttp/pull/2242))
* run\_app: Make print=None disable printing ([#2260](https://github.com/aio-libs/aiohttp/pull/2260))
* Support brotli encoding (generic-purpose lossless compression algorithm)
  ([#2270](https://github.com/aio-libs/aiohttp/pull/2270))
* Add server support for WebSockets Per-Message Deflate. Add client option to
  add deflate compress header in WebSockets request header. If calling
  ClientSession.ws\_connect() with compress=15 the client will support deflate
  compress negotiation. ([#2273](https://github.com/aio-libs/aiohttp/pull/2273))
* Support verify\_ssl, fingerprint, ssl\_context and proxy\_headers by
  client.ws\_connect. ([#2292](https://github.com/aio-libs/aiohttp/pull/2292))
* Added aiohttp.ClientConnectorSSLError when connection fails due
  ssl.SSLError ([#2294](https://github.com/aio-libs/aiohttp/pull/2294))
* aiohttp.web.Application.make\_handler support access\_log\_class ([#2315](https://github.com/aio-libs/aiohttp/pull/2315))
* Build HTTP parser extension in non-strict mode by default. ([#2332](https://github.com/aio-libs/aiohttp/pull/2332))

### Bugfixes[¶](#id963 "Link to this heading")

* Clear auth information on redirecting to other domain ([#1699](https://github.com/aio-libs/aiohttp/pull/1699))
* Fix missing app.loop on startup hooks during tests ([#2060](https://github.com/aio-libs/aiohttp/pull/2060))
* Fix issue with synchronous session closing when using ClientSession as an
  asynchronous context manager. ([#2063](https://github.com/aio-libs/aiohttp/pull/2063))
* Fix issue with CookieJar incorrectly expiring cookies in some edge cases.
  ([#2084](https://github.com/aio-libs/aiohttp/pull/2084))
* Force use of IPv4 during test, this will make tests run in a Docker container
  ([#2104](https://github.com/aio-libs/aiohttp/pull/2104))
* Warnings about unawaited coroutines now correctly point to the user’s code.
  ([#2106](https://github.com/aio-libs/aiohttp/pull/2106))
* Fix issue with IndexError being raised by the StreamReader.iter\_chunks()
  generator. ([#2112](https://github.com/aio-libs/aiohttp/pull/2112))
* Support HTTP 308 Permanent redirect in client class. ([#2114](https://github.com/aio-libs/aiohttp/pull/2114))
* Fix FileResponse sending empty chunked body on 304. ([#2143](https://github.com/aio-libs/aiohttp/pull/2143))
* Do not add Content-Length: 0 to GET/HEAD/TRACE/OPTIONS requests by default.
  ([#2167](https://github.com/aio-libs/aiohttp/pull/2167))
* Fix parsing the Forwarded header according to RFC 7239. ([#2170](https://github.com/aio-libs/aiohttp/pull/2170))
* Securely determining remote/scheme/host #2171 ([#2171](https://github.com/aio-libs/aiohttp/pull/2171))
* Fix header name parsing, if name is split into multiple lines ([#2183](https://github.com/aio-libs/aiohttp/pull/2183))
* Handle session close during connection, KeyError:
  <aiohttp.connector.\_TransportPlaceholder> ([#2193](https://github.com/aio-libs/aiohttp/pull/2193))
* Fixes uncaught TypeError in helpers.guess\_filename if name is not a
  string ([#2201](https://github.com/aio-libs/aiohttp/pull/2201))
* Raise OSError on async DNS lookup if resolved domain is an alias for another
  one, which does not have an A or CNAME record. ([#2231](https://github.com/aio-libs/aiohttp/pull/2231))
* Fix incorrect warning in StreamReader. ([#2251](https://github.com/aio-libs/aiohttp/pull/2251))
* Properly clone state of web request ([#2284](https://github.com/aio-libs/aiohttp/pull/2284))
* Fix C HTTP parser for cases when status line is split into different TCP
  packets. ([#2311](https://github.com/aio-libs/aiohttp/pull/2311))
* Fix web.FileResponse overriding user supplied Content-Type ([#2317](https://github.com/aio-libs/aiohttp/pull/2317))

### Improved Documentation[¶](#id984 "Link to this heading")

* Add a note about possible performance degradation in await resp.text() if
  charset was not provided by Content-Type HTTP header. Pass explicit
  encoding to solve it. ([#1811](https://github.com/aio-libs/aiohttp/pull/1811))
* Drop disqus widget from documentation pages. ([#2018](https://github.com/aio-libs/aiohttp/pull/2018))
* Add a graceful shutdown section to the client usage documentation. ([#2039](https://github.com/aio-libs/aiohttp/pull/2039))
* Document connector\_owner parameter. ([#2072](https://github.com/aio-libs/aiohttp/pull/2072))
* Update the doc of web.Application ([#2081](https://github.com/aio-libs/aiohttp/pull/2081))
* Fix mistake about access log disabling. ([#2085](https://github.com/aio-libs/aiohttp/pull/2085))
* Add example usage of on\_startup and on\_shutdown signals by creating and
  disposing an aiopg connection engine. ([#2131](https://github.com/aio-libs/aiohttp/pull/2131))
* Document encoded=True for yarl.URL, it disables all yarl transformations.
  ([#2198](https://github.com/aio-libs/aiohttp/pull/2198))
* Document that all app’s middleware factories are run for every request.
  ([#2225](https://github.com/aio-libs/aiohttp/pull/2225))
* Reflect the fact that default resolver is threaded one starting from aiohttp
  1.1 ([#2228](https://github.com/aio-libs/aiohttp/pull/2228))

### Deprecations and Removals[¶](#id995 "Link to this heading")

* Drop deprecated Server.finish\_connections ([#2006](https://github.com/aio-libs/aiohttp/pull/2006))
* Drop %O format from logging, use %b instead. Drop %e format from logging,
  environment variables are not supported anymore. ([#2123](https://github.com/aio-libs/aiohttp/pull/2123))
* Drop deprecated secure\_proxy\_ssl\_header support ([#2171](https://github.com/aio-libs/aiohttp/pull/2171))
* Removed TimeService in favor of simple caching. TimeService also had a bug
  where it lost about 0.5 seconds per second. ([#2176](https://github.com/aio-libs/aiohttp/pull/2176))
* Drop unused response\_factory from static files API ([#2290](https://github.com/aio-libs/aiohttp/pull/2290))

### Misc[¶](#id1001 "Link to this heading")

* #2013, #2014, #2048, #2094, #2149, #2187, #2214, #2225, #2243, #2248

---

## 2.2.5 (2017-08-03)[¶](#id1002 "Link to this heading")

* Don’t raise deprecation warning on
  loop.run\_until\_complete(client.close()) ([#2065](https://github.com/aio-libs/aiohttp/pull/2065))

---

## 2.2.4 (2017-08-02)[¶](#id1004 "Link to this heading")

* Fix issue with synchronous session closing when using ClientSession
  as an asynchronous context manager. ([#2063](https://github.com/aio-libs/aiohttp/pull/2063))

---

## 2.2.3 (2017-07-04)[¶](#id1006 "Link to this heading")

* Fix \_CoroGuard for python 3.4

---

## 2.2.2 (2017-07-03)[¶](#id1007 "Link to this heading")

* Allow await session.close() along with yield from session.close()

---

## 2.2.1 (2017-07-02)[¶](#id1008 "Link to this heading")

* Relax yarl requirement to 0.11+
* Backport #2026: session.close *is* a coroutine ([#2029](https://github.com/aio-libs/aiohttp/pull/2029))

---

## 2.2.0 (2017-06-20)[¶](#id1010 "Link to this heading")

* Add doc for add\_head, update doc for add\_get. ([#1944](https://github.com/aio-libs/aiohttp/pull/1944))
* Fixed consecutive calls for Response.write\_eof.
* Retain method attributes (e.g. `__doc__`) when registering synchronous
  handlers for resources. ([#1953](https://github.com/aio-libs/aiohttp/pull/1953))
* Added signal TERM handling in run\_app to gracefully exit ([#1932](https://github.com/aio-libs/aiohttp/pull/1932))
* Fix websocket issues caused by frame fragmentation. ([#1962](https://github.com/aio-libs/aiohttp/pull/1962))
* Raise RuntimeError is you try to set the Content Length and enable
  chunked encoding at the same time ([#1941](https://github.com/aio-libs/aiohttp/pull/1941))
* Small update for unittest\_run\_loop
* Use CIMultiDict for ClientRequest.skip\_auto\_headers ([#1970](https://github.com/aio-libs/aiohttp/pull/1970))
* Fix wrong startup sequence: test server and run\_app() are not raise
  DeprecationWarning now ([#1947](https://github.com/aio-libs/aiohttp/pull/1947))
* Make sure cleanup signal is sent if startup signal has been sent ([#1959](https://github.com/aio-libs/aiohttp/pull/1959))
* Fixed server keep-alive handler, could cause 100% cpu utilization ([#1955](https://github.com/aio-libs/aiohttp/pull/1955))
* Connection can be destroyed before response get processed if
  await aiohttp.request(..) is used ([#1981](https://github.com/aio-libs/aiohttp/pull/1981))
* MultipartReader does not work with -OO ([#1969](https://github.com/aio-libs/aiohttp/pull/1969))
* Fixed ClientPayloadError with blank Content-Encoding header ([#1931](https://github.com/aio-libs/aiohttp/pull/1931))
* Support deflate encoding implemented in httpbin.org/deflate ([#1918](https://github.com/aio-libs/aiohttp/pull/1918))
* Fix BadStatusLine caused by extra CRLF after POST data ([#1792](https://github.com/aio-libs/aiohttp/pull/1792))
* Keep a reference to ClientSession in response object ([#1985](https://github.com/aio-libs/aiohttp/pull/1985))
* Deprecate undocumented app.on\_loop\_available signal ([#1978](https://github.com/aio-libs/aiohttp/pull/1978))

---

## 2.1.0 (2017-05-26)[¶](#id1027 "Link to this heading")

* Added support for experimental async-tokio event loop written in Rust
  <https://github.com/PyO3/tokio>
* Write to transport `\r\n` before closing after keepalive timeout,
  otherwise client can not detect socket disconnection. ([#1883](https://github.com/aio-libs/aiohttp/pull/1883))
* Only call loop.close in run\_app if the user did *not* supply a loop.
  Useful for allowing clients to specify their own cleanup before closing the
  asyncio loop if they wish to tightly control loop behavior
* Content disposition with semicolon in filename ([#917](https://github.com/aio-libs/aiohttp/pull/917))
* Added request\_info to response object and ClientResponseError. ([#1733](https://github.com/aio-libs/aiohttp/pull/1733))
* Added history to ClientResponseError. ([#1741](https://github.com/aio-libs/aiohttp/pull/1741))
* Allow to disable redirect url re-quoting ([#1474](https://github.com/aio-libs/aiohttp/pull/1474))
* Handle RuntimeError from transport ([#1790](https://github.com/aio-libs/aiohttp/pull/1790))
* Dropped “%O” in access logger ([#1673](https://github.com/aio-libs/aiohttp/pull/1673))
* Added args and kwargs to unittest\_run\_loop. Useful with other
  decorators, for example @patch. ([#1803](https://github.com/aio-libs/aiohttp/pull/1803))
* Added iter\_chunks to response.content object. ([#1805](https://github.com/aio-libs/aiohttp/pull/1805))
* Avoid creating TimerContext when there is no timeout to allow
  compatibility with Tornado. ([#1817](https://github.com/aio-libs/aiohttp/pull/1817)) ([#1180](https://github.com/aio-libs/aiohttp/pull/1180))
* Add proxy\_from\_env to ClientRequest to read from environment
  variables. ([#1791](https://github.com/aio-libs/aiohttp/pull/1791))
* Add DummyCookieJar helper. ([#1830](https://github.com/aio-libs/aiohttp/pull/1830))
* Fix assertion errors in Python 3.4 from noop helper. ([#1847](https://github.com/aio-libs/aiohttp/pull/1847))
* Do not unquote + in match\_info values ([#1816](https://github.com/aio-libs/aiohttp/pull/1816))
* Use Forwarded, X-Forwarded-Scheme and X-Forwarded-Host for better scheme and
  host resolution. ([#1134](https://github.com/aio-libs/aiohttp/pull/1134))
* Fix sub-application middlewares resolution order ([#1853](https://github.com/aio-libs/aiohttp/pull/1853))
* Fix applications comparison ([#1866](https://github.com/aio-libs/aiohttp/pull/1866))
* Fix static location in index when prefix is used ([#1662](https://github.com/aio-libs/aiohttp/pull/1662))
* Make test server more reliable ([#1896](https://github.com/aio-libs/aiohttp/pull/1896))
* Extend list of web exceptions, add HTTPUnprocessableEntity,
  HTTPFailedDependency, HTTPInsufficientStorage status codes ([#1920](https://github.com/aio-libs/aiohttp/pull/1920))

---

## 2.0.7 (2017-04-12)[¶](#id1049 "Link to this heading")

* Fix *pypi* distribution
* Fix exception description ([#1807](https://github.com/aio-libs/aiohttp/pull/1807))
* Handle socket error in FileResponse ([#1773](https://github.com/aio-libs/aiohttp/pull/1773))
* Cancel websocket heartbeat on close ([#1793](https://github.com/aio-libs/aiohttp/pull/1793))

---

## 2.0.6 (2017-04-04)[¶](#id1053 "Link to this heading")

* Keeping blank values for request.post() and multipart.form() ([#1765](https://github.com/aio-libs/aiohttp/pull/1765))
* TypeError in data\_received of ResponseHandler ([#1770](https://github.com/aio-libs/aiohttp/pull/1770))
* Fix `web.run_app` not to bind to default host-port pair if only socket is
  passed ([#1786](https://github.com/aio-libs/aiohttp/pull/1786))

---

## 2.0.5 (2017-03-29)[¶](#id1057 "Link to this heading")

* Memory leak with aiohttp.request ([#1756](https://github.com/aio-libs/aiohttp/pull/1756))
* Disable cleanup closed ssl transports by default.
* Exception in request handling if the server responds before the body
  is sent ([#1761](https://github.com/aio-libs/aiohttp/pull/1761))

---

## 2.0.4 (2017-03-27)[¶](#id1060 "Link to this heading")

* Memory leak with aiohttp.request ([#1756](https://github.com/aio-libs/aiohttp/pull/1756))
* Encoding is always UTF-8 in POST data ([#1750](https://github.com/aio-libs/aiohttp/pull/1750))
* Do not add “Content-Disposition” header by default ([#1755](https://github.com/aio-libs/aiohttp/pull/1755))

---

## 2.0.3 (2017-03-24)[¶](#id1064 "Link to this heading")

* Call https website through proxy will cause error ([#1745](https://github.com/aio-libs/aiohttp/pull/1745))
* Fix exception on multipart/form-data post if content-type is not set ([#1743](https://github.com/aio-libs/aiohttp/pull/1743))

---

## 2.0.2 (2017-03-21)[¶](#id1067 "Link to this heading")

* Fixed Application.on\_loop\_available signal ([#1739](https://github.com/aio-libs/aiohttp/pull/1739))
* Remove debug code

---

## 2.0.1 (2017-03-21)[¶](#id1069 "Link to this heading")

* Fix allow-head to include name on route ([#1737](https://github.com/aio-libs/aiohttp/pull/1737))
* Fixed AttributeError in WebSocketResponse.can\_prepare ([#1736](https://github.com/aio-libs/aiohttp/pull/1736))

---

## 2.0.0 (2017-03-20)[¶](#id1072 "Link to this heading")

* Added json to ClientSession.request() method ([#1726](https://github.com/aio-libs/aiohttp/pull/1726))
* Added session’s raise\_for\_status parameter, automatically calls
  raise\_for\_status() on any request. ([#1724](https://github.com/aio-libs/aiohttp/pull/1724))
* response.json() raises ClientResponseError exception if response’s
  content type does not match ([#1723](https://github.com/aio-libs/aiohttp/pull/1723))
  - Cleanup timer and loop handle on any client exception.
* Deprecate loop parameter for Application’s constructor
* Properly handle payload errors ([#1710](https://github.com/aio-libs/aiohttp/pull/1710))
* Added ClientWebSocketResponse.get\_extra\_info() ([#1717](https://github.com/aio-libs/aiohttp/pull/1717))
* It is not possible to combine Transfer-Encoding and chunked parameter,
  same for compress and Content-Encoding ([#1655](https://github.com/aio-libs/aiohttp/pull/1655))
* Connector’s limit parameter indicates total concurrent connections.
  New limit\_per\_host added, indicates total connections per endpoint. ([#1601](https://github.com/aio-libs/aiohttp/pull/1601))
* Use url’s raw\_host for name resolution ([#1685](https://github.com/aio-libs/aiohttp/pull/1685))
* Change ClientResponse.url to yarl.URL instance ([#1654](https://github.com/aio-libs/aiohttp/pull/1654))
* Add max\_size parameter to web.Request reading methods ([#1133](https://github.com/aio-libs/aiohttp/pull/1133))
* Web Request.post() stores data in temp files ([#1469](https://github.com/aio-libs/aiohttp/pull/1469))
* Add the allow\_head=True keyword argument for add\_get ([#1618](https://github.com/aio-libs/aiohttp/pull/1618))
* run\_app and the Command Line Interface now support serving over
  Unix domain sockets for faster inter-process communication.
* run\_app now supports passing a preexisting socket object. This can be useful
  e.g. for socket-based activated applications, when binding of a socket is
  done by the parent process.
* Implementation for Trailer headers parser is broken ([#1619](https://github.com/aio-libs/aiohttp/pull/1619))
* Fix FileResponse to not fall on bad request (range out of file size)
* Fix FileResponse to correct stream video to Chromes
* Deprecate public low-level api ([#1657](https://github.com/aio-libs/aiohttp/pull/1657))
* Deprecate encoding parameter for ClientSession.request() method
* Dropped aiohttp.wsgi ([#1108](https://github.com/aio-libs/aiohttp/pull/1108))
* Dropped version from ClientSession.request() method
* Dropped websocket version 76 support ([#1160](https://github.com/aio-libs/aiohttp/pull/1160))
* Dropped: aiohttp.protocol.HttpPrefixParser ([#1590](https://github.com/aio-libs/aiohttp/pull/1590))
* Dropped: Servers response’s .started, .start() and
  .can\_start() method ([#1591](https://github.com/aio-libs/aiohttp/pull/1591))
* Dropped: Adding sub app via app.router.add\_subapp() is deprecated
  use app.add\_subapp() instead ([#1592](https://github.com/aio-libs/aiohttp/pull/1592))
* Dropped: Application.finish() and Application.register\_on\_finish() ([#1602](https://github.com/aio-libs/aiohttp/pull/1602))
* Dropped: web.Request.GET and web.Request.POST
* Dropped: aiohttp.get(), aiohttp.options(), aiohttp.head(),
  aiohttp.post(), aiohttp.put(), aiohttp.patch(), aiohttp.delete(), and
  aiohttp.ws\_connect() ([#1593](https://github.com/aio-libs/aiohttp/pull/1593))
* Dropped: aiohttp.web.WebSocketResponse.receive\_msg() ([#1605](https://github.com/aio-libs/aiohttp/pull/1605))
* Dropped: ServerHttpProtocol.keep\_alive\_timeout attribute and
  keep-alive, keep\_alive\_on, timeout, log constructor parameters ([#1606](https://github.com/aio-libs/aiohttp/pull/1606))
* Dropped: TCPConnector’s` .resolve, .resolved\_hosts,
  .clear\_resolved\_hosts() attributes and resolve constructor
  parameter ([#1607](https://github.com/aio-libs/aiohttp/pull/1607))
* Dropped ProxyConnector ([#1609](https://github.com/aio-libs/aiohttp/pull/1609))

---

## 1.3.5 (2017-03-16)[¶](#id1098 "Link to this heading")

* Fixed None timeout support ([#1720](https://github.com/aio-libs/aiohttp/pull/1720))

---

## 1.3.4 (2017-03-14)[¶](#id1100 "Link to this heading")

* Revert timeout handling in client request
* Fix StreamResponse representation after eof
* Fix file\_sender to not fall on bad request (range out of file size)
* Fix file\_sender to correct stream video to Chromes
* Fix NotImplementedError server exception ([#1703](https://github.com/aio-libs/aiohttp/pull/1703))
* Clearer error message for URL without a host name. ([#1691](https://github.com/aio-libs/aiohttp/pull/1691))
* Silence deprecation warning in \_\_repr\_\_ ([#1690](https://github.com/aio-libs/aiohttp/pull/1690))
* IDN + HTTPS = ssl.CertificateError ([#1685](https://github.com/aio-libs/aiohttp/pull/1685))

---

## 1.3.3 (2017-02-19)[¶](#id1105 "Link to this heading")

* Fixed memory leak in time service ([#1656](https://github.com/aio-libs/aiohttp/pull/1656))

---

## 1.3.2 (2017-02-16)[¶](#id1107 "Link to this heading")

* Awaiting on WebSocketResponse.send\_\* does not work ([#1645](https://github.com/aio-libs/aiohttp/pull/1645))
* Fix multiple calls to client ws\_connect when using a shared header
  dict ([#1643](https://github.com/aio-libs/aiohttp/pull/1643))
* Make CookieJar.filter\_cookies() accept plain string parameter. ([#1636](https://github.com/aio-libs/aiohttp/pull/1636))

---

## 1.3.1 (2017-02-09)[¶](#id1111 "Link to this heading")

* Handle CLOSING in WebSocketResponse.\_\_anext\_\_
* Fixed AttributeError ‘drain’ for server websocket handler ([#1613](https://github.com/aio-libs/aiohttp/pull/1613))

---

## 1.3.0 (2017-02-08)[¶](#id1113 "Link to this heading")

* Multipart writer validates the data on append instead of on a
  request send ([#920](https://github.com/aio-libs/aiohttp/pull/920))
* Multipart reader accepts multipart messages with or without their epilogue
  to consistently handle valid and legacy behaviors ([#1526](https://github.com/aio-libs/aiohttp/pull/1526)) ([#1581](https://github.com/aio-libs/aiohttp/pull/1581))
* Separate read + connect + request timeouts # 1523
* Do not swallow Upgrade header ([#1587](https://github.com/aio-libs/aiohttp/pull/1587))
* Fix polls demo run application ([#1487](https://github.com/aio-libs/aiohttp/pull/1487))
* Ignore unknown 1XX status codes in client ([#1353](https://github.com/aio-libs/aiohttp/pull/1353))
* Fix sub-Multipart messages missing their headers on serialization ([#1525](https://github.com/aio-libs/aiohttp/pull/1525))
* Do not use readline when reading the content of a part
  in the multipart reader ([#1535](https://github.com/aio-libs/aiohttp/pull/1535))
* Add optional flag for quoting FormData fields ([#916](https://github.com/aio-libs/aiohttp/pull/916))
* 416 Range Not Satisfiable if requested range end > file size ([#1588](https://github.com/aio-libs/aiohttp/pull/1588))
* Having a : or @ in a route does not work ([#1552](https://github.com/aio-libs/aiohttp/pull/1552))
* Added receive\_timeout timeout for websocket to receive complete
  message. ([#1325](https://github.com/aio-libs/aiohttp/pull/1325))
* Added heartbeat parameter for websocket to automatically send
  ping message. ([#1024](https://github.com/aio-libs/aiohttp/pull/1024)) ([#777](https://github.com/aio-libs/aiohttp/pull/777))
* Remove web.Application dependency from web.UrlDispatcher ([#1510](https://github.com/aio-libs/aiohttp/pull/1510))
* Accepting back-pressure from slow websocket clients ([#1367](https://github.com/aio-libs/aiohttp/pull/1367))
* Do not pause transport during set\_parser stage ([#1211](https://github.com/aio-libs/aiohttp/pull/1211))
* Lingering close does not terminate before timeout ([#1559](https://github.com/aio-libs/aiohttp/pull/1559))
* setsockopt may raise OSError exception if socket is closed already ([#1595](https://github.com/aio-libs/aiohttp/pull/1595))
* Lots of CancelledError when requests are interrupted ([#1565](https://github.com/aio-libs/aiohttp/pull/1565))
* Allow users to specify what should happen to decoding errors
  when calling a responses text() method ([#1542](https://github.com/aio-libs/aiohttp/pull/1542))
* Back port std module http.cookies for python3.4.2 ([#1566](https://github.com/aio-libs/aiohttp/pull/1566))
* Maintain url’s fragment in client response ([#1314](https://github.com/aio-libs/aiohttp/pull/1314))
* Allow concurrently close WebSocket connection ([#754](https://github.com/aio-libs/aiohttp/pull/754))
* Gzipped responses with empty body raises ContentEncodingError ([#609](https://github.com/aio-libs/aiohttp/pull/609))
* Return 504 if request handle raises TimeoutError.
* Refactor how we use keep-alive and close lingering timeouts.
* Close response connection if we can not consume whole http
  message during client response release
* Abort closed ssl client transports, broken servers can keep socket
  open un-limit time ([#1568](https://github.com/aio-libs/aiohttp/pull/1568))
* Log warning instead of RuntimeError is websocket connection is closed.
* Deprecated: aiohttp.protocol.HttpPrefixParser
  will be removed in 1.4 ([#1590](https://github.com/aio-libs/aiohttp/pull/1590))
* Deprecated: Servers response’s .started, .start() and
  .can\_start() method will be removed in 1.4 ([#1591](https://github.com/aio-libs/aiohttp/pull/1591))
* Deprecated: Adding sub app via app.router.add\_subapp() is deprecated
  use app.add\_subapp() instead, will be removed in 1.4 ([#1592](https://github.com/aio-libs/aiohttp/pull/1592))
* Deprecated: aiohttp.get(), aiohttp.options(), aiohttp.head(), aiohttp.post(),
  aiohttp.put(), aiohttp.patch(), aiohttp.delete(), and aiohttp.ws\_connect()
  will be removed in 1.4 ([#1593](https://github.com/aio-libs/aiohttp/pull/1593))
* Deprecated: Application.finish() and Application.register\_on\_finish()
  will be removed in 1.4 ([#1602](https://github.com/aio-libs/aiohttp/pull/1602))

---

## 1.2.0 (2016-12-17)[¶](#id1145 "Link to this heading")

* Extract BaseRequest from web.Request, introduce web.Server
  (former RequestHandlerFactory), introduce new low-level web server
  which is not coupled with web.Application and routing ([#1362](https://github.com/aio-libs/aiohttp/pull/1362))
* Make TestServer.make\_url compatible with yarl.URL ([#1389](https://github.com/aio-libs/aiohttp/pull/1389))
* Implement range requests for static files ([#1382](https://github.com/aio-libs/aiohttp/pull/1382))
* Support task attribute for StreamResponse ([#1410](https://github.com/aio-libs/aiohttp/pull/1410))
* Drop TestClient.app property, use TestClient.server.app instead
  (BACKWARD INCOMPATIBLE)
* Drop TestClient.handler property, use TestClient.server.handler instead
  (BACKWARD INCOMPATIBLE)
* TestClient.server property returns a test server instance, was
  asyncio.AbstractServer (BACKWARD INCOMPATIBLE)
* Follow gunicorn’s signal semantics in Gunicorn[UVLoop]WebWorker ([#1201](https://github.com/aio-libs/aiohttp/pull/1201))
* Call worker\_int and worker\_abort callbacks in
  Gunicorn[UVLoop]WebWorker ([#1202](https://github.com/aio-libs/aiohttp/pull/1202))
* Has functional tests for client proxy ([#1218](https://github.com/aio-libs/aiohttp/pull/1218))
* Fix bugs with client proxy target path and proxy host with port ([#1413](https://github.com/aio-libs/aiohttp/pull/1413))
* Fix bugs related to the use of unicode hostnames ([#1444](https://github.com/aio-libs/aiohttp/pull/1444))
* Preserve cookie quoting/escaping ([#1453](https://github.com/aio-libs/aiohttp/pull/1453))
* FileSender will send gzipped response if gzip version available ([#1426](https://github.com/aio-libs/aiohttp/pull/1426))
* Don’t override Content-Length header in web.Response if no body
  was set ([#1400](https://github.com/aio-libs/aiohttp/pull/1400))
* Introduce router.post\_init() for solving ([#1373](https://github.com/aio-libs/aiohttp/pull/1373))
* Fix raise error in case of multiple calls of TimeServive.stop()
* Allow to raise web exceptions on router resolving stage ([#1460](https://github.com/aio-libs/aiohttp/pull/1460))
* Add a warning for session creation outside of coroutine ([#1468](https://github.com/aio-libs/aiohttp/pull/1468))
* Avoid a race when application might start accepting incoming requests
  but startup signals are not processed yet e98e8c6
* Raise a RuntimeError when trying to change the status of the HTTP response
  after the headers have been sent ([#1480](https://github.com/aio-libs/aiohttp/pull/1480))
* Fix bug with https proxy acquired cleanup ([#1340](https://github.com/aio-libs/aiohttp/pull/1340))
* Use UTF-8 as the default encoding for multipart text parts ([#1484](https://github.com/aio-libs/aiohttp/pull/1484))

---

## 1.1.6 (2016-11-28)[¶](#id1164 "Link to this heading")

* Fix BodyPartReader.read\_chunk bug about returns zero bytes before
  EOF ([#1428](https://github.com/aio-libs/aiohttp/pull/1428))

---

## 1.1.5 (2016-11-16)[¶](#id1166 "Link to this heading")

* Fix static file serving in fallback mode ([#1401](https://github.com/aio-libs/aiohttp/pull/1401))

---

## 1.1.4 (2016-11-14)[¶](#id1168 "Link to this heading")

* Make TestServer.make\_url compatible with yarl.URL ([#1389](https://github.com/aio-libs/aiohttp/pull/1389))
* Generate informative exception on redirects from server which
  does not provide redirection headers ([#1396](https://github.com/aio-libs/aiohttp/pull/1396))

---

## 1.1.3 (2016-11-10)[¶](#id1171 "Link to this heading")

* Support *root* resources for sub-applications ([#1379](https://github.com/aio-libs/aiohttp/pull/1379))

---

## 1.1.2 (2016-11-08)[¶](#id1173 "Link to this heading")

* Allow starting variables with an underscore ([#1379](https://github.com/aio-libs/aiohttp/pull/1379))
* Properly process UNIX sockets by gunicorn worker ([#1375](https://github.com/aio-libs/aiohttp/pull/1375))
* Fix ordering for FrozenList
* Don’t propagate pre and post signals to sub-application ([#1377](https://github.com/aio-libs/aiohttp/pull/1377))

---

## 1.1.1 (2016-11-04)[¶](#id1177 "Link to this heading")

* Fix documentation generation ([#1120](https://github.com/aio-libs/aiohttp/pull/1120))

---

## 1.1.0 (2016-11-03)[¶](#id1179 "Link to this heading")

* Drop deprecated WSClientDisconnectedError (BACKWARD INCOMPATIBLE)
* Use yarl.URL in client API. The change is 99% backward compatible
  but ClientResponse.url is an yarl.URL instance now. ([#1217](https://github.com/aio-libs/aiohttp/pull/1217))
* Close idle keep-alive connections on shutdown ([#1222](https://github.com/aio-libs/aiohttp/pull/1222))
* Modify regex in AccessLogger to accept underscore and numbers ([#1225](https://github.com/aio-libs/aiohttp/pull/1225))
* Use yarl.URL in web server API. web.Request.rel\_url and web.Request.url are added. URLs and templates are
  percent-encoded now. ([#1224](https://github.com/aio-libs/aiohttp/pull/1224))
* Accept yarl.URL by server redirections ([#1278](https://github.com/aio-libs/aiohttp/pull/1278))
* Return yarl.URL by .make\_url() testing utility ([#1279](https://github.com/aio-libs/aiohttp/pull/1279))
* Properly format IPv6 addresses by aiohttp.web.run\_app ([#1139](https://github.com/aio-libs/aiohttp/pull/1139))
* Use yarl.URL by server API ([#1288](https://github.com/aio-libs/aiohttp/pull/1288))

  + Introduce resource.url\_for(), deprecate resource.url().
  + Implement StaticResource.
  + Inherit SystemRoute from AbstractRoute
  + Drop old-style routes: Route, PlainRoute, DynamicRoute,
    StaticRoute, ResourceAdapter.
* Revert resp.url back to str, introduce resp.url\_obj ([#1292](https://github.com/aio-libs/aiohttp/pull/1292))
* Raise ValueError if BasicAuth login has a “:” character ([#1307](https://github.com/aio-libs/aiohttp/pull/1307))
* Fix bug when ClientRequest send payload file with opened as
  open(‘filename’, ‘r+b’) ([#1306](https://github.com/aio-libs/aiohttp/pull/1306))
* Enhancement to AccessLogger (pass *extra* dict) ([#1303](https://github.com/aio-libs/aiohttp/pull/1303))
* Show more verbose message on import errors ([#1319](https://github.com/aio-libs/aiohttp/pull/1319))
* Added save and load functionality for CookieJar ([#1219](https://github.com/aio-libs/aiohttp/pull/1219))
* Added option on StaticRoute to follow symlinks ([#1299](https://github.com/aio-libs/aiohttp/pull/1299))
* Force encoding of application/json content type to utf-8 ([#1339](https://github.com/aio-libs/aiohttp/pull/1339))
* Fix invalid invocations of errors.LineTooLong ([#1335](https://github.com/aio-libs/aiohttp/pull/1335))
* Websockets: Stop async for iteration when connection is closed ([#1144](https://github.com/aio-libs/aiohttp/pull/1144))
* Ensure TestClient HTTP methods return a context manager ([#1318](https://github.com/aio-libs/aiohttp/pull/1318))
* Raise ClientDisconnectedError to FlowControlStreamReader read function
  if ClientSession object is closed by client when reading data. ([#1323](https://github.com/aio-libs/aiohttp/pull/1323))
* Document deployment without Gunicorn ([#1120](https://github.com/aio-libs/aiohttp/pull/1120))
* Add deprecation warning for MD5 and SHA1 digests when used for fingerprint
  of site certs in TCPConnector. ([#1186](https://github.com/aio-libs/aiohttp/pull/1186))
* Implement sub-applications ([#1301](https://github.com/aio-libs/aiohttp/pull/1301))
* Don’t inherit web.Request from dict but implement
  MutableMapping protocol.
* Implement frozen signals
* Don’t inherit web.Application from dict but implement
  MutableMapping protocol.
* Support freezing for web applications
* Accept access\_log parameter in web.run\_app, use None to disable logging
* Don’t flap tcp\_cork and tcp\_nodelay in regular request handling.
  tcp\_nodelay is still enabled by default.
* Improve performance of web server by removing premature computing of
  Content-Type if the value was set by web.Response constructor.

  While the patch boosts speed of trivial web.Response(text=’OK’,
  content\_type=’text/plain) very well please don’t expect significant
  boost of your application – a couple DB requests and business logic
  is still the main bottleneck.
* Boost performance by adding a custom time service ([#1350](https://github.com/aio-libs/aiohttp/pull/1350))
* Extend ClientResponse with content\_type and charset
  properties like in web.Request. ([#1349](https://github.com/aio-libs/aiohttp/pull/1349))
* Disable aiodns by default ([#559](https://github.com/aio-libs/aiohttp/pull/559))
* Don’t flap tcp\_cork in client code, use TCP\_NODELAY mode by default.
* Implement web.Request.clone() ([#1361](https://github.com/aio-libs/aiohttp/pull/1361))

---

## 1.0.5 (2016-10-11)[¶](#id1207 "Link to this heading")

* Fix StreamReader.\_read\_nowait to return all available
  data up to the requested amount ([#1297](https://github.com/aio-libs/aiohttp/pull/1297))

---

## 1.0.4 (2016-09-22)[¶](#id1209 "Link to this heading")

* Fix FlowControlStreamReader.read\_nowait so that it checks
  whether the transport is paused ([#1206](https://github.com/aio-libs/aiohttp/pull/1206))

---

## 1.0.2 (2016-09-22)[¶](#id1211 "Link to this heading")

* Make CookieJar compatible with 32-bit systems ([#1188](https://github.com/aio-libs/aiohttp/pull/1188))
* Add missing WSMsgType to web\_ws.\_\_all\_\_, see ([#1200](https://github.com/aio-libs/aiohttp/pull/1200))
* Fix CookieJar ctor when called with loop=None ([#1203](https://github.com/aio-libs/aiohttp/pull/1203))
* Fix broken upper-casing in wsgi support ([#1197](https://github.com/aio-libs/aiohttp/pull/1197))

---

## 1.0.1 (2016-09-16)[¶](#id1216 "Link to this heading")

* Restore aiohttp.web.MsgType alias for aiohttp.WSMsgType for sake
  of backward compatibility ([#1178](https://github.com/aio-libs/aiohttp/pull/1178))
* Tune alabaster schema.
* Use text/html content type for displaying index pages by static
  file handler.
* Fix AssertionError in static file handling ([#1177](https://github.com/aio-libs/aiohttp/pull/1177))
* Fix access log formats %O and %b for static file handling
* Remove debug setting of GunicornWorker, use app.debug
  to control its debug-mode instead

---

## 1.0.0 (2016-09-16)[¶](#id1219 "Link to this heading")

* Change default size for client session’s connection pool from
  unlimited to 20 ([#977](https://github.com/aio-libs/aiohttp/pull/977))
* Add IE support for cookie deletion. ([#994](https://github.com/aio-libs/aiohttp/pull/994))
* Remove deprecated WebSocketResponse.wait\_closed method (BACKWARD
  INCOMPATIBLE)
* Remove deprecated force parameter for ClientResponse.close
  method (BACKWARD INCOMPATIBLE)
* Avoid using of mutable CIMultiDict kw param in make\_mocked\_request
  ([#997](https://github.com/aio-libs/aiohttp/pull/997))
* Make WebSocketResponse.close a little bit faster by avoiding new
  task creating just for timeout measurement
* Add proxy and proxy\_auth params to client.get() and family,
  deprecate ProxyConnector ([#998](https://github.com/aio-libs/aiohttp/pull/998))
* Add support for websocket send\_json and receive\_json, synchronize
  server and client API for websockets ([#984](https://github.com/aio-libs/aiohttp/pull/984))
* Implement router shourtcuts for most useful HTTP methods, use
  app.router.add\_get(), app.router.add\_post() etc. instead of
  app.router.add\_route() ([#986](https://github.com/aio-libs/aiohttp/pull/986))
* Support SSL connections for gunicorn worker ([#1003](https://github.com/aio-libs/aiohttp/pull/1003))
* Move obsolete examples to legacy folder
* Switch to multidict 2.0 and title-cased strings ([#1015](https://github.com/aio-libs/aiohttp/pull/1015))
* {FOO}e logger format is case-sensitive now
* Fix logger report for unix socket 8e8469b
* Rename aiohttp.websocket to aiohttp.\_ws\_impl
* Rename `aiohttp.MsgType` to `aiohttp.WSMsgType`
* Introduce `aiohttp.WSMessage` officially
* Rename Message -> WSMessage
* Remove deprecated decode param from resp.read(decode=True)
* Use 5min default client timeout ([#1028](https://github.com/aio-libs/aiohttp/pull/1028))
* Relax HTTP method validation in UrlDispatcher ([#1037](https://github.com/aio-libs/aiohttp/pull/1037))
* Pin minimal supported asyncio version to 3.4.2+ (loop.is\_close()
  should be present)
* Remove aiohttp.websocket module (BACKWARD INCOMPATIBLE)
  Please use high-level client and server approaches
* Link header for 451 status code is mandatory
* Fix test\_client fixture to allow multiple clients per test ([#1072](https://github.com/aio-libs/aiohttp/pull/1072))
* make\_mocked\_request now accepts dict as headers ([#1073](https://github.com/aio-libs/aiohttp/pull/1073))
* Add Python 3.5.2/3.6+ compatibility patch for async generator
  protocol change ([#1082](https://github.com/aio-libs/aiohttp/pull/1082))
* Improvement test\_client can accept instance object ([#1083](https://github.com/aio-libs/aiohttp/pull/1083))
* Simplify ServerHttpProtocol implementation ([#1060](https://github.com/aio-libs/aiohttp/pull/1060))
* Add a flag for optional showing directory index for static file
  handling ([#921](https://github.com/aio-libs/aiohttp/pull/921))
* Define web.Application.on\_startup() signal handler ([#1103](https://github.com/aio-libs/aiohttp/pull/1103))
* Drop ChunkedParser and LinesParser ([#1111](https://github.com/aio-libs/aiohttp/pull/1111))
* Call Application.startup in GunicornWebWorker ([#1105](https://github.com/aio-libs/aiohttp/pull/1105))
* Fix client handling hostnames with 63 bytes when a port is given in
  the url ([#1044](https://github.com/aio-libs/aiohttp/pull/1044))
* Implement proxy support for ClientSession.ws\_connect ([#1025](https://github.com/aio-libs/aiohttp/pull/1025))
* Return named tuple from WebSocketResponse.can\_prepare ([#1016](https://github.com/aio-libs/aiohttp/pull/1016))
* Fix access\_log\_format in GunicornWebWorker ([#1117](https://github.com/aio-libs/aiohttp/pull/1117))
* Setup Content-Type to application/octet-stream by default ([#1124](https://github.com/aio-libs/aiohttp/pull/1124))
* Deprecate debug parameter from app.make\_handler(), use
  Application(debug=True) instead ([#1121](https://github.com/aio-libs/aiohttp/pull/1121))
* Remove fragment string in request path ([#846](https://github.com/aio-libs/aiohttp/pull/846))
* Use aiodns.DNSResolver.gethostbyname() if available ([#1136](https://github.com/aio-libs/aiohttp/pull/1136))
* Fix static file sending on uvloop when sendfile is available ([#1093](https://github.com/aio-libs/aiohttp/pull/1093))
* Make prettier urls if query is empty dict ([#1143](https://github.com/aio-libs/aiohttp/pull/1143))
* Fix redirects for HEAD requests ([#1147](https://github.com/aio-libs/aiohttp/pull/1147))
* Default value for StreamReader.read\_nowait is -1 from now ([#1150](https://github.com/aio-libs/aiohttp/pull/1150))
* aiohttp.StreamReader is not inherited from asyncio.StreamReader from now
  (BACKWARD INCOMPATIBLE) ([#1150](https://github.com/aio-libs/aiohttp/pull/1150))
* Streams documentation added ([#1150](https://github.com/aio-libs/aiohttp/pull/1150))
* Add multipart coroutine method for web Request object ([#1067](https://github.com/aio-libs/aiohttp/pull/1067))
* Publish ClientSession.loop property ([#1149](https://github.com/aio-libs/aiohttp/pull/1149))
* Fix static file with spaces ([#1140](https://github.com/aio-libs/aiohttp/pull/1140))
* Fix piling up asyncio loop by cookie expiration callbacks ([#1061](https://github.com/aio-libs/aiohttp/pull/1061))
* Drop Timeout class for sake of async\_timeout external library.
  aiohttp.Timeout is an alias for async\_timeout.timeout
* use\_dns\_cache parameter of aiohttp.TCPConnector is True by
  default (BACKWARD INCOMPATIBLE) ([#1152](https://github.com/aio-libs/aiohttp/pull/1152))
* aiohttp.TCPConnector uses asynchronous DNS resolver if available by
  default (BACKWARD INCOMPATIBLE) ([#1152](https://github.com/aio-libs/aiohttp/pull/1152))
* Conform to RFC3986 - do not include url fragments in client requests ([#1174](https://github.com/aio-libs/aiohttp/pull/1174))
* Drop ClientSession.cookies (BACKWARD INCOMPATIBLE) ([#1173](https://github.com/aio-libs/aiohttp/pull/1173))
* Refactor AbstractCookieJar public API (BACKWARD INCOMPATIBLE) ([#1173](https://github.com/aio-libs/aiohttp/pull/1173))
* Fix clashing cookies with have the same name but belong to different
  domains (BACKWARD INCOMPATIBLE) ([#1125](https://github.com/aio-libs/aiohttp/pull/1125))
* Support binary Content-Transfer-Encoding ([#1169](https://github.com/aio-libs/aiohttp/pull/1169))

---

## 0.22.5 (08-02-2016)[¶](#id1264 "Link to this heading")

* Pin miltidict version to >=1.2.2

---

## 0.22.3 (07-26-2016)[¶](#id1265 "Link to this heading")

* Do not filter cookies if unsafe flag provided ([#1005](https://github.com/aio-libs/aiohttp/pull/1005))

---

## 0.22.2 (07-23-2016)[¶](#id1267 "Link to this heading")

* Suppress CancelledError when Timeout raises TimeoutError ([#970](https://github.com/aio-libs/aiohttp/pull/970))
* Don’t expose aiohttp.\_\_version\_\_
* Add unsafe parameter to CookieJar ([#968](https://github.com/aio-libs/aiohttp/pull/968))
* Use unsafe cookie jar in test client tools
* Expose aiohttp.CookieJar name

---

## 0.22.1 (07-16-2016)[¶](#id1270 "Link to this heading")

* Large cookie expiration/max-age does not break an event loop from now
  (fixes ([#967](https://github.com/aio-libs/aiohttp/pull/967)))

---

## 0.22.0 (07-15-2016)[¶](#id1272 "Link to this heading")

* Fix bug in serving static directory ([#803](https://github.com/aio-libs/aiohttp/pull/803))
* Fix command line arg parsing ([#797](https://github.com/aio-libs/aiohttp/pull/797))
* Fix a documentation chapter about cookie usage ([#790](https://github.com/aio-libs/aiohttp/pull/790))
* Handle empty body with gzipped encoding ([#758](https://github.com/aio-libs/aiohttp/pull/758))
* Support 451 Unavailable For Legal Reasons http status ([#697](https://github.com/aio-libs/aiohttp/pull/697))
* Fix Cookie share example and few small typos in docs ([#817](https://github.com/aio-libs/aiohttp/pull/817))
* UrlDispatcher.add\_route with partial coroutine handler ([#814](https://github.com/aio-libs/aiohttp/pull/814))
* Optional support for aiodns ([#728](https://github.com/aio-libs/aiohttp/pull/728))
* Add ServiceRestart and TryAgainLater websocket close codes ([#828](https://github.com/aio-libs/aiohttp/pull/828))
* Fix prompt message for web.run\_app ([#832](https://github.com/aio-libs/aiohttp/pull/832))
* Allow to pass None as a timeout value to disable timeout logic ([#834](https://github.com/aio-libs/aiohttp/pull/834))
* Fix leak of connection slot during connection error ([#835](https://github.com/aio-libs/aiohttp/pull/835))
* Gunicorn worker with uvloop support
  aiohttp.worker.GunicornUVLoopWebWorker ([#878](https://github.com/aio-libs/aiohttp/pull/878))
* Don’t send body in response to HEAD request ([#838](https://github.com/aio-libs/aiohttp/pull/838))
* Skip the preamble in MultipartReader ([#881](https://github.com/aio-libs/aiohttp/pull/881))
* Implement BasicAuth decode classmethod. ([#744](https://github.com/aio-libs/aiohttp/pull/744))
* Don’t crash logger when transport is None ([#889](https://github.com/aio-libs/aiohttp/pull/889))
* Use a create\_future compatibility wrapper instead of creating
  Futures directly ([#896](https://github.com/aio-libs/aiohttp/pull/896))
* Add test utilities to aiohttp ([#902](https://github.com/aio-libs/aiohttp/pull/902))
* Improve Request.\_\_repr\_\_ ([#875](https://github.com/aio-libs/aiohttp/pull/875))
* Skip DNS resolving if provided host is already an ip address ([#874](https://github.com/aio-libs/aiohttp/pull/874))
* Add headers to ClientSession.ws\_connect ([#785](https://github.com/aio-libs/aiohttp/pull/785))
* Document that server can send pre-compressed data ([#906](https://github.com/aio-libs/aiohttp/pull/906))
* Don’t add Content-Encoding and Transfer-Encoding if no body ([#891](https://github.com/aio-libs/aiohttp/pull/891))
* Add json() convenience methods to websocket message objects ([#897](https://github.com/aio-libs/aiohttp/pull/897))
* Add client\_resp.raise\_for\_status() ([#908](https://github.com/aio-libs/aiohttp/pull/908))
* Implement cookie filter ([#799](https://github.com/aio-libs/aiohttp/pull/799))
* Include an example of middleware to handle error pages ([#909](https://github.com/aio-libs/aiohttp/pull/909))
* Fix error handling in StaticFileMixin ([#856](https://github.com/aio-libs/aiohttp/pull/856))
* Add mocked request helper ([#900](https://github.com/aio-libs/aiohttp/pull/900))
* Fix empty ALLOW Response header for cls based View ([#929](https://github.com/aio-libs/aiohttp/pull/929))
* Respect CONNECT method to implement a proxy server ([#847](https://github.com/aio-libs/aiohttp/pull/847))
* Add pytest\_plugin ([#914](https://github.com/aio-libs/aiohttp/pull/914))
* Add tutorial
* Add backlog option to support more than 128 (default value in
  “create\_server” function) concurrent connections ([#892](https://github.com/aio-libs/aiohttp/pull/892))
* Allow configuration of header size limits ([#912](https://github.com/aio-libs/aiohttp/pull/912))
* Separate sending file logic from StaticRoute dispatcher ([#901](https://github.com/aio-libs/aiohttp/pull/901))
* Drop deprecated share\_cookies connector option (BACKWARD INCOMPATIBLE)
* Drop deprecated support for tuple as auth parameter.
  Use aiohttp.BasicAuth instead (BACKWARD INCOMPATIBLE)
* Remove deprecated request.payload property, use content instead.
  (BACKWARD INCOMPATIBLE)
* Drop all mentions about api changes in documentation for versions
  older than 0.16
* Allow to override default cookie jar ([#963](https://github.com/aio-libs/aiohttp/pull/963))
* Add manylinux wheel builds
* Dup a socket for sendfile usage ([#964](https://github.com/aio-libs/aiohttp/pull/964))

---

## 0.21.6 (05-05-2016)[¶](#id1311 "Link to this heading")

* Drop initial query parameters on redirects ([#853](https://github.com/aio-libs/aiohttp/pull/853))

---

## 0.21.5 (03-22-2016)[¶](#id1313 "Link to this heading")

* Fix command line arg parsing ([#797](https://github.com/aio-libs/aiohttp/pull/797))

---

## 0.21.4 (03-12-2016)[¶](#id1315 "Link to this heading")

* Fix ResourceAdapter: don’t add method to allowed if resource is not
  match ([#826](https://github.com/aio-libs/aiohttp/pull/826))
* Fix Resource: append found method to returned allowed methods

---

## 0.21.2 (02-16-2016)[¶](#id1317 "Link to this heading")

* Fix a regression: support for handling ~/path in static file routes was
  broken ([#782](https://github.com/aio-libs/aiohttp/pull/782))

---

## 0.21.1 (02-10-2016)[¶](#id1319 "Link to this heading")

* Make new resources classes public ([#767](https://github.com/aio-libs/aiohttp/pull/767))
* Add router.resources() view
* Fix cmd-line parameter names in doc

---

## 0.21.0 (02-04-2016)[¶](#id1321 "Link to this heading")

* Introduce on\_shutdown signal ([#722](https://github.com/aio-libs/aiohttp/pull/722))
* Implement raw input headers ([#726](https://github.com/aio-libs/aiohttp/pull/726))
* Implement web.run\_app utility function ([#734](https://github.com/aio-libs/aiohttp/pull/734))
* Introduce on\_cleanup signal
* Deprecate Application.finish() / Application.register\_on\_finish() in favor of on\_cleanup.
* Get rid of bare aiohttp.request(), aiohttp.get() and family in docs ([#729](https://github.com/aio-libs/aiohttp/pull/729))
* Deprecate bare aiohttp.request(), aiohttp.get() and family ([#729](https://github.com/aio-libs/aiohttp/pull/729))
* Refactor keep-alive support ([#737](https://github.com/aio-libs/aiohttp/pull/737))

  + Enable keepalive for HTTP 1.0 by default
  + Disable it for HTTP 0.9 (who cares about 0.9, BTW?)
  + For keepalived connections

    > - Send Connection: keep-alive for HTTP 1.0 only
    > - don’t send Connection header for HTTP 1.1
  + For non-keepalived connections

    > - Send Connection: close for HTTP 1.1 only
    > - don’t send Connection header for HTTP 1.0
* Add version parameter to ClientSession constructor,
  deprecate it for session.request() and family ([#736](https://github.com/aio-libs/aiohttp/pull/736))
* Enable access log by default ([#735](https://github.com/aio-libs/aiohttp/pull/735))
* Deprecate app.router.register\_route() (the method was not documented intentionally BTW).
* Deprecate app.router.named\_routes() in favor of app.router.named\_resources()
* route.add\_static accepts pathlib.Path now ([#743](https://github.com/aio-libs/aiohttp/pull/743))
* Add command line support: $ python -m aiohttp.web package.main ([#740](https://github.com/aio-libs/aiohttp/pull/740))
* FAQ section was added to docs. Enjoy and fill free to contribute new topics
* Add async context manager support to ClientSession
* Document ClientResponse’s host, method, url properties
* Use CORK/NODELAY in client API ([#748](https://github.com/aio-libs/aiohttp/pull/748))
* ClientSession.close and Connector.close are coroutines now
* Close client connection on exception in ClientResponse.release()
* Allow to read multipart parts without content-length specified ([#750](https://github.com/aio-libs/aiohttp/pull/750))
* Add support for unix domain sockets to gunicorn worker ([#470](https://github.com/aio-libs/aiohttp/pull/470))
* Add test for default Expect handler ([#601](https://github.com/aio-libs/aiohttp/pull/601))
* Add the first demo project
* Rename loader keyword argument in web.Request.json method. ([#646](https://github.com/aio-libs/aiohttp/pull/646))
* Add local socket binding for TCPConnector ([#678](https://github.com/aio-libs/aiohttp/pull/678))

---

## 0.20.2 (01-07-2016)[¶](#id1338 "Link to this heading")

* Enable use of await for a class based view ([#717](https://github.com/aio-libs/aiohttp/pull/717))
* Check address family to fill wsgi env properly ([#718](https://github.com/aio-libs/aiohttp/pull/718))
* Fix memory leak in headers processing (thanks to Marco Paolini) ([#723](https://github.com/aio-libs/aiohttp/pull/723)

—-)

## 0.20.1 (12-30-2015)[¶](#id1342 "Link to this heading")

* Raise RuntimeError is Timeout context manager was used outside of
  task context.
* Add number of bytes to stream.read\_nowait ([#700](https://github.com/aio-libs/aiohttp/pull/700))
* Use X-FORWARDED-PROTO for wsgi.url\_scheme when available

---

## 0.20.0 (12-28-2015)[¶](#id1344 "Link to this heading")

* Extend list of web exceptions, add HTTPMisdirectedRequest,
  HTTPUpgradeRequired, HTTPPreconditionRequired, HTTPTooManyRequests,
  HTTPRequestHeaderFieldsTooLarge, HTTPVariantAlsoNegotiates,
  HTTPNotExtended, HTTPNetworkAuthenticationRequired status codes ([#644](https://github.com/aio-libs/aiohttp/pull/644))
* Do not remove AUTHORIZATION header by WSGI handler ([#649](https://github.com/aio-libs/aiohttp/pull/649))
* Fix broken support for https proxies with authentication ([#617](https://github.com/aio-libs/aiohttp/pull/617))
* Get REMOTE\_\* and SEVER\_\* http vars from headers when listening on
  unix socket ([#654](https://github.com/aio-libs/aiohttp/pull/654))
* Add HTTP 308 support ([#663](https://github.com/aio-libs/aiohttp/pull/663))
* Add Tf format (time to serve request in seconds, %06f format) to
  access log ([#669](https://github.com/aio-libs/aiohttp/pull/669))
* Remove one and a half years long deprecated
  ClientResponse.read\_and\_close() method
* Optimize chunked encoding: use a single syscall instead of 3 calls
  on sending chunked encoded data
* Use TCP\_CORK and TCP\_NODELAY to optimize network latency and
  throughput ([#680](https://github.com/aio-libs/aiohttp/pull/680))
* Websocket XOR performance improved ([#687](https://github.com/aio-libs/aiohttp/pull/687))
* Avoid sending cookie attributes in Cookie header ([#613](https://github.com/aio-libs/aiohttp/pull/613))
* Round server timeouts to seconds for grouping pending calls. That
  leads to less amount of poller syscalls e.g. epoll.poll(). ([#702](https://github.com/aio-libs/aiohttp/pull/702))
* Close connection on websocket handshake error ([#703](https://github.com/aio-libs/aiohttp/pull/703))
* Implement class based views ([#684](https://github.com/aio-libs/aiohttp/pull/684))
* Add *headers* parameter to ws\_connect() ([#709](https://github.com/aio-libs/aiohttp/pull/709))
* Drop unused function parse\_remote\_addr() ([#708](https://github.com/aio-libs/aiohttp/pull/708))
* Close session on exception ([#707](https://github.com/aio-libs/aiohttp/pull/707))
* Store http code and headers in WSServerHandshakeError ([#706](https://github.com/aio-libs/aiohttp/pull/706))
* Make some low-level message properties readonly ([#710](https://github.com/aio-libs/aiohttp/pull/710))

---

## 0.19.0 (11-25-2015)[¶](#id1362 "Link to this heading")

* Memory leak in ParserBuffer ([#579](https://github.com/aio-libs/aiohttp/pull/579))
* Support gunicorn’s max\_requests settings in gunicorn worker
* Fix wsgi environment building ([#573](https://github.com/aio-libs/aiohttp/pull/573))
* Improve access logging ([#572](https://github.com/aio-libs/aiohttp/pull/572))
* Drop unused host and port from low-level server ([#586](https://github.com/aio-libs/aiohttp/pull/586))
* Add Python 3.5 async for implementation to server websocket ([#543](https://github.com/aio-libs/aiohttp/pull/543))
* Add Python 3.5 async for implementation to client websocket
* Add Python 3.5 async with implementation to client websocket
* Add charset parameter to web.Response constructor ([#593](https://github.com/aio-libs/aiohttp/pull/593))
* Forbid passing both Content-Type header and content\_type or charset
  params into web.Response constructor
* Forbid duplicating of web.Application and web.Request ([#602](https://github.com/aio-libs/aiohttp/pull/602))
* Add an option to pass Origin header in ws\_connect ([#607](https://github.com/aio-libs/aiohttp/pull/607))
* Add json\_response function ([#592](https://github.com/aio-libs/aiohttp/pull/592))
* Make concurrent connections respect limits ([#581](https://github.com/aio-libs/aiohttp/pull/581))
* Collect history of responses if redirects occur ([#614](https://github.com/aio-libs/aiohttp/pull/614))
* Enable passing pre-compressed data in requests ([#621](https://github.com/aio-libs/aiohttp/pull/621))
* Expose named routes via UrlDispatcher.named\_routes() ([#622](https://github.com/aio-libs/aiohttp/pull/622))
* Allow disabling sendfile by environment variable AIOHTTP\_NOSENDFILE ([#629](https://github.com/aio-libs/aiohttp/pull/629))
* Use ensure\_future if available
* Always quote params for Content-Disposition ([#641](https://github.com/aio-libs/aiohttp/pull/641))
* Support async for in multipart reader ([#640](https://github.com/aio-libs/aiohttp/pull/640))
* Add Timeout context manager ([#611](https://github.com/aio-libs/aiohttp/pull/611))

---

## 0.18.4 (13-11-2015)[¶](#id1380 "Link to this heading")

* Relax rule for router names again by adding dash to allowed
  characters: they may contain identifiers, dashes, dots and columns

---

## 0.18.3 (25-10-2015)[¶](#id1381 "Link to this heading")

* Fix formatting for \_RequestContextManager helper ([#590](https://github.com/aio-libs/aiohttp/pull/590))

---

## 0.18.2 (22-10-2015)[¶](#id1383 "Link to this heading")

* Fix regression for OpenSSL < 1.0.0 ([#583](https://github.com/aio-libs/aiohttp/pull/583))

---

## 0.18.1 (20-10-2015)[¶](#id1385 "Link to this heading")

* Relax rule for router names: they may contain dots and columns
  starting from now

---

## 0.18.0 (19-10-2015)[¶](#id1386 "Link to this heading")

* Use errors.HttpProcessingError.message as HTTP error reason and
  message ([#459](https://github.com/aio-libs/aiohttp/pull/459))
* Optimize cythonized multidict a bit
* Change repr’s of multidicts and multidict views
* default headers in ClientSession are now case-insensitive
* Make ‘=’ char and ‘wss://’ schema safe in urls ([#477](https://github.com/aio-libs/aiohttp/pull/477))
* ClientResponse.close() forces connection closing by default from now ([#479](https://github.com/aio-libs/aiohttp/pull/479))

  N.B. Backward incompatible change: was .close(force=False) Using
  `force parameter for the method is deprecated: use .release()
  instead.
* Properly requote URL’s path ([#480](https://github.com/aio-libs/aiohttp/pull/480))
* add skip\_auto\_headers parameter for client API ([#486](https://github.com/aio-libs/aiohttp/pull/486))
* Properly parse URL path in aiohttp.web.Request ([#489](https://github.com/aio-libs/aiohttp/pull/489))
* Raise RuntimeError when chunked enabled and HTTP is 1.0 ([#488](https://github.com/aio-libs/aiohttp/pull/488))
* Fix a bug with processing io.BytesIO as data parameter for client API ([#500](https://github.com/aio-libs/aiohttp/pull/500))
* Skip auto-generation of Content-Type header ([#507](https://github.com/aio-libs/aiohttp/pull/507))
* Use sendfile facility for static file handling ([#503](https://github.com/aio-libs/aiohttp/pull/503))
* Default response\_factory in app.router.add\_static now is
  StreamResponse, not None. The functionality is not changed if
  default is not specified.
* Drop ClientResponse.message attribute, it was always implementation detail.
* Streams are optimized for speed and mostly memory in case of a big
  HTTP message sizes ([#496](https://github.com/aio-libs/aiohttp/pull/496))
* Fix a bug for server-side cookies for dropping cookie and setting it
  again without Max-Age parameter.
* Don’t trim redirect URL in client API ([#499](https://github.com/aio-libs/aiohttp/pull/499))
* Extend precision of access log “D” to milliseconds ([#527](https://github.com/aio-libs/aiohttp/pull/527))
* Deprecate StreamResponse.start() method in favor of
  StreamResponse.prepare() coroutine ([#525](https://github.com/aio-libs/aiohttp/pull/525))

  .start() is still supported but responses begun with .start()
  does not call signal for response preparing to be sent.
* Add StreamReader.\_\_repr\_\_
* Drop Python 3.3 support, from now minimal required version is Python
  3.4.1 ([#541](https://github.com/aio-libs/aiohttp/pull/541))
* Add async with support for ClientSession.request() and family ([#536](https://github.com/aio-libs/aiohttp/pull/536))
* Ignore message body on 204 and 304 responses ([#505](https://github.com/aio-libs/aiohttp/pull/505))
* TCPConnector processed both IPv4 and IPv6 by default ([#559](https://github.com/aio-libs/aiohttp/pull/559))
* Add .routes() view for urldispatcher ([#519](https://github.com/aio-libs/aiohttp/pull/519))
* Route name should be a valid identifier name from now ([#567](https://github.com/aio-libs/aiohttp/pull/567))
* Implement server signals ([#562](https://github.com/aio-libs/aiohttp/pull/562))
* Drop a year-old deprecated *files* parameter from client API.
* Added async for support for aiohttp stream ([#542](https://github.com/aio-libs/aiohttp/pull/542))

---

## 0.17.4 (09-29-2015)[¶](#id1409 "Link to this heading")

* Properly parse URL path in aiohttp.web.Request ([#489](https://github.com/aio-libs/aiohttp/pull/489))
* Add missing coroutine decorator, the client api is await-compatible now

---

## 0.17.3 (08-28-2015)[¶](#id1411 "Link to this heading")

* Remove Content-Length header on compressed responses ([#450](https://github.com/aio-libs/aiohttp/pull/450))
* Support Python 3.5
* Improve performance of transport in-use list ([#472](https://github.com/aio-libs/aiohttp/pull/472))
* Fix connection pooling ([#473](https://github.com/aio-libs/aiohttp/pull/473))

---

## 0.17.2 (08-11-2015)[¶](#id1415 "Link to this heading")

* Don’t forget to pass data argument forward ([#462](https://github.com/aio-libs/aiohttp/pull/462))
* Fix multipart read bytes count ([#463](https://github.com/aio-libs/aiohttp/pull/463))

---

## 0.17.1 (08-10-2015)[¶](#id1418 "Link to this heading")

* Fix multidict comparison to arbitrary abc.Mapping

---

## 0.17.0 (08-04-2015)[¶](#id1419 "Link to this heading")

* Make StaticRoute support Last-Modified and If-Modified-Since headers ([#386](https://github.com/aio-libs/aiohttp/pull/386))
* Add Request.if\_modified\_since and Stream.Response.last\_modified properties
* Fix deflate compression when writing a chunked response ([#395](https://github.com/aio-libs/aiohttp/pull/395))
* Request`s content-length header is cleared now after redirect from
  POST method ([#391](https://github.com/aio-libs/aiohttp/pull/391))
* Return a 400 if server received a non HTTP content ([#405](https://github.com/aio-libs/aiohttp/pull/405))
* Fix keep-alive support for aiohttp clients ([#406](https://github.com/aio-libs/aiohttp/pull/406))
* Allow gzip compression in high-level server response interface ([#403](https://github.com/aio-libs/aiohttp/pull/403))
* Rename TCPConnector.resolve and family to dns\_cache ([#415](https://github.com/aio-libs/aiohttp/pull/415))
* Make UrlDispatcher ignore quoted characters during url matching ([#414](https://github.com/aio-libs/aiohttp/pull/414))
  Backward-compatibility warning: this may change the url matched by
  your queries if they send quoted character (like %2F for /) ([#414](https://github.com/aio-libs/aiohttp/pull/414))
* Use optional cchardet accelerator if present ([#418](https://github.com/aio-libs/aiohttp/pull/418))
* Borrow loop from Connector in ClientSession if loop is not set
* Add context manager support to ClientSession for session closing.
* Add toplevel get(), post(), put(), head(), delete(), options(),
  patch() coroutines.
* Fix IPv6 support for client API ([#425](https://github.com/aio-libs/aiohttp/pull/425))
* Pass SSL context through proxy connector ([#421](https://github.com/aio-libs/aiohttp/pull/421))
* Make the rule: path for add\_route should start with slash
* Don’t process request finishing by low-level server on closed event loop
* Don’t override data if multiple files are uploaded with same key ([#433](https://github.com/aio-libs/aiohttp/pull/433))
* Ensure multipart.BodyPartReader.read\_chunk read all the necessary data
  to avoid false assertions about malformed multipart payload
* Don’t send body for 204, 205 and 304 http exceptions ([#442](https://github.com/aio-libs/aiohttp/pull/442))
* Correctly skip Cython compilation in MSVC not found ([#453](https://github.com/aio-libs/aiohttp/pull/453))
* Add response factory to StaticRoute ([#456](https://github.com/aio-libs/aiohttp/pull/456))
* Don’t append trailing CRLF for multipart.BodyPartReader ([#454](https://github.com/aio-libs/aiohttp/pull/454))

---

## 0.16.6 (07-15-2015)[¶](#id1437 "Link to this heading")

* Skip compilation on Windows if vcvarsall.bat cannot be found ([#438](https://github.com/aio-libs/aiohttp/pull/438))

---

## 0.16.5 (06-13-2015)[¶](#id1439 "Link to this heading")

* Get rid of all comprehensions and yielding in \_multidict ([#410](https://github.com/aio-libs/aiohttp/pull/410))

---

## 0.16.4 (06-13-2015)[¶](#id1441 "Link to this heading")

* Don’t clear current exception in multidict’s \_\_repr\_\_ (cythonized
  versions) ([#410](https://github.com/aio-libs/aiohttp/pull/410))

---

## 0.16.3 (05-30-2015)[¶](#id1443 "Link to this heading")

* Fix StaticRoute vulnerability to directory traversal attacks ([#380](https://github.com/aio-libs/aiohttp/pull/380))

---

## 0.16.2 (05-27-2015)[¶](#id1445 "Link to this heading")

* Update python version required for \_\_del\_\_ usage: it’s actually
  3.4.1 instead of 3.4.0
* Add check for presence of loop.is\_closed() method before call the
  former ([#378](https://github.com/aio-libs/aiohttp/pull/378))

---

## 0.16.1 (05-27-2015)[¶](#id1447 "Link to this heading")

* Fix regression in static file handling ([#377](https://github.com/aio-libs/aiohttp/pull/377))

---

## 0.16.0 (05-26-2015)[¶](#id1449 "Link to this heading")

* Unset waiter future after cancellation ([#363](https://github.com/aio-libs/aiohttp/pull/363))
* Update request url with query parameters ([#372](https://github.com/aio-libs/aiohttp/pull/372))
* Support new fingerprint param of TCPConnector to enable verifying
  SSL certificates via MD5, SHA1, or SHA256 digest ([#366](https://github.com/aio-libs/aiohttp/pull/366))
* Setup uploaded filename if field value is binary and transfer
  encoding is not specified ([#349](https://github.com/aio-libs/aiohttp/pull/349))
* Implement ClientSession.close() method
* Implement connector.closed readonly property
* Implement ClientSession.closed readonly property
* Implement ClientSession.connector readonly property
* Implement ClientSession.detach method
* Add \_\_del\_\_ to client-side objects: sessions, connectors,
  connections, requests, responses.
* Refactor connections cleanup by connector ([#357](https://github.com/aio-libs/aiohttp/pull/357))
* Add limit parameter to connector constructor ([#358](https://github.com/aio-libs/aiohttp/pull/358))
* Add request.has\_body property ([#364](https://github.com/aio-libs/aiohttp/pull/364))
* Add response\_class parameter to ws\_connect() ([#367](https://github.com/aio-libs/aiohttp/pull/367))
* ProxyConnector does not support keep-alive requests by default
  starting from now ([#368](https://github.com/aio-libs/aiohttp/pull/368))
* Add connector.force\_close property
* Add ws\_connect to ClientSession ([#374](https://github.com/aio-libs/aiohttp/pull/374))
* Support optional chunk\_size parameter in router.add\_static()

---

## 0.15.3 (04-22-2015)[¶](#id1460 "Link to this heading")

* Fix graceful shutdown handling
* Fix Expect header handling for not found and not allowed routes ([#340](https://github.com/aio-libs/aiohttp/pull/340))

---

## 0.15.2 (04-19-2015)[¶](#id1462 "Link to this heading")

* Flow control subsystem refactoring
* HTTP server performance optimizations
* Allow to match any request method with \*
* Explicitly call drain on transport ([#316](https://github.com/aio-libs/aiohttp/pull/316))
* Make chardet module dependency mandatory ([#318](https://github.com/aio-libs/aiohttp/pull/318))
* Support keep-alive for HTTP 1.0 ([#325](https://github.com/aio-libs/aiohttp/pull/325))
* Do not chunk single file during upload ([#327](https://github.com/aio-libs/aiohttp/pull/327))
* Add ClientSession object for cookie storage and default headers ([#328](https://github.com/aio-libs/aiohttp/pull/328))
* Add keep\_alive\_on argument for HTTP server handler.

---

## 0.15.1 (03-31-2015)[¶](#id1468 "Link to this heading")

* Pass Autobahn Testsuite tests
* Fixed websocket fragmentation
* Fixed websocket close procedure
* Fixed parser buffer limits
* Added timeout parameter to WebSocketResponse ctor
* Added WebSocketResponse.close\_code attribute

---

## 0.15.0 (03-27-2015)[¶](#id1469 "Link to this heading")

* Client WebSockets support
* New Multipart system ([#273](https://github.com/aio-libs/aiohttp/pull/273))
* Support for “Except” header ([#287](https://github.com/aio-libs/aiohttp/pull/287)) ([#267](https://github.com/aio-libs/aiohttp/pull/267))
* Set default Content-Type for post requests ([#184](https://github.com/aio-libs/aiohttp/pull/184))
* Fix issue with construction dynamic route with regexps and trailing slash ([#266](https://github.com/aio-libs/aiohttp/pull/266))
* Add repr to web.Request
* Add repr to web.Response
* Add repr for NotFound and NotAllowed match infos
* Add repr for web.Application
* Add repr to UrlMappingMatchInfo ([#217](https://github.com/aio-libs/aiohttp/pull/217))
* Gunicorn 19.2.x compatibility

---

## 0.14.4 (01-29-2015)[¶](#id1476 "Link to this heading")

* Fix issue with error during constructing of url with regex parts ([#264](https://github.com/aio-libs/aiohttp/pull/264))

---

## 0.14.3 (01-28-2015)[¶](#id1478 "Link to this heading")

* Use path=’/’ by default for cookies ([#261](https://github.com/aio-libs/aiohttp/pull/261))

---

## 0.14.2 (01-23-2015)[¶](#id1480 "Link to this heading")

* Connections leak in BaseConnector ([#253](https://github.com/aio-libs/aiohttp/pull/253))
* Do not swallow websocket reader exceptions ([#255](https://github.com/aio-libs/aiohttp/pull/255))
* web.Request’s read, text, json are memorized ([#250](https://github.com/aio-libs/aiohttp/pull/250))

---

## 0.14.1 (01-15-2015)[¶](#id1484 "Link to this heading")

* HttpMessage.\_add\_default\_headers does not overwrite existing headers ([#216](https://github.com/aio-libs/aiohttp/pull/216))
* Expose multidict classes at package level
* add aiohttp.web.WebSocketResponse
* According to RFC 6455 websocket subprotocol preference order is
  provided by client, not by server
* websocket’s ping and pong accept optional message parameter
* multidict views do not accept getall parameter anymore, it
  returns the full body anyway.
* multidicts have optional Cython optimization, cythonized version of
  multidicts is about 5 times faster than pure Python.
* multidict.getall() returns list, not tuple.
* Backward incompatible change: now there are two mutable multidicts
  (MultiDict, CIMultiDict) and two immutable multidict proxies
  (MultiDictProxy and CIMultiDictProxy). Previous edition of
  multidicts was not a part of public API BTW.
* Router refactoring to push Not Allowed and Not Found in middleware processing
* Convert ConnectionError to aiohttp.DisconnectedError and don’t
  eat ConnectionError exceptions from web handlers.
* Remove hop headers from Response class, wsgi response still uses hop headers.
* Allow to send raw chunked encoded response.
* Allow to encode output bytes stream into chunked encoding.
* Allow to compress output bytes stream with deflate encoding.
* Server has 75 seconds keepalive timeout now, was non-keepalive by default.
* Application does not accept \*\*kwargs anymore (([#243](https://github.com/aio-libs/aiohttp/pull/243))).
* Request is inherited from dict now for making per-request storage to
  middlewares (([#242](https://github.com/aio-libs/aiohttp/pull/242))).

---

## 0.13.1 (12-31-2014)[¶](#id1488 "Link to this heading")

* Add aiohttp.web.StreamResponse.started property ([#213](https://github.com/aio-libs/aiohttp/pull/213))
* HTML escape traceback text in ServerHttpProtocol.handle\_error
* Mention handler and middlewares in aiohttp.web.RequestHandler.handle\_request
  on error (([#218](https://github.com/aio-libs/aiohttp/pull/218)))

---

## 0.13.0 (12-29-2014)[¶](#id1491 "Link to this heading")

* StreamResponse.charset converts value to lower-case on assigning.
* Chain exceptions when raise ClientRequestError.
* Support custom regexps in route variables ([#204](https://github.com/aio-libs/aiohttp/pull/204))
* Fixed graceful shutdown, disable keep-alive on connection closing.
* Decode HTTP message with utf-8 encoding, some servers send headers
  in utf-8 encoding ([#207](https://github.com/aio-libs/aiohttp/pull/207))
* Support aiohtt.web middlewares ([#209](https://github.com/aio-libs/aiohttp/pull/209))
* Add ssl\_context to TCPConnector ([#206](https://github.com/aio-libs/aiohttp/pull/206))

---

## 0.12.0 (12-12-2014)[¶](#id1496 "Link to this heading")

* Deep refactoring of aiohttp.web in backward-incompatible manner.
  Sorry, we have to do this.
* Automatically force aiohttp.web handlers to coroutines in
  UrlDispatcher.add\_route() ([#186](https://github.com/aio-libs/aiohttp/pull/186))
* Rename Request.POST() function to Request.post()
* Added POST attribute
* Response processing refactoring: constructor does not accept Request
  instance anymore.
* Pass application instance to finish callback
* Exceptions refactoring
* Do not unquote query string in aiohttp.web.Request
* Fix concurrent access to payload in RequestHandle.handle\_request()
* Add access logging to aiohttp.web
* Gunicorn worker for aiohttp.web
* Removed deprecated AsyncGunicornWorker
* Removed deprecated HttpClient

---

## 0.11.0 (11-29-2014)[¶](#id1498 "Link to this heading")

* Support named routes in aiohttp.web.UrlDispatcher ([#179](https://github.com/aio-libs/aiohttp/pull/179))
* Make websocket subprotocols conform to spec ([#181](https://github.com/aio-libs/aiohttp/pull/181))

---

## 0.10.2 (11-19-2014)[¶](#id1501 "Link to this heading")

* Don’t unquote environ[‘PATH\_INFO’] in wsgi.py ([#177](https://github.com/aio-libs/aiohttp/pull/177))

---

## 0.10.1 (11-17-2014)[¶](#id1503 "Link to this heading")

* aiohttp.web.HTTPException and descendants now files response body
  with string like 404: NotFound
* Fix multidict \_\_iter\_\_, the method should iterate over keys, not
  (key, value) pairs.

---

## 0.10.0 (11-13-2014)[¶](#id1504 "Link to this heading")

* Add aiohttp.web subpackage for highlevel HTTP server support.
* Add *reason* optional parameter to aiohttp.protocol.Response ctor.
* Fix aiohttp.client bug for sending file without content-type.
* Change error text for connection closed between server responses
  from ‘Can not read status line’ to explicit ‘Connection closed by
  server’
* Drop closed connections from connector ([#173](https://github.com/aio-libs/aiohttp/pull/173))
* Set server.transport to None on .closing() ([#172](https://github.com/aio-libs/aiohttp/pull/172))

---

## 0.9.3 (10-30-2014)[¶](#id1507 "Link to this heading")

* Fix compatibility with asyncio 3.4.1+ ([#170](https://github.com/aio-libs/aiohttp/pull/170))

---

## 0.9.2 (10-16-2014)[¶](#id1509 "Link to this heading")

* Improve redirect handling ([#157](https://github.com/aio-libs/aiohttp/pull/157))
* Send raw files as is ([#153](https://github.com/aio-libs/aiohttp/pull/153))
* Better websocket support ([#150](https://github.com/aio-libs/aiohttp/pull/150))

---

## 0.9.1 (08-30-2014)[¶](#id1513 "Link to this heading")

* Added MultiDict support for client request params and data ([#114](https://github.com/aio-libs/aiohttp/pull/114)).
* Fixed parameter type for IncompleteRead exception ([#118](https://github.com/aio-libs/aiohttp/pull/118)).
* Strictly require ASCII headers names and values ([#137](https://github.com/aio-libs/aiohttp/pull/137))
* Keep port in ProxyConnector ([#128](https://github.com/aio-libs/aiohttp/pull/128)).
* Python 3.4.1 compatibility ([#131](https://github.com/aio-libs/aiohttp/pull/131)).

---

## 0.9.0 (07-08-2014)[¶](#id1519 "Link to this heading")

* Better client basic authentication support ([#112](https://github.com/aio-libs/aiohttp/pull/112)).
* Fixed incorrect line splitting in HttpRequestParser ([#97](https://github.com/aio-libs/aiohttp/pull/97)).
* Support StreamReader and DataQueue as request data.
* Client files handling refactoring ([#20](https://github.com/aio-libs/aiohttp/pull/20)).
* Backward incompatible: Replace DataQueue with StreamReader for
  request payload ([#87](https://github.com/aio-libs/aiohttp/pull/87)).

---

## 0.8.4 (07-04-2014)[¶](#id1524 "Link to this heading")

* Change ProxyConnector authorization parameters.

---

## 0.8.3 (07-03-2014)[¶](#id1525 "Link to this heading")

* Publish TCPConnector properties: verify\_ssl, family, resolve, resolved\_hosts.
* Don’t parse message body for HEAD responses.
* Refactor client response decoding.

---

## 0.8.2 (06-22-2014)[¶](#id1526 "Link to this heading")

* Make ProxyConnector.proxy immutable property.
* Make UnixConnector.path immutable property.
* Fix resource leak for aiohttp.request() with implicit connector.
* Rename Connector’s reuse\_timeout to keepalive\_timeout.

---

## 0.8.1 (06-18-2014)[¶](#id1527 "Link to this heading")

* Use case insensitive multidict for server request/response headers.
* MultiDict.getall() accepts default value.
* Catch server ConnectionError.
* Accept MultiDict (and derived) instances in aiohttp.request header argument.
* Proxy ‘CONNECT’ support.

---

## 0.8.0 (06-06-2014)[¶](#id1528 "Link to this heading")

* Add support for utf-8 values in HTTP headers
* Allow to use custom response class instead of HttpResponse
* Use MultiDict for client request headers
* Use MultiDict for server request/response headers
* Store response headers in ClientResponse.headers attribute
* Get rid of timeout parameter in aiohttp.client API
* Exceptions refactoring

---

## 0.7.3 (05-20-2014)[¶](#id1529 "Link to this heading")

* Simple HTTP proxy support.

---

## 0.7.2 (05-14-2014)[¶](#id1530 "Link to this heading")

* Get rid of \_\_del\_\_ methods
* Use ResourceWarning instead of logging warning record.

---

## 0.7.1 (04-28-2014)[¶](#id1531 "Link to this heading")

* Do not unquote client request urls.
* Allow multiple waiters on transport drain.
* Do not return client connection to pool in case of exceptions.
* Rename SocketConnector to TCPConnector and UnixSocketConnector to
  UnixConnector.

---

## 0.7.0 (04-16-2014)[¶](#id1532 "Link to this heading")

* Connection flow control.
* HTTP client session/connection pool refactoring.
* Better handling for bad server requests.

---

## 0.6.5 (03-29-2014)[¶](#id1533 "Link to this heading")

* Added client session reuse timeout.
* Better client request cancellation support.
* Better handling responses without content length.
* Added HttpClient verify\_ssl parameter support.

---

## 0.6.4 (02-27-2014)[¶](#id1534 "Link to this heading")

* Log content-length missing warning only for put and post requests.

---

## 0.6.3 (02-27-2014)[¶](#id1535 "Link to this heading")

* Better support for server exit.
* Read response body until EOF if content-length is not defined ([#14](https://github.com/aio-libs/aiohttp/pull/14))

---

## 0.6.2 (02-18-2014)[¶](#id1537 "Link to this heading")

* Fix trailing char in allowed\_methods.
* Start slow request timer for first request.

---

## 0.6.1 (02-17-2014)[¶](#id1538 "Link to this heading")

* Added utility method HttpResponse.read\_and\_close()
* Added slow request timeout.
* Enable socket SO\_KEEPALIVE if available.

---

## 0.6.0 (02-12-2014)[¶](#id1539 "Link to this heading")

* Better handling for process exit.

---

## 0.5.0 (01-29-2014)[¶](#id1540 "Link to this heading")

* Allow to use custom HttpRequest client class.
* Use gunicorn keepalive setting for asynchronous worker.
* Log leaking responses.
* python 3.4 compatibility

---

## 0.4.4 (11-15-2013)[¶](#id1541 "Link to this heading")

* Resolve only AF\_INET family, because it is not clear how to pass
  extra info to asyncio.

---

## 0.4.3 (11-15-2013)[¶](#id1542 "Link to this heading")

* Allow to wait completion of request with HttpResponse.wait\_for\_close()

---

## 0.4.2 (11-14-2013)[¶](#id1543 "Link to this heading")

* Handle exception in client request stream.
* Prevent host resolving for each client request.

---

## 0.4.1 (11-12-2013)[¶](#id1544 "Link to this heading")

* Added client support for expect: 100-continue header.

---

## 0.4 (11-06-2013)[¶](#id1545 "Link to this heading")

* Added custom wsgi application close procedure
* Fixed concurrent host failure in HttpClient

---

## 0.3 (11-04-2013)[¶](#id1546 "Link to this heading")

* Added PortMapperWorker
* Added HttpClient
* Added TCP connection timeout to HTTP client
* Better client connection errors handling
* Gracefully handle process exit

---

## 0.2[¶](#id1547 "Link to this heading")

* Fix packaging

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
  + [Essays](essays.html)
  + [Glossary](glossary.html)
  + [Changelog](#)
  + [Indices and tables](misc.html#indices-and-tables)
* [Who uses aiohttp?](external.html)
* [Contributing](contributing.html)

### Quick search

©aiohttp contributors.
|
Powered by [Sphinx 9.0.4](http://sphinx-doc.org/)
|
[Page source](_sources/changes.rst.txt)

[![Fork me on GitHub](https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png)](https://github.com/aio-libs/aiohttp)
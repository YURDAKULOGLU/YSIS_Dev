aiosqlite: Sqlite for AsyncIO — aiosqlite documentation

# [aiosqlite](#)

Sqlite for Python AsyncIO

[Star](https://github.com/omnilib/aiosqlite)

### Navigation

* [API Reference](api.html)
  + [Connection](api.html#connection)
  + [Cursors](api.html#cursors)
  + [Errors](api.html#errors)
  + [Advanced](api.html#advanced)

* [Changelog](changelog.html)
* [Contributing](contributing.html)

---

* [Report Issues](https://github.com/omnilib/aiosqlite/issues)

### Related Topics

* [Documentation overview](#)
  + Next: [API Reference](api.html "next chapter")

### Quick search

#### The Omnilib Project

[Omnilib](https://omnilib.dev) is a group of MIT licensed software libraries developed under a
common, inclusive [Code of Conduct](https://omnilib.dev/code_of_conduct.html).
We are committed to providing a welcoming and open space for all contributors who adhere to these rules.

# aiosqlite: Sqlite for AsyncIO[¶](#aiosqlite-sqlite-for-asyncio "Link to this heading")

[![Documentation Status](https://readthedocs.org/projects/aiosqlite/badge/?version=latest)](https://aiosqlite.omnilib.dev/en/latest/?badge=latest)
[![PyPI Release](https://img.shields.io/pypi/v/aiosqlite.svg)](https://pypi.org/project/aiosqlite)
[![Changelog](https://img.shields.io/badge/change-log-blue)](https://github.com/omnilib/aiosqlite/blob/master/CHANGELOG.md)
[![MIT Licensed](https://img.shields.io/pypi/l/aiosqlite.svg)](https://github.com/omnilib/aiosqlite/blob/master/LICENSE)

aiosqlite provides a friendly, async interface to sqlite databases.

It replicates the standard `sqlite3` module, but with async versions
of all the standard connection and cursor methods, plus context managers for
automatically closing connections and cursors:

```
async with aiosqlite.connect(...) as db:
    await db.execute("INSERT INTO some_table ...")
    await db.commit()

    async with db.execute("SELECT * FROM some_table") as cursor:
        async for row in cursor:
            ...
```

It can also be used in the traditional, procedural manner:

```
db = await aiosqlite.connect(...)
cursor = await db.execute('SELECT * FROM some_table')
row = await cursor.fetchone()
rows = await cursor.fetchall()
await cursor.close()
await db.close()
```

aiosqlite also replicates most of the advanced features of `sqlite3`:

```
async with aiosqlite.connect(...) as db:
    db.row_factory = aiosqlite.Row
    async with db.execute('SELECT * FROM some_table') as cursor:
        async for row in cursor:
            value = row['column']

    await db.execute('INSERT INTO foo some_table')
    assert db.total_changes > 0
```

## Install[¶](#install "Link to this heading")

aiosqlite is compatible with Python 3.8 and newer.
You can install it from PyPI:

```
$ pip install aiosqlite
```

## Details[¶](#details "Link to this heading")

aiosqlite allows interaction with SQLite databases on the main AsyncIO event
loop without blocking execution of other coroutines while waiting for queries
or data fetches. It does this by using a single, shared thread per connection.
This thread executes all actions within a shared request queue to prevent
overlapping actions.

Connection objects are proxies to the real connections, contain the shared
execution thread, and provide context managers to handle automatically closing
connections. Cursors are similarly proxies to the real cursors, and provide
async iterators to query results.

## License[¶](#license "Link to this heading")

aiosqlite is copyright [Amethyst Reese](https://noswap.com), and licensed under the
MIT license. I am providing code in this repository to you under an open source
license. This is my personal repository; the license you receive to my code
is from me and not from my employer. See the [LICENSE](https://github.com/omnilib/aiosqlite/blob/master/LICENSE) file for details.

©2025, Amethyst Reese.
|
[Page source](_sources/index.rst.txt)
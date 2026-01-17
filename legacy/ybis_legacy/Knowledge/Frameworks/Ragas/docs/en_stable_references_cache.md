Cache - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#ragas.cache)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Cache

## CacheInterface

Bases: `ABC`

Abstract base class defining the interface for cache implementations.

This class provides a standard interface that all cache implementations must follow.
It supports basic cache operations like get, set and key checking.

### get `abstractmethod`

```
get(key: str) -> Any
```

Retrieve a value from the cache by key.

Args:
key: The key to look up in the cache.

Returns:
The cached value associated with the key.

Source code in `src/ragas/cache.py`

|  |  |
| --- | --- |
| ``` 22 23 24 25 26 27 28 29 30 31 32 ``` | ``` @abstractmethod def get(self, key: str) -> Any:     """Retrieve a value from the cache by key.      Args:         key: The key to look up in the cache.      Returns:         The cached value associated with the key.     """     pass ``` |

### set `abstractmethod`

```
set(key: str, value) -> None
```

Store a value in the cache with the given key.

Args:
key: The key to store the value under.
value: The value to cache.

Source code in `src/ragas/cache.py`

|  |  |
| --- | --- |
| ``` 34 35 36 37 38 39 40 41 42 ``` | ``` @abstractmethod def set(self, key: str, value) -> None:     """Store a value in the cache with the given key.      Args:         key: The key to store the value under.         value: The value to cache.     """     pass ``` |

### has\_key `abstractmethod`

```
has_key(key: str) -> bool
```

Check if a key exists in the cache.

Args:
key: The key to check for.

Returns:
True if the key exists in the cache, False otherwise.

Source code in `src/ragas/cache.py`

|  |  |
| --- | --- |
| ``` 44 45 46 47 48 49 50 51 52 53 54 ``` | ``` @abstractmethod def has_key(self, key: str) -> bool:     """Check if a key exists in the cache.      Args:         key: The key to check for.      Returns:         True if the key exists in the cache, False otherwise.     """     pass ``` |

## DiskCacheBackend

```
DiskCacheBackend(cache_dir: str = '.cache')
```

Bases: `CacheInterface`

A cache implementation that stores data on disk using the diskcache library.

This cache backend persists data to disk, allowing it to survive between program runs.
It implements the CacheInterface for use with Ragas caching functionality.

Args:
cache\_dir (str, optional): Directory where cache files will be stored. Defaults to ".cache".

Source code in `src/ragas/cache.py`

|  |  |
| --- | --- |
| ``` 79 80 81 82 83 84 85 86 87 ``` | ``` def __init__(self, cache_dir: str = ".cache"):     try:         from diskcache import Cache     except ImportError:         raise ImportError(             "For using the diskcache backend, please install it with `pip install diskcache`."         )      self.cache = Cache(cache_dir) ``` |

### get

```
get(key: str) -> Any
```

Retrieve a value from the disk cache by key.

Args:
key: The key to look up in the cache.

Returns:
The cached value associated with the key, or None if not found.

Source code in `src/ragas/cache.py`

|  |  |
| --- | --- |
| ``` 89 90 91 92 93 94 95 96 97 98 ``` | ``` def get(self, key: str) -> Any:     """Retrieve a value from the disk cache by key.      Args:         key: The key to look up in the cache.      Returns:         The cached value associated with the key, or None if not found.     """     return self.cache.get(key) ``` |

### set

```
set(key: str, value) -> None
```

Store a value in the disk cache with the given key.

Args:
key: The key to store the value under.
value: The value to cache.

Source code in `src/ragas/cache.py`

|  |  |
| --- | --- |
| ``` 100 101 102 103 104 105 106 107 ``` | ``` def set(self, key: str, value) -> None:     """Store a value in the disk cache with the given key.      Args:         key: The key to store the value under.         value: The value to cache.     """     self.cache.set(key, value) ``` |

### has\_key

```
has_key(key: str) -> bool
```

Check if a key exists in the disk cache.

Args:
key: The key to check for.

Returns:
True if the key exists in the cache, False otherwise.

Source code in `src/ragas/cache.py`

|  |  |
| --- | --- |
| ``` 109 110 111 112 113 114 115 116 117 118 ``` | ``` def has_key(self, key: str) -> bool:     """Check if a key exists in the disk cache.      Args:         key: The key to check for.      Returns:         True if the key exists in the cache, False otherwise.     """     return key in self.cache ``` |

## cacher

```
cacher(cache_backend: Optional[CacheInterface] = None)
```

Decorator that adds caching functionality to a function.

This decorator can be applied to both synchronous and asynchronous functions to cache their results.
If no cache backend is provided, the original function is returned unchanged.

Args:
cache\_backend (Optional[CacheInterface]): The cache backend to use for storing results.
If None, caching is disabled.

Returns:
Callable: A decorated function that implements caching behavior.

Source code in `src/ragas/cache.py`

|  |  |
| --- | --- |
| ``` 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 ``` | ``` def cacher(cache_backend: Optional[CacheInterface] = None):     """Decorator that adds caching functionality to a function.      This decorator can be applied to both synchronous and asynchronous functions to cache their results.     If no cache backend is provided, the original function is returned unchanged.      Args:         cache_backend (Optional[CacheInterface]): The cache backend to use for storing results.             If None, caching is disabled.      Returns:         Callable: A decorated function that implements caching behavior.     """      def decorator(func):         if cache_backend is None:             return func          # hack to make pyright happy         backend: CacheInterface = cache_backend          is_async = inspect.iscoroutinefunction(func)          @functools.wraps(func)         async def async_wrapper(*args, **kwargs):             cache_key = _generate_cache_key(func, args, kwargs)              if backend.has_key(cache_key):                 logger.debug(f"Cache hit for {cache_key}")                 return backend.get(cache_key)              result = await func(*args, **kwargs)             backend.set(cache_key, result)             return result          @functools.wraps(func)         def sync_wrapper(*args, **kwargs):             cache_key = _generate_cache_key(func, args, kwargs)              if backend.has_key(cache_key):                 logger.debug(f"Cache hit for {cache_key}")                 return backend.get(cache_key)              result = func(*args, **kwargs)             backend.set(cache_key, result)             return result          return async_wrapper if is_async else sync_wrapper      return decorator ``` |

November 28, 2025




November 28, 2025

Back to top
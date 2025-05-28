from ..extensions import cache

def get_or_cache(key, func, timeout):
    cached = cache.get(key)
    if cached:
        return cached
    result = func()
    cache.set(key, result, timeout=timeout)
    return result

    

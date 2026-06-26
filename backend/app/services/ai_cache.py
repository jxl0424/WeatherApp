import hashlib
import threading

from cachetools import TTLCache

_SUMMARY_CACHE: TTLCache = TTLCache(maxsize=512, ttl=15 * 60)
_ADVICE_CACHE: TTLCache = TTLCache(maxsize=512, ttl=30 * 60)
_LOCK = threading.Lock()


def _key(location: str, condition: str, temp_c: float) -> str:
    raw = f"{location.lower().strip()}|{condition.lower()}|{round(temp_c)}"
    return hashlib.sha256(raw.encode()).hexdigest()


def get_summary(location: str, condition: str, temp_c: float):
    with _LOCK:
        return _SUMMARY_CACHE.get(_key(location, condition, temp_c))


def set_summary(location: str, condition: str, temp_c: float, value) -> None:
    with _LOCK:
        _SUMMARY_CACHE[_key(location, condition, temp_c)] = value


def get_advice(location: str, condition: str, temp_c: float):
    with _LOCK:
        return _ADVICE_CACHE.get(_key(location, condition, temp_c))


def set_advice(location: str, condition: str, temp_c: float, value) -> None:
    with _LOCK:
        _ADVICE_CACHE[_key(location, condition, temp_c)] = value

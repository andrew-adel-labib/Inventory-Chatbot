from collections import OrderedDict
from apps.api.src.app_logging import get_logger
from apps.api.src.config import CACHE_SIZE

logger = get_logger(__name__)


class IntentCache:
    def __init__(self):
        self._cache = OrderedDict()

    def get(self, key):
        if key not in self._cache:
            return None
        self._cache.move_to_end(key)
        return self._cache[key]

    def set(self, key, value):
        self._cache[key] = value
        self._cache.move_to_end(key)
        if len(self._cache) > CACHE_SIZE:
            evicted = self._cache.popitem(last=False)
            logger.debug("Evicted cache entry: %s", evicted[0])
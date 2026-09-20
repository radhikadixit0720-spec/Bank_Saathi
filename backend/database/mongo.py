"""
MongoDB connection handling.

The real deployment uses MongoDB / MongoDB Atlas via Motor (the async
PyMongo driver). Because a local/hackathon environment does not always have
MONGODB_URI configured, this module falls back to a small in-process store
that mirrors the same async interface used by the services layer. This
means every feature is fully usable out of the box, and automatically
switches to real persistence the moment a valid MONGODB_URI is supplied -
no code changes required elsewhere.
"""
import logging
from typing import Any, Dict, List, Optional

from backend.config.settings import settings

logger = logging.getLogger("bank_saathi.database")

_motor_client = None
_motor_db = None
_using_fallback = True


class _InMemoryCollection:
    """Minimal stand-in for a Motor collection, used only when no real
    MongoDB connection is available. Supports exactly the operations this
    project needs so the rest of the codebase does not need to know or
    care whether Mongo is really connected."""

    def __init__(self):
        self._docs: List[Dict[str, Any]] = []

    async def insert_one(self, doc: Dict[str, Any]):
        self._docs.append(dict(doc))
        return doc

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for doc in self._docs:
            if _matches(doc, query):
                return dict(doc)
        return None

    def find(self, query: Optional[Dict[str, Any]] = None):
        query = query or {}
        results = [dict(doc) for doc in self._docs if _matches(doc, query)]
        return _InMemoryCursor(results)

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any]):
        for doc in self._docs:
            if _matches(doc, query):
                set_fields = update.get("$set", {})
                doc.update(set_fields)
                return {"matched_count": 1}
        return {"matched_count": 0}

    async def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        query = query or {}
        return len([d for d in self._docs if _matches(d, query)])


class _InMemoryCursor:
    def __init__(self, results: List[Dict[str, Any]]):
        self._results = results

    def sort(self, field: str, direction: int = -1):
        self._results.sort(key=lambda d: d.get(field, ""), reverse=direction < 0)
        return self

    def limit(self, n: int):
        self._results = self._results[:n]
        return self

    async def to_list(self, length: Optional[int] = None):
        return self._results[: length or len(self._results)]

    def __aiter__(self):
        self._iter_index = 0
        return self

    async def __anext__(self):
        if self._iter_index >= len(self._results):
            raise StopAsyncIteration
        item = self._results[self._iter_index]
        self._iter_index += 1
        return item


def _matches(doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
    for key, value in query.items():
        if doc.get(key) != value:
            return False
    return True


class _InMemoryDatabase:
    def __init__(self):
        self._collections: Dict[str, _InMemoryCollection] = {}

    def __getitem__(self, name: str) -> _InMemoryCollection:
        if name not in self._collections:
            self._collections[name] = _InMemoryCollection()
        return self._collections[name]

    def get_collection(self, name: str) -> _InMemoryCollection:
        return self[name]


_fallback_db = _InMemoryDatabase()


def connect_to_mongo() -> None:
    """Attempt to connect to MongoDB Atlas / MongoDB using MONGODB_URI.

    If the URI is missing or the connection cannot be established, the
    app silently continues on the in-memory fallback store so the rest of
    the product keeps working end-to-end during local development/demo.
    """
    global _motor_client, _motor_db, _using_fallback

    if not settings.MONGODB_URI:
        logger.warning(
            "MONGODB_URI is not set. Bank Saathi is running with an in-memory "
            "data store (data will NOT persist between restarts). Set "
            "MONGODB_URI and MONGODB_DB_NAME in backend/.env to use real "
            "MongoDB / MongoDB Atlas."
        )
        _using_fallback = True
        return

    try:
        import motor.motor_asyncio  # imported lazily so it's optional

        _motor_client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.MONGODB_URI, serverSelectionTimeoutMS=4000
        )
        _motor_db = _motor_client[settings.MONGODB_DB_NAME]
        _using_fallback = False
        logger.info("Connected to MongoDB database '%s'.", settings.MONGODB_DB_NAME)
    except Exception as exc:  # noqa: BLE001 - we want to fall back on ANY error
        logger.error("Could not connect to MongoDB (%s). Falling back to "
                      "in-memory store.", exc)
        _motor_client = None
        _motor_db = None
        _using_fallback = True


def close_mongo_connection() -> None:
    global _motor_client
    if _motor_client is not None:
        _motor_client.close()
        _motor_client = None


def get_collection(name: str):
    """Return a collection-like object, backed by real MongoDB when
    available and by the in-memory fallback otherwise."""
    if _using_fallback or _motor_db is None:
        return _fallback_db[name]
    return _motor_db[name]


def is_using_fallback() -> bool:
    return _using_fallback

"""Storage adapters: local filesystem now, object storage in a future phase."""

from storytime.adapters.storage.base import StorageAdapter
from storytime.adapters.storage.local import LocalFilesystemStorage, StorageKeyError

__all__ = ["LocalFilesystemStorage", "StorageAdapter", "StorageKeyError"]

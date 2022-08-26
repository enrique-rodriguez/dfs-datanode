import os
import pytest
from datanode.blockstorage.infrastructure.fs_store import FileSystemStore


@pytest.fixture
def get_store(tmp_path):
    location = os.path.join(tmp_path, "data")
    os.mkdir(location)

    def factory():
        return FileSystemStore(location)

    return factory


def test_get_with_non_stored_key_gives_none(get_store):
    store = get_store()

    assert store.get("payload") == None


def test_saves_payload(get_store):
    store = get_store()

    store.put("payload", b"the payload")

    assert store.get("payload") == b"the payload"


def test_persistence(get_store):
    store = get_store()

    store.put("payload", b"the payload")

    store = get_store()

    assert store.get("payload") == b"the payload"

import os
import pytest
from datanode.blockstorage.infrastructure import fs_store


@pytest.fixture
def get_store(tmp_path):
    location = os.path.join(tmp_path, "data")
    os.mkdir(location)

    def factory():
        return fs_store.FileSystemStore(location)

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


def test_delete(get_store):
    store = get_store()

    store.put("payload", b"the payload")
    store.delete("payload")

    assert store.get("payload") == None


def test_raises_value_if_delete_key_that_doesnt_exist(get_store):
    store = get_store()

    with pytest.raises(ValueError):
        store.delete("payload")

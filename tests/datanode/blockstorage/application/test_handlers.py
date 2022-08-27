import pytest
from datanode.blockstorage.domain import commands, exceptions


def test_put_block(bus, store):
    bus.handle(commands.PutBlock(block_id="1", payload=b"paylod"))

    assert store.put_called


def test_delete_block(bus, store):
    bus.handle(commands.PutBlock(block_id="1", payload=b"paylod"))
    bus.handle(commands.DeleteBlock(block_id="1"))

    assert store.delete_called


def test_raises_block_not_found(bus, store):
    with pytest.raises(exceptions.BlockNotFoundError):
        bus.handle(commands.DeleteBlock(block_id="1"))

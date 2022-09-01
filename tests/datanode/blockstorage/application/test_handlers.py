import pytest
from datanode.blockstorage.domain import model
from datanode.blockstorage.domain import commands
from datanode.blockstorage.domain import exceptions


def test_adds_block_to_storage(bus, store):
    bus.handle(commands.PutBlock(file_id="1", block_id="1", payload=b"paylod"))

    assert store.put_called


def test_saves_block_to_repository(bus, uow):
    bus.handle(commands.PutBlock(file_id="1", block_id="2", payload=b"paylod"))

    file = uow.repository.get(model.File, id="1")

    assert uow.committed
    assert file.blocks[0].id == "2"


def test_delete_file_blocks_from_storage(bus, store):
    bus.handle(commands.PutBlock(file_id="1", block_id="1", payload=b"paylod"))
    bus.handle(commands.PutBlock(file_id="1", block_id="2", payload=b"paylod"))
    bus.handle(commands.PutBlock(file_id="2", block_id="3", payload=b"paylod"))
    bus.handle(commands.DeleteFile(file_id="1"))

    assert store.get("1") == None
    assert store.get("2") == None
    assert store.get("3") != None


def test_delete_file_from_repository(bus, uow):
    bus.handle(commands.PutBlock(file_id="1", block_id="1", payload=b"paylod"))
    bus.handle(commands.DeleteFile(file_id="1"))

    assert uow.committed
    assert uow.repository.get(model.File, id="1") == None


def test_raises_block_not_found(bus):
    with pytest.raises(exceptions.BlockNotFoundError):
        bus.handle(commands.DeleteBlock(block_id="1"))

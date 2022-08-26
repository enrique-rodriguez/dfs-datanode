from datanode.blockstorage.domain import commands


def test_put_block(bus, store):
    bus.handle(commands.PutBlock(block_id="1", payload=b"paylod"))

    assert store.put_called
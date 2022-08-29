from ..domain import commands
from ..domain import exceptions


def put_block(cmd: commands.PutBlock, **deps):
    store = deps.get("store")
    store.put(cmd.block_id, cmd.payload)


def delete_block(cmd: commands.DeleteBlock, **deps):
    store = deps.get("store")
    if not store.get(cmd.block_id):
        raise exceptions.BlockNotFoundError
    store.delete(cmd.block_id)



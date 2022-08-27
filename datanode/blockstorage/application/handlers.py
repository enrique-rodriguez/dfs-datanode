from dfs_shared.application.uow import UnitOfWork
from ..domain import commands
from ..domain import exceptions

def put_block(cmd: commands.PutBlock, store, **deps):
    store.put(cmd.block_id, cmd.payload)


def delete_block(cmd: commands.DeleteBlock, store, **deps):
    if not store.get(cmd.block_id):
        raise exceptions.BlockNotFoundError
    store.delete(cmd.block_id)
from dfs_shared.application.uow import UnitOfWork
from ..domain import commands

def put_block(cmd: commands.PutBlock, store, **deps):
    store.put(cmd.block_id, cmd.payload)

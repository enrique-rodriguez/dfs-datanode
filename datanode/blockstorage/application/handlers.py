from ..domain import model
from ..domain import events
from ..domain import commands
from ..domain import exceptions
from datanode.blockstorage.domain.store import Store
from datanode.blockstorage.application.uow import UnitOfWork


def put_block_to_storage(cmd: commands.PutBlock, uow: UnitOfWork, store, **deps):
    store.put(cmd.block_id, cmd.payload)

    uow.add_event(events.BlockStored(cmd.file_id, cmd.block_id))


def add_block_to_file(event: events.BlockStored, uow: UnitOfWork, **deps):
    file_id = event.file_id
    if not (file := uow.repository.get(model.File, id=file_id)):
        file = model.File(id=file_id)
    file.add_block(event.block_id)
    with uow:
        uow.repository.save(file)
        uow.commit()


def delete_block_from_storage(cmd: commands.DeleteBlock, store: Store, **deps):
    if not store.get(cmd.block_id):
        raise exceptions.BlockNotFoundError
    store.delete(cmd.block_id)


def delete_file(cmd: commands.DeleteFile, uow: UnitOfWork, **deps):
    file = uow.repository.get(model.File, id=cmd.file_id)
    if not file:
        return
    with uow:
        uow.repository.delete(file)
        uow.commit()
        uow.add_event(events.FileDeleted(file))


def delete_file_blocks(event: events.FileDeleted, store: Store, **deps):
    file = event.file
    for blk in file.blocks:
        store.delete(blk.id)

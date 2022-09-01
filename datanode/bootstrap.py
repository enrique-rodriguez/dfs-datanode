import os
from datanode.blockstorage.infrastructure.json_repo import JsonRepository
from datanode.uow import JsonUnitOfWork
from datanode.blockstorage import EVENT_HANDLERS
from datanode.blockstorage import COMMAND_HANDLERS
from dfs_shared.application import message_bus
from datanode.blockstorage.infrastructure.fs_store import FileSystemStore



class MessageBus(message_bus.MessageBus):
    def __init__(self, uow, command_handlers, event_handlers, **deps):
        super().__init__(uow, command_handlers, event_handlers)
        self.deps = deps

    def handle_command(self, command):
        handler = self.command_handlers.get(type(command))

        if not handler:
            raise ValueError(
                f"Handler for command '{command.__class__.__name__}' not found."
            )

        handler(command, uow=self.uow, **self.deps)

    def handle_event(self, event):
        handlers = self.event_handlers.get(type(event), list())

        for handler in handlers:
            handler(event, uow=self.uow, **self.deps)


def get_unit_of_work(basedir, db, **kwargs):
    dbpath = os.path.join(basedir, db.get("name"))

    return JsonUnitOfWork(dbpath)


def get_store(basedir, blocks_save_location, **kwargs):
    path = os.path.join(basedir, blocks_save_location)
    if not os.path.exists(path):
        os.mkdir(path)
    return FileSystemStore(path)


def bootstrap(config, **kwargs):
    store = kwargs.pop("store", get_store(**config))
    uow = kwargs.pop("uow", get_unit_of_work(**config))

    return MessageBus(uow, COMMAND_HANDLERS, EVENT_HANDLERS, store=store)

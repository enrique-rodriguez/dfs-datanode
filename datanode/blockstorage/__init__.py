from .domain import events
from .domain import commands
from .application import handlers


COMMAND_HANDLERS = {
    commands.PutBlock: handlers.put_block_to_storage,
    commands.DeleteBlock: handlers.delete_block_from_storage,
    commands.DeleteFile: handlers.delete_file,
}


EVENT_HANDLERS = {
    events.BlockStored: [handlers.add_block_to_file],
    events.FileDeleted: [handlers.delete_file_blocks],
}

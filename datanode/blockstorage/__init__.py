from .domain import events
from .domain import commands
from .application import handlers


COMMAND_HANDLERS = {
    commands.PutBlock: handlers.put_block,
    commands.DeleteBlock: handlers.delete_block,
}


EVENT_HANDLERS = {
}

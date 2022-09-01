from datanode.blockstorage.domain import commands


def file_deleted(bus, body):
    file_id = body.get("id")
    
    bus.handle(commands.DeleteFile(file_id))

import uuid
import bottle
from bottle import request
from bottle import response
from datanode.blockstorage import views
from datanode.blockstorage.domain import commands
from datanode.blockstorage.domain import exceptions


def routes(bus):
    root = bottle.Bottle()

    @root.get("/health")
    def health():
        return "ok"

    @root.post("/blocks/<file_id>")
    def put_block(file_id):
        block_id = uuid.uuid4().hex
        response.status = 201
        upload = request.files.get("block")
        contents = upload.file.read() if upload else b""
        if len(contents) == 0:
            response.status = 400
            return
        bus.handle(commands.PutBlock(
            file_id=file_id, 
            block_id=block_id, 
            payload=contents
        ))
        return {"id": block_id}

    @root.get("/blocks/<bid>")
    def get_block(bid):
        content = views.get_block(bus, bid)
        if not content:
            response.status = 404
            content = b""
        response.set_header("Content-Type", "application/octet-stream")
        return content

    @root.delete("/blocks/<bid>")
    def delete_block(bid):
        try:
            bus.handle(commands.DeleteBlock(bid))
        except exceptions.BlockNotFoundError:
            response.status = 404
        return {}

    return root

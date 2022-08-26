import uuid
import bottle
from bottle import request
from bottle import response
from datanode.blockstorage.domain import commands


def routes(bus):
    root = bottle.Bottle()

    @root.get("/health")
    def health():
        return "ok"

    @root.post("/blocks")
    def put_block():
        block_id = uuid.uuid4().hex
        response.status = 201
        upload = request.files.get("block")
        contents = upload.file.read() if upload else b''
        if len(contents) == 0:
            response.status = 400
            return
        bus.handle(commands.PutBlock(block_id=block_id, payload=contents))
        return {'id': block_id}
    
    @root.get("/blocks/<bid>")
    def get_block(bid):
        store = bus.deps.get("store")
        content = store.get(bid)
        if not content:
            response.status = 404
            content = b""
        response.set_header("Content-Type", "application/octet-stream")
        return content

    return root

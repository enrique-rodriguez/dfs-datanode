import bottle
from routes import routes
from datanode.bootstrap import bootstrap


def get_app(bus):
    app = bottle.Bottle()
    app.mount("/dfs", routes(bus))
    return app

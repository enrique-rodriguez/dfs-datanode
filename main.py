import logging
import argparse
import external
import messaging
from app import get_app
from settings import get_config
from utils.interval import set_interval
from utils.interval import clear_interval
from datanode.bootstrap import bootstrap

logging.basicConfig(
    filename="std.log",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def register_datanode(host, port, logger):
    logger.info(f"Publishing datanode registration message.")

    messaging.publish_message(
        messaging.ExternalMessage(
            exchange="datanodes",
            exchange_type="fanout",
            routing_key="register_datanode",
            body={"host": host, "port": port},
        )
    )


def get_parser():
    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("port", type=int)
    parser.add_argument("dir")

    return parser


def start_consumers(bus):
    for exchange, handlers in external.HANDLERS.items():
        for hndlr in handlers:
            callback = messaging.consumer_factory(hndlr, bus)
            messaging.register(exchange, callback)


def start_webapp(bus, host, port, logger):
    app = get_app(bus)
    app.run(host=host, port=port, server="paste", debug=True)


if __name__ == "__main__":
    config = get_config()
    parser = get_parser()
    args = parser.parse_args()
    config["blocks_save_location"] = args.dir
    bus = bootstrap(config)

    host = args.host
    port = args.port

    logger = logging.getLogger(__name__)

    reg_interval = set_interval(
        register_datanode, args=(host, port, logger), interval=20
    )

    start_consumers(bus)
    start_webapp(bus, host, port, logger)

    clear_interval(reg_interval)

    logger.info(f"SHUTTING DOWN DATANODE SERVER {host}:{port}")

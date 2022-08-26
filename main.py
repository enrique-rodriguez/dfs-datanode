import json
import logging
import requests
import argparse
from app import get_app
from pathlib import Path


logging.basicConfig(
    filename="std.log",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def register_to_metadata_server(url, host, port, logger):
    try:
        res = requests.post(f"{url}/datanodes", data={"host": host, "port": port})
    except requests.exceptions.ConnectionError:
        exit(f"Could not establish connection with metadata server at {address}")

    msg = f"Registration with metadata server at {url} successful."
    if res.status_code == 400:
        msg = "Datanode already registered."
    logger.info(msg)


def get_parser():
    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("port", type=int)
    parser.add_argument("dir")

    return parser


def main(config, host, port, logger):
    meta_host = config["meta"]["host"]
    meta_port = config["meta"]["port"]

    address = f"{meta_host}:{meta_port}"
    meta_url = f"http://{address}/dfs"

    logger.info(f"Registrating datanode {host}:{port} with metadata server {address}.")

    register_to_metadata_server(meta_url, host, port, logger)

    app = get_app(config)

    app.run(host=host, port=port, debug=True, reloader=True)


if __name__ == "__main__":

    with open("conf.json", "r") as f:
        config = json.load(f)

    parser = get_parser()

    args = parser.parse_args()

    config["basedir"] = str(Path(__file__).resolve().parent)
    config["blocks_save_location"] = args.dir

    logger = logging.getLogger(__name__)

    main(config, args.host, args.port, logger)

    logger.info(f"SHUTTING DOWN DATANODE SERVER {args.host}:{args.port}")

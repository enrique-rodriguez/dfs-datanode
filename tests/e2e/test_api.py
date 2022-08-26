import os
import uuid
import pytest
from . import api_client as client


@pytest.fixture
def api_client(tmp_path):
    client.set_config(
        {
            "basedir": str(tmp_path),
            "db": {"name": "data.json"},
            "blocks_save_location": "blocks"
        }
    )

    return client

def test_put_block(api_client):
    payload = b'g\r9\x075YF\xdf\xb7\xbfzsB\xc2\xcb\xa6'
    files = [("block", "block", payload)]
    put_res = api_client.put_block(files)
    bid = put_res.json.get("id")
    get_res = api_client.get_block(bid)

    assert put_res.status_code == 201
    assert get_res.status_code == 200
    assert get_res.body == payload


def test_put_block_with_no_file(api_client):
    put_res = api_client.put_block([], expect_errors=True)

    assert put_res.status_code == 400

def test_put_empty_block(api_client):
    payload = b''
    files = [("block", "block", payload)]
    put_res = api_client.put_block(files, expect_errors=True)

    assert put_res.status_code == 400

def test_get_gives_404_when_block_not_found(api_client):
    get_res = api_client.get_block(uuid.uuid4().hex, expect_errors=True)

    assert get_res.status_code == 404


import json
from app import get_app
from webtest import TestApp


config = {}


def set_config(new_config):
    global config
    config = new_config


def use_client(func):
    def inner(*args, **kwargs):
        return func(client=TestApp(get_app(config)), *args, **kwargs)

    return inner


@use_client
def home(client):
    return client.get("/", expect_errors=True)


@use_client
def put_block(files, client: TestApp, expect_errors=False):

    res = client.post(
        "/dfs/blocks",
        upload_files=files,
        expect_errors=expect_errors,
    )

    if not expect_errors:
        assert res.status_code == 201

    return res


@use_client
def get_block(bid, client: TestApp, expect_errors=False):
    res = client.get(f"/dfs/blocks/{bid}", expect_errors=expect_errors)

    if not expect_errors:
        assert res.status_code == 200

    return res


@use_client
def delete_block(bid, client: TestApp, expect_errors=False):
    res = client.delete(f"/dfs/blocks/{bid}", expect_errors=expect_errors)

    if not expect_errors:
        assert res.status_code == 200

    return res
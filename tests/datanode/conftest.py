from collections import defaultdict
import pytest
from datanode.bootstrap import bootstrap
from dfs_shared.application.uow import UnitOfWork


class InMemoryStore:
    def __init__(self):
        self.storage = dict()

    def put(self, name, value):
        self.put_called = True
        self.storage[name] = value

    def get(self, name):
        return self.storage.get(name, None)

    def delete(self, name):
        if name not in self.storage:
            raise ValueError
        del self.storage[name]


class InMemoryRepository:
    def __init__(self):
        self.objects = defaultdict(list)

    def get(self, obj_class, id):
        try:
            return next(o for o in self.objects[obj_class] if o.id == id)
        except StopIteration:
            return None

    def save(self, obj):
        obj_class = obj.__class__
        self.objects[obj_class].append(obj)

    def delete(self, obj):
        obj_class = obj.__class__
        objects = self.objects[obj_class]
        objects = list(filter(lambda o: o != obj, objects))
        self.objects[obj_class] = objects


class FakeUnitOfWork(UnitOfWork):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = InMemoryRepository()

    def __enter__(self):
        self.committed = False
        return super().__enter__()

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@pytest.fixture
def config(tmp_path):
    return {
        "basedir": str(tmp_path),
        "db": {"name": "data.json"},
        "blocks_save_location": "blocks",
    }


@pytest.fixture
def store():
    return InMemoryStore()


@pytest.fixture
def bus(uow, store, config):
    return bootstrap(config, uow=uow, store=store)


@pytest.fixture
def uow(config):
    return FakeUnitOfWork(seen=set())

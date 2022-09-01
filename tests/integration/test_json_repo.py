import os
import pytest

from datanode.blockstorage.infrastructure.json_repo import JsonRepository


# Objects for testing purposes

class MyObject:
    def __init__(self, id, **kwargs):
        self.id = id
        for field, value in kwargs.items():
            setattr(self, field, value)

    def __eq__(self, o):
        if not isinstance(o, self.__class__):
            return False

        return self.id == o.id

    def __hash__(self):
        return hash(self.id)


class MyCompoundObject(MyObject):
    def __init__(self, myobjects=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.myobjects = myobjects or list()


@pytest.fixture
def get_repo(tmp_path):
    path = os.path.join(tmp_path, "data.json")

    def inner(autocommit=False):
        return JsonRepository(
            path,
            autocommit=autocommit,
            seen=set(),
            objects=[MyObject, MyCompoundObject],
        )

    return inner


def test_object_not_found_gives_none(get_repo):
    repo = get_repo()

    assert repo.get(MyObject, id="1") == None


def test_save_obj(get_repo):
    repo = get_repo()

    obj = MyObject(id="1")

    repo.save(obj)
    repo.commit()

    assert repo.get(MyObject, id="1")


def test_autocommit(get_repo):
    repo = get_repo()
    repo.set_autocommit(True)

    obj = MyObject(id="1")

    repo.save(obj)
    # repo.commit()        # No manual commit this time.

    assert repo.get(MyObject, id="1") == obj


def test_persistence(get_repo):
    repo = get_repo()
    obj = MyObject(id="1")

    repo.save(obj)
    repo.commit()

    repo = get_repo()
    assert repo.get(MyObject, id="1") == obj


def test_save_compound_object(get_repo):
    repo = get_repo()

    objects = [MyObject(id=str(i)) for i in range(1, 6)]
    compound = MyCompoundObject(objects, id="1")

    repo.save(compound)
    repo.commit()

    fetched = repo.get(MyCompoundObject, id="1")

    assert fetched == compound
    assert fetched.myobjects == compound.myobjects


def test_does_not_save_if_changes_are_not_commited(get_repo):
    repo = get_repo()

    obj = MyObject(id="1")

    repo.save(obj)

    repo = get_repo()

    assert repo.get(MyObject, id="1") == None


def test_delete(get_repo):
    repo = get_repo()

    obj = MyObject(id="1")

    repo.save(obj)
    repo.commit()
    repo.delete(obj)
    repo.commit()

    assert repo.get(MyObject, id="1") == None


def test_does_not_delete_if_changes_are_not_commited(get_repo):
    repo = get_repo()

    obj = MyObject(id="1")

    repo.save(obj)
    repo.commit()
    repo.delete(obj)

    assert repo.get(MyObject, id="1") == obj


def test_rollback(get_repo):
    repo = get_repo()

    obj = MyObject(id="1")

    repo.save(obj)
    repo.rollback()

    # Commit prove the changes were discarded when we do the assertion.
    repo.commit()

    assert repo.get(MyObject, id="1") == None

from dfs_shared.application import uow
from datanode.blockstorage.domain import model
from datanode.blockstorage.infrastructure import json_repo


OBJECTS = [
    model.File,
    model.Block,
]


class JsonUnitOfWork(uow.UnitOfWork):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = json_repo.JsonRepository(
            path=path, 
            objects=OBJECTS, 
            seen=self.seen, 
            autocommit=False
        )

    def __enter__(self):
        self.last_autocommit = self.repository.autocommit
        self.repository.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args, **kwargs):
        self.repository.set_autocommit(self.last_autocommit)
        del self.last_autocommit
        return super().__exit__(*args, **kwargs)

    def commit(self):
        self.repository.commit()

    def rollback(self):
        self.repository.rollback()

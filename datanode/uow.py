from dfs_shared.application import uow
from dfs_shared.infrastructure import json_db
from dfs_shared.infrastructure import json_db
from dfs_shared.domain.repository import RepositoryManager




class JsonUnitOfWork(uow.UnitOfWork):
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repository = json_db.JsonDatabase(path)

    def __enter__(self):
        self.repository.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args, **kwargs):
        self.repository.set_autocommit(True)
        return super().__exit__(*args, **kwargs)

    def commit(self):
        self.repository.commit()

    def rollback(self):
        self.repository.rollback()

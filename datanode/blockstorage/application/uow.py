from dfs_shared.application import uow
from dfs_shared.domain.repository import Repository


class UnitOfWork(uow.UnitOfWork):
    repository: Repository
from . import model
from dataclasses import dataclass
from dfs_shared.domain import events


@dataclass(frozen=True)
class BlockStored(events.Event):
    file_id: str
    block_id: str


@dataclass(frozen=True)
class BlocksDeleted(events.Event):
    file_id: str


@dataclass(frozen=True)
class FileDeleted(events.Event):
    file: model.File
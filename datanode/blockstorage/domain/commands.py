from dataclasses import dataclass
from dfs_shared.domain import commands


@dataclass(frozen=True)
class PutBlock(commands.Command):
    block_id: str
    payload: bytes

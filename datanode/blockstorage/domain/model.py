from dfs_shared.domain.model import Entity
from dfs_shared.domain.model import AggregateRoot


class File(AggregateRoot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocks = list()
    
    def add_block(self, block_id):
        self.blocks.append(Block(self.id, id=block_id))


class Block(Entity):
    def __init__(self, file_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_id = file_id

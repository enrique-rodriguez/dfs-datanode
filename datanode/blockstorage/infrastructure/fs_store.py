import os
from datanode.blockstorage.domain.store import Store

class FileSystemStore(Store):

    def __init__(self, save_location):
        self.save_location = save_location

    def put(self, name, value):
        path = os.path.join(self.save_location, name)
        with open(path, 'wb') as f:
            f.write(value)
    
    def get(self, name):
        path = os.path.join(self.save_location, name)
        if not os.path.exists(path):
            return None
        with open(path, 'rb') as f:
            return f.read()
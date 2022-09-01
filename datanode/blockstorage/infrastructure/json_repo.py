import os
import json
from dfs_shared.domain.repository import Repository


class JsonRepository(Repository):
    def __init__(
        self, path, objects, encoder=None, decoder=None, autocommit=False, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.path = path
        self.encoder = encoder or MyJSONEncoder
        self.decoder = decoder or MyJSONDecoder
        self.decoder.objects = objects
        self.staging = dict()
        self.autocommit = autocommit

    def set_autocommit(self, autocommit):
        self.autocommit = autocommit

    def get(self, obj_class, id):
        obj = self._get(obj_class, id)
        if obj:
            self.seen.add(obj)
        return obj

    def delete(self, obj):
        self.seen.add(obj)
        self._delete(obj)

    def _save(self, obj):
        key = self.get_key(obj.__class__)
        objects = self.get_objects(key)
        objects.append(obj)
        self.staging[key] = objects
        if self.autocommit:
            self.commit()

    def _get(self, obj_class, id):
        key = self.get_key(obj_class)
        objects = self.get_objects(key)

        for obj in objects:
            if obj.id == id:
                return obj

        return None

    def _update(self, obj):
        pass

    def _delete(self, obj):
        key = self.get_key(obj.__class__)
        objects = self.get_objects(key)
        objects = list(filter(lambda o: o.id != obj.id, objects))
        self.staging[key] = objects

    def get_by_spec(self, spec):
        pass

    def commit(self):
        db = self.get_db()
        db.update(self.staging)
        self.write_to_file(db)
        self.rollback()

    def rollback(self):
        self.staging.clear()

    def get_db(self):
        if not os.path.exists(self.path):
            return dict()
        with open(self.path, "r") as f:
            return json.load(f, cls=self.decoder)

    def get_objects(self, key):
        db = self.get_db()
        return db.get(key, list())

    def write_to_file(self, db):
        with open(self.path, "w") as f:
            json.dump(db, f, cls=self.encoder)

    def get_key(self, obj_class):
        return obj_class.__name__


class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return super().default(o)
        except:
            encoded = vars(o)
            encoded.update({"obj_class": o.__class__.__name__})
            return encoded


class MyJSONDecoder(json.JSONDecoder):
    objects = []

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):

        if not (obj_class := o.pop("obj_class", None)):
            return o

        for obj in self.objects:
            if obj_class == obj.__name__:
                return obj(**o)

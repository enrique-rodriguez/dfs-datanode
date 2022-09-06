import abc


class Store(abc.ABC):
    @abc.abstractmethod
    def put(self, name, value):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, name):
        raise NotImplementedError

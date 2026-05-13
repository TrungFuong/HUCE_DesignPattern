from abc import ABC, abstractmethod


class HashService(ABC):

    @abstractmethod
    def hash_data(self, data: dict) -> str:
        pass

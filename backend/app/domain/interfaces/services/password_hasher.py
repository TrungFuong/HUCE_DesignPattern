from abc import ABC, abstractmethod


class PasswordHasher(ABC):

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        pass

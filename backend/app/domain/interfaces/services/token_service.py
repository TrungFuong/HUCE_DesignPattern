from abc import ABC, abstractmethod


class TokenService(ABC):

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        pass

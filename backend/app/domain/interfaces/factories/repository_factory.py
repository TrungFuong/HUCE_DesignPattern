from abc import ABC, abstractmethod


class RepositoryFactory(ABC):

    @abstractmethod
    def create_batch_repository(self):
        pass

    @abstractmethod
    def create_sensor_log_repository(self):
        pass

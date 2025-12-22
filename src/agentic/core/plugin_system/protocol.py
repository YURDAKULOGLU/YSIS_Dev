from abc import ABC, abstractmethod

class ToolProtocol(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

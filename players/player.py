from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def play(self, query):
        pass

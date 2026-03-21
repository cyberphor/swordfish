# agent/swordfish/history.py

from abc import ABC, abstractmethod

class HistoryStore(ABC):
    @abstractmethod
    async def get(self, session_id: str) -> list:
        pass

    @abstractmethod
    async def save(self, session_id: str, messages: list):
        pass

class InMemoryStore(HistoryStore):
    def __init__(self):
        self.storage = {}

    async def get(self, session_id: str):
        return self.storage.get(session_id, [])

    async def save(self, session_id: str, messages: list):
        self.storage[session_id] = messages

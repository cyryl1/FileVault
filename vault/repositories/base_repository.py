from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """Base repository class"""

    def __init__(self, db):
        self.db = db
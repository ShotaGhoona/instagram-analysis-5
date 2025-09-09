from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List
from core.database import database

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    """Base repository with common CRUD operations"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.client = database.client
    
    @abstractmethod
    async def create(self, entity: T) -> Optional[T]:
        """Create a new entity"""
        pass
    
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[T]:
        """Get all entities"""
        pass
    
    @abstractmethod
    async def update(self, entity_id: str, update_data: dict) -> Optional[T]:
        """Update entity by ID"""
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete entity by ID"""
        pass
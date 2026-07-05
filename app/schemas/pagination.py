from typing import Generic, List, TypeVar

from pydantic import BaseModel

# T es un comodín. Puede ser UserResponse, StudyRoomResponse, etc.
T = TypeVar('T')

class PaginationMeta(BaseModel):
    total_records: int
    current_page: int
    total_pages: int
    has_next: bool
    has_previous: bool

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta
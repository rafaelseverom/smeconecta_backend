from pydantic import BaseModel
from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel

T = TypeVar("T")

class Page(GenericModel, Generic[T]):
    page: int
    limit: int
    total: int
    total_pages: int
    data: List[T]
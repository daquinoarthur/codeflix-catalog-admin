from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class GetCategoryInput:
    id: UUID


@dataclass
class GetCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool


class GetCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: GetCategoryInput) -> GetCategoryResponse:
        category = self.repository.get_by_id(request.id)
        if category is None:
            raise CategoryNotFoundException(f"Category with {request.id} not found.")
        return GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import (
    InvalidCategoryDataException,
)
from src.core.category.domain.category import Category


@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CreateCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool


class CreateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        try:
            created_category = Category(
                name=request.name,
                description=request.description,
                is_active=request.is_active,
            )
        except ValueError as error:
            raise InvalidCategoryDataException(str(error))

        created_category = self.repository.save(created_category)

        return CreateCategoryResponse(
            id=created_category.id,
            name=created_category.name,
            description=created_category.description,
            is_active=created_category.is_active,
        )

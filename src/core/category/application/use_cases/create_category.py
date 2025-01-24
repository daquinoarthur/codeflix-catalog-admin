from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import InvalidCategoryDataException
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class CreateCategoryInput:
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CreateCategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


class CreateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: CreateCategoryInput) -> CreateCategoryOutput:
        try:
            created_category = Category(
                name=request.name,
                description=request.description,
                is_active=request.is_active,
            )
        except ValueError as error:
            raise InvalidCategoryDataException(str(error))
        created_category = self.repository.save(created_category)
        return CreateCategoryOutput(
            id=created_category.id,
            name=created_category.name,
            description=created_category.description,
            is_active=created_category.is_active,
        )

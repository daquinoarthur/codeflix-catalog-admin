from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import (
    CategoryNotFoundException,
    InvalidCategoryDataException,
)


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool = True


@dataclass
class UpdateCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> UpdateCategoryResponse:
        category = self.repository.get_by_id(request.id)

        if not category:
            raise CategoryNotFoundException(
                "Can not update category with id: {request.id}. Category not found."
            )

        category_name = request.name if request.name else category.name
        category_description = (
            request.description if request.description else category.description
        )

        try:
            category.update_category(category_name, category_description)
        except ValueError as error:
            raise InvalidCategoryDataException(str(error))

        category.activate() if request.is_active else category.deactivate()

        self.repository.update(category)

        return UpdateCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

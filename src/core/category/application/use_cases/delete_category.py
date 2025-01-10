from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class DeleteCategoryInput:
    id: UUID


@dataclass
class DeleteCategoryOutput:
    detail: str


class DeleteCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: DeleteCategoryInput) -> DeleteCategoryOutput:
        category = self.repository.get_by_id(request.id)
        if category is None:
            raise CategoryNotFoundException(
                f"Can not delete Category with id: {request.id}. Category not found."
            )
        self.repository.delete(category.id)
        return DeleteCategoryOutput(detail="Category deleted successfully.")

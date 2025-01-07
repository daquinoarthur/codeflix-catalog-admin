from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories=None):
        self.categories = categories or []

    def save(self, category: Category) -> Category:
        self.categories.append(category)
        return category

    def get_by_id(self, id: UUID) -> Category | None:
        return next(
            (category for category in self.categories if category.id == id), None
        )

    def delete(self, id: UUID) -> None:
        self.categories = [
            category for category in self.categories if category.id != id
        ]

    def update(self, category: Category) -> Category:
        self.categories.remove(category)
        self.categories.append(category)
        return category

    def list(self) -> list[Category]:
        return [category for category in self.categories]

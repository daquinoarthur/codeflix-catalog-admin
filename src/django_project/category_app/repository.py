from uuid import UUID

from src.django_project.category_app.models import Category as CategoryModel
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel | None = None):
        self.category_model = category_model or CategoryModel

    def save(self, category: Category) -> Category:
        self.category_model.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
        return category

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = self.category_model.objects.get(id=id)
            return Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
        except self.category_model.DoesNotExist:
            return None

    def update(self, category: Category) -> Category:
        category_from_db = self.get_by_id(category.id)
        if category_from_db is None:
            raise ValueError("Category not found")
        self.category_model.objects.filter(id=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
        updated_category = self.get_by_id(category.id)
        return updated_category

    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()

    def list(self) -> list[Category]:
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in self.category_model.objects.all()
        ]

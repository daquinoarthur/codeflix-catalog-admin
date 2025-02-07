from uuid import UUID

from django.db import transaction

from src.django_project.category_app.models import Category as CategoryModel
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel | None = None):
        self.category_model = category_model or CategoryModel

    def save(self, category: Category) -> Category:
        category_model = CategoryModelMapper.from_entity_to_model(category)
        category_model.save()
        return CategoryModelMapper.from_model_to_entity(category_model)

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = self.category_model.objects.get(id=id)
            return CategoryModelMapper.from_model_to_entity(category)
        except self.category_model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()

    def list(self) -> list[Category]:
        return [
            CategoryModelMapper.from_model_to_entity(category)
            for category in self.category_model.objects.all()
        ]

    def update(self, category: Category) -> Category | None:
        try:
            with transaction.atomic():
                persisted_category = (
                    self.category_model.objects.select_for_update().get(id=category.id)
                )
                update_fields = {
                    "name": category.name,
                    "description": category.description,
                    "is_active": category.is_active,
                }
                self.category_model.objects.filter(id=category.id).update(
                    **update_fields
                )
                persisted_category.refresh_from_db()
                return Category(
                    id=persisted_category.id,
                    name=persisted_category.name,
                    is_active=persisted_category.is_active,
                    description=persisted_category.description,
                )
        except self.category_model.DoesNotExist:
            return None


class CategoryModelMapper:
    @staticmethod
    def from_entity_to_model(category: Category) -> CategoryModel:
        return CategoryModel(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    @staticmethod
    def from_model_to_entity(category_model: CategoryModel) -> Category:
        return Category(
            id=category_model.id,
            name=category_model.name,
            description=category_model.description,
            is_active=category_model.is_active,
        )

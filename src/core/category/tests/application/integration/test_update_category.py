from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryInput,
    UpdateCategoryOutput,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(
            name="Category 1",
            description="Description 1",
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)
        use_case = UpdateCategory(repository)
        request = UpdateCategoryInput(
            id=category.id,
            name="Category 1 Updated",
            description="Description 1 Updated",
        )
        response = use_case.execute(request)
        assert response == UpdateCategoryOutput(
            id=category.id,
            name="Category 1 Updated",
            description="Description 1 Updated",
            is_active=category.is_active,
        )
        updated_category = repository.get_by_id(category.id)
        if updated_category:
            assert updated_category.id == category.id
            assert updated_category.name == "Category 1 Updated"
            assert updated_category.description == "Description 1 Updated"

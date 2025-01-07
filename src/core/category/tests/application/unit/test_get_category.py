from unittest.mock import create_autospec

from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryInput, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestGetCategory:
    def test_return_found_category(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category
        use_case = GetCategory(repository)
        request = GetCategoryInput(id=category.id)
        response = use_case.execute(request)
        assert response == GetCategoryResponse(
            id=category.id,
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )

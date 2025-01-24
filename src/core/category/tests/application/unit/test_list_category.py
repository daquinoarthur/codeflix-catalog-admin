import uuid
from unittest.mock import create_autospec

from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryInput,
    ListCategoryOutput,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestListCategory:
    def test_when_no_categories_in_database_return_empty_list(self):
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = []
        use_case = ListCategory(repository)
        request = ListCategoryInput()
        response = use_case.execute(request)
        assert response == ListCategoryOutput(data=[])

    def test_when_categories_in_database_return_list(self):
        category_filme = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria de filmes",
        )
        category_serie = Category(
            id=uuid.uuid4(),
            name="Série",
            description="Categoria de séries",
        )
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = [category_filme, category_serie]
        use_case = ListCategory(repository)
        request = ListCategoryInput()
        response = use_case.execute(request)
        expected_response = ListCategoryOutput(
            data=[
                CategoryOutput(
                    id=category_filme.id,
                    name=category_filme.name,
                    description=category_filme.description,
                    is_active=category_filme.is_active,
                ),
                CategoryOutput(
                    id=category_serie.id,
                    name=category_serie.name,
                    description=category_serie.description,
                    is_active=category_serie.is_active,
                ),
            ]
        )
        if response:
            assert response == expected_response
            assert len(response.data) == 2

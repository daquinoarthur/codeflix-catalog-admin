import uuid

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryInput, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_get_category_by_id(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        category_series = Category(
            name="Série",
            description="Categoria para séries",
            is_active=True,
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_series]
        )
        use_case = GetCategory(repository)
        request = GetCategoryInput(id=category_filme.id)
        response = use_case.execute(request)
        assert response == GetCategoryResponse(
            id=category_filme.id,
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_filme = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        category_series = Category(
            name="Série",
            description="Categoria para séries",
            is_active=True,
        )
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_series]
        )
        use_case = GetCategory(repository)
        request = GetCategoryInput(id=uuid.uuid4())
        with pytest.raises(
            CategoryNotFoundException, match=f"Category with {request.id} not found."
        ):
            use_case.execute(request)

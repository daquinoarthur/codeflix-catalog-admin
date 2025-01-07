from uuid import UUID

import pytest

from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryInput
from src.core.category.application.use_cases.exceptions import InvalidCategoryDataException
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository)
        request = CreateCategoryInput(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        response = use_case.execute(request)
        assert response is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        persisted_category = repository.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == "Filme"
        assert persisted_category.description == "Categoria para filmes"
        assert persisted_category.is_active

    def test_create_category_with_invalid_data(self):
        with pytest.raises(
            InvalidCategoryDataException, match="'name' cannot be empty"
        ):
            repository = InMemoryCategoryRepository()
            use_case = CreateCategory(repository)
            request = CreateCategoryInput(
                name="",
                description="",
                is_active=True,
            )
            use_case.execute(request)

from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = MagicMock(InMemoryCategoryRepository)
        use_case = CreateCategory(repository)
        request = CreateCategoryRequest(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        category_id = use_case.execute(request)
        assert category_id is not None
        assert isinstance(category_id, UUID)
        assert repository.save.called

    def test_create_category_with_invalid_data(self):
        with pytest.raises(InvalidCategoryData, match="'name' cannot be empty"):
            repository = MagicMock(InMemoryCategoryRepository)
            use_case = CreateCategory(repository)
            request = CreateCategoryRequest(
                name="",
                description="Categoria para filmes",
                is_active=True,
            )
            use_case.execute(request)
            assert repository.save.called

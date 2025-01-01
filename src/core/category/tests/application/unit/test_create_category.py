from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.exceptions import InvalidCategoryData


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository)
        request = CreateCategoryRequest(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        response = use_case.execute(request)
        assert response.id is not None
        assert isinstance(response.id, UUID)
        assert repository.save.called

    def test_create_category_with_invalid_data(self):
        with pytest.raises(InvalidCategoryData, match="'name' cannot be empty"):
            repository = MagicMock(CategoryRepository)
            use_case = CreateCategory(repository)
            request = CreateCategoryRequest(
                name="",
                description="Categoria para filmes",
                is_active=True,
            )
            use_case.execute(request)
            assert repository.save.called

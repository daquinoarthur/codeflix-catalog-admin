import uuid
from unittest.mock import create_autospec
from uuid import UUID

import pytest

from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryInput
from src.core.category.application.use_cases.exceptions import InvalidCategoryDataException
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = create_autospec(CategoryRepository)
        use_case = CreateCategory(repository)
        request = CreateCategoryInput(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        repository.save.return_value = Category(
            id=uuid.uuid4(),
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        response = use_case.execute(request)
        assert response.id is not None
        assert isinstance(response.id, UUID)
        assert repository.save.called

    def test_create_category_with_invalid_data(self):
        with pytest.raises(
            InvalidCategoryDataException, match="'name' cannot be empty"
        ):
            repository = create_autospec(CategoryRepository)
            use_case = CreateCategory(repository)
            request = CreateCategoryInput(
                name="",
                description="Categoria para filmes",
                is_active=True,
            )
            use_case.execute(request)
            assert repository.save.called

import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryInput,
    UpdateCategoryOutput,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            name="Filme",
            description="Categoria de filmes",
            is_active=True,
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category
        use_case = UpdateCategory(repository)
        request = UpdateCategoryInput(
            id=category.id,
            name="Filme updated",
        )
        repository.update.return_value = UpdateCategoryOutput(
            id=category.id,
            name="Filme updated",
            description=category.description,
            is_active=category.is_active,
        )
        response = use_case.execute(request)
        assert response == UpdateCategoryOutput(
            id=category.id,
            name="Filme updated",
            description=category.description,
            is_active=category.is_active,
        )
        repository.update.assert_called_once_with(category)

    def test_udpate_category_description(self):
        category = Category(
            name="Filme",
            description="Categoria de filmes",
            is_active=True,
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category
        use_case = UpdateCategory(repository)
        request = UpdateCategoryInput(
            id=category.id,
            description="Categoria de filmes updated",
        )
        repository.update.return_value = UpdateCategoryOutput(
            id=category.id,
            name=category.name,
            description="Categoria de filmes updated",
            is_active=category.is_active,
        )
        response = use_case.execute(request)
        assert response == UpdateCategoryOutput(
            id=category.id,
            name=category.name,
            description="Categoria de filmes updated",
            is_active=category.is_active,
        )
        repository.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        category = Category(
            name="Filme",
            description="Categoria de filmes",
            is_active=False,
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category
        use_case = UpdateCategory(repository)
        request = UpdateCategoryInput(
            id=category.id,
            is_active=True,
        )
        repository.update.return_value = UpdateCategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=True,
        )
        response = use_case.execute(request)
        assert response == UpdateCategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=True,
        )
        repository.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category(
            name="Filme",
            description="Categoria de filmes",
            is_active=True,
        )
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category
        use_case = UpdateCategory(repository)
        request = UpdateCategoryInput(
            id=category.id,
            is_active=False,
        )
        repository.update.return_value = UpdateCategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=False,
        )
        response = use_case.execute(request)
        assert response == UpdateCategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=False,
        )
        repository.update.assert_called_once_with(category)

    def test_update_category_raise_exception_when_category_not_found(self):
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = None
        use_case = UpdateCategory(repository)
        request = UpdateCategoryInput(
            id=uuid.uuid4(),
            name="Filme updated",
        )
        with pytest.raises(
            CategoryNotFoundException,
            match=f"Can not update category with id: {request.id}. Category not found.",
        ):
            use_case.execute(request)

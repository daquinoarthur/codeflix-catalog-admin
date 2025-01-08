import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryInput,
)
from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(name="Filme")
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category
        use_case = DeleteCategory(repository)
        request = DeleteCategoryInput(id=category.id)
        use_case.execute(request)
        repository.delete.assert_called_once_with(category.id)

    def test_when_category_not_found_then_raise_exception(self):
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = None
        use_case = DeleteCategory(repository)
        id = uuid.uuid4()
        request = DeleteCategoryInput(id=id)
        with pytest.raises(
            CategoryNotFoundException,
            match=f"Can not delete Category with id: {id}. Category not found.",
        ):
            use_case.execute(request)
        repository.delete.assert_not_called()

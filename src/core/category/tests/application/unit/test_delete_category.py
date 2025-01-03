import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(name="Filme")
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = category
        use_case = DeleteCategory(repository)
        request = DeleteCategoryRequest(id=category.id)

        use_case.execute(request)

        repository.delete.assert_called_once_with(category.id)

    def test_when_category_not_found_then_raise_exception(self):
        repository = create_autospec(CategoryRepository)
        repository.get_by_id.return_value = None
        use_case = DeleteCategory(repository)
        id = uuid.uuid4()
        request = DeleteCategoryRequest(id=id)

        with pytest.raises(
            CategoryNotFoundException, match=f"Could not delete Category with id: {id}."
        ):
            use_case.execute(request)

        repository.delete.assert_not_called()

import uuid
import pytest
from unittest.mock import patch

from category import Category


class TestCategory:
    def test_category_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_category_name_must_have_less_than_255_characters(self):
        with pytest.raises(
            ValueError, match="'name' cannot be longer than 255 characters."
        ):
            Category("a" * 256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category("Filme")
        assert category.id is not None
        assert len(str(category.id)) == 36
        assert isinstance(category.id, uuid.UUID)

    def test_created_category_with_default_values(self):
        category = Category("Filme")
        assert category.name == "Filme"
        assert category.description == ""
        assert category.is_active is True

    def test_created_category_is_active_by_default(self):
        category = Category("Filme")
        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            "Filme",
            id=category_id,
            description="Filmes em geral",
            is_active=False,
        )
        assert category.id == category_id
        assert category.name == "Filme"
        assert category.description == "Filmes em geral"
        assert category.is_active is False

    def test_category_str_method(self):
        category = Category("Filme")
        assert (
            str(category)
            == "Category name: Filme - Category description:  - Category is active: Yes"
        )

    def test_category_repr_method(self):
        category = Category("Filme")
        assert repr(category) == f"<Category: Filme - id: {category.id}>"

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="'name' cannot be empty."):
            Category("")


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category("Filme")
        category.update_category(name="Séries", description="Séries em geral")
        assert category.name == "Séries"
        assert category.description == "Séries em geral"

    def test_update_category_with_invalid_name(self):
        category = Category("Filme")
        with pytest.raises(
            ValueError, match="'name' cannot be longer than 255 characters."
        ):
            category.update_category(name="a" * 256, description="Séries em geral")

    def test_cannot_update_category_with_empty_name(self):
        with pytest.raises(ValueError, match="'name' cannot be empty."):
            category = Category("Filme")
            category.update_category(name="", description="Séries em geral")


class TestCategoryValidation:
    def test_private_validate_method_is_working(self):
        with patch("category.Category._validate") as mock_validate:
            mock_validate.side_effect = ValueError(
                "'name' cannot be longer than 255 characters"
            )
            with pytest.raises(
                ValueError, match="'name' cannot be longer than 255 characters"
            ):
                Category("")
                assert mock_validate.called
                assert mock_validate.call_count == 1

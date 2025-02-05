import uuid
from unittest.mock import patch

import pytest

from src.core.category.domain.category import Category


class TestCategoryCreation:
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

    def test_category_description_must_have_less_than_1024_characters(self):
        with pytest.raises(
            ValueError, match="'description' cannot be longer than 1024 characters."
        ):
            Category("Filme", description="a" * 1025)

    def test_category_name_and_description_invalid(self):
        with pytest.raises(
            ValueError,
            match="^'name' cannot be empty., 'description' cannot be longer than 1024 characters.$",
        ):
            Category("", description="a" * 1025)

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
            == "Category name: Filme - Category description:  - Active: Yes"
        )

    def test_category_repr_method(self):
        category = Category("Filme")
        assert repr(category) == f"<Category: Filme - id: {category.id}>"

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="'name' cannot be empty."):
            Category("")


class TestCategoryUpdate:
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

    def test_update_category_with_description_longer_than_1024_characters(self):
        category = Category("Filme")
        with pytest.raises(
            ValueError, match="'description' cannot be longer than 1024 characters."
        ):
            category.update_category(name="Séries", description="a" * 1025)

    def test_update_category_with_name_and_description_invalid(self):
        category = Category("Filme")
        with pytest.raises(
            ValueError,
            match="^'name' cannot be empty., 'description' cannot be longer than 1024 characters.$",
        ):
            category.update_category(name="", description="a" * 1025)

    def test_cannot_update_category_with_empty_name(self):
        with pytest.raises(ValueError, match="'name' cannot be empty."):
            category = Category("Filme")
            category.update_category(name="", description="Séries em geral")


class TestCategoryValidation:
    def test_private_validate_method_is_working(self):
        with patch(
            "src.core.category.domain.category.Category._validate"
        ) as mock_validate:
            mock_validate.side_effect = ValueError(
                "'name' cannot be longer than 255 characters"
            )
            with pytest.raises(
                ValueError, match="'name' cannot be longer than 255 characters"
            ):
                Category("")
                assert mock_validate.called
                assert mock_validate.call_count == 1


class TestCategoryActivation:
    def test_activate_inactive_category(self):
        category = Category("Filme", is_active=False)
        category.is_active = False
        category.activate()
        assert category.is_active is True

    def test_activate_active_category(self):
        """
        This is a test to show that the 'activate' method is working
        when the category is already active. The method should not
        raise any exceptions and the 'is_active' attribute should
        remain True. This is called a "happy path" test or a "success"
        test case.

        - 'is_active' is True by default when not passing the argument
        to the 'Category' constructor
        """
        category = Category("Filme")
        category.activate()
        assert category.is_active is True

    def test_deactivate_active_category(self):
        category = Category("File")
        category.deactivate()
        assert category.is_active is False

    def test_deactivate_inactive_category(self):
        """
        This is a test to show that the 'deactivate' method is working
        when the category is already inactive. The method should not
        raise any exceptions and the 'is_active' attribute should
        remain False. This is called a "happy path" test or a "success"
        test case.
        """
        category = Category("Filme", is_active=False)
        category.deactivate()
        assert category.is_active is False


class TestEquality:
    def test_when_categories_have_the_same_id_they_are_considered_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category("Filme", id=common_id)
        category_2 = Category("Séries", id=common_id)
        assert category_1 == category_2

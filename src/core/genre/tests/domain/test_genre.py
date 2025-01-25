import uuid

import pytest

from src.core.genre.domain.genre import Genre


class TestGenreCreation:
    def test_genre_name_cannot_be_empty(self):
        with pytest.raises(ValueError, match="Name cannot be empty."):
            Genre(name="")

    def test_genre_name_is_required(self):
        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument: 'name'",
        ):
            Genre()

    def test_genre_name_must_have_less_than_255_characters(self):
        with pytest.raises(
            ValueError, match="Name cannot be longer than 255 characters."
        ):
            Genre(name="a" * 256)

    def test_genre_is_created_with_default_values(self):
        genre = Genre(name="Action")
        assert genre.name == "Action"
        assert isinstance(genre.id, uuid.UUID)
        assert genre.is_active == True
        assert genre.categories == set()

    def test_genre_is_created_with_provided_values(self):
        genre_id = uuid.uuid4()
        categories_ids = {uuid.uuid4(), uuid.uuid4()}
        genre = Genre(
            id=genre_id,
            name="Action",
            is_active=False,
            categories=categories_ids,
        )
        assert genre.id == genre_id
        assert genre.name == "Action"
        assert isinstance(genre.id, uuid.UUID)
        assert genre.is_active == False
        assert genre.categories == categories_ids

    def test_genre_is_activated(self):
        genre = Genre(name="Action", is_active=False)
        genre.activate()
        assert genre.is_active == True

    def test_genre_is_deactivated(self):
        genre = Genre(name="Action")
        genre.deactivate()
        assert genre.is_active == False

    def test_genre_is_activated_even_if_it_is_already_active(self):
        genre = Genre(name="Action")
        genre.activate()
        assert genre.is_active == True

    def test_genre_is_deactivated_even_if_it_is_already_inactive(self):
        genre = Genre(name="Action", is_active=False)
        genre.deactivate()
        assert genre.is_active == False

    def test_genre_str_representation(self):
        genre = Genre(name="Action")
        assert str(genre) == "Genre: Action - Is Active: Yes - id: " + str(genre.id)

    def test_genre_repr_representation(self):
        genre = Genre(name="Action")
        assert repr(genre) == f"<Genre: Action - id: {genre.id}>"

    def test_genre_equality(self):
        common_id = uuid.uuid4()
        genre1 = Genre(id=common_id, name="Action")
        genre2 = Genre(id=common_id, name="Action")
        assert genre1 == genre2

    def teste_genre_updated_name(self):
        genre = Genre(name="Action")
        genre.change_name("Adventure")
        assert genre.name == "Adventure"

    def test_genre_change_name_with_empty_name(self):
        genre = Genre(name="Action")
        with pytest.raises(ValueError, match="Name cannot be empty."):
            genre.change_name("")

    def test_genre_change_name_with_name_longer_than_255_characters(self):
        genre = Genre(name="Action")
        with pytest.raises(
            ValueError, match="Name cannot be longer than 255 characters."
        ):
            genre.change_name("a" * 256)

    def test_genre_add_category(self):
        genre = Genre(name="Action")
        category_id = uuid.uuid4()
        assert category_id not in genre.categories
        genre.add_category(category_id)
        assert category_id in genre.categories

    def test_genre_remove_category(self):
        genre = Genre(name="Action")
        category_id = uuid.uuid4()
        assert category_id not in genre.categories
        genre.add_category(category_id)
        assert category_id in genre.categories
        genre.remove_category(category_id)
        assert category_id not in genre.categories

    def test_genre_add_multiple_categories(self):
        genre = Genre(name="Action")
        category_1 = uuid.uuid4()
        category_2 = uuid.uuid4()
        genre.add_category(category_1)
        genre.add_category(category_2)
        assert genre.categories == {category_1, category_2}

import pytest

from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category


class TestSaveCategory:
    @pytest.mark.django_db
    def test_save_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie description",
        )
        repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        assert CategoryModel.objects.count() == 0
        response = repository.save(category)
        assert CategoryModel.objects.count() == 1
        assert response == category
        assert response.id == category.id
        assert response.name == category.name
        assert response.description == category.description
        assert response.is_active == category.is_active

    @pytest.mark.django_db
    def test_list_categories_from_database(self):
        category_filme = CategoryModel.objects.create(
            name="Filme",
            description="Filme description",
        )
        category_serie = CategoryModel.objects.create(
            name="Serie",
            description="Serie description",
        )
        repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        categories = repository.list()
        assert len(categories) == 2
        category_filme_from_db = categories[0]
        assert category_filme_from_db.id == category_filme.id
        assert category_filme_from_db.name == category_filme.name
        assert category_filme_from_db.description == category_filme.description
        assert category_filme_from_db.is_active == category_filme.is_active
        category_serie_from_db = categories[1]
        assert category_serie_from_db.id == category_serie.id
        assert category_serie_from_db.name == category_serie.name
        assert category_serie_from_db.description == category_serie.description
        assert category_serie_from_db.is_active == category_serie.is_active

    @pytest.mark.django_db
    def test_get_category_by_id_from_database(self):
        category_filme = CategoryModel.objects.create(
            name="Filme",
            description="Filme description",
        )
        repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        category = repository.get_by_id(category_filme.id)
        if category:
            assert category.id == category_filme.id
            assert category.name == category_filme.name
            assert category.description == category_filme.description
            assert category.is_active == category_filme.is_active

    @pytest.mark.django_db
    def test_update_category_in_database(self):
        category_filme = CategoryModel.objects.create(
            name="Filme",
            description="Filme description",
        )
        repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        category = Category(
            id=category_filme.id,
            name="Filme updated",
            description="Filme description updated",
        )
        response = repository.update(category)
        assert response.id == category.id
        assert response.name == category.name
        assert response.description == category.description
        assert response.is_active == category.is_active

    @pytest.mark.django_db
    def test_delete_category_in_database(self):
        category_filme = CategoryModel.objects.create(
            name="Filme",
            description="Filme description",
        )
        repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        assert CategoryModel.objects.count() == 1
        repository.delete(category_filme.id)
        assert CategoryModel.objects.count() == 0

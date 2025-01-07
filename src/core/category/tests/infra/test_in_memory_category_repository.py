from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestSaveCategory:
    def test_can_save_category(self):
        category = Category(name="test")
        repository = InMemoryCategoryRepository()
        repository.save(category)
        assert len(repository.categories) == 1
        assert repository.categories[0] == category


class TestGetCategoryById:
    def test_can_get_category_by_id(self):
        category_filme = Category(name="Filme")
        category_serie = Category(name="Serie")
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        category = repository.get_by_id(category_filme.id)
        if category:
            assert category == category_filme
            assert category.name == "Filme"
            assert category.id == category_filme.id
            assert category.description == ""
            assert category.is_active == True


class TestDeleteCategory:
    def test_delete_existing_category(self):
        category_filme = Category(name="Filme")
        category_serie = Category(name="Serie")
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        category = repository.get_by_id(category_filme.id)
        assert category is not None
        assert len(repository.categories) == 2
        repository.delete(category_filme.id)
        assert repository.get_by_id(category_filme.id) is None
        assert len(repository.categories) == 1

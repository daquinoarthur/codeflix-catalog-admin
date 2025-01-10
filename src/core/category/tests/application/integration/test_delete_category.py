from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryInput,
    DeleteCategoryOutput,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category_filme = Category(name="Filme")
        category_series = Category(name="Séries")
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_series]
        )
        use_case = DeleteCategory(repository)
        request = DeleteCategoryInput(id=category_filme.id)
        assert len(repository.categories) == 2
        assert repository.get_by_id(category_filme.id) is not None
        response = use_case.execute(request)
        assert repository.get_by_id(category_filme.id) is None
        assert len(repository.categories) == 1
        assert response == DeleteCategoryOutput(detail="Category deleted successfully.")

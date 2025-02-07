from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    def test_return_empty_list(self):
        repository = InMemoryCategoryRepository()
        use_case = ListCategory(repository)
        request = ListCategory.Input()
        response = use_case.execute(request)
        if response:
            assert response == ListCategory.Output(data=[])

    def test_return_existing_categories(self):
        category_filme = Category(
            name="Filme",
            description="Categoria de filmes",
        )
        category_serie = Category(
            name="Série",
            description="Categoria de séries",
        )
        repository = InMemoryCategoryRepository()
        repository.save(category_filme)
        repository.save(category_serie)
        use_case = ListCategory(repository)
        request = ListCategory.Input()
        response = use_case.execute(request)
        if response:
            assert response == ListCategory.Output(
                data=[
                    CategoryOutput(
                        id=category_filme.id,
                        name=category_filme.name,
                        description=category_filme.description,
                        is_active=category_filme.is_active,
                    ),
                    CategoryOutput(
                        id=category_serie.id,
                        name=category_serie.name,
                        description=category_serie.description,
                        is_active=category_serie.is_active,
                    ),
                ]
            )

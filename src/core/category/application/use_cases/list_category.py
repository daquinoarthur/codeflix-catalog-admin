from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class Meta:
    current_page: int
    page_size: int
    total_items: int
    total_pages: int


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    @dataclass
    class Input:
        order_by: str = "name"
        current_page: int = 1
        page_size: int = 2

    @dataclass
    class Output:
        data: list[CategoryOutput]
        meta: Meta = field(default_factory=Meta)

    def execute(self, request: Input) -> Output:
        categories = self.repository.list()
        sorted_categories = sorted(
            [
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ],
            key=lambda category: getattr(category, request.order_by),
        )
        page_offset = (request.current_page - 1) * request.page_size
        categories_page = sorted_categories[
            page_offset : page_offset + request.page_size
        ]
        total_pages = (
            len(sorted_categories) // request.page_size
            if self._is_list_length_even(sorted_categories)
            else (len(sorted_categories) // request.page_size) + 1
        )
        return ListCategory.Output(
            data=categories_page,
            meta=Meta(
                current_page=request.current_page,
                page_size=request.page_size,
                total_items=len(sorted_categories),
                total_pages=total_pages,
            ),
        )

    def _is_list_length_even(self, list: list) -> bool:
        return len(list) % 2 == 0

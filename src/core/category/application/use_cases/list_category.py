from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    @dataclass
    class Input:
        order_by: str = "name"

    @dataclass
    class Output:
        data: list[CategoryOutput]

    def execute(self, request: Input) -> Output:
        categories = self.repository.list()
        return ListCategory.Output(
            data=sorted(
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
        )

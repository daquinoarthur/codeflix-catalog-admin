from uuid import UUID

from src.core.category.application.exceptions import InvalidCategoryData
from src.core.category.domain.category import Category


def create_category(
    repository,
    name: str,
    description: str = "",
    is_active: bool = True,
) -> UUID:
    try:
        category = Category(
            name=name,
            description=description,
            is_active=is_active,
        )
    except ValueError as error:
        raise InvalidCategoryData(str(error))
    repository.save(category)
    return category.id

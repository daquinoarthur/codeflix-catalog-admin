import uuid
from dataclasses import dataclass, field


@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self._validate()

    def __str__(self):
        is_active = "Yes" if self.is_active else "No"
        return (
            f"Category name: {self.name}"
            f" - Category description: {self.description}"
            f" - Category is active: {is_active}"
        )

    def __repr__(self):
        return f"<Category: {self.name} - id: {self.id}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def update_category(self, name, description):
        self.name = name
        self.description = description
        self._validate()

    def _validate(self):
        if len(self.name) > 255:
            raise ValueError("'name' cannot be longer than 255 characters.")
        if not self.name:
            raise ValueError("'name' cannot be empty.")

    def activate(self):
        self.is_active = True
        self._validate()

    def deactivate(self):
        self.is_active = False
        self._validate()

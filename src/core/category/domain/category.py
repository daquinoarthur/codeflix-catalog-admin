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
        return f"Category name: {self.name} - Category description: {self.description} - Active: {'Yes' if self.is_active else 'No'}"

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
        self._validate_name()

    def _validate_name(self):
        if not self.name:
            raise ValueError("'name' cannot be empty.")
        if len(self.name) > 255:
            raise ValueError("'name' cannot be longer than 255 characters.")

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

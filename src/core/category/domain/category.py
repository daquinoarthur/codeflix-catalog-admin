import uuid
from dataclasses import dataclass, field

from src.core.category.domain.notification import Notification


@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    notification: Notification = field(default_factory=Notification)

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
        self._validate_description()
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def _validate_name(self):
        if not self.name:
            self.notification.add_error("'name' cannot be empty.")
        if len(self.name) > 255:
            self.notification.add_error("'name' cannot be longer than 255 characters.")

    def _validate_description(self):
        if len(self.description) > 1024:
            self.notification.add_error(
                "'description' cannot be longer than 1024 characters."
            )

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

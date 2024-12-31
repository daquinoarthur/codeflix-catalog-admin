import unittest
import uuid

from category import Category


class TestCategory(unittest.TestCase):
    def test_category_name_is_required(self):
        with self.assertRaisesRegex(
            TypeError, "missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_category_name_must_have_less_than_255_characters(self):
        with self.assertRaisesRegex(
            ValueError, "name must have less than 256 characters"
        ):
            Category("a" * 256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category("Filme")
        self.assertIsNotNone(category.id)
        self.assertEqual(len(str(category.id)), 36)
        self.assertEqual(type(category.id), uuid.UUID)

    def test_created_category_with_default_values(self):
        category = Category("Filme")
        self.assertEqual(category.name, "Filme")
        self.assertEqual(category.description, "")
        self.assertTrue(category.is_active)

    def test_created_category_is_active_by_default(self):
        category = Category("Filme")
        self.assertTrue(category.is_active)

    def test_category_is_created_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            "Filme",
            id=category_id,
            description="Filmes em geral",
            is_active=False,
        )
        self.assertEqual(category.id, category_id)
        self.assertEqual(category.name, "Filme")
        self.assertEqual(category.description, "Filmes em geral")
        self.assertFalse(category.is_active)

    def test_category_str_method(self):
        category = Category("Filme")
        self.assertEqual(
            str(category),
            "Category name: Filme - Category description:  - Category is active: Yes",
        )

    def test_category_repr_method(self):
        category = Category("Filme")
        self.assertEqual(
            repr(category),
            f"<Category: Filme - id: {category.id}>",
        )


if __name__ == "__main__":
    unittest.main()

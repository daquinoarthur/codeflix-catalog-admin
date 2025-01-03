from rest_framework.test import APITestCase
from rest_framework.views import status


# Create your tests here.
class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"
        response = self.client.get(url)
        expected_data = [
            {
                "id": "6b955d67-11a1-4240-8340-c61b9b040bdc",
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
            },
            {
                "id": "8b955d67-11a1-4240-8340-c61b9b040bdc",
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

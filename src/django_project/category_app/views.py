from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import status

from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryInput,
)
from src.django_project.category_app.repository import DjangoORMCategoryRepository


# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryInput()
        repository = DjangoORMCategoryRepository()
        use_case = ListCategory(repository)

        output = use_case.execute(input)
        categories = output.data

        return Response(
            status=status.HTTP_200_OK,
            data=[
                {
                    "id": str(category.id),
                    "name": category.name,
                    "description": category.description,
                    "is_active": category.is_active,
                }
                for category in categories
            ],
        )

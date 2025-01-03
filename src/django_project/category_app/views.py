from django.forms.fields import uuid
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response


# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        return Response(
            data=[
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
        )

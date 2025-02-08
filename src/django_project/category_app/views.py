from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import status

from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryInput,
)
from src.core.category.application.use_cases.exceptions import CategoryNotFoundException
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryInput,
)
from src.core.category.application.use_cases.list_category import (
    ListCategory,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryInput,
)
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryInput,
)
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    ListCategoryResponseSerializer,
    PartialUpdateCategoryRequestSerializer,
    PartialUpdateCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
    UpdateCategoryResponseSerializer,
)


# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        current_page = request.query_params.get("current_page", 1)
        input = ListCategory.Input(order_by=order_by, current_page=current_page)
        repository = DjangoORMCategoryRepository()
        use_case = ListCategory(repository)
        output = use_case.execute(input)
        serializer = ListCategoryResponseSerializer(instance=output)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data,
        )

    def retrieve(self, request: Request, pk=None) -> Response:
        request_serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        request_serializer.is_valid(raise_exception=True)
        repository = DjangoORMCategoryRepository()
        use_case = GetCategory(repository)
        input = GetCategoryInput(id=request_serializer.validated_data["id"])

        try:
            output = use_case.execute(input)
            category_serializer = RetrieveCategoryResponseSerializer(instance=output)
            return Response(category_serializer.data, status=status.HTTP_200_OK)
        except CategoryNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request) -> Response:
        request_serializer = CreateCategoryRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        repository = DjangoORMCategoryRepository()
        use_case = CreateCategory(repository)
        input = CreateCategoryInput(
            **request_serializer.validated_data,
        )
        try:
            output = use_case.execute(input)
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response_serializer = CreateCategoryResponseSerializer(instance=output)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk=None) -> Response:
        request_payload_serializer = UpdateCategoryRequestSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        request_payload_serializer.is_valid(raise_exception=True)
        repository = DjangoORMCategoryRepository()
        use_case = UpdateCategory(repository)
        input = UpdateCategoryInput(**request_payload_serializer.validated_data)
        try:
            output = use_case.execute(input)
        except CategoryNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            status=status.HTTP_200_OK,
            data=UpdateCategoryResponseSerializer(output).data,
        )

    def partial_update(self, request: Request, pk=None) -> Response:
        serializer = PartialUpdateCategoryRequestSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)
        repository = DjangoORMCategoryRepository()
        use_case = UpdateCategory(repository)
        input = UpdateCategoryInput(**serializer.validated_data)
        try:
            output = use_case.execute(input)
        except CategoryNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            PartialUpdateCategoryResponseSerializer(output).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request: Request, pk=None) -> Response:
        request_serializer = DeleteCategoryRequestSerializer(data={"id": pk})
        request_serializer.is_valid(raise_exception=True)
        repository = DjangoORMCategoryRepository()
        use_case = DeleteCategory(repository)
        input = DeleteCategoryInput(id=request_serializer.validated_data["id"])
        try:
            output = use_case.execute(input)
        except CategoryNotFoundException as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"detail": output.detail},
            status=status.HTTP_200_OK,
        )

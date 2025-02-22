from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.admin.utils import generate_password
from apps.admin.serializers import GeneratePasswordSerializer
from apps.blog.models import Category
from apps.core.permissions import IsSuperuserStaffAdmin


@extend_schema_view(
    post=extend_schema(
        summary="Создание пароля через генератор паролей",
        tags=["Админка"],
        operation_id="generate password",
        request=GeneratePasswordSerializer,
    )
)
class GeneratePasswordView(APIView):
    serializer_class = GeneratePasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            length_password = serializer.validated_data["length_password"]
            password = generate_password(length_password=length_password)
            return Response(
                data={"status": "success", "new_password": password}, status=status.HTTP_200_OK
            )

        return Response(
            data={"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CategoryDeleteView(APIView):
    permission_classes = [IsSuperuserStaffAdmin]

    def delete(self, request, category_id, *args, **kwargs):
        instance = Category.objects.filter(pk=category_id).first()
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

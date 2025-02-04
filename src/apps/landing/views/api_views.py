from rest_framework import generics, viewsets, status, mixins
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiTypes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from landing.models import *
from landing.serializers.serializers import *
from .schemas import MAIN_INF_SCHEMAS, ABOUT_ME_SCHEMAS, CONTENT_SCHEMAS

from apps.core.permissions import IsSuperuserStaffAdmin

class ReadAnyOtherOnlyStaffMixin:
    """Просмотр (GET) всем пользователям, остальные запросы только для SuperuserStaffAdmin"""
    def get_permissions(self):
        """Переопределяем get_permissions, чтобы использовать разные права доступа для POST и GET"""
        permissions = [AllowAny] if self.request.method == "GET" else [IsSuperuserStaffAdmin]
        self.permission_classes = permissions
        return super().get_permissions()

@extend_schema_view(**MAIN_INF_SCHEMAS)
class MainInfAPIViews(ReadAnyOtherOnlyStaffMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    queryset = MainInf.objects.all().order_by('pk')[:1]
    serializer_class = MainInfSerializer

    def list(self, request, *args, **kwargs):
        """Возвращаем первую запись."""
        instance = self.queryset.first()
        if instance is None:
            return Response({"error": "No record found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Обновляем или создаем первую запись."""
        instance = self.queryset.first()
        if instance is None:
            # Если записи нет, создаем новую
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Если запись существует, обновляем её
            serializer = self.get_serializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Частично обновляем первую запись."""
        instance = self.queryset.first()
        if instance is None:
            return Response({"error": "No record to partially update."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Метод не реализован, т.к. работа по API предполагается с одним экземпляром класса модели
    # def destroy(self, request, *args, **kwargs):
    #     """Удаляем первую запись."""
    #     instance = self.queryset.first()
    #     if instance is None:
    #         return Response({"error": "No record to delete."}, status=status.HTTP_404_NOT_FOUND)
    #
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(**ABOUT_ME_SCHEMAS)
class AboutMeViewSet(ReadAnyOtherOnlyStaffMixin, viewsets.ModelViewSet):
    queryset = AboutMe.objects.all()
    serializer_class = AboutMeSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

@extend_schema_view(**CONTENT_SCHEMAS)
class ContentViewSet(ReadAnyOtherOnlyStaffMixin, viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer



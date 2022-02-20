from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from api.serializers import CategorySerializer
from reviews.models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    # permission_classes = (OwnerOrAuth,) не забыть дописать класс для сравнения роли пользователя
    # со значением "админ" вариант на уровне объекта  request.user.role ==“admin”
    
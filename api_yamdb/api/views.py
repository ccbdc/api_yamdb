from rest_framework import viewsets
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from api.serializers import CategorySerializer, GenreSerializer, TitleSerializer
from reviews.models import Category, Genre, Title
from api.permissions import AdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,) # не забыть дописать класс для сравнения роли пользователя
    # со значением "админ" вариант на уровне объекта  request.user.role ==“admin”


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,) # не забыть дописать класс для сравнения роли пользователя
    # со значением "админ" вариант на уровне объекта  request.user.role ==“admin”

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    search_fields = ('category__slug', 'genre__slug', 'name', 'year')
    permission_classes = (AdminOrReadOnly,)
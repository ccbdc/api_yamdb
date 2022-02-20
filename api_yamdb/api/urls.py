from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, GenreViewSet

app_name = 'api'

router = DefaultRouter()

router.register('v1/categories', CategoryViewSet, basename='categories')
router.register('v1/genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
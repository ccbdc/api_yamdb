from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views
from .views import UserViewSet, SignupView, TokenView


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    'users',
    UserViewSet,
    basename='users')
router_v1.register(
    'categories',
    views.CategoryViewSet,
    basename='categories')
router_v1.register(
    'genres',
    views.GenreViewSet,
    basename='genres')
router_v1.register(
    'titles',
    views.TitleViewSet,
    basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment')


auth_urls = [
    path('signup/', SignupView.as_view()),
    path('token/', TokenView.as_view())
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls)),
]

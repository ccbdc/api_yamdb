from rest_framework.routers import DefaultRouter
from api import views
from django.urls import path, include

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('titles', views.TitleViewSet, basename='Title')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

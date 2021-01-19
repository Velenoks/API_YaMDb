from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'api'

router = DefaultRouter()
router.register(r'categories',
                views.CategoryViewSet,
                basename=app_name)
router.register(r'genres',
                views.GenreViewSet,
                basename=app_name)
router.register(r'titles',
                views.TitleViewSet,
                basename=app_name)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet,
                basename=app_name)
router.register(r'titles/(?P<title_id>\d+)/'
                r'reviews/(?P<review_id>\d+)/comments',
                views.CommentViewSet,
                basename=app_name)

urlpatterns = [
    path('v1/', include(router.urls)),
]

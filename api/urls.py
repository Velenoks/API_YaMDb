from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

app_name = 'api'

router = DefaultRouter()
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
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/', include(router.urls)),
]

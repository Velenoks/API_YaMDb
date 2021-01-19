from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, auth, get_token


router = DefaultRouter()

urlpatterns = [
    path('v1/auth/email/', csrf_exempt(auth)),
    path('v1/auth/token/', get_token, name='token_obtain_pair'),
    path(
        'v1/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
router.register(
    r'users',
    UserViewSet,
    basename='users'
)
urlpatterns += [
    path('v1/', include(router.urls)),
]

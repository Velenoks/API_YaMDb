from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='title-api')),
    path('api/', include(('users.urls', 'users'), namespace='users-auth-api')),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html'),
         name='redoc'
         ),
    ]

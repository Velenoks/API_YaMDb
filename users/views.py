from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import viewsets, filters, mixins, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import (
    AdminOnlyPermission, AdminOrModeratorOrAuthorPermission
)
from .serializers import UserSerializer


class AuthPost(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = email[0:email.find('@')]
            serializer.save(username=username)
            user = User.objects.get(email=email)
            confirmation_code = urlsafe_base64_encode(force_bytes(user.username))
            send_mail(
                subject='Confirmation Code',
                message=f'Код подтверждения для получения токена: {confirmation_code}',
                from_email='api@yandex.ru',
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import viewsets, filters, mixins, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import (
    AdminOnlyPermission, AdminOrModeratorOrAuthorPermission
)
from .serializers import UserSerializerForAdmin, UserSerializer


USER_DOES_NOT_EXIST = 'Ошибка при отправке запроса: такого пользователя нет в базе данных'


@api_view(['POST'])
@permission_classes([AllowAny])
def auth(request):
    email = request.data['email']
    username = email[0:email.find('@')]
    serializer = UserSerializerForAdmin(
        data={
            'email': email,
            'username': username
        }
    )
    if serializer.is_valid():
        confirmation_code = urlsafe_base64_encode(force_bytes(username))
        serializer.save(
            username=username,
            confirmation_code=confirmation_code
        )
        send_mail(
            subject='Confirmation Code',
            message=f'Код подтверждения для получения токена: {confirmation_code}',
            from_email='api@yandex.ru',
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    email = request.data['email']
    confirmation_code = request.data['confirmation_code']
    if User.objects.filter(
            email=email,
            confirmation_code=confirmation_code
    ).exists():
        user = User.objects.get(
            confirmation_code=confirmation_code,
            email=email
        )
        tokens = RefreshToken.for_user(user)
        data = {
            "refresh": str(tokens),
            "access": str(tokens.access_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(USER_DOES_NOT_EXIST, status.HTTP_400_BAD_REQUEST)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    queryset = User.objects.all()
    serializer_class = UserSerializerForAdmin
    permission_classes = (AdminOnlyPermission,)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializerForAdmin(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = urlsafe_base64_encode(force_bytes(username))
            serializer.save(confirmation_code=confirmation_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['pk'])
        return user

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[AdminOrModeratorOrAuthorPermission]
    )
    def me(self, request):
        self.kwargs['pk'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            instance = self.get_object()
            serializer = UserSerializer(
                instance,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            raise Exception('Not implemented')

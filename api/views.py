from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import (Review, Comment, Title,
                     Genre, Category)
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    TitleSerializer)
from .permission import IsAuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(review=review_id)

    def perform_create(self, serializer, *args, **kwargs):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # тут, по идее, не должно быть ограничений вообще. или только Администратор на создание, патч и удаление

    def perform_create(self, serializer):
        if self.request.user.role == 'admin':  # не уверен, правильно ли я здесь ссылаюсь на роль
            serializer.save()
    #     а если нет - то что ???

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .models import (Review, Comment, Title,
                     Genre, Category)
from .serializers import (ReviewSerializer, CommentSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleSerializer)
from .permission import IsAdmin, IsModerOrAuthorOrReadOnly


class MixListCreateDestroy(mixins.ListModelMixin, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


class CategoryViewSet(MixListCreateDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(MixListCreateDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsModerOrAuthorOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer, *args, **kwargs):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        if not Review.objects.filter(author=self.request.user,
                                     title=title).exists():
            serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsModerOrAuthorOrReadOnly)

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
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']


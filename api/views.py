from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import (Review, Comment, Titles,
                     Genre, Category)
from .serializers import (
    ReviewSerializer, CommentSerializer)
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


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # тут, по идее, не должно быть ограничений вообще. или только Администратор на создание, патч и удаление

    def perform_create(self, serializer):
        serializer.save()
    #     пока не пойму - тут делать проверку на права администратора. или в сериализаторе?
    # и вообще - эта операция справляется со всей троицей put/patch/delete?

    def get_titles(self):
        titles = Titles.objects.all().filter('pub_date')
        if request.method == 'GET':
            serializer = TitlesSerializer(Titles)
            if serializer.is_valid():
                serializer = TitlesSerializer(Titles, titles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_titles(self, id):
        titles = Titles.objects.get(pk=id)
        if request.method == 'GET':
            serializer = TitlesSerializer(Titles)
            if serializer.is_valid():
                serializer = TitlesSerializer(Titles, titles)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
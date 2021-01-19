from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Category, Comment, Genre, Review, Title
from .permission import IsAdmin, IsModerOrAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, TitleSerializerWrite)


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
        if not title.reviews.filter(author=self.request.user,
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
    # serializer_class = TitleSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['year']

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return TitleSerializerWrite
        return TitleSerializer

    def get_queryset(self):
        print(self.action)
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return Title.objects.all()
        queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
        genre = self.request.query_params.get('genre', None)
        category = self.request.query_params.get('category', None)
        name = self.request.query_params.get('name', None)
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        elif category is not None:
            queryset = queryset.filter(category__slug=category)
        elif name is not None:
            queryset = queryset.filter(name__contains=name)
        return queryset

    def create(self, request, *args, **kwargs):
        # response = super(TitleViewSet, self).create(request, args, kwargs)
        # print(response)
        data = self.request.data
        name = data['name']
        print(data)
        category_slug = data['category']
        category = get_object_or_404(Category, slug=category_slug)
        print(category)
        # genres = self.request.POST.getlist('genre')
        genres = data['genre']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        newdata = serializer.validated_data
        # serializer.save(category=category)
        obj = Title(
            name=newdata['name'],
            category=category,
            description=newdata["description"],
            year=newdata['year'])
        obj.save()
        for g in genres:
            genre = get_object_or_404(Genre, slug=g)
            print(genre)
            obj.genre.add(genre)
        print('tofind')
        print(obj)
        rating = 1
        read_serializer = TitleSerializer(obj, rating=rating)
        print('out')
        print(read_serializer.data)
        return Response(read_serializer.data)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # def perform_create(self, serializer):
    #     data = self.request.data
    #     name = data['name']
    #     category_slug = data['category']
    #     category = get_object_or_404(Category, slug=category_slug)
    #     # genres = self.request.POST.getlist('genre')
    #     genres = self.request.data['genre']
    #     serializer.save(category=category, rating=rating)
    #     obj = Title.objects.get(name=name)
    #     for g in genres:
    #         genre = get_object_or_404(Genre, slug=g)
    #         obj.genre.add(genre)
    #
    # def perform_update(self, serializer):
    #     category_slug = self.request.data['category']
    #     category = get_object_or_404(Category, slug=category_slug)
    #     serializer.save(category=category,)

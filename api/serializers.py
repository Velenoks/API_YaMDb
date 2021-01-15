from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg

from .models import Review, Comment, Titles


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author']
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', )
        model = Comment


class TitlesSerializer(serializers.ModelSerializer):
    rating = Review.objects.aggregate(Avg('score'))
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug'
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Titles

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg

from .models import Review, Comment, Title


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


class TitleSerializer(serializers.ModelSerializer):
    # rating = Review.objects.filter(title=id).aggregate(Avg('score'))
    # как вариант. но не уверен, что он воспримет id, как поле id из этого сериализатора
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug'
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title

    def get_rating(self):
        return Review.objects.filter(title=self.id).aggregate(Avg('score'))
    # в таком способе можно использовать self, так что он должен работать.
    # надо только удостовериться, с каким названием поля сравниваем
    # в смысле - содержит ли поле title именно id

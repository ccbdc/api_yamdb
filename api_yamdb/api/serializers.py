from datetime import datetime
from django.db.models import Avg
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (
    CurrentUserDefault,
    SerializerMethodField,
    ModelSerializer,
    ValidationError)
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import MyUser
from .models import Category, Genre, Title

from reviews.models import Comment, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'role',
            'email',
            'first_name',
            'last_name',
            'bio',
        )
        model = MyUser


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=(UniqueValidator(queryset=MyUser.objects.all()),)
    )
    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=MyUser.objects.all()),)
    )

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
        )

    def validate_username(self, data):
        if data == 'me':
            raise ValidationError(message='Username не может быть me!')
        return data


class GenTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=100)

    class Meta:
        model = MyUser
        fields = (
            'username',
            'confirmation_code',
        )


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        read_only_fields = ('id', 'rating')
        model = Title

    def validate_year(self, year):
        if year > datetime.now().year:
            raise ValidationError(
                'Нельзя добавить это произведение.')
        return year

    def get_rating(self, obj):
        return obj.reviews.aggregate(average=Avg('score'))['average']


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('id', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = (self.context['request'].path).split('/')[4]
        author = self.context['request'].user
        if Review.objects.values(
            'author', 'title').filter(
                author=author, title__id=title_id).exists():
            raise ValidationError('Отзыв уже был написан.')
        return data


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
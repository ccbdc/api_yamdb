from api_yamdb.reviews.models import Category
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        # read_only_fields = ('id', 'name', 'slug',)
    
    def validate(self, data):
        # Нужно сделать запрос в Бд попробовть поискать слаг из пост запроса
        new_slug = data['slug']
        query = Category.objects.filter(slug=new_slug)
        if new_slug in query:
            raise serializers.ValidationError(
                'Такой slug уже существует'
            )
        # А может и такой вариант сработать, нужно тестить в шелле...
        # slug = self.context['request'].slug
        # if new_slug == slug:
        #     raise serializers.ValidationError(
        #         'Такой slug уже существует'
        #     )
        return data


class  GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        # read_only_fields = ('id',)
    def validate(self, data):
    # Нужно сделать запрос в Бд попробовть поискать слаг из пост запроса
        new_slug = data['slug']
        query = Genre.objects.filter(slug=new_slug)
        if new_slug in query:
            raise serializers.ValidationError(
                'Такой slug уже существует'
            )
        # А может и такой вариант сработать, нужно тестить в шелле...
        # slug = self.context['request'].slug
        # if new_slug == slug:
        #     raise serializers.ValidationError(
        #         'Такой slug уже существует'
        #     )
        return data

class  TitleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

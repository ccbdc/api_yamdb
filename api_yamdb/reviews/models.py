from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    username = models.CharField(max_length=150, blank=True,
                                null=True, unique=True)
    email = models.EmailField(max_length=254, unique=True, blank=True)
    first_name = models.TextField(max_length=150, null=True)
    last_name = models.TextField(max_length=150, null=True)
    bio = models.TextField(null=True)
    role = models.CharField(choices=ROLES, default='user', max_length=50)

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return f'{self.username}'


class Category(models.Model):
    name = models.CharField(max_length=256, blank=True)
    slug = models.SlugField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(blank=True, max_length=50)
    slug = models.SlugField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.CharField(blank=False, max_length=50)
    year = models.DateField(blank=False)
    description = models.TextField(blank=True)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='title'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='title'
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return f'{self.name}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        blank=True,
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        blank=True,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField()
    score = models.PositiveIntegerField(blank=False,
                                        validators=[
                                            MinValueValidator(1),
                                            MaxValueValidator(10)])
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True, db_index=True,)

    class Meta:
        verbose_name = 'Отзыв'

    def __str__(self):
        return f'{self.text}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Ревью',
        blank=True,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        blank=True,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True, db_index=True,)

    class Meta:
        verbose_name = 'Комментарий'

    def __str__(self):
        return f'{self.text}'

from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, TextField


class MyUser(AbstractUser):
    """
    The user model with choose role.
    """
    USER = 'user'
    MODERATOR = 'moderator'
    ANONYMOUS = 'anonymous'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
        (ANONYMOUS, 'Аноним'),
    ]

    username = CharField(
        verbose_name='Никнейм',
        max_length=150,
        unique=True
    )
    email = EmailField(
        max_length=150,
        unique=True,
        verbose_name='E-mail'
    )
    first_name = CharField(
        max_length=30,
        blank=True,
        verbose_name='Имя'
    )
    last_name = CharField(
        max_length=30,
        blank=True,
        verbose_name='Фамилия'
    )
    bio = TextField(
        blank=True,
        null=True,
        verbose_name='О себе'
    )
    role = CharField(
        max_length=30,
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )
    confirmation_code = CharField(
        max_length=70,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Проверочный код'
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == MyUser.ADMIN

    @property
    def is_moderator(self):
        return self.role == MyUser.MODERATOR

    @property
    def is_user(self):
        return self.role == MyUser.USER

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

def this_year():
    return datetime.now().year


def max_value_this_year(value):
    return MaxValueValidator(
        this_year(),
        'Нельзя добавлять произведения из будущего.'
    )(value)


class Category(models.Model):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Название', max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.PositiveSmallIntegerField(
        'Год издания',
        validators=[
            max_value_this_year,
            MinValueValidator(
                1,
                'Введите корректный год.'
            ),
        ],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Жанр'
    )
    description = models.TextField('Описание', blank=True,)

    class Meta:
        verbose_name = 'Произвдение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name

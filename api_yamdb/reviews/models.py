from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator, MaxValueValidator, MinValueValidator)
from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_year, validate_slug

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
)


class Genre(models.Model):
    """Модель для создания обьектов класса Genre."""
    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        validators=[validate_slug],
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры',
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для создания обьектов класса Category."""
    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        validators=[validate_slug],
        unique=True
    )

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории',
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для создания обьектов класса Title."""
    name = models.CharField(
        max_length=100,
        verbose_name='Hазвание',
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year],
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Выберите категорию'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')


class User(AbstractUser):
    """Модель для создания обьектов класса User."""
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=20,
        verbose_name='роль',
        choices=CHOICES,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == 'admin'

    def is_moderator(self):
        return self.role == 'moderator'

    def is_user(self):
        return self.role == 'user'


class GenreTitle(models.Model):
    """Модель для создания обьектов класса GenreTitle."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'Произведение: {self.title}, жанр:{self.genre}'


class Review(models.Model):
    """Модель для создания обьектов класса Review."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Отзыв'),
        help_text=_('Отзыв к произведению')
    )
    text = models.TextField(
        verbose_name=_('Текст отзыва'),
        help_text=_('Введите текст отзыва'),
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Автор отзыва')
    )
    score = models.IntegerField(
        verbose_name=_('Рейтинг произведения'),
        help_text=_('Введите значение от 1 до 10'),
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name=_('Дата публикации'),
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(score_gte=1) & models.Q(score_lt=10),
                name='Значение рейтинга произведения допустимо'
                     'в диапозоне от 1 до 10',
            )
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique review')
        ]
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель для создания обьектов класса Comment."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Отзыв'),
        help_text=_('Отзыв к произведению')
    )
    text = models.TextField(
        verbose_name=_('Текст комментария'),
        help_text=_('Введите текст комментария'),
        blank=False
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Автор комментария')
    )
    pub_date = models.DateTimeField(
        verbose_name=_('Дата публикации'),
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]

from django.contrib.auth import get_user_model
from django.db import models

from .managers import CustomQuerySet
from .constants import MAX_FIELD_LENGTH, REPRESENTATION_LENGTH


User = get_user_model()


class BasePublicationModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class Category(BasePublicationModel):
    title = models.CharField(
        'Заголовок',
        max_length=MAX_FIELD_LENGTH
    )
    description = models.TextField(
        'Описание')
    slug = models.SlugField(
        'Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'),
        unique=True
    )

    class Meta(BasePublicationModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:REPRESENTATION_LENGTH]


class Location(BasePublicationModel):
    name = models.CharField(
        'Название места',
        max_length=MAX_FIELD_LENGTH
    )

    class Meta(BasePublicationModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:REPRESENTATION_LENGTH]


class Post(BasePublicationModel):
    title = models.CharField(
        'Заголовок',
        max_length=MAX_FIELD_LENGTH
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
    )
    location = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение',
    )
    objects = CustomQuerySet.as_manager()

    class Meta(BasePublicationModel.Meta):
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.title[:REPRESENTATION_LENGTH]

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_qeryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

class Post(models.Model):
    """
    Модель представляет собой запись блога.

    Атрибуты:
        title (CharField): Заголовок поста.
        slug (SlugField): Слаг поста, используется для URL-адресов.
        body (TextField): Содержимое поста.
        publish (DateTimeField): Дата публикации поста.
        created (DateTimeField): Дата создания поста.
        updated (DateTimeField): Дата последнего обновления поста.
        status (CharField): Статус поста (например, черновик или опубликованный).

    Методы:
        __str__(): Возвращает строку представления объекта.
    """

    class Status(models.TextChoices):
        """
        Возможные статусы поста.

        Атрибуты:
            DRAFT (tuple): Черновой статус.
            PUBLISHED (tuple): Опубликованный статус.
        """
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"


    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date="publish",
        )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
        )

    objects = models.Manager()
    published = PublishedManager()
    class Meta:
        """
        Опции метаданных для модели.
        
        Атрибуты:
            ordering (list): Список полей для сортировки объектов.
            indexes (list): Список индексов для оптимизации запросов.
        """
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"],)
        ]


    def __str__(self):
        """Возвращает заголовок поста."""
        return self.title
    

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )
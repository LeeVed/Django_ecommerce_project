from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.utils import timezone
from django.utils.text import slugify


class BlogPost(models.Model):
    """
    Модель блоковой записи
    """
    # Заголовок
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Введите заголовок статьи (макс. 200 символов)'
    )

    # Делаем красивые url
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг',
        help_text='Уникальная часть URL (заполняется автоматически)'
    )

    # Cодержимое
    content = models.TextField(
        verbose_name='Содержимое',
        help_text='Введите текст статьи'
    )

    # Превью (изображение)
    preview_image = models.ImageField(
        upload_to='blog/previews/',
        verbose_name='Превью (изображение)',
        blank=True,
        null=True,
        help_text='Загрузите изображение для превью статьи'
    )

    # Дата создания
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания',
        help_text='Дата и время создания записи'
    )

    # Признак публикации
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано',
        help_text='Отметьте для публикации статьи'
    )

    # Количество просмотров
    views_count = PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров',
        help_text='Счетчик просмотров статьи'
    )

    def save(self, *args, **kwargs):
        # 1. Проверяем: если slug не заполнен (пустая строка или None)
        if not self.slug:
            # 2. Преобразуем заголовок в slug:

            self.slug = slugify(self.title)

        # 3. Вызываем родительский метод save() для сохранения в БД
        super().save(*args, **kwargs)


    def __str__(self):
        """Строковое представление"""
        return self.title


    class Meta:
        """Мета-данные модели"""
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
        ordering = ['-created_at']  # Сортировка по убыванию даты создания

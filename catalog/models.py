from django.db import models


class Category(models.Model):
    """
    Модель категории товаров
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
        help_text='Введите название категории'
    )
    # поле description необязательно
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Введите описание категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']  # Сортировка по названию по умолчанию

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель товара
    """
    name = models.CharField(
        max_length=150,
        verbose_name='Наименование',
        help_text='Введите название товара'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание товара'
    )
    # фото продукта необязательно
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Загрузите изображение товара'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        help_text='Выберите категорию товара',
        related_name='products'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за покупку',
        help_text='Введите цену товара'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at', 'name']  # Сначала новые товары, потом по названию
        indexes = [
            models.Index(fields=['name']),  # индексация по названию товара
            models.Index(fields=['category', 'created_at']), # составная ндексация для пагинации, фильтрации и отображения новинок
        ]

    def __str__(self):
        return f"{self.name} - {self.price} руб."

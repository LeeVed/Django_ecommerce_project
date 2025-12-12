from django.contrib import admin

from .models import Category
from .models import Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ("id", "name")

    # Поиск по названию категории
    search_fields = ("name", "description")

    # Поля для отображения при редактировании
    fields = ("name", "description")

    readonly_fields = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ("id", "name", "price", "category", "created_at", "updated_at")

    # Фильтрация по категории
    list_filter = ("category",)

    # Поиск по полям name и description
    search_fields = ("name", "description")

    # Поля для отображения при редактировании
    fieldsets = (
        ("Основная информация", {"fields": ("name", "category", "price", "image")}),
        ("Описание", {"fields": ("description",), "classes": ("wide",)}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    # Поля только для чтения
    readonly_fields = ("created_at", "updated_at")

    # Добавляем предпросмотр изображения (опционально)
    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import format_html

            return format_html(f'<img src="{obj.image.url}" style="max-height: 100px;" />')
        return "Нет изображения"

    image_preview.short_description = "Предпросмотр"

    # Сортировка по умолчанию
    ordering = ("-created_at",)

    # Количество элементов на странице
    list_per_page = 20

    # Добавляем возможность быстрого редактирования
    list_editable = ("price",)

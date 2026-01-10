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

    list_display = ("id", "name", "price", "category", "publishing_status", "created_at", "updated_at")

    list_filter = ("category", "publishing_status")

    search_fields = ("name", "description")

    # Поля для отображения при редактировании
    fieldsets = (
        ("Основная информация", {"fields": ("name", "category", "price", "image")}),
        ("Описание", {"fields": ("description",), "classes": ("wide",)}),
        ("Публикация", {"fields": ("publishing_status",), "classes": ("collapse",)}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    readonly_fields = ("created_at", "updated_at")

    # предпросмотр изображения
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

    # быстрое редактирование
    list_editable = ("price", "publishing_status")

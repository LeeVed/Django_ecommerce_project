from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published", "views_count")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("views_count", "created_at")

    fieldsets = (
        (None, {"fields": ("title", "slug", "content", "preview_image")}),
        ("Публикация", {"fields": ("is_published", "created_at", "views_count")}),
    )

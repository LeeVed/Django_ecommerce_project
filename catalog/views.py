from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    """CBV для главной страницы (список продуктов) - ОБЩЕДОСТУПНА"""

    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_queryset(self):
        """Показываем только опубликованные продукты"""

        return Product.objects.filter(publishing_status="published")

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст"""

        context = super().get_context_data(**kwargs)
        context["title"] = "Skystore - Главная"
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """CBV для создания нового продукта только для АВТОРИЗОВАННЫХ"""

    model = Product
    form_class = ProductForm  # форма с валидацией
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст"""

        context = super().get_context_data(**kwargs)
        context["title"] = "Создание нового продукта"
        return context

    def form_valid(self, form):
        """Действия при успешной валидации формы"""

        form.instance.owner = self.request.user
        messages.success(self.request, "Продукт успешно создан!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Действия при невалидной форме"""

        messages.error(self.request, "Исправьте ошибки в форме")
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """CBV для редактирования существующего продукта только для АВТОРИЗОВАННЫХ"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_object(self, queryset=None):
        """Получаем объект или выбрасываем PermissionDenied"""

        obj = super().get_object(queryset)
        if obj.owner is None or obj.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта")
        return obj

    def get_success_url(self):
        """Перенаправляем на страницу продукта после редактирования"""

        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст"""

        context = super().get_context_data(**kwargs)
        context["title"] = f"Редактирование: {self.object.name}"
        return context

    def form_valid(self, form):
        """Действия при успешной валидации формы"""

        messages.success(self.request, "Продукт успешно обновлен!")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """CBV для удаления продукта только для АВТОРИЗОВАННЫХ"""

    model = Product
    template_name = "catalog/product_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        """Получаем объект с проверкой прав"""

        obj = super().get_object(queryset)

        is_moderator = self.request.user.groups.filter(name="Модератор продуктов").exists()
        is_owner = obj.owner is not None and obj.owner == self.request.user  # ← проверка на None

        if not (is_moderator or is_owner):
            raise PermissionDenied("Вы не можете удалить этот продукт")
        return obj

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст"""

        context = super().get_context_data(**kwargs)
        context["title"] = f"Удаление: {self.object.name}"
        return context

    def delete(self, request, *args, **kwargs):
        """Действия при удалении"""

        messages.success(self.request, "Продукт успешно удален!")
        return super().delete(request, *args, **kwargs)


class ContactsView(LoginRequiredMixin, TemplateView):
    """CBV для страницы контактов только для АВТОРИЗОВАННЫХ"""

    template_name = "contacts.html"
    # Если нужно добавить контекст (например, заголовок)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """CBV для отображения детальной информации о товаре только для АВТОРИЗОВАННЫХ"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст"""

        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.object.name} - Детальная информация"
        return context


class ProductUnpublishView( LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = "catalog.can_unpublish_product"
    fields = []
    template_name = "catalog/product_unpublish_confirm.html"

    def form_valid(self, form):
        self.object.publishing_status = "draft"
        self.object.save()
        messages.success(self.request, f"Продукт '{self.object.name}' снят с публикации")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

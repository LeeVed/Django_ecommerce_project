from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    """CBV для главной страницы (список продуктов) - ОБЩЕДОСТУПНА"""

    model = Product
    template_name = "home.html"
    context_object_name = "products"

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

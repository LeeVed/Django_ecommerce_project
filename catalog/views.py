from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from .models import Product


class HomeView(ListView):
    """CBV для главной страницы (список продуктов)"""
    model = Product
    template_name = "home.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = "Skystore - Главная"
        return context


class ContactsView(TemplateView):
    """CBV для страницы контактов"""
    template_name = "contacts.html"

    # Если нужно добавить контекст (например, заголовок)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductDetailView(DetailView):
    """CBV для отображения детальной информации о товаре"""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.object.name} - Детальная информация"
        return context

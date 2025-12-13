from typing import Any

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Product


def home(request: Any) -> HttpResponse:
    """
    Контроллер главной страницы.
    Выполняет ORM-запрос для получения списка всех продуктов.
    """
    # ORM-запрос: получить все продукты из базы данных
    products = Product.objects.all()
    context = {"products": products, "title": "Skystore - Главная"}
    return render(request, "home.html", context)


def contacts(request: Any) -> HttpResponse:
    """Контроллер страницы контактов"""
    return render(request, "contacts.html")


def product_detail(request: Any, pk: Any) -> HttpResponse:
    """Контроллер для отображения детальной информации о товаре"""
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product, "title": f"{product.name} - Детальная информация"}
    return render(request, "catalog/product_detail.html", context)

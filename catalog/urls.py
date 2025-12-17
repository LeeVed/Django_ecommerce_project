from catalog.apps import CatalogConfig
from django.urls import path
from .views import HomeView, ContactsView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]

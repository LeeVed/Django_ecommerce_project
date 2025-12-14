from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import contacts
from catalog.views import home

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
]

from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home_page, contacts_page, product_page

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_page),
    path('contacts/', contacts_page),
    path('product/<int:pk>/', product_page, name='product')
]
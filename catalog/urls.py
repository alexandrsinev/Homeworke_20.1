from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactView, ProductCreate, ProductUpdate, ProductDelete

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home_page'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('create/', ProductCreate.as_view(), name='product_create'),
    path('edit/<int:pk>/', ProductUpdate.as_view(), name='product_update'),
    path('delete/<int:pk>/', ProductDelete.as_view(), name='product_delete'),
]

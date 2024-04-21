from django.urls import path

from catalog.views import home_page, contacts_page

urlpatterns = [
    path('', home_page),
    path('contacts/', contacts_page)
]
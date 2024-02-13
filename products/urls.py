from django.urls import path

from .views import products_list

urlpatterns = [
    path("", products_list, name="products-list"),
]

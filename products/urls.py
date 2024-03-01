from django.urls import path
from django.urls import re_path


from .views import products_list

urlpatterns = [
    re_path(r"^$", products_list, name="products-list"),
]

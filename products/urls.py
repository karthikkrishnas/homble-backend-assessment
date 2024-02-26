from django.urls import path

from .views import products_list,create_sku,product_detail,edit_sku_status,active_categories_with_sku_count,all_skus_with_category

urlpatterns = [
    path("", products_list, name="products-list"),
    path('create_sku/', create_sku, name='create_sku'),
    path('product_detail/<int:pk>/', product_detail, name='product_detail'),
    path('edit_sku_status/<int:sku_id>/', edit_sku_status, name='edit_sku_status'),
    path('active_categories/', active_categories_with_sku_count, name='active_categories'),
    path('Skus_category/', all_skus_with_category, name='active_categories'),

]

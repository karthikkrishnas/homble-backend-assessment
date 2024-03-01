from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "managed_by","edited_at","ingredients" )
    ordering = ("-id",)
    search_fields = ("name",)
    list_filter = ("is_refrigerated", "category")
    fields = (
        ("name", "price"),
        ("category", "is_refrigerated"),
        "description",
        ("id", "created_at"),
        "managed_by",
    )
    autocomplete_fields = ("category", "managed_by")
    readonly_fields = ("id", "created_at")


class ProductInline(admin.StackedInline):
    """
    For display in CategoryAdmin
    """

    model = Product
    extra = 0
    ordering = ("-id",)
    readonly_fields = ("name", "price", "is_refrigerated")
    fields = (readonly_fields,)
    show_change_link = True

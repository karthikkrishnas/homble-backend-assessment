from django.contrib import admin

from products.models import Product, Sku


class SkuInline(admin.StackedInline):
    """
    For display in SkuInline
    """

    model = Sku
    extra = 0
    ordering = ("-id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "managed_by")
    ordering = ("-id",)
    search_fields = ("name",)
    list_filter = ("is_refrigerated", "category", "ingredients")
    fields = (
        ("name", "price"),
        ("category", "is_refrigerated"),
        "description",
        "ingredients",
        ("id", "created_at", "edited_at"),
        "managed_by",
    )
    autocomplete_fields = ("category", "managed_by")
    readonly_fields = ("id", "created_at", "edited_at")
    inlines = [SkuInline]


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


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]
    list_display = ("id", "product", "size", "price")
    ordering = ("id",)
    search_fields = ("product__name",)
    list_filter = ("size",)
    fields = (
        ("product",),
        ("size", "price"),
        ("id"),
    )
    readonly_fields = ("id",)

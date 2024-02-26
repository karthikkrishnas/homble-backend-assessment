from django.contrib import admin

from products.models import Product, Sku


class SkuInline(admin.StackedInline):
    """
    For display in SkuInline
    """

    model = Sku
    extra = 1
    ordering = ("-id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name" , "managed_by")
    ordering = ("-id",)
    search_fields = ("name",)
    list_filter = ("is_refrigerated", "category", "ingredients")
    fields = (
        ("name" ),
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
    readonly_fields = ("name", "is_refrigerated")
    fields = (readonly_fields,)
    show_change_link = True


@admin.register(Sku)
class SkuAdmin(admin.ModelAdmin):
    autocomplete_fields = ["product"]
    list_display = ("id", "product", "size", "selling_price","status")
    ordering = ("id",)
    search_fields = ("product__name","status")
    list_filter = ("size",)
    fields = (
        ("product",),
        ("size", "selling_price", "platform_commission", "cost_price","status"),
        ("id"),
    )
    readonly_fields = ("id", "selling_price")

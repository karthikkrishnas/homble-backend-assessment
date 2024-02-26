from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    Very basic structure. To be further built up.
    """

    name = models.CharField(
        _("display name"),
        max_length=150,
        unique=True,
        help_text=_("This will be displayed to user as-is"),
    )

    description = models.TextField(
        _("descriptive write-up"),
        unique=True,
        help_text=_("Few sentences that showcase the appeal of the product"),
    )
    is_refrigerated = models.BooleanField(
        help_text=_("Whether the product needs to be refrigerated"),
        default=False,
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="products",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    managed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="managed_products",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    # ingrediants added by me

    ingredients = models.CharField(
        max_length=500,
        help_text=_("Add new ingredients "),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

   

    edited_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} )"

    class Meta:
       
        db_table = "product"
        ordering = []
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Sku(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text=("Size and quantity of the products in gms")
    )

    measurement_unit = models.CharField(
        max_length=2,
        choices=[
            ("gm", "Grams"),
            ("kg", "Kilograms"),
            ("mL", "Milliliters"),
            ("L", "Liters"),
            ("pc", "Piece"),
        ],
        default="gm",
    )
    status = models.IntegerField(
        choices=[
            (0, "Pending for approval"),
            (1, "Approved"),
            (2, "Discontinued"),
        ],
        default=0,
    )

    selling_price = models.DecimalField(
        _("selling price (Rs.)"),
        help_text=_("Price payable by customer (Rs.)"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    platform_commission = models.PositiveBigIntegerField(null=True, blank=True)
    cost_price = models.PositiveBigIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.cost_price is not None and self.platform_commission is not None:
            self.selling_price = self.cost_price + self.platform_commission
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.product.name} - {self.size} {self.get_measurement_unit_display()}"
        )

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(size__lte=999), name="size_limit")
        ]

from django.core.management.base import BaseCommand
from products.models import Sku
from django.db.models import F, ExpressionWrapper, DecimalField

from decimal import Decimal


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        Sku.objects.update(
            platform_commission=F("selling_price") * Decimal("0.25"),
            cost_price=ExpressionWrapper(
                F("selling_price") - (F("selling_price") * Decimal("0.25")),
                output_field=DecimalField(),
            ),
        )

        self.stdout.write(self.style.SUCCESS("Prices updated successfully"))

from rest_framework import serializers
from products.models import Product, Sku


class SkuSerializer(serializers.ModelSerializer):
    """
    To Show all products based on selling price.
    """

    class Meta:
        model = Sku
        fields = [
            "product",
            "size",
            "selling_price",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    """
    To show list of products.
    """

    sku = serializers.SerializerMethodField()
    print(sku, "here just testing the output ")

    def get_sku(self, obj):

        sku_objects = obj.sku_set.all()
        sku_serializer = SkuSerializer(sku_objects, many=True)
        return sku_serializer.data

    class Meta:
        model = Product
        fields = ["name", "ingredients", "is_refrigerated", "sku"]

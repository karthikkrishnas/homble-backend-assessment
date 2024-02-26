from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from .models import Product, Sku
from .serializers import (
    ProductListSerializer,
    SkuSerializer,
    SkuCreateSerializer,
    SkuListSerializer,
)
from categories.models import Category
from django.db.models import Count, Q


@api_view(["GET"])
@permission_classes([AllowAny])
def products_list(request):
    """
    List of all products.
    """

    refrigerated_params = request.GET.get("refrigerated")

    if refrigerated_params == "true":
        products = Product.objects.filter(is_refrigerated=True)

    elif refrigerated_params == "false":
        products = Product.objects.filter(is_refrigerated=False)
    else:
        products = Product.objects.all()

    serializer = ProductListSerializer(products, many=True)

    return Response({"products": serializer.data}, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_sku(request):
    data = request.data.copy()

    if "cost_price" not in data or "platform_commission" not in data:
        return Response(
            {"error": "cost_price and platform_commission are required fields"},
            status=HTTP_400_BAD_REQUEST,
        )

    serializer = SkuCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    skus = product.sku_set.filter(status=1)

    product_serializer = ProductListSerializer(product)
    sku_serializer = SkuSerializer(skus, many=True)

    product_data = product_serializer.data

    return Response({"products": product_data})


@api_view(["PATCH"])
@permission_classes([IsAdminUser])
def edit_sku_status(request, sku_id):
    try:
        sku = Sku.objects.get(id=sku_id)
    except Sku.DoesNotExist:
        return JsonResponse({"error": "Sku not found"}, status=HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        status_value = request.data.get("status")
        if status_value is not None:
            sku.status = status_value
            sku.save()
            return JsonResponse(
                {"message": "Sku status updated successfully"}, status=HTTP_200_OK
            )
        else:
            return JsonResponse(
                {"error": "Status value not provided"}, status=HTTP_400_BAD_REQUEST
            )

    return JsonResponse(
        {"error": "Invalid request method"}, status=HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def active_categories_with_sku_count(request):
    active_categories = (
        Category.objects.filter(is_active=True)
        .annotate(
            approved_sku_count=Count("products__sku", filter=Q(products__sku__status=1))
        )
        .values("id", "name", "approved_sku_count")
    )

    return Response({"active_categories": active_categories}, status=HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def all_skus_with_category(request):
    skus = Sku.objects.select_related("product__category").all()
    serializer = SkuListSerializer(skus, many=True)
    return Response({"Skus_category": serializer.data}, status=HTTP_200_OK)

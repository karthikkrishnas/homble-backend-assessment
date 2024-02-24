from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
)

from .models import Product
from .serializers import ProductListSerializer


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


# /////////////////////////////
#   refrigerated products view
# /////////////////////////////

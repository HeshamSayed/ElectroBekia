from rest_framework import generics
from products.models import Product, Category
from .serializers import ProductSerializer
# from .decorators import validate_request_data
from rest_framework.response import Response
from rest_framework.views import status


class ListProductView(generics.ListAPIView):
    """
    /api/categories/2/products/
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_products = self.queryset.filter(category=kwargs["pk"])

            serializer = ProductSerializer(a_products, many=True)
            return Response({"products": serializer.data})

            # return Response(ProductSerializer(a_products).data)
        except Product.DoesNotExist:
            return Response(
                data={
                    "message": "Category with id: {} does not exist".format(kwargs["pk"]),
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs["pk"])
        a_product = Product.objects.create(
            name = request.data["name"],
            description = request.data["description"],
            min_price = request.data["min_price"],
            max_price = request.data["max_price"],
            image = request.data["image"],
            category = category,
        )
        return Response(
            data=ProductSerializer(a_product).data,
            status=status.HTTP_201_CREATED
        )
    




from rest_framework import generics
from products.models import Product, Category
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import status
from .CustomPermission import IsGetOrIsAdmin
from rest_framework import permissions


class ListProductView(generics.ListAPIView):
    """
    /api/categories/2/products/
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsGetOrIsAdmin)
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




class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET categories/:fk/products/:id/
    PUT categories/:fk/products/:id/
    DELETE categories/:fk/products/:id/
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsGetOrIsAdmin)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_product = self.queryset.get(pk=kwargs["id"])
            return Response(ProductSerializer(a_product).data)
        except Product.DoesNotExist:
            return Response(
                data={
                    "message": "Product with id: {} does not exist".format(kwargs["id"]),
                },
                status=status.HTTP_404_NOT_FOUND
            )


    def put(self, request, *args, **kwargs):
        try:
            a_product = self.queryset.get(pk=kwargs["id"])
            a_category = Category.objects.get(pk=request.data['category'])

            a_product.category = a_category or a_product.category
            a_product.name = request.data['name'] or a_product.name
            a_product.description = request.data['description'] or a_product.description
            a_product.min_price = request.data['min_price'] or a_product.min_price
            a_product.max_price = request.data['max_price'] or a_product.max_price
            a_product.image = request.data['image'] or a_product.image
            a_product.save()
            return Response(ProductSerializer(a_product).data)
        except Product.DoesNotExist:
            return Response(
                data={
                    "message": "Product with id: {} does not exist".format(kwargs["id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_product = self.queryset.get(pk=kwargs["id"])
            a_product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(
                data={
                    "message": "Product with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

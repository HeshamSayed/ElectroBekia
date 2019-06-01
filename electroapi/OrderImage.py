from rest_framework import generics
from orders.models import Order,OrderItem, OrderImage
from .serializers import OrderImageSerializer
from rest_framework.response import Response
from rest_framework.views import status
from .CustomPermission import IsGetOrIsAdmin
from rest_framework import permissions


class ListOrderImageView(generics.ListAPIView):
    """
    /api/orders/2/images/
    """
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsGetOrIsAdmin)
    queryset = OrderImage.objects.all()
    serializer_class = OrderImageSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_images = self.queryset.filter(order=kwargs["pk"])
            serializer = OrderImageSerializer(a_images, many=True)
            return Response({"order_images": serializer.data})

        except OrderImage.DoesNotExist:
            return Response(
                data={
                    "message": "Order with id: {} does not exist".format(kwargs["pk"]),
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, *args, **kwargs):
        a_order = Order.objects.get(pk=kwargs["pk"])
        a_image = OrderImage.objects.create(
            img = request.data["img"],
            order=a_order,
        )
        return Response(
            data=OrderImageSerializer(a_image).data,
            status=status.HTTP_201_CREATED
        )


class OrderImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    DELETE orders/:fk/image/:id/
    Get orders/:fk/image/:id/
    """
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsGetOrIsAdmin)
    queryset = OrderImage.objects.all()
    serializer_class = OrderImageSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_image = self.queryset.get(pk=kwargs["id"])
            return Response(OrderImageSerializer(a_image).data)
        except OrderImage.DoesNotExist:
            return Response(
                data={
                    "message": "Order Item with id: {} does not exist".format(kwargs["id"]),
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_image = self.queryset.get(pk=kwargs["id"])
            a_image.delete()
            return Response(data={
                    "message": "image Deleted successfuly "
                 },
                    status=status.HTTP_204_NO_CONTENT)

        except OrderItem.DoesNotExist:
            return Response(
                data={
                    "message": "Order Item with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

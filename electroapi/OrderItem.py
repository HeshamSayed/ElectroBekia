from rest_framework import generics
from orders.models import Order,OrderItem
from .serializers import OrderItemSerializer
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import permissions
from products.models import Product



class ListOrderItemView(generics.ListAPIView):
    """
    /api/orders/2/items/
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            a_items = self.queryset.filter(order=kwargs["pk"])

            serializer = OrderItemSerializer(a_items, many=True)
            return Response({"order_items": serializer.data})

            # return Response(ProductSerializer(a_products).data)
        except OrderItem.DoesNotExist:
            return Response(
                data={
                    "message": "Order with id: {} does not exist".format(kwargs["pk"]),
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, *args, **kwargs):
        a_order = Order.objects.get(pk=kwargs["pk"])
        a_product = Product.objects.get(pk=request.data["product"])
        a_item = OrderItem.objects.create(
            price = request.data["price"],
            quantity = request.data["quantity"],
            status = request.data["status"],
            order=a_order,
            product=a_product
        )
        return Response(
            data=OrderItemSerializer(a_item).data,
            status=status.HTTP_201_CREATED
        )


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET orders/:fk/items/:id/
    PUT orders/:fk/items/:id/
    DELETE orders/:fk/items/:id/
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            a_item = self.queryset.get(pk=kwargs["id"])
            return Response(OrderItemSerializer(a_item).data)
        except OrderItem.DoesNotExist:
            return Response(
                data={
                    "message": "Order Item with id: {} does not exist".format(kwargs["id"]),
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_item = self.queryset.get(pk=kwargs["id"])
            a_order = Order.objects.get(pk=request.data['order'])
            a_product = Product.objects.get(pk=request.data['product'])

            a_item.order = a_order or a_item.order
            a_item.product = a_product or a_item.product
            a_item.price = request.data['price'] or a_item.price
            a_item.quantity = request.data['quantity'] or a_item.quantity
            a_item.status = request.data['status'] or a_item.status
            a_item.save()
            return Response(OrderItemSerializer(a_item).data)
        except OrderItem.DoesNotExist:
            return Response(
                data={
                    "message": "Order Item with id: {} does not exist".format(kwargs["id"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_item = self.queryset.get(pk=kwargs["id"])
            a_item.delete()
            return Response(data={
                    "message": "item Deleted successfuly "
                 },
                    status=status.HTTP_204_NO_CONTENT)

        except OrderItem.DoesNotExist:
            return Response(
                data={
                    "message": "Order Item with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

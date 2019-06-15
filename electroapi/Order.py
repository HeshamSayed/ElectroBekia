from rest_framework import generics
from orders.models import Order
from accounts.models import User, City
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import permissions


class ListOrderView(generics.ListAPIView):
    """
    Provides a get, post method handler.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.data["user"])
        city = City.objects.get(pk=request.data["city"])
        a_category = Order.objects.create(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            email=request.data["email"],
            phone=request.data["phone"],
            address=request.data["address"],
            order_status=request.data["order_status"],
            user=user,
            city=city,
            description=request.data["description"]
        )

        return Response(
            data=OrderSerializer(a_category).data,
            status=status.HTTP_201_CREATED
        )



class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET orders/:id/
    PUT orders/:id/
    DELETE orders/:id/
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            a_order = self.queryset.get(pk=kwargs["pk"])
            return Response(OrderSerializer(a_order).data)
        except Order.DoesNotExist:
            return Response(
                data={
                    "message": "Order with id: {} does not exist".format(kwargs["pk"]),
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_order = self.queryset.get(pk=kwargs["pk"])

            a_user = User.objects.get(pk=request.data['user'])
            a_city = City.objects.get(pk=request.data['city'])

            a_order.first_name = request.data["first_name"]
            a_order.last_name = request.data["last_name"]
            a_order.email = request.data["email"]
            a_order.phone = request.data["phone"]
            a_order.address = request.data["address"]
            a_order.order_status = request.data["order_status"]
            a_order.description = request.data["description"]
            a_order.user = a_user
            a_order.city = a_city

            a_order.save()
            return Response(OrderSerializer(a_order).data)

        except Order.DoesNotExist:
            return Response(
                data={
                    "message": "Order with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_order = self.queryset.get(pk=kwargs["pk"])
            a_order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(
                data={
                    "message": "Order with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


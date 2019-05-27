from rest_framework import generics
from products.models import Category
from .serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import permissions

from .CustomPermission import IsGetOrIsAdmin



class ListCategoryView(generics.ListAPIView):
    """
    Provides a get, post method handler.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsGetOrIsAdmin )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        a_category = Category.objects.create(
            name=request.data["name"],
        )
        return Response(
            data=CategorySerializer(a_category).data,
            status=status.HTTP_201_CREATED
        )


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET categories/:id/
    PUT categories/:id/
    DELETE categories/:id/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsGetOrIsAdmin)

    def get(self, request, *args, **kwargs):
        try:
            a_category = self.queryset.get(pk=kwargs["pk"])
            return Response(CategorySerializer(a_category).data)
        except Category.DoesNotExist:
            return Response(
                data={
                    "message": "Category with id: {} does not exist".format(kwargs["pk"]),
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_category = self.queryset.get(pk=kwargs["pk"])
            serializer = CategorySerializer()
            updated_song = serializer.update(a_category, request.data)
            return Response(CategorySerializer(updated_song).data)
        except Category.DoesNotExist:
            return Response(
                data={
                    "message": "Category with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_category = self.queryset.get(pk=kwargs["pk"])
            a_category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(
                data={
                    "message": "Category with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


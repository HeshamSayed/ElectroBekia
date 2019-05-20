from django.urls import path
from .views import ListCategoryView, CategoryDetailView, ListProductView
app_name = 'electroapi'

urlpatterns = [
    path('categories/', ListCategoryView.as_view(), name="categories"),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name="CategoryDetails"),
    path('categories/<int:pk>/products/', ListProductView.as_view(), name="products"),
]
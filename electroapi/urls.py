from django.urls import path
from .views import ListCategoryView, CategoryDetailView
app_name = 'electroapi'

urlpatterns = [
    path('categories/', ListCategoryView.as_view(), name="categories"),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name="CategoryDetails"),
]
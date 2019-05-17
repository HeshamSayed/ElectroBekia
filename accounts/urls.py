from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name = 'accounts'

urlpatterns = [
  path('login/', views.user_login, name='login'),
  path('logout/', auth_view.LogoutView.as_view(), name='logout'),
  path('signup/', views.Signup.as_view(), name='signup'),
]

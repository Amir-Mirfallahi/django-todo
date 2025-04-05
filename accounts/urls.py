from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]

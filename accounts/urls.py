from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.users, name="users"),
    path("signup/", views.signup, name="signup"),
    path('login/', views.login, name='login'),
]

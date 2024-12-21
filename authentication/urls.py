from django.urls import path

from . import views

urlpatterns = [
    path('login', views.AuthLoginView, name="auth-login"),
    path('logout', views.AuthLogoutView, name="auth-logout"),

]
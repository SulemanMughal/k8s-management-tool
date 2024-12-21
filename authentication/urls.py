from django.urls import path

from .views import (
    AuthLoginView,
    AuthLogoutView,
    AuthRegisterationView,
    AuthUserActivationView
)

urlpatterns = [
    path('login', AuthLoginView, name="auth-login"),
    path('logout', AuthLogoutView, name="auth-logout"),
    path('registeration', AuthRegisterationView, name="auth-register"),
    path('activate/<slug:uidb64>/<slug:token>/', AuthUserActivationView, name='auth-activate'),

]
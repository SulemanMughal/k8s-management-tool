from django.urls import path

from .views import (
    AuthLoginView,
    AuthLogoutView,
    AuthRegisterationView,
    AuthUserActivationView
)

from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)


urlpatterns = [
    path('login', AuthLoginView, name="auth-login"),
    path('logout', AuthLogoutView, name="auth-logout"),
    path('registeration', AuthRegisterationView, name="auth-register"),
    path('activate/<slug:uidb64>/<slug:token>/', AuthUserActivationView, name='auth-activate'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
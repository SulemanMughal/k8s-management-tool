from django.urls import path
from .views import create_secret_view, get_secret_view, update_secret_view, delete_secret_view

urlpatterns = [
    path("create-secret/", create_secret_view, name="create-secret"),
    path("get-secret/", get_secret_view, name="get-secret"),
    path("update-secret/", update_secret_view, name="update-secret"),
    path("delete-secret/", delete_secret_view, name="delete-secret"),
]

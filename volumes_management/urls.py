from django.urls import path

from .views import create_stateful_set_with_storage_view

urlpatterns = [

    path("create-stateful-set-with-storage", create_stateful_set_with_storage_view, name="create-stateful-set-with-storage"),

]

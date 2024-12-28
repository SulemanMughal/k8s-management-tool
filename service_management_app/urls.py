from django.urls import path
from .views import get_service_details_view

urlpatterns = [
    path("get-service-details/", get_service_details_view, name="get-service-details"),
]

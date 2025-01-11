from django.urls import path

from .views import list_events_view

urlpatterns = [
    path("list", list_events_view, name="list-events"),
    # path("create", create_new_namespace_view, name="create-namespaces"),
    # path("details", namespace_detils_view, name="details-namespaces"),
    # path("delete", delete_a_namespace_view, name="delete-namespaces"),
    # path("update", update_a_namespace_view, name="update-namespaces"),
]
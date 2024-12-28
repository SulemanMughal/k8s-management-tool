from django.urls import path

from .views import create_pod_view, get_pod_view, update_pod_view, delete_pod_view, list_pods_view, port_forward_view, get_pod_logs_view, create_pod_with_resources_view, create_pod_with_startup_probe_view, create_pod_with_liveness_probe_view, create_pod_with_readiness_probe_view





urlpatterns = [

    path("create-pod/", create_pod_view, name="create-pod"),

    path("get-pod/", get_pod_view, name="get-pod"),

    path("update-pod/", update_pod_view, name="update-pod"),

    path("delete-pod/", delete_pod_view, name="delete-pod"),

    path("list-pods/", list_pods_view, name="list-pods"),

    path("port-forward/", port_forward_view, name="port-forward"),

    path("get-pod-logs/", get_pod_logs_view, name="get-pod-logs"),

    path("create-pod-with-resources/", create_pod_with_resources_view, name="create-pod-with-resources"),

    path("create-pod-with-startup-probe/", create_pod_with_startup_probe_view, name="create-pod-with-startup-probe"),


    path("create-pod-with-liveness-probe/", create_pod_with_liveness_probe_view, name="create-pod-with-liveness-probe"),


    path("create-pod-with-readiness-probe/", create_pod_with_readiness_probe_view, name="create-pod-with-readiness-probe"),



]

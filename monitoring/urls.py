from django.urls import path
from .views import get_node_metrics_view, get_pod_metrics_view

urlpatterns = [
    path("get-node-metrics/", get_node_metrics_view, name="get-node-metrics"),
    path("get-pod-metrics/", get_pod_metrics_view, name="get-pod-metrics"),
]

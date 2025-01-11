from django.urls import path

from .views import create_pod_view, get_pod_view, update_pod_view, delete_pod_view, list_pods_view, port_forward_view, get_pod_logs_view, create_pod_with_resources_view, create_pod_with_startup_probe_view, create_pod_with_liveness_probe_view, create_pod_with_readiness_probe_view, create_pod_with_security_context_view, set_namespace_psa_labels_view, create_pod_psa_compliant_view, get_kube_proxy_pods_view, get_pods_by_label_selector_view,list_container_images_views




urlpatterns = [

    path("create-pod/", create_pod_view, name="create-pod"),

    path("get-pod", get_pod_view, name="get-pod"),

    path("update-pod/", update_pod_view, name="update-pod"),

    path("delete-pod/", delete_pod_view, name="delete-pod"),

    # List down all pods
    path("list-pods/", list_pods_view, name="list-pods"),

    path("port-forward/", port_forward_view, name="port-forward"),

    path("get-pod-logs/", get_pod_logs_view, name="get-pod-logs"),

    path("create-pod-with-resources/", create_pod_with_resources_view, name="create-pod-with-resources"),

    path("create-pod-with-startup-probe/", create_pod_with_startup_probe_view, name="create-pod-with-startup-probe"),


    path("create-pod-with-liveness-probe/", create_pod_with_liveness_probe_view, name="create-pod-with-liveness-probe"),


    path("create-pod-with-readiness-probe/", create_pod_with_readiness_probe_view, name="create-pod-with-readiness-probe"),

    path("create-pod-with-security-context/", create_pod_with_security_context_view, name="create-pod-with-security-context"),

    path("set-namespace-psa-labels/", set_namespace_psa_labels_view, name="set-namespace-psa-labels"),
    path("create-pod-psa-compliant/", create_pod_psa_compliant_view, name="create-pod-psa-compliant"),

    path("get-kube-proxy-pods/", get_kube_proxy_pods_view, name="get-kube-proxy-pods"),

    # Get pods by label selector
    path("get-pods-by-label-selector", get_pods_by_label_selector_view, name="get-pods-by-labels"),

    path("list-all-container-images", list_container_images_views, name="container-images-list"),
    




]

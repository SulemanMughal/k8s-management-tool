from django.urls import path

from .views import list_network_policies_view, create_network_policy_view, list_all_ip_pools_view, create_ip_pool_view, get_ip_pool_details_view, update_ip_pool_view, delete_ip_pool_view, monitor_ip_pool_usage_view, get_ip_pool_metrics_view, assign_ip_pool_view

urlpatterns = [
    path("list", list_network_policies_view, name="list-network-policies"),
    path("create", create_network_policy_view, name="create-network-policy"),
    path("ip-pools", list_all_ip_pools_view, name="list-ip-pools"),
    path("ip-pools/create", create_ip_pool_view, name="create-ip-pools"),
    path("ip-pools/details", get_ip_pool_details_view, name="details-ip-pools"),
    path("ip-pools/updates", update_ip_pool_view, name="updates-ip-pools"),
    path("ip-pools/delete", delete_ip_pool_view, name="delete-ip-pools"),
    path("ip-pools/monitor", monitor_ip_pool_usage_view, name="monitor-ip-pools"),
    path("ip-pools/metrics", get_ip_pool_metrics_view, name="metrics-ip-pools"),
    path("ip-pools/assign", assign_ip_pool_view, name="assign-ip-pools"),
]
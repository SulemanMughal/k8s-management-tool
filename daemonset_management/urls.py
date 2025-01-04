from django.urls import path
from .views import create_daemonset_view, describe_daemonset_view, list_daemonsets_view, update_daemonset_image_view, delete_daemonset_view, get_pods_managed_by_daemonsets_view, get_pods_managed_by_specific_daemonset_view, update_daemonset_node_selector_view, update_daemonset_node_affinity_view, pause_daemonset_view, resume_daemonset_view,get_nodes_for_daemonset_view, change_daemonset_namespace_view, daemonset_rollout_status_view,daemonset_rollout_status_periodic_view, get_daemonset_events_view, update_rollout_history_view,get_rollout_history_view,update_rollingupdate_strategy_view,update_daemonset_strategy_view
urlpatterns = [
    path('daemonset/create', create_daemonset_view, name='create_daemonset'),
    path('daemonset/describe', describe_daemonset_view, name='describe_daemonset'),
    path('daemonset/list', list_daemonsets_view, name='list_daemonsets'),
    path('daemonset/update/image', update_daemonset_image_view, name='update_daemonset_image'),
    path('daemonset/delete', delete_daemonset_view, name='delete_daemonset'),
    path('daemonset/pods', get_pods_managed_by_daemonsets_view, name='get_pods_managed_by_daemonsets'),
    path('daemonset/pods/specific', get_pods_managed_by_specific_daemonset_view, name='get_pods_managed_by_specific_daemonset'),
    path('daemonset/update/node-selector', update_daemonset_node_selector_view, name='update_daemonset_node_selector'),
    path('daemonset/update/node-affinity', update_daemonset_node_affinity_view, name='update_daemonset_node_affinity'),
    path('daemonset/pause', pause_daemonset_view, name='pause_daemonset'),
    path('daemonset/resume', resume_daemonset_view, name='resume_daemonset'),
    path("daemonset/nodes", get_nodes_for_daemonset_view, name="get_nodes_for_daemonset"),
    path("daemonset/change-namespace", change_daemonset_namespace_view, name="change_daemonset_namespace"),
    path("daemonset/rollout-status", daemonset_rollout_status_view, name="daemonset_rollout_status"),
    path("daemonset/rollout-status-periodic", daemonset_rollout_status_periodic_view, name="daemonset_rollout_status_periodic"),
    path("daemonset/events", get_daemonset_events_view, name="get_daemonset_events"),
    path("daemonset/update-rollout-history", update_rollout_history_view, name="update_rollout_history"),
    path("daemonset/get-rollout-history", get_rollout_history_view, name="get_rollout_history"),
    path("daemonset/update-rollingupdate-strategy", update_rollingupdate_strategy_view, name="update_rollingupdate_strategy"),
    path("daemonset/update-strategy", update_daemonset_strategy_view, name="update_daemonset_strategy"),
]

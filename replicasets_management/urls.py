from django.urls import path
from .views import list_replicasets_view, create_replicaset_view, update_replicate_view, get_replicate_view, delete_replicate_view, get_replicate_pods_view, get_replicate_events_view, get_replicate_logs_view, delete_replicate_orphan_view

urlpatterns = [
    path('replicasets/get/<str:namespace>', list_replicasets_view, name='list_replicasets'),
    path('replicasets/create', create_replicaset_view, name='create_replicasets'),
    path('replicasets/update', update_replicate_view, name='update_replicate'),
    path('replicasets/details', get_replicate_view, name='get_replicate'),
    path('replicasets/delete', delete_replicate_view, name='delete_replicate'),
    path('replicasets/pods', get_replicate_pods_view, name='get_replicaset_pods'),
    path('replicasets/events', get_replicate_events_view, name='get_replicaset_events'),
    path('replicasets/logs', get_replicate_logs_view, name='get_replicaset_logs'),
    path('replicasets/delete/orphan', delete_replicate_orphan_view, name='delete_replicate_orphan'),
]

